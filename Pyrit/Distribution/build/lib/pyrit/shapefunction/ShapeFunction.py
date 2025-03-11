# -*- coding: utf-8 -*-
"""Contains the abstract class ShapeFunction.

.. sectionauthor:: Christ, Bundschuh
"""
# pylint: disable=no-else-return

from typing import Any, Tuple, TYPE_CHECKING, Protocol, Dict, Union, Callable, Type, Generator, NewType
from inspect import signature, isclass
from abc import ABC, abstractmethod
from functools import partial
from enum import Enum

from numpy import ndarray
import numpy as np
from scipy.sparse import coo_matrix

from pyrit.material import MatProperty, Materials
from pyrit.excitation import Excitations, Exci
from pyrit.region import Regions, Regi
from pyrit.bdrycond import BdryCond, BC
from pyrit.toolbox.QuadratureToolbox import gauss_triangle, gauss_tetrahedron, gauss
from pyrit import get_logger
from pyrit import ValueHandler

if TYPE_CHECKING:
    from pyrit.mesh import Mesh
    from pyrit.problem import Problem, FieldCircuitCouplingProblem

logger = get_logger(__name__)

Number = NewType('Number', Union[int, float, complex])
AssemblyGenerator = NewType('AssemblyGenerator', Generator[Tuple[np.ndarray, ValueHandler, int], None, None])
NumericalData = NewType('NumericalData', Union[Callable[..., Union[Number, np.ndarray]], Number, np.ndarray])
MaterialData = NewType('MaterialData', Tuple[Regions, Materials, Type[MatProperty]])
BoundaryData = NewType('BoundaryData', Tuple[Regions, BdryCond, Type[BC]])
ExcitationData = NewType('ExcitationData', Tuple[Regions, Excitations, Type[Exci]])


def is_valid_index_array(x: Any) -> bool:
    """Returns true if x is an array with positive integers"""
    if isinstance(x, np.ndarray):
        if np.ndim(x) > 0:
            if issubclass(x.dtype.type, np.integer) and np.min(x) >= 0:
                return True
    return False


def is_single_float(x: Any) -> bool:
    """Returns true if x is an int, float or a one-dimensional numpy array."""
    if isinstance(x, (int, float, complex, np.int64, np.int32)):
        return True
    if isinstance(x, ndarray):
        if len(x.shape) == 1:
            return True
    return False


def check_integration_order(integration_order: Any) -> None:
    """Check whether the integration order is an integer."""
    if not isinstance(integration_order, int):
        raise ValueError(f"integration order is of type {type(integration_order)} but has to be an int.")


# pylint: disable=invalid-name
class ValueType(Enum):
    """Possible cases for arguments passed to a matrix routine or vector routine"""

    SCALAR = 1
    VECTOR = 2
    TENSOR = 3
    SCALAR_PER_ELEMENT = 4
    VECTOR_PER_ELEMENT = 5
    TENSOR_PER_ELEMENT = 6
    SCALAR_EVALUATIONS = 7
    VECTOR_EVALUATIONS = 8
    TENSOR_EVALUATIONS = 9


class ShrinkInflateProblemShapeFunction(Protocol):
    """A protocol for the minimal content of a problem such that the shrink and inflate methods can work"""

    mesh: 'Mesh'
    regions: 'Regions'
    boundary_conditions: 'BdryCond'


