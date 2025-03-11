# coding=utf-8
"""Polynomial shape function

.. sectionauthor:: Bundschuh
"""

import itertools
from typing import Iterable, Union, Callable, Tuple, TYPE_CHECKING, List
import numpy as np
from scipy import sparse

from pyrit.toolbox.QuadratureToolbox import gauss
from .SpectralShapeFunction import SpectralShapeFunction, Number

if TYPE_CHECKING:
    from pyrit.mesh import LineMesh
    from pyrit.region import Regions
    from pyrit.material import Materials, MatProperty
    from pyrit.excitation import Excitations


def spectral_matrix_scalar(scalar: Number, polynomials: List[np.polynomial.Polynomial],
                           domain: List[float], **kwargs) -> np.ndarray:
    r"""Compute a spectral matrix with a scalar weight.

    Let :math:`p_i` be the :math:`i`-th polynomial, :math:`\Omega` the given domain and :math:`\alpha` the
    given scalar. The matrix is defined as

    .. math::
        S_{ij} = \int_\Omega \alpha p_i p_j \mathrm{d}s\,.

    Parameters
    ----------
    scalar : Number
        The scalar :math:`\alpha`.
    polynomials : List[np.polynomial.Polynomial]
        A number of polynomials.
    domain : List[float]
        A list with two entries that are the lower and upper bound of the domain

    Returns
    -------
    matrix : np.ndarray
        The matrix :math:`\mathbf{S}`
    """
    if not isinstance(scalar, (int, float, complex)):
        raise ValueError("Not a scalar value")
    # Set the domain to all polynomials
    for poly in polynomials:
        poly.domain = domain

    if isinstance(scalar, complex) or any(issubclass(poly.coef.dtype.type, complex) for poly in polynomials):
        matrix_type = complex
    else:
        matrix_type = float

    matrix = np.empty((len(polynomials), len(polynomials)), dtype=matrix_type)

    for i, poly_i in enumerate(polynomials):
        for j, poly_j in enumerate(polynomials):
            integrand = scalar * poly_i * poly_j
            integral = integrand.integ()
            matrix[i, j] = integral(domain[1]) - integral(domain[0])

    return matrix


def spectral_matrix_function(function: Callable[[float], Number],
                             polynomials: List[np.polynomial.Polynomial],
                             domain: List[float],
                             integration_order: int = None, **kwargs) -> np.ndarray:
    r"""Compute a spectral matrix with a function as weight.

    Let :math:`p_i` be the :math:`i`-th polynomial, :math:`\Omega` the given domain and :math:`f` the given
    function. The matrix is defined as

    .. math::
        S_{ij} = \int_\Omega f p_i p_j \mathrm{d}s\,.

    Parameters
    ----------
    function : Callable[[float],Number]
        The function :math:`f`.
    polynomials : List[np.polynomial.Polynomial]
        A number of polynomials.
    domain : List[float]
        A list with two entries that are the lower and upper bound of the domain
    integration_order: int, optional
        The integration order for the integral. Default is the degree of the polynomials.

    Returns
    -------
    matrix : np.ndarray
        The matrix :math:`\mathbf{S}`
    """
    # Set the domain to all polynomials
    for poly in polynomials:
        poly.domain = domain

    if isinstance(function(domain[0]), complex) or \
            any(issubclass(poly.coef.dtype.type, complex) for poly in polynomials):
        matrix_type = complex
    else:
        matrix_type = float

    matrix = np.empty((len(polynomials), len(polynomials)), dtype=matrix_type)

    for i, poly_i in enumerate(polynomials):
        for j, poly_j in enumerate(polynomials):
            multiplied_poly = poly_i * poly_j
            if integration_order is None:
                order = max(1, multiplied_poly.degree() + 2)
            else:
                order = integration_order
            weights, points = gauss(order, domain[0], domain[1])

            value = 0
            for weight, point in zip(weights, points):
                value += weight * function(point) * multiplied_poly(point)
            matrix[i, j] = value

    return matrix


