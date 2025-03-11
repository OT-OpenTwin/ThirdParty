# coding=utf-8
"""The class SpectralShapeFunction

.. sectionauthor:: Bundschuh
"""

from abc import ABC, abstractmethod
from typing import Iterable, Union, Callable, Tuple, Any
from inspect import signature, isclass

import numpy as np
from scipy import sparse

# if TYPE_CHECKING:
from pyrit.mesh import LineMesh
from pyrit.region import Regions
from pyrit.material import Materials, MatProperty
from pyrit.excitation import Excitations

Number = Union[int, float, complex]


class SpectralShapeFunction(ABC):
    """Abstract class for a spectral shape function"""

    def __init__(self, line_mesh: LineMesh):
        self.mesh = line_mesh

    def _process_single_argument(self, arg: Any) -> str:
        """Process the argument of a single value.

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
            if len(signature(arg).parameters) == 1:
                return "function"
            raise ValueError(f"The function has not the expected number of {str(self.mesh.node.shape[1])} arguments")

        if isinstance(arg, np.ndarray):
            arg = arg.flatten()
            if arg.size != self.mesh.num_elem:
                raise ValueError(f"The array has {arg.size} entries, but needs {self.mesh.num_elem} entries")
            return "array"

        if isinstance(arg, (complex, float, int)):
            return "number"

        raise ValueError("Argument type not excepted.")

    @staticmethod
    def _process_multiple_materials(material: Tuple[Any]) -> Tuple['Regions', 'Materials', 'MatProperty']:
        """Process materials when more than one value is given"""
        material_out = [None, None, None]
        classes: list = [Regions, Materials, MatProperty]
        for k, mat in enumerate(material):
            if isinstance(mat, Regions):
                material_out[0] = mat
            elif isinstance(mat, Materials):
                material_out[1] = mat
            elif isclass(mat) and issubclass(mat, MatProperty):
                material_out[2] = mat
            else:
                raise ValueError(f"Unexpected argument: {mat}")

        for k, c in enumerate(classes):
            if material_out[k] is None:
                raise ValueError(f"The class {c} is missing in the materials.")

        return material_out

    @staticmethod
    def _process_multiple_loads(load: Tuple[Any]) -> Tuple['Regions', 'Excitations']:
        """Process loads when more than one value is given"""
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

        return load_out

    def _process_material(self, material: Tuple[Any]) -> Tuple[str,
                                                               Union[Callable[[float], Number], np.ndarray, Number,
                                                                     Tuple['Regions', 'Materials', 'MatProperty']]]:
        """Process the material arguments.

        Parameters
        ----------
        material : Tuple[Any]
            The material arguments.

        Returns
        -------
        type : str
            The type of the arguments. Either "tuple", "function", "array" or "number".
        material : Union[Callable[[float], Number], np.ndarray, Number, Tuple['Regions', 'Materials', 'MatProperty']]
            The arguments in a standard format. If case is "tuple", the order in `material` is as given (independent of
            the order of the input). If case is not "tuple", `material` is no list but just the value.

        Raises
        ------
        ValueError
            When args has not the expected format and type
        """
        if len(material) not in (1, 3):
            raise ValueError(f"Wrong number of inputs. Got {len(material)} but has to be 1 or 3.")

        case, material_out = None, ''

        if not isinstance(material, tuple):  # needed for TetCartesianNodal
            raise ValueError("An internal error occurred.")

        if len(material) == 1:
            case = self._process_single_argument(material[0])  # pylint: disable=no-value-for-parameter
            material_out = material[0]

        if len(material) == 3:
            case = 'tuple'
            material_out = self._process_multiple_materials(material)

        return case, material_out

    def _process_load(self, load: Tuple[Any]) -> Tuple[str,
                                                       Union[Callable[[float], Number], np.ndarray, Number,
                                                             Tuple['Regions', 'Excitations']]]:
        """Process the load arguments

        Parameters
        ----------
        load : Tuple[Any]
            The load argument

        Returns
        -------
        type : str
            The type of the arguments. Either "tuple", "function", "array" or "number".
        load : Union[Callable[[float], Number], np.ndarray, Number, Tuple['Regions', 'Excitations']]
            The arguments in a standard format. If case is "tuple", the order in `load` is as given (independent of
            the order of the input). If case is not "tuple", `load` is no list but just the value.

        Raises
        ------
        ValueError
            When args has not the expected format and type
        """
        if len(load) not in (1, 2):
            raise ValueError(f"Wrong number of inputs. Got {len(load)} but has to be 1 or 2.")

        load_out = None
        case = ''
        if len(load) == 1:
            case = self._process_single_argument(*load)  # pylint: disable=no-value-for-parameter
            load_out = load[0]

        if len(load) == 2:
            case = 'tuple'
            load_out = self._process_multiple_loads(load)

        return case, load_out

    @abstractmethod
    def stiffness_matrix(self, *material: Union[Callable[[float], Number], np.ndarray, Number,
                                                Tuple['Regions', 'Materials', 'MatProperty']],
                         **kwargs) -> sparse.spmatrix:
        r"""Compute the stiffness matrix

        Let :math:`f_i` be a basis function, :math:`\Omega` be the whole domain and :math:`\alpha` be the material
        parameter. The stiffness matrix is defined as

        .. math::
            S_{ij} = \int_\Omega \alpha f'_i f'_j \mathrm{d}s\,.

        Parameters
        ----------
        material : Union[Callable[[float], Number], np.ndarray, Number, Tuple['Regions', 'Materials', 'MatProperty']]
            Information about the material :math:`\alpha`. This can be:

                - A function that returns a scalar value for every point inside the domain
                - A (T,) array that has one value for every element (T elements)
                - A single value if the material has everywhere the same value
                - A tuple (Regions, Materials, MatProperty). MatProperty has to be the class of the property that
                    shall be considered, e.g. Permittivity

        Returns
        -------
        stiffness_matrix : sparse.spmatrix
            The stiffness matrix
        """

    @abstractmethod
    def mass_matrix(self, *material: Union[Callable[[float], Number], np.ndarray, Number,
                                           Tuple['Regions', 'Materials', 'MatProperty']], **kwargs) -> sparse.spmatrix:
        r"""Compute the mass matrix

        Let :math:`f_i` be a basis function, :math:`\Omega` be the whole domain and :math:`\alpha` be the material
        parameter. The mass matrix is defined as

        .. math::
            M_{ij} = \int_\Omega \alpha f_i f_j \mathrm{d}s\,.

        Parameters
        ----------
        material : Union[Callable[[float], Number], np.ndarray, Number, Tuple['Regions', 'Materials', 'MatProperty']]
            Information about the material :math:`\alpha`. This can be:

                - A function that returns a scalar value for every point inside the domain
                - A (T,) array that has one value for every element (T elements)
                - A single value if the material has everywhere the same value
                - A tuple (Regions, Materials, MatProperty). MatProperty has to be the class of the property that
                    shall be considered, e.g. Permittivity

        Returns
        -------
        mass_matrix : sparse.spmatrix
            The mass matrix
        """

    @abstractmethod
    def load_vector(self, *load: Union[Callable[[float], Number], np.ndarray, Number, Tuple['Regions', 'Excitations']],
                    **kwargs) -> sparse.spmatrix:
        r"""Compute the load vector

        Let :math:`f_i` be a basis function, :math:`\Omega` be the whole domain and :math:`g` be the load function. The
        load vector is defines as

        .. math::

            q_{i} = \int_\Omega g f_i \mathrm{d}s

        Parameters
        ----------
        load : Union[Callable[[float], Number], np.ndarray, Number, Tuple['Regions', 'Excitations']]
            Information about the excitation :math:`g`. This can be:

                - A function that gives a value for every point inside the domain
                - A (T,) array that has one value for every element (T elements)
                - A single value if the excitation has everywhere the same value
                - A tuple (Regions, Excitations)

        Returns
        -------
        load_vector : sparse.spmatrix
            The load_vector
        """

    @abstractmethod
    def evaluate(self, position: float, number_basis_functions: Union[int, Iterable[int]] = None) -> \
            Union[float, np.ndarray]:
        """Evaluate basis functions at a certain position

        Parameters
        ----------
        position : float
            The position to evaluate. Must lie inside the mesh.
        number_basis_functions : Union[int, Iterable[int]], optional
            The indices of the basis functions to evaluate. Default is all functions

        Returns
        -------
        evaluations : Union[float, np.ndarray]
            The evaluations of the functions. Depending on the `number_basis_functions` this is either a single number
            or an array.
        """

    @abstractmethod
    def evaluate_derivative(self, derivative: int, position: float,
                            number_basis_functions: Union[int, Iterable[int]] = None) -> Union[float, np.ndarray]:
        """Evaluate derivatives of basis functions at certain positions

        Parameters
        ----------
        derivative : int
            The number of differentiations
        position : float
            The position to evaluate. Must lie inside the mesh
        number_basis_functions : Union[int, Iterable[int]], optional
            The indices of the basis functions to evaluate. Default is all functions

        Returns
        -------
        evaluations : Union[float, np.ndarray]
            The evaluations of the derivatives. Depending on the `number_basis_functions` this is either a single number
            or an array.
        """

    @abstractmethod
    def evaluate_on_element(self, element: int, relative_position: float,
                            number_basis_functions: Union[int, Iterable[int]] = None) -> Union[float, np.ndarray]:
        """Evaluate basis functions at a relative position on an element

        Parameters
        ----------
        element : int
            The element index in the mesh
        relative_position : float
            The relative position on the element. Must be in :math:`[0,1]`.
        number_basis_functions : Union[int, Iterable[int]], optional
            The indices of the basis functions to evaluate. Default is all functions

        Returns
        -------
        evaluations : Union[float, np.ndarray]
            The evaluations of the functions. Depending on the `number_basis_functions` this is either a single number
            or an array.
        """

    @abstractmethod
    def evaluate_derivative_on_element(self, element: int, derivative: int, relative_position: float,
                                       number_basis_functions: Union[int, Iterable[int]] = None) -> \
            Union[float, np.ndarray]:
        """Evaluate derivatives of basis functions at a relative position on an element

        Parameters
        ----------
        element : int
            The element index in the mesh
        derivative : int
            The number of differentiations
        relative_position : float
            The relative position on the element. Must be in :math:`[0,1]`.
        number_basis_functions : Union[int, Iterable[int]], optional
            The indices of the basis functions to evaluate. Default is all functions

        Returns
        -------
        evaluations : Union[float, np.ndarray]
            The evaluations of the derivatives. Depending on the `number_basis_functions` this is either a single number
            or an array.
        """

    @abstractmethod
    def get_function(self, number_basis_function: int, derivative: int = 0):
        """Return a callable for a certain basis function"""