class ShapeFunction(ABC):
    """Abstract class for shape function (sft) object.

    See Also
    --------
    pyrit.mesh : Abstract underlying Mesh object on whose entities the SFT
                  parameters are computed.
    """

    @abstractmethod
    def __init__(self, mesh: 'Mesh', dim: int, allocation_size: int) -> None:
        """
        Constructor for the abstract class ShapeFunction.

        Parameters
        ----------
        mesh : Mesh object
            Representing the underlying geometry on which the SFTs are defined.
        dim : int
            Dimensionality of the shape function.
        allocation_size : int
            Size used for vector allocation in matrix creation.

        Returns
        -------
        None
        """
        self.mappingcoeff = None
        self._mesh = mesh
        self._dim = dim
        self.__allocation_size = allocation_size

    @property
    def mesh(self) -> 'Mesh':
        """Returns the mesh."""
        return self._mesh

    @property
    def dim(self) -> int:
        """Return the dimension."""
        return self._dim

    @property
    def _allocation_size(self):
        """Get the size need to allocate for sparse creation."""
        return self.__allocation_size

    def _process_single_argument(self, arg: Any) -> str:
        """Process the arguments if the arguments consists of a single value.

        Parameters
        ----------
        arg : Any
            The single argument.

        Returns
        -------
        type : str
            The type of the argument. Either "function", "array" or "number".

        Raises
        ------
        ValueError
            When arg has not the expected format and type
        """
        if callable(arg):
            if len(signature(arg).parameters) != self.mesh.node.shape[1]:
                raise ValueError(f"The function has not the expected number of {str(self.mesh.node.shape[1])} "
                                 f"arguments")
            if is_single_float(arg(*self.mesh.node[0])):  # returns a single floating number
                return "function"
            raise ValueError("The function does not return scalar fields (i.e. single, number valued return value).")

        if isinstance(arg, ndarray):
            if len(arg.shape) == 1:
                if arg.shape[0] == self.mesh.num_elem:
                    return "array"
                else:
                    raise ValueError(f"The array has {str(arg.shape[0])} entries, but needs {str(self.mesh.num_elem)} "
                                     f"entries")
            if len(arg.shape) == 2:
                if arg.shape[0] == self.mesh.num_elem and arg.shape[1] == 1:
                    return "array"
                if arg.shape[0] == 2 and arg.shape[1] == 2:
                    return "single_tensor"
                else:
                    raise ValueError("The array has not the right shape")
            if len(arg.shape) == 3:
                if arg.shape[0] == self.mesh.num_elem and arg.shape[1] == 2 and arg.shape[2] == 2:
                    return "tensor_per_element"
                else:
                    raise ValueError("The array has not the right shape")

        if isinstance(arg, (float, int)):
            return "number"

        raise ValueError("Argument type not excepted.")

    def _process_input_single(self, input_data, **kwargs) -> AssemblyGenerator:
        integration_order = kwargs.pop("integration_order", 1)

        check_integration_order(integration_order)

        def assembly_generator():
            yield np.arange(self.mesh.num_elem), ValueHandler(input_data), integration_order

        return assembly_generator()

    def _process_input_general(self, regions, get_value_handler: Callable[[Regi], ValueHandler], **kwargs):
        default_integration_order = 1
        integration_order = kwargs.pop("integration_order", default_integration_order)
        regions_only = kwargs.pop("regions_only", None)

        flag_integration_order_dict = False
        if isinstance(integration_order, dict):
            flag_integration_order_dict = True
        elif not isinstance(integration_order, int):
            raise ValueError("integration order is of wrong type. Is neither an integer nor a dictionary. "
                             f"It is of type {type(integration_order)}")

        def assembly_generator():
            for regi in regions:  # iterate over regions
                if regi.dim != self.dim:
                    continue
                if regions_only is not None:
                    if regi.ID not in regions_only:
                        continue

                value_handler = get_value_handler(regi)
                if value_handler is None:
                    continue

                # get indices of all mesh elements within the region:
                indices = np.where(self.mesh.elem2regi == regi.ID)[0].astype(np.int32, casting="same_kind", copy=False)

                if flag_integration_order_dict:
                    local_integration_order = integration_order.get(regi.ID, None)
                    if local_integration_order is None:
                        logger.warning("The dictionary of integration orders has no entry for region %d. "
                                       "Using default integration order 1.", regi.ID)
                        local_integration_order = default_integration_order
                else:
                    local_integration_order = integration_order

                check_integration_order(local_integration_order)

                yield indices, value_handler, local_integration_order

        return assembly_generator()

    def _process_input_material(self, regions: Regions, materials: Materials, property_class: Type[MatProperty],
                                **kwargs) -> AssemblyGenerator:
        def get_value_handler(regi: Regi) -> ValueHandler:
            material_id = regi.mat
            if material_id is None:
                logger.warning("Iteration over a region without a material. This may be an error. Continue anyway.")
                return None

            material = materials.get_material(material_id)
            prop = material.get_property(property_class)
            if prop is None:
                return None

            return prop

        return self._process_input_general(regions, get_value_handler, **kwargs)

    def _process_input_boundary_condition(self, regions: Regions, boundary_conditions: BdryCond,
                                          boundary_condition_class: Type[BC], **kwargs) -> AssemblyGenerator:
        def get_value_handler(regi: Regi) -> ValueHandler:
            boundary_condition_id = regi.bc
            if boundary_condition_id is None:
                logger.warning("Iteration over a region without a boundary condition. This may be an error. "
                               "Continue anyway.")
                return None

            bc = boundary_conditions.get_bc(boundary_condition_id)
            if not isinstance(bc, boundary_condition_class):
                return None

            return bc

        return self._process_input_general(regions, get_value_handler, **kwargs)

    def _process_input_excitation(self, regions: Regions, excitations: Excitations, excitation_class: Type[Exci],
                                  **kwargs) -> AssemblyGenerator:
        def get_value_handler(regi: Regi) -> ValueHandler:
            excitation_id = regi.exci
            if excitation_id is None:
                logger.warning("Iteration over a region without an excitation. This may be an error. "
                               "Continue anyway.")
                return None

            exci = excitations.get_exci(excitation_id)
            if not isinstance(exci, excitation_class):
                return None

            return exci

        return self._process_input_general(regions, get_value_handler, **kwargs)

    def _process_input(self, *input_data, **kwargs) -> AssemblyGenerator:
        """Process input data for matrix or vector routines

        Parameters
        ----------
        input_data : Any
            Input data
        kwargs : Dict
            Optional arguments:

                - integration_order : Union[int,Dict[int,int]]
                    Either a constant integration order or a dictionary with one integration order per region.
                - default_property_class : Type[MatProperty]
                    Default class for the MatProperty in the case of MaterialData (for backwards compatibility)
                - default_boundary_condition_class : Type[BC]
                    Default class for the BC in the case of BoundaryData (for backwards compatibility)
                - default_excitation_class : Type[Exci]
                    Default class for the Exci in the case of ExcitationData (for backwards compatibility)
                - regions_only : List[int]
                    A list of region IDs that are considered. If not given, all regions are considered.

        Returns
        -------
        assembly_generator : AssemblyGenerator
        """
        if len(input_data) not in (1, 2, 3):
            raise ValueError(f"Wrong number of inputs. Got {len(input_data)} but has to be 1 or 3.")

        # if isinstance(input_data[0], tuple):  # needed for TetCartesianNodal
        #     input_data = input_data[0]

        if len(input_data) == 1:
            return self._process_input_single(input_data[0], **kwargs)

        if len(input_data) in (2, 3):
            regions, materials, boundary_conditions, excitations = None, None, None, None

            # Default values for backwards compatibility
            property_class = kwargs.pop("default_property_class", None)
            boundary_condition_class = kwargs.pop("default_boundary_condition_class", None)
            excitation_class = kwargs.pop("default_excitation_class", None)

            for data in input_data:
                if isinstance(data, Regions):
                    regions = data
                elif isinstance(data, Materials):
                    materials = data
                elif isinstance(data, BdryCond):
                    boundary_conditions = data
                elif isinstance(data, Excitations):
                    excitations = data
                elif not isclass(data):
                    raise ValueError(f"Argument of unsupported type: {type(data)}")
                elif issubclass(data, MatProperty):
                    property_class = data
                elif issubclass(data, BC):
                    boundary_condition_class = data
                elif issubclass(data, Exci):
                    excitation_class = data
                else:
                    raise ValueError(f"Argument of unsupported type: {type(data)}")

            if regions is not None and materials is not None and property_class is not None:
                return self._process_input_material(regions, materials, property_class, **kwargs)
            if regions is not None and boundary_conditions is not None and boundary_condition_class is not None:
                return self._process_input_boundary_condition(regions, boundary_conditions, boundary_condition_class,
                                                              **kwargs)
            if regions is not None and excitations is not None and excitation_class is not None:
                return self._process_input_excitation(regions, excitations, excitation_class, **kwargs)

            raise ValueError("With the given input data, no further processing is possible.")

        raise ValueError("Internal error. This should not be reachable")

    def _process_load(self, *load: Any) \
            -> Tuple[str, Union[Callable[..., float], ndarray, float, Union[Regions, Excitations]]]:
        """Process the load arguments.

        Parameters
        ----------
        load : Any
            The load arguments.

        Returns
        -------
        type : str
            The type of the arguments. Either "tuple", "function", "array" or "number".
        load : Tuple[str, Union[Callable[..., float], ndarray, float, Union[Regions, Excitations]]]
            The arguments in a standard format. If case is "tuple", the order in `load` is as given (independent of
            the order of the input). If case is not "tuple", `load` is no list but just the value.

        Raises
        ------
        ValueError
            When args has not the expected format and type
        """
        if len(load) == 1 and isinstance(load[0], tuple):
            load = load[0]
        if len(load) not in (1, 2):
            raise ValueError(f"Wrong number of inputs. Got {len(load)} but has to be 1 or 2.")

        load_out = None
        case = ''
        if len(load) == 1:
            case = self._process_single_argument(*load)  # pylint: disable=no-value-for-parameter
            load_out = load[0]

        if len(load) == 2:
            case = 'tuple'
            load_out = [None, None]
            classes: list = [Regions, Excitations]
            for k, l in enumerate(load):
                if isinstance(l, Regions):
                    load_out[0] = l
                elif isinstance(l, Excitations):
                    load_out[1] = l
                else:
                    raise ValueError(f"Unexpected argument: {l}")

            for k, c in enumerate(classes):
                if load_out[k] is None:
                    raise ValueError(f"The class {c} is missing in load.")

        return case, load_out

    def _process_neumann(self, *args: Any, allow_indices_tuple: bool = False) -> Tuple[bool, str]:
        """
        Process the neumann_term arguments.

        Parameters
        ----------
        args: Any
            The neumann_term arguments.
        allow_indices_tuple : bool
            Flag to allow the second argument to be a tuple in case of index value pairs.

        Returns
        -------
        flag_regions : bool
            True, if regions are used.
        flag_value : str
            'none' if regions are used,
            'callable' if indices and a function are passed,
            'array' if indices and a numpy array are passed,
            'value' if indices and a single value are passed.

        Raises
        ------
        ValueError
            If args has not the expected format and type
        Exception
            If len(args) is unequal to two or the first argument is neither a Regions-object nor an array.
        """
        flag_regions = False
        flag_value = 'none'
        if len(args) != 2:
            raise Exception(f"Not right number of arguments given. Needs 2 and has {len(args)}.")
        if isinstance(args[0], Regions) and isinstance(args[1], BdryCond):
            flag_regions = True
        elif isinstance(args[0], ndarray):
            if is_valid_index_array(args[0]) is False:
                raise ValueError("The (first array) provided is not a valid index array.")
            if allow_indices_tuple and isinstance(args[1], tuple):  # used in TriAxisymmetricEdgeShapeFunction
                if len(args[1]) != 1:
                    raise Exception(f"If the second argument is tuple, then its length is supposed to be 1 instead of"
                                    f"{len(args[1])}!")
                arg = args[1][0]
            else:
                arg = args[1]

            if callable(arg):
                num_args = len(signature(arg).parameters)
                if isinstance(arg, partial):
                    # If the provided callable is a functools.partial object, the args and kwargs set in order to
                    # create the partial object are stored in two dicts. The length of the new signature is still the
                    # same as the original function. Hence, num_args that still need to be provided needs to be adapted.
                    num_args -= len(arg.keywords) + len(arg.args)
                if num_args != self.mesh.node.shape[1]:
                    raise ValueError(f"The function has not the expected number of {str(self.mesh.node.shape[1])} "
                                     f"arguments")
                flag_value = 'callable'
            elif isinstance(arg, ndarray):
                if args[0].size != arg.size:
                    raise ValueError(
                        "The value array does not provide exactly one entry per element in the index array.")
                flag_value = 'array'
            elif isinstance(arg, (float, int)):
                flag_value = 'value'
            else:
                raise ValueError(f"Second argument has wrong type (is {type(args[1])})")
        else:
            raise Exception("Arguments have not the required types.")

        return flag_regions, flag_value

    def _process_value_homogeneous(self, value: Any, number_elements: int)\
            -> Tuple[Union[Number, np.ndarray], ValueType]:
        if isinstance(value, ndarray):
            dimension = self._dim
            elements = number_elements
            if elements <= dimension:
                logger.warning("Because the mesh is so small, the processing of the arguments may go wrong.")

            if value.size == 1:
                return value.flatten()[0], ValueType.SCALAR
            if value.shape in ((dimension, ), (dimension, 1)):
                return value.flatten(), ValueType.VECTOR
            if value.shape == (dimension, dimension):
                return value, ValueType.TENSOR
            if value.size == elements:
                return value, ValueType.SCALAR_PER_ELEMENT
            if value.shape == (elements, dimension):
                return value, ValueType.VECTOR_PER_ELEMENT
            if value.shape == (elements, dimension, dimension):
                return value, ValueType.TENSOR_PER_ELEMENT

            raise ValueError("The array has not the right shape")

        if isinstance(value, (complex, float, int)):
            return value, ValueType.SCALAR

        raise ValueError("The value is of unknown type")

    def _process_value_inhomogeneous(self, value: Any, number_elements: int,
                                     number_evaluation_points: int) -> ValueType:
        if isinstance(value, ndarray):
            dimension = self._dim
            elements = number_elements
            evaluation = number_evaluation_points

            if value.shape == (elements, evaluation):
                return ValueType.SCALAR_EVALUATIONS
            if value.shape == (elements, evaluation, dimension):
                return ValueType.VECTOR_EVALUATIONS
            if value.shape == (elements, evaluation, dimension, dimension):
                return ValueType.TENSOR_EVALUATIONS

            raise ValueError("The array has not the right shape")

        raise ValueError("The value is of unknown type")

    def _default_integrator(self, integration_order: int, dim: int = -1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the weights and local coordinates using the default integrators: gaussian triangle and tetrahedron.

        Parameters
        ----------
        integration_order : int
            Integration Order.
        dim : int
            Dimensionality. Default is -1; Dimensionality of shape function is used.

        Returns
        -------
        weights: np.ndarray
            (K,) array. K weights used for numerical integration.
        local_coordinates: np.ndarray
            (K, dim) array. K local coordinates used for numerical integration.
        """
        if dim == -1:
            dim = self.dim

        if dim == 1:
            return gauss(integration_order)
        if dim == 2:
            return gauss_triangle(integration_order)
        if dim == 3:
            return gauss_tetrahedron(integration_order)
        raise ValueError(f"Dimension {dim} is unknown.")

    def _matrix_routine(self, matrix_type: str, assembly_generator: AssemblyGenerator,
                        **kwargs) -> coo_matrix:
        """
        Create a matrix according to the matrix assembly routine for a shapefunction-class.

        See Also: doc/src/writing%20a%20shape%20function%20class.html#matrix-assembly-routines.

        Parameters
        ----------
        eval_func : Callable
            Method that handels all the evaluations.
        calc_func : Callable
            Method that handels all the calculations.
        weights : np.ndarray
            Weights for numerical integration.
        local_coordinates : np.ndarray
            Local coordinates for numerical integration.
        material : Union[Callable[..., float], np.ndarray, float, Union['Regions', 'Materials', 'MatProperty']])
            Material.

        Returns
        -------
        coo_matrix
            Matrix in sparse format.
        """
        evaluation_functions = kwargs.pop("evaluation_functions", {})
        if not isinstance(evaluation_functions, dict):
            raise ValueError("evaluation_functions must be a dictionary")

        integrator_dict = {}
        row, col, val = [], [], []  # row indices, column indices, values
        for indices, value_handler, integration_order in assembly_generator:
            if integration_order not in integrator_dict:
                integrator_dict[integration_order] = self._default_integrator(integration_order)

            weights, local_coordinates = integrator_dict[integration_order]

            if value_handler.is_homogeneous:
                # No evaluation at integration points necessary
                if value_handler.is_linear:
                    value = value_handler.evaluate()
                else:
                    value = value_handler.evaluate(elements=indices)
                value, value_type = self._process_value_homogeneous(value, len(indices))

                if value_type == ValueType.SCALAR:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_constant_scalar(matrix_type, indices, value, weights,
                                                                                  local_coordinates, **kwargs)
                elif value_type == ValueType.VECTOR:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_constant_vector(matrix_type, indices, value, weights,
                                                                                  local_coordinates, **kwargs)
                elif value_type == ValueType.TENSOR:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_constant_tensor(matrix_type, indices, value, weights,
                                                                                  local_coordinates, **kwargs)
                elif value_type == ValueType.SCALAR_PER_ELEMENT:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_elementwise_scalar(matrix_type, indices, value,
                                                                                     weights, local_coordinates,
                                                                                     **kwargs)
                elif value_type == ValueType.VECTOR_PER_ELEMENT:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_elementwise_vector(matrix_type, indices, value,
                                                                                     weights, local_coordinates,
                                                                                     **kwargs)
                elif value_type == ValueType.TENSOR_PER_ELEMENT:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_elementwise_tensor(matrix_type, indices, value,
                                                                                     weights, local_coordinates,
                                                                                     **kwargs)
                else:
                    logger.error("Internal Error. The value_type must be one of the types above.")
                    raise ValueError("Internal Error")
            else:
                # Evaluation at integration points
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)
                if value_handler.is_linear:
                    value = value_handler.evaluate(evaluation_points, **evaluation_functions)
                else:
                    value = value_handler.evaluate(evaluation_points, elements=indices, **evaluation_functions)
                value_type = self._process_value_inhomogeneous(value, len(indices), len(weights))

                if value_type == ValueType.SCALAR_EVALUATIONS:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_function_scalar(matrix_type, indices, value, weights,
                                                                                  local_coordinates,
                                                                                  evaluation_points=evaluation_points,
                                                                                  **kwargs)
                elif value_type == ValueType.VECTOR_EVALUATIONS:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_function_vector(matrix_type, indices, value, weights,
                                                                                  local_coordinates,
                                                                                  evaluation_points=evaluation_points,
                                                                                  **kwargs)
                elif value_type == ValueType.TENSOR_EVALUATIONS:
                    row_tmp, col_tmp, val_tmp = self._calc_matrix_function_tensor(matrix_type, indices, value, weights,
                                                                                  local_coordinates,
                                                                                  evaluation_points=evaluation_points,
                                                                                  **kwargs)
                else:
                    logger.error("Internal Error. The value_type must be one of the types above.")
                    raise ValueError("Internal Error")

            row.append(row_tmp)
            col.append(col_tmp)
            val.append(val_tmp)

        if len(row) == 0 or len(col) == 0 or len(val) == 0:
            logger.warning("The data for generating the matrix was empty. This may be an error. Proceeding anyway with "
                           "empty matrix.")
        else:
            row = np.hstack(row)
            col = np.hstack(col)
            val = np.hstack(val)

        return coo_matrix((val, (row, col)), shape=(self.mesh.num_node, self.mesh.num_node))

    def _vector_routine(self, vector_type: str, assembly_generator: AssemblyGenerator,
                        **kwargs) -> coo_matrix:
        evaluation_functions = kwargs.pop("evaluation_functions", {})
        if not isinstance(evaluation_functions, dict):
            raise ValueError("evaluation_functions must be a dictionary")

        integrator_dict = {}
        row, val = [], []  # row indices, values
        for indices, value_handler, integration_order in assembly_generator:
            if integration_order not in integrator_dict:
                integrator_dict[integration_order] = self._default_integrator(integration_order)

            weights, local_coordinates = integrator_dict[integration_order]

            if value_handler.is_homogeneous:
                # No evaluation at integration points necessary
                if value_handler.is_linear:
                    value = value_handler.evaluate()
                else:
                    value = value_handler.evaluate(elements=indices)
                value, value_type = self._process_value_homogeneous(value, len(indices))

                if value_type == ValueType.SCALAR:
                    row_tmp, val_tmp = self._calc_vector_constant_scalar(vector_type, indices, value, weights,
                                                                                  local_coordinates, **kwargs)
                elif value_type == ValueType.VECTOR:
                    row_tmp, val_tmp = self._calc_vector_constant_vector(vector_type, indices, value, weights,
                                                                                  local_coordinates, **kwargs)
                elif value_type == ValueType.TENSOR:
                    row_tmp, val_tmp = self._calc_vector_constant_tensor(vector_type, indices, value, weights,
                                                                                  local_coordinates, **kwargs)
                elif value_type == ValueType.SCALAR_PER_ELEMENT:
                    row_tmp, val_tmp = self._calc_vector_elementwise_scalar(vector_type, indices, value,
                                                                                     weights, local_coordinates,
                                                                                     **kwargs)
                elif value_type == ValueType.VECTOR_PER_ELEMENT:
                    row_tmp, val_tmp = self._calc_vector_elementwise_vector(vector_type, indices, value,
                                                                                     weights, local_coordinates,
                                                                                     **kwargs)
                elif value_type == ValueType.TENSOR_PER_ELEMENT:
                    row_tmp, val_tmp = self._calc_vector_elementwise_tensor(vector_type, indices, value,
                                                                                     weights, local_coordinates,
                                                                                     **kwargs)
                else:
                    logger.error("Internal Error. The value_type must be one of the types above.")
                    raise ValueError("Internal Error")
            else:
                # Evaluation at integration points
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)
                if value_handler.is_linear:
                    value = value_handler.evaluate(evaluation_points, **evaluation_functions)
                else:
                    value = value_handler.evaluate(evaluation_points, elements=indices, **evaluation_functions)
                value_type = self._process_value_inhomogeneous(value, len(indices), len(weights))

                if value_type == ValueType.SCALAR_EVALUATIONS:
                    row_tmp, val_tmp = self._calc_vector_function_scalar(vector_type, indices, value, weights,
                                                                                  local_coordinates,
                                                                                  evaluation_points=evaluation_points,
                                                                                  **kwargs)
                elif value_type == ValueType.VECTOR_EVALUATIONS:
                    row_tmp, val_tmp = self._calc_vector_function_vector(vector_type, indices, value, weights,
                                                                                  local_coordinates,
                                                                                  evaluation_points=evaluation_points,
                                                                                  **kwargs)
                elif value_type == ValueType.TENSOR_EVALUATIONS:
                    row_tmp, val_tmp = self._calc_vector_function_tensor(vector_type, indices, value, weights,
                                                                                  local_coordinates,
                                                                                  evaluation_points=evaluation_points,
                                                                                  **kwargs)
                else:
                    logger.error("Internal Error. The value_type must be one of the types above.")
                    raise ValueError("Internal Error")

            row.append(row_tmp)
            val.append(val_tmp)

        if len(row) == 0 or len(val) == 0:
            logger.warning("The data for generating the vector was empty. This may be an error. Proceeding anyway with "
                           "empty vector.")
        else:
            row = np.hstack(row)
            val = np.hstack(val)

        return coo_matrix((val, (row, np.zeros_like(row))), shape=(self.mesh.num_node, 1))

    @abstractmethod
    def _calc_evaluation_points_element(self, local_coordinates: np.ndarray, indices: np.ndarray) -> np.ndarray:
        r"""
        Compute the coordinates at which a function needs to be evaluated if numerical integration is needed.

        Returns a three-dimensional array with the evaluation coordinates for all elements specified. The returned array
        is of dimensions (N,E,T) with [n,e,0] being the x coordinates and [n,e,1] being the y coordinates.
        Mathematically the transformation can be expressed as
        :math:`(x,\,y)^T  = \mathbf{B}\,(\hat{x},\,\hat{y})^T + offset`.

        .. table:: Symbols

            ======  =======
            Symbol  Meaning
            ======  =======
            I       Number of indices of mesh elements for which the matrix is computed.
            D       Dimension of shape function.
            N       Number of evaluation points.
            ======  =======

        Parameters
        ----------
        local_coordinates : np.ndarray
            (N,D) array. x and y coordinates for each evaluation point.
        indices : np.ndarray
            (I,) array. Array with indices of considered elements.

        Returns
        -------
        coord : np.ndarray
            (I,N,D) array. For each index I there are N evaluations points with D coordinates.
        """

    @abstractmethod
    def _calc_matrix_constant_scalar(self, matrix_type: str, indices: np.ndarray, value: Number,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a value that is represented by a constant scalar.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : Number
            A single number. Value in the definition of the matrix.
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        if not isinstance(value, (int, float, complex)):
            raise ValueError("Value is of unexpected type")

    @abstractmethod
    def _calc_matrix_constant_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a value that is represented by a constant vector.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : np.ndarray
            (D,) array. Vector in the definition of the matrix.
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        expected_shape = (self.dim,)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_matrix_constant_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a value that is represented by a constant tensor.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : np.ndarray
            (D,D) array. Tensor in the definition of the matrix.
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        expected_shape = (self.dim, self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_matrix_elementwise_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray,
                                        **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a material that is represented by a scalar for each mesh element.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : np.ndarray
            (I,) array. Values per element in the definition of the matrix
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        expected_shape = (len(indices),)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_matrix_elementwise_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray,
                                        **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a material that is represented by a vector for each mesh element.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : np.ndarray
            (I,D) array. Vector per element in the definition of the matrix
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        expected_shape = (len(indices), self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_matrix_elementwise_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a material that is represented by a tensor for each mesh element.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : np.ndarray
            (I,D,D) array. Tensor per element in the definition of the matrix
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        expected_shape = (len(indices), self.dim, self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_matrix_function_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a material that is represented by a function that returns a scalar.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : np.ndarray
            (I,N) array. Scalar integration point per element in the definition of the matrix.
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        expected_shape = (len(indices), len(weights))
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_matrix_function_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a material that is represented by a function that returns a vector.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : np.ndarray
            (I,N,D) array. Vector per integration point per element in the definition of the matrix.
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        expected_shape = (len(indices), len(weights), self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_matrix_function_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate a matrix for a material that is represented by a function that returns a tensor.

        This method calls the correct calc method for a given matrix type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        matrix_type : str
            Label used for identification of matrix type. Defined in the non-abstract shape function classes.
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : np.ndarray
            (I,N,D,D) array. Tensor per integration point per element in the definition of the matrix.
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        row : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        column : np.ndarray
            (I,) array. Column index vector used for sparse creation.
        value : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        expected_shape = (len(indices), len(weights), self.dim, self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_vector_constant_scalar(self, vector_type: str, indices: np.ndarray, value: Number,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate a vector for a property that is represented by a scalar constant.

        This method calls the correct calc method for a given vector type. And returns vectors for the sparse creation.

        .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        I       Number of indices of mesh elements for which the matrix is computed.
        D       Dimension of shape function.
        N       Number of evaluation points.
        ======  =======

        Parameters
        ----------
        vector_type : str
            Label used for identification of vector type (e.g. "load", "neumann").
        indices : np.ndarray
            (I,) array. Indices of mesh elements for which the matrix is computed.
        value : float
            Material value.
        weights : np.ndarray
            (N,) array. Weights for each evaluation point (numerical integration).
        local_coordinates : np.ndarray
            (N, D) array. Local coordinates for each evaluation point (numerical integration).
        kwargs : Dict
            Further keyword arguments passed to the calc method.

        Returns
        -------
        i : np.ndarray
            (I,) array. Row index vector used for sparse creation.
        v : np.ndarray
            (I,) array. Value vector used for sparse creation.
        """
        if not isinstance(value, (int, float, complex)):
            raise ValueError("Value is of unexpected type")

    @abstractmethod
    def _calc_vector_constant_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        expected_shape = (self.dim,)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_vector_constant_tensor(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        expected_shape = (self.dim, self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_vector_elementwise_scalar(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray,
                                        **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        expected_shape = (len(indices),)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_vector_elementwise_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray,
                                        **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        expected_shape = (len(indices), self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_vector_elementwise_tensor(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        expected_shape = (len(indices), self.dim, self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_vector_function_scalar(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        expected_shape = (len(indices), len(weights))
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_vector_function_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        expected_shape = (len(indices), len(weights), self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def _calc_vector_function_tensor(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        expected_shape = (len(indices), len(weights), self.dim, self.dim)
        if value.shape != expected_shape:
            raise ValueError(f"The value has an unexpected shape. It is {value.shape} but should be {expected_shape}")

    @abstractmethod
    def shrink(self, matrix: 'coo_matrix', rhs: 'coo_matrix', problem: 'Problem',
               integration_order: int = 1) -> Tuple['coo_matrix', 'coo_matrix', ndarray, int, Dict['str', Any]]:
        r"""Shrink the system of equations of a problem.

        Shrinks the system of equations where `matrix` is the matrix and `rhs` is the right-hand-side. Additionally,
        there is returned side information that can be used for further computations with the system or for inflating.

        Parameters
        ----------
        matrix : coo_matrix
            The matrix of the system of equations.
        rhs : coo_matrix
            The right-hand-side of the system of equations.
        problem : Problem
            A problem containing additional data structures. See :py:class:`Problem`.
        integration_order : int, optional
            The integration order used by specific shrink methods. Default is 1

        Returns
        -------
        matrix_shrink: coo_matrix
            The shrunk matrix of the system.
        rhs_shrink: coo_matrix
            The shrunk right-hand-side of the system.
        indices_not_dof: ndarray
            An array containing these lines of the original matrix that are no longer in the resulting matrix.
        num_new_dof: int
            The number of newly introduced degrees of freedom
        support_data: Dict[str,Any]
            A dict containing additional data that is needed for inflating the problem.

        Notes
        -----
        Suppose the original matrix :math:`\mathbf{A}` is of dimension :math:`N\times N` and the length of
        `indices_not_dof` is :math:`M`. Then, the dimension of the returned matrix is :math:`N_{out}\times N_{out}` with

        .. math::

            N_{out} = N - M + \text{num\_new\_dof}\,.
        """

    @abstractmethod
    def shrink_fcc(self, matrix: 'coo_matrix', rhs: 'coo_matrix', problem: 'FieldCircuitCouplingProblem',
                   integration_order: int = 1) -> Tuple['coo_matrix', 'coo_matrix', ndarray, int, Dict['str', Any]]:
        """Shrink the system of equations of a field-circuit coupling problem

        Parameters
        ----------
        matrix : coo_matrix
            The matrix of the system of equations.
        rhs : coo_matrix
            The right-hand-side of the system of equations.
        problem : FieldCircuitCouplingProblem
            A problem containing additional data structures. See :py:class:`Problem`.
        integration_order : int, optional
            The integration order used by specific shrink methods. Default is 1

        Returns
        -------
        matrix_shrink: coo_matrix
            The shrunk matrix of the system.
        rhs_shrink: coo_matrix
            The shrunk right-hand-side of the system.
        indices_not_dof: ndarray
            An array containing these lines of the original matrix that are no longer in the resulting matrix.
        num_new_dof: int
            The number of newly introduced degrees of freedom
        support_data: Dict[str,Any]
            A dict containing additional data that is needed for inflating the problem.

        """

    @abstractmethod
    def inflate(self, solution: ndarray, problem: 'Problem', support_data: Dict[str, Any] = None) -> ndarray:
        """Inflates a solution.

        After the system of equations of a problem was shrunk and solved, its solution can be inflated with this method.

        Parameters
        ----------
        solution : ndarray
            The solution of the shrunk system of equations.
        problem : Problem
            A problem containing additional data structures. See :py:class:`Problem`.
        support_data : Dict[str,Any], optional
            A dictionary with data needed for the inflation process. It is provided by the shrink method. If not given,
            these data is computed inside the function. By passing the data provided by the shrink method, this time
            can be saved. Default is None

        Returns
        -------
        solution_inflated: ndarray
            The solution of the original system of equations.
        """

    @abstractmethod
    def inflate_fcc(self, solution: ndarray, problem: 'FieldCircuitCouplingProblem',
                    support_data: Dict[str, Any] = None) -> ndarray:
        """Inflate the solution of a field-circuit coupling problem.

        Parameters
        ----------
        solution : ndarray
            The solution of the shrunk system of equations.
        problem : Problem
            A problem containing additional data structures. See :py:class:`Problem`.
        support_data : Dict[str,Any], optional
            A dictionary with data needed for the inflation process. It is provided by the shrink method. If not given,
            these data is computed inside the function. By passing the data provided by the shrink method, this time
            can be saved. Default is None

        Returns
        -------
        solution_inflated: ndarray
            The solution of the original system of equations.
        """