def spectral_matrix_polynomial(function: np.polynomial.Polynomial,
                               polynomials: List[np.polynomial.Polynomial],
                               domain: List[float], **kwargs) -> np.ndarray:
    r"""Compute a spectral matrix with a function as weight, where the function is a polynomial.

    Let :math:`p_i` be the :math:`i`-th polynomial, :math:`\Omega` the given domain and :math:`f` the given
    function. The matrix is defined as

    .. math::
        S_{ij} = \int_\Omega f p_i p_j \mathrm{d}s\,.

    Parameters
    ----------
    function : Callable[[float],Number]
        The function :math:`f`.
    polynomials : List[np.polynomial.Polynomial]
        A number of polynomials.
    domain : List[float]
        A list with two entries that are the lower and upper bound of the domain

    Returns
    -------
    matrix : np.ndarray
        The matrix :math:`\mathbf{S}`
    """
    # Set the domain to all polynomials
    for poly in polynomials:
        poly.domain = domain

    if issubclass(function.coef.dtype.type, complex) or \
            any(issubclass(poly.coef.dtype.type, complex) for poly in polynomials):
        matrix_type = complex
    else:
        matrix_type = float

    matrix = np.empty((len(polynomials), len(polynomials)), dtype=matrix_type)

    for i, poly_i in enumerate(polynomials):
        for j, poly_j in enumerate(polynomials):
            integrand = function * poly_i * poly_j
            integral = integrand.integ()
            matrix[i, j] = integral(domain[1]) - integral(domain[0])

    return matrix


def spectral_vector_scalar(scalar: Number, polynomials: List[np.polynomial.Polynomial],
                           domain: List[float], **kwargs) -> np.ndarray:
    r"""Compute a spectral vector with a scalar weight.

    Let :math:`p_i` be the :math:`i`-th polynomial, :math:`\Omega` the given domain and :math:`\alpha` the
    given scalar. The matrix is defined as

    .. math::
        v_{i} = \int_\Omega \alpha p_i \mathrm{d}s\,.

    Parameters
    ----------
    scalar : Number
        The scalar :math:`\alpha`.
    polynomials : List[np.polynomial.Polynomial]
        A number of polynomials.
    domain : List[float]
        A list with two entries that are the lower and upper bound of the domain

    Returns
    -------
    vector : np.ndarray
        The matrix :math:`\mathbf{v}`
    """
    if not isinstance(scalar, (int, float, complex)):
        raise ValueError("Not a scalar value")
    # Set the domain to all polynomials
    for poly in polynomials:
        poly.domain = domain

    if isinstance(scalar, complex) or any(issubclass(poly.coef.dtype.type, complex) for poly in polynomials):
        matrix_type = complex
    else:
        matrix_type = float

    vector = np.empty(len(polynomials), dtype=matrix_type)

    for i, poly_i in enumerate(polynomials):
        integral = poly_i.integ()
        vector[i] = scalar * integral(domain[1]) - integral(domain[0])

    return vector


def spectral_vector_function(function: Callable[[float], Number], polynomials: List[np.polynomial.Polynomial],
                             domain: List[float], integration_order: int = None, **kwargs) -> np.ndarray:
    r"""Compute a spectral vector with a function as weight.

    Let :math:`p_i` be the :math:`i`-th polynomial, :math:`\Omega` the given domain and :math:`f` the given
    function. The matrix is defined as

    .. math::
        v_{i} = \int_\Omega f p_i \mathrm{d}s\,.

    Parameters
    ----------
    function : Callable[[float],Number]
        The function :math:`f`.
    polynomials : List[np.polynomial.Polynomial]
        A number of polynomials.
    domain : List[float]
        A list with two entries that are the lower and upper bound of the domain
    integration_order: int, optional
        The integration order for the integral. Default is the degree of the polynomials.

    Returns
    -------
    vector : np.ndarray
        The matrix :math:`\mathbf{v}`
    """
    for poly in polynomials:
        poly.domain = domain

    if isinstance(function(domain[0]), complex) or \
            any(issubclass(poly.coef.dtype.type, complex) for poly in polynomials):
        matrix_type = complex
    else:
        matrix_type = float

    vector = np.empty(len(polynomials), dtype=matrix_type)

    for i, poly_i in enumerate(polynomials):
        if integration_order is None:
            order = max(poly_i.degree() + 2, 1)
        else:
            order = integration_order
        weights, points = gauss(order, domain[0], domain[1])

        value = 0
        for weight, point in zip(weights, points):
            value += weight * function(point) * poly_i(point)
        vector[i] = value

    return vector


def spectral_vector_polynomial(function: np.polynomial.Polynomial,
                               polynomials: List[np.polynomial.Polynomial],
                               domain: List[float], **kwargs) -> np.ndarray:
    r"""Compute a spectral vector with a function as weight, where the function is a polynomial.

    Let :math:`p_i` be the :math:`i`-th polynomial, :math:`\Omega` the given domain and :math:`f` the given
    function. The matrix is defined as

    .. math::
        v_{i} = \int_\Omega f p_i \mathrm{d}s\,.

    Parameters
    ----------
    function : Callable[[float],Number]
        The function :math:`f`.
    polynomials : List[np.polynomial.Polynomial]
        A number of polynomials.
    domain : List[float]
        A list with two entries that are the lower and upper bound of the domain

    Returns
    -------
    vector : np.ndarray
        The matrix :math:`\mathbf{s}`
    """
    # Set the domain to all polynomials
    for poly in polynomials:
        poly.domain = domain

    if issubclass(function.coef.dtype.type, complex) or \
            any(issubclass(poly.coef.dtype.type, complex) for poly in polynomials):
        matrix_type = complex
    else:
        matrix_type = float

    vector = np.empty(len(polynomials), dtype=matrix_type)

    for i, poly_i in enumerate(polynomials):
        integrand = function * poly_i
        integral = integrand.integ()
        vector[i] = integral(domain[1]) - integral(domain[0])

    return vector


class PolynomialShapeFunction(SpectralShapeFunction):
    r"""A spectral shape function class with polynomials

    The polynomial implementation of numpy is used for that. What can be confusing there is the usage of the window
    and the domain. Thus, it is here explained.

    One gives to Polynomial the coefficients of the respective polynomial basis. This can be monoms, i.e. the
    functions :math:`1`, :math:`x`, :math:`x^2` and so on, or other functions like e.g. Chebyshev polynomials. These
    polynomial basis functions are defined on the window :math:`[w_0,w_1]`. The evaluation, however, happens not on
    the window but on the domain :math:`[d_0,d_1]`. It is such that if you evaluate the Polynomial-object at
    :math:`d_0`, the value you get is the value of the polynomial you passed, evaluated at :math:`w_0`. The same
    holds for the right boundaries.

    So if you generate a polynomial :math:`x^2` (on the window) and you evaluate it at point :math:`4` you get
    the value :math:`1` (since :math:`(-1)^2 = 1`):

    >>> poly = Polynomial([0,0,1], window=(-1,1), domain=(4,5))
    >>> poly(4), poly(4.5), poly(5)
    (1.0, 0.0, 1.0)

    If we define the same polynomial on a different window, we get:

    >>> poly = Polynomial([0,0,1], window=(0,1), domain=(4,5))
    >>> poly(4), poly(4.5), poly(5)
    (0.0, 0.25, 1.0)

    To make this more formally, let :math:`p` be the polynomial we evaluate and :math:`r` be the polynomial we get
    from the coefficients that we passed to the constructor (:math:`x^2` in the examples). With the boundaries of
    the domain and window from above, we can define a linear mapping :math:`m(x)` such that :math:`m(d_0) = w_0`
    and :math:`m(d_1) = w_1`. Then the polynomail we evaluate is

    .. math::

        p(x) = r(m(x))\,.

    If you wish to evaluate the same polynomial to passed to the constructor, i.e. :math:`p\equiv r`, set the domain
    equal to the window (the actual values of the boundaries do not matter then). In this case, the mapping becomes
    the identity.

    When the polynomial object is integrated or differentiated, the resulting (returned) polynomial object has the
    same window and domain (and thus the same mapping as well). This, however, leads to wrong looking
    representations of the polynomial on the window. For example

    >>> poly = Polynomial([0,0,1], window=(0,1), domain=(4,5))
    >>> derivative = poly.deriv()
    >>> derivative.coef
    array([0., 4.])

    So this coefficients mean :math:`4x`, even though the derivative of :math:`x^2` is :math:`2x`. Due to the
    mapping it is correct.
    """

    def __init__(self, line_mesh: 'LineMesh', polynomials: Iterable[np.polynomial.Polynomial]):
        r"""Initialize a general polynomial shape function with a number of polynomials.

        Parameters
        ----------
        line_mesh : LineMesh
            The mesh
        polynomials : Iterable[np.polynomial.Polynomial]
            A number of polynomials to use as basis functions. The domain of the polynomials is unimportant because it
            will be changed based on the mesh.
        """
        super().__init__(line_mesh)
        self._polynomials = tuple(polynomials)
        if len(self._polynomials) == 0:
            raise ValueError("No polynomials given")

        for polynomial in self._polynomials:
            if not isinstance(polynomial, np.polynomial.polynomial.ABCPolyBase):
                raise ValueError("The polynomial is not of right type")
            if not np.allclose(polynomial.domain, polynomial.window):
                polynomial.domain = (polynomial.window[0], polynomial.window[1])

        self._polynomials_derivative = tuple(poly.deriv() for poly in self._polynomials)

    @property
    def number_polynomials(self):
        """The number of polynomials per element"""
        return len(self._polynomials)

    @property
    def degree(self):
        """Maximum degree of the polynomials"""
        return max(polynomial.degree() for polynomial in self._polynomials)

    def _calc_matrix_scalar(self, scalar: Union[List[Number], Number], elements: List[int],
                            polynomials: Tuple[np.polynomial.Polynomial], **kwargs) -> List[np.ndarray]:
        """Calc the matrices with scalar weight for the given elements

        Parameters
        ----------
        scalar : Union[List[Number], Number]
            The scalar value inside the matrix definition for every element. If a number is given, it is the same value
            in each element.
        elements : List[int]
            List of the indices of the elements
        polynomials : Tuple[np.polynomial.Polynomial]
            A tuple of polynomials to use for the method spectral_matrix_scalar
        kwargs : Any
            Passed to the function :py:func:`spectral_matrix_scalar`.

        Returns
        -------
        matrices : List[np.ndarray]
            A list of the matrices in each element
        """
        matrices = []
        if isinstance(scalar, (int, float, complex)):
            for element in elements:
                matrices.append(spectral_matrix_scalar(scalar, polynomials,
                                                        self.mesh.node[self.mesh.elem2node[element]], **kwargs))
        else:
            for value, element in zip(scalar, elements):
                matrices.append(spectral_matrix_scalar(value, polynomials, self.mesh.elem2node[element], **kwargs))

        return matrices

    def _calc_matrix_function(self, function: Union[List[Callable[[float], Number]], Callable[[float], Number]],
                              elements: List[int], polynomials: Tuple[np.polynomial.Polynomial],
                              **kwargs) -> List[np.ndarray]:
        """Calc the matrices with functional weight for the given elements

        Parameters
        ----------
        function : Union[List[Callable[[float], Number]], Callable[[float], Number]]
            The function inside the matrix definition for every element. If a single function is given, it is the same
            in each element.
        elements : List[int]
            List of the indices of the elements
        polynomials : Tuple[np.polynomial.Polynomial]
            A tuple of polynomials to use for the method spectral_matrix_scalar
        kwargs : Any
            Passed to the function :py:func:`spectral_matrix_scalar`.

        Returns
        -------
        matrices : List[np.ndarray]
            A list of the matrices in each element
        """
        matrices = []
        try:
            iter(function)
        except TypeError:
            for element in elements:
                matrices.append(spectral_matrix_function(function, polynomials, self.mesh.elem2node[element], **kwargs))
        else:
            for func, element in zip(function, elements):
                matrices.append(spectral_matrix_function(func, polynomials, self.mesh.elem2node[element], **kwargs))

        return matrices

    def _calc_vector_scalar(self, scalar: Union[List[Number], Number], elements: List[int],
                            polynomials: Tuple[np.polynomial.Polynomial], **kwargs) -> List[np.ndarray]:
        """Calc the vectors with scalar weight for the given elements

        Parameters
        ----------
        scalar : Union[List[Number], Number]
            The scalar value inside the matrix definition for every element. If a number is given, it is the same value
            in each element.
        elements : List[int]
            List of the indices of the elements
        polynomials : Tuple[np.polynomial.Polynomial]
            A tuple of polynomials to use for the method spectral_matrix_scalar
        kwargs : Any
            Passed to the function :py:func:`spectral_matrix_scalar`.

        Returns
        -------
        vectors : List[np.ndarray]
            A list of the vectors in each element
        """
        vectors = []
        if isinstance(scalar, (int, float, complex)):
            for element in elements:
                vectors.append(spectral_vector_scalar(scalar, polynomials, self.mesh.elem2node[element], **kwargs))
        else:
            for value, element in zip(scalar, elements):
                vectors.append(spectral_vector_scalar(value, polynomials, self.mesh.elem2node[element], **kwargs))

        return vectors

    def _calc_vector_function(self, function: Union[List[Callable[[float], Number]], Callable[[float], Number]],
                              elements: List[int], polynomials: Tuple[np.polynomial.Polynomial],
                              **kwargs) -> List[np.ndarray]:
        """Calc the vectors with functional weight for the given elements

        Parameters
        ----------
        function : Union[List[Callable[[float], Number]], Callable[[float], Number]]
            The function inside the matrix definition for every element. If a single function is given, it is the same
            in each element.
        elements : List[int]
            List of the indices of the elements
        polynomials : Tuple[np.polynomial.Polynomial]
            A tuple of polynomials to use for the method spectral_matrix_scalar
        kwargs : Any
            Passed to the function :py:func:`spectral_matrix_scalar`.

        Returns
        -------
        vectors : List[np.ndarray]
            A list of the vectors in each element
        """
        vectors = []
        try:
            iter(function)
        except TypeError:
            for element in elements:
                vectors.append(spectral_vector_function(function, polynomials, self.mesh.elem2node[element], **kwargs))
        else:
            for func, element in zip(function, elements):
                vectors.append(spectral_vector_function(func, polynomials, self.mesh.elem2node[element], **kwargs))

        return vectors

    def _matrix_routine(self, material: Union[Callable[[float], Number], np.ndarray, Number,
                                              Tuple['Regions', 'Materials', 'MatProperty']],
                        polynomials: Tuple[np.polynomial.Polynomial], **kwargs) -> sparse.spmatrix:
        case, material = self._process_material(material)

        if case == "tuple":
            regions, materials, mat_property_class = material
            offset, matrices = [], []

            for key in regions.get_keys():  # iterate over regions
                regi = regions.get_regi(key)

                if regi.dim != 1:
                    continue

                material_id = regi.mat
                if material_id is None:  # only consider regions with a material
                    continue

                material = materials.get_material(material_id)  # get material of current region
                prop = material.get_property(mat_property_class)  # get property of material, e.g. Permeability
                if prop is None:  # Consider only regions that have the desired material property
                    continue

                if not prop.is_isotrop:
                    raise ValueError("Only isotrope materials can be handled"
                                     "")
                # get indices of all mesh elements within the region:
                indices = np.where(self.mesh.elem2regi == regi.ID)[0].astype(np.int32, casting="same_kind", copy=False)
                if prop.is_homogeneous:
                    if prop.is_linear:  # homogeneous, linear, isotropic
                        if prop.is_time_dependent:
                            value = prop.value()
                        else:  # homogeneous, linear, isotropic, time independent
                            value = prop.value

                        if isinstance(value, np.ndarray):
                            if len(value.shape) != 1:
                                raise NotImplementedError("The value shape is not supported.")
                        matrices_tmp = self._calc_matrix_scalar(value, indices, polynomials, **kwargs)
                    else:  # nonlinear
                        raise NotImplementedError

                else:  # inhomogeneous
                    if prop.is_linear:  # inhomogeneous, linear
                        matrices_tmp = self._calc_matrix_function(prop.value, indices, polynomials, **kwargs)
                    else:  # nonlinear
                        raise NotImplementedError

                offset.append(indices)
                matrices.append(matrices_tmp)
            matrices = list(itertools.chain(*matrices))
            offset = np.hstack(offset)
        else:
            offset = np.arange(self.mesh.num_elem)
            if case == "number":  # material is a float -> constant for all mesh elements
                matrices = self._calc_matrix_scalar(material, offset, polynomials, **kwargs)
            elif case == "array":  # material is an array -> one value per mesh element
                matrices = self._calc_matrix_scalar(material, offset, polynomials, **kwargs)
            elif case == "function":  # material is a function
                matrices = self._calc_matrix_function(material, offset, polynomials, **kwargs)
            else:
                raise ValueError("An internal error occurred. Case unknown")

        # Bring all matrices together to a block diag matrix
        order = np.argsort(offset)
        matrix = sparse.block_diag([matrices[k] for k in order])

        return matrix

    def stiffness_matrix(self, *material: Union[Callable[[float], Number], np.ndarray, Number,
                                                Tuple['Regions', 'Materials', 'MatProperty']],
                         **kwargs) -> sparse.spmatrix:
        return self._matrix_routine(material, self._polynomials_derivative, **kwargs)

    def mass_matrix(self, *material: Union[Callable[[float], Number], np.ndarray, Number,
                                           Tuple['Regions', 'Materials', 'MatProperty']], **kwargs) -> sparse.spmatrix:
        return self._matrix_routine(material, self._polynomials, **kwargs)

    def _vector_routine(self, load: Union[Callable[[float], Number], np.ndarray, Number,
                                          Tuple['Regions', 'Excitations']],
                        polynomials: Tuple[np.polynomial.Polynomial], **kwargs):
        case, load = self._process_load(load)

        if case == "tuple":
            regions, excitations = load
            offset, vectors = [], []

            for key in regions.get_keys():
                regi = regions.get_regi(key)

                if regi.dim != 1:
                    continue

                if regi.exci is None:
                    continue
                exci = excitations.get_exci(regi.exci)

                indices = np.where(self.mesh.elem2regi == regi.ID)[0]

                if exci.is_homogeneous:
                    if exci.is_linear:
                        if exci.is_time_dependent:  # homogeneous, linear, time dependent
                            value = exci.value()
                        else:  # homogeneous, linear, time independent
                            value = exci.value

                        vectors_tmp = self._calc_vector_scalar(value, indices, polynomials, **kwargs)
                    else:  # homogeneous, nonlinear
                        raise NotImplementedError
                else:
                    if exci.is_linear:  # inhomogeneous, linear
                        vectors_tmp = self._calc_vector_function(exci.value, indices, polynomials, **kwargs)
                    else:  # inhomogeneous, nonlinear
                        raise NotImplementedError

                offset.append(indices)
                vectors.append(vectors_tmp)

            vectors = list(itertools.chain(*vectors))
            offset = np.hstack(offset)
        else:
            offset = np.arange(self.mesh.num_elem)
            if case == "number":
                vectors = self._calc_vector_scalar(load, offset, polynomials, **kwargs)
            elif case == "array":
                vectors = self._calc_vector_scalar(load, offset, polynomials, **kwargs)
            elif case == "function":
                vectors = self._calc_vector_function(load, offset, polynomials, **kwargs)
            else:
                raise ValueError("An internal error occurred. Case unknown")

        order = np.argsort(offset)
        vector = sparse.coo_matrix(np.vstack([vectors[k] for k in order]).reshape(-1, 1))
        vector.resize((self.number_polynomials * self.mesh.num_elem, 1))
        return vector

    def load_vector(self,
                    *load: Union[Callable[[float], Number], np.ndarray, Number, Tuple['Regions', 'Excitations']],
                    **kwargs):
        return self._vector_routine(load, self._polynomials, **kwargs)

    def _evaluate(self, position: float, polynomials: List[np.polynomial.Polynomial]):
        element_index = self.mesh.find_elemidx([position])[0]
        nodes = self.mesh.node[self.mesh.elem2node[element_index]]

        for poly in polynomials:
            poly.domain = nodes

        return np.array([poly(position) for poly in polynomials])

    def _evaluate_on_element(self, element: int, relative_position: float, polynomials: List[np.polynomial.Polynomial]):
        nodes = self.mesh.node[self.mesh.elem2node[element]]
        position = nodes[0] + relative_position * (nodes[1] - nodes[0])

        for poly in polynomials:
            poly.domain = nodes

        return np.array([poly(position) for poly in polynomials])

    def evaluate(self, position: float, number_basis_functions: Union[int, Iterable[int]] = None) -> \
            Union[float, np.ndarray]:
        if isinstance(number_basis_functions, int):
            return self._evaluate(position, [self._polynomials[number_basis_functions]])[0]

        if number_basis_functions is None:
            number_basis_functions = np.arange(self.number_polynomials)

        return np.array(self._evaluate(position, [self._polynomials[k] for k in number_basis_functions]))

    def evaluate_derivative(self, derivative: int, position: float,
                            number_basis_functions: Union[int, Iterable[int]] = None) -> Union[float, np.ndarray]:
        if isinstance(number_basis_functions, int):
            polynomial = self._polynomials[number_basis_functions]
            polynomial.domain = (polynomial.window[0], polynomial.window[1])
            return self._evaluate(position, [polynomial.deriv(derivative)])[0]

        if number_basis_functions is None:
            number_basis_functions = np.arange(self.number_polynomials)

        polynomials = [self._polynomials[k] for k in number_basis_functions]
        for poly in polynomials:
            poly.domain = (poly.window[0], poly.window[1])

        return np.array(self._evaluate(position, [poly.deriv(derivative) for poly in polynomials]))

    def evaluate_on_element(self, element: int, relative_position: float,
                            number_basis_functions: Union[int, Iterable[int]] = None) -> Union[float, np.ndarray]:
        if isinstance(number_basis_functions, int):
            return self._evaluate_on_element(element, relative_position, [self._polynomials[number_basis_functions]])[0]

        if number_basis_functions is None:
            number_basis_functions = np.arange(self.number_polynomials)

        return np.array(self._evaluate_on_element(element, relative_position,
                                                  [self._polynomials[k] for k in number_basis_functions]))

    def evaluate_derivative_on_element(self, element: int, derivative: int, relative_position: float,
                                       number_basis_functions: Union[int, Iterable[int]] = None) -> \
            Union[float, np.ndarray]:
        if isinstance(number_basis_functions, int):
            polynomial = self._polynomials[number_basis_functions]
            polynomial.domain = (polynomial.window[0], polynomial.window[1])
            return self._evaluate_on_element(element, relative_position, [polynomial.deriv(derivative)])[0]

        if number_basis_functions is None:
            number_basis_functions = np.arange(self.number_polynomials)

        polynomials = [self._polynomials[k] for k in number_basis_functions]
        for poly in polynomials:
            poly.domain = (poly.window[0], poly.window[1])

        return np.array(self._evaluate_on_element(element, relative_position,
                                                  [poly.deriv(derivative) for poly in polynomials]))

    def get_function(self, number_basis_function: int, derivative: int = 0):
        poly = self._polynomials[number_basis_function].copy()
        poly.domain = (poly.window[0], poly.window[1])

        return poly.deriv(derivative)
