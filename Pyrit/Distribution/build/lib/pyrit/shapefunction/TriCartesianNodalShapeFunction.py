# coding=utf-8
"""
File containing the class TriAxisymmetricNodalShapeFunction.

Numba is used with a lot functions to get a good performance. The data types of the arguments of the numa functions
can be given in the decorator. If one of these functions is called with another data type it does not work anymore.
Because different data types of some arguments should be supported the data types are not indicated in the decorator.
Anyway, the code is written such that the data types of the arguments are as equal as possible for different user input
parameters. So the number of compilations with numba should be at a minimum.

.. sectionauthor:: bundschuh, ruppert
"""
# pylint: disable=duplicate-code

from typing import Union, Callable, Tuple, TYPE_CHECKING

import numpy as np
from numpy import ndarray
from scipy.sparse import coo_matrix, csr_matrix
from numba import prange

from pyrit.region import Regions
from pyrit.bdrycond import BdryCond, BCNeumann  # , BCRobin

from pyrit.toolbox.QuadratureToolbox import gauss
from pyrit.toolbox.NumbaToolbox import njit_cache
from pyrit.ValueHandler import evaluate_for_num_int_edge

from .ShapeFunction import Number, MaterialData, NumericalData
from .NodalShapeFunction import NodalShapeFunction

if TYPE_CHECKING:
    from pyrit.mesh import TriMesh


# region General functions
@njit_cache(parallel=True)
def calc_evaluation_points_element(local_coordinates: np.ndarray, transform_coefficients: np.ndarray,
                                   elements: np.ndarray) -> np.ndarray:
    """Calculates the coordinates (rho,z) needed for the evaluation of the numerical integration on an element.

    Returns a three dimensional array with the evaluation coordinates for all elements specified. The return values is
    a (E,N,2) array. It is `out[e,n,0]` and `out[e,n,1]` the rho and z coordinate on element e and evaluation point
    n, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        ======  =======

    Parameters
    ----------
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    transform_coefficients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elements : np.ndarray
        (E,) array. Array with the indices of elements the evaluation points should calculated for.

    Returns
    -------
    out : np.ndarray
        (E,N,2) array.
    """
    num_elements = len(elements)
    num_coordinates = local_coordinates.shape[0]
    coords = np.empty((num_elements, num_coordinates, 2))
    ones = np.ones(num_coordinates)
    local_cds = np.column_stack((local_coordinates, ones))
    for k in prange(num_elements):
        element = elements[k]
        tc = transform_coefficients[element]  # (2,3) array
        tct = tc.T
        coords[k] = local_cds @ tct
    return coords


@njit_cache(parallel=True)
def calc_evaluation_points_edge(local_coordinates: np.ndarray, nodes: np.ndarray,
                                edges: np.ndarray, edge2node: np.ndarray) -> np.ndarray:
    """Calculates the coordinates (s,z) needed for the evaluation of the numerical integration on an edge.

    Returns a three dimensional array with the evaluation coordinates for all edges specified. The return values is
    a (E,N,2) array. It is `out[e,n,0]` and `out[e,n,1]` the s and z coordinate on edge e and evaluation point n,
    respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of edges in `edges`
        T       Number of elements in the mesh
        ======  =======

    Parameters
    ----------
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    node_transformed : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edges : np.ndarray
        (E,) array. Array with the indices of edges the evalutaion points should calculated for.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    out : np.ndarray
        (E,N,2) array.
    """
    num_edges = len(edges)
    num_coordinates = len(local_coordinates)
    coords = np.empty((num_edges, num_coordinates, 2))

    for k in prange(num_edges):
        edge = edges[k]
        for kk in range(num_coordinates):
            coords[k, kk] = nodes[edge2node[edge, 0]] + local_coordinates[kk] * (nodes[edge2node[edge, 1]] -
                                                                                 nodes[edge2node[edge, 0]])

    return coords


def eval_inhom_lin_aniso(fun: Callable[[float, float], np.ndarray], evaluation_points: np.ndarray):
    """Evaluates an inhomogeneous, linear and anisotropic function

    Parameters
    ----------
    fun : Callable[[float, float], np.ndarray]
        The function to evaluate
    evaluation_points : np.ndarray
        (E,N,2) array. For every element E there are N points with 2 coordinates.

    Returns
    -------
    evaluations : np.ndarray
        (E,N,X) array with evaluations. X is the dimension of the return type from fun
    """
    vfun = np.vectorize(fun, signature='(),()->(i,i)')
    evaluations = vfun(evaluation_points[:, :, 0], evaluation_points[:, :, 1])
    # evaluations.astype(float, copy=False)  #change: why make it float?
    return evaluations


def eval_inhom_lin_vec(fun: Callable[[float, float], np.ndarray], evaluation_points: np.ndarray):
    """Evaluates an inhomogeneous, linear and anisotropic function

    Parameters
    ----------
    fun : Callable[[float, float], np.ndarray]
        The function to evaluate
    evaluation_points : np.ndarray
        (E,N,2) array. For every element E there are N points with 2 coordinates.

    Returns
    -------
    evaluations : np.ndarray
        (E,N,X) array with evaluations. X is the dimension of the return type from fun
    """
    vfun = np.vectorize(fun, signature='(),()->(i)')
    evaluations = vfun(evaluation_points[:, :, 0], evaluation_points[:, :, 1])
    # evaluations.astype(float, copy=False)  #change: why make it float?
    return evaluations


# def evaluate_for_num_int_edge(fun: Callable[[float, float], float], evaluation_points: np.ndarray):
#     """Evaluates the function `fun` for numerical integration on edges.
#
#     Evaluates `fun` at the evaluation points for the numerical integration for all specified edges.
#
#     .. table:: Symbols
#
#         ======  =======
#         Symbol  Meaning
#         ======  =======
#         N       Number of evaluation points
#         E       Number of edges in `edges`
#         ======  =======
#
#     Parameters
#     ----------
#     fun : Callable[[float, float], float]
#         The function to evaluate.
#     evaluation_points : np.ndarray
#         (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_edge`.
#
#     Returns
#     -------
#     evaluations : np.ndarray
#         (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
#         numerical integration.
#
#     Notes
#     -----
#     This function has to be called before matrix elements, where a numerical integration of a arbitrary funtion is
#     necessary, can be computed.
#     """
#     evaluations = np.vectorize(fun)(evaluation_points[:, :, 0], evaluation_points[:, :, 1])
#     evaluations.astype(float, copy=False)
#     return evaluations


# endregion


# region Functions for divgrad


@njit_cache(parallel=True)
def calc_divgrad_constant_scalar(elements: np.ndarray, value: Union[int, float], b: np.ndarray, c: np.ndarray,
                                 length: float, determinant_b: np.ndarray, elem2node) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the divgrad_operator with a constant material.

    Calculates the contribution of the elements specified in `elements` to the divgrad matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered.
    value : Union[int, float]
        The value of the material.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianNodalShapeFunction.divgrad_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9), np.int_)
    j = np.empty((num_elements, 9), np.int_)
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        b_mat = np.outer(b[element], b[element])
        c_mat = np.outer(c[element], c[element])

        mat_elem = length / 2 / determinant_b[element] * value * (c_mat + b_mat)
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


# todo:docstring
@njit_cache(parallel=True)
def calc_divgrad_constant_tensor(elements: np.ndarray, value: np.ndarray, b: np.ndarray, c: np.ndarray,
                                 length: float, determinant_b: np.ndarray, elem2node) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculates elements for the divgrad_operator with a constant material tensor.

    Calculates the contribution of the elements specified in `elements` to the divgrad matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered.
    value : np.ndarray
        (2,2) The value of the material.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9), np.int_)
    j = np.empty((num_elements, 9), np.int_)
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        b_mat = np.outer(b[element], b[element])
        c_mat = np.outer(c[element], c[element])
        bc_mat = np.outer(b[element], c[element])
        cb_mat = np.outer(c[element], b[element])

        mat_elem = length / 2 / determinant_b[element] * \
                   (b_mat * value[0, 0] + cb_mat * value[1, 0] + bc_mat * value[0, 1] + c_mat * value[1, 1])
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


# @njit_cache(parallel=True)
def calc_divgrad_scalar_per_elem(elements: np.ndarray, value: np.ndarray, b: np.ndarray, c: np.ndarray, length: float,
                                 determinant_b: np.ndarray, elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the divgrad_operator with one constant value of the material per element.

    Calculates the contribution of the elements specified in `elements` to the divgrad matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered
    value : np.ndarray
        (E,) array. One material value per element.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9))
    j = np.empty((num_elements, 9))
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        b_mat = np.outer(b[element], b[element])
        c_mat = np.outer(c[element], c[element])

        mat_elem = length / 2 / determinant_b[element] * value[k] * (c_mat + b_mat)

        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


# todo:docstring
@njit_cache(parallel=True)
def calc_divgrad_tensor_per_elem(elements: np.ndarray, value: np.ndarray, b: np.ndarray, c: np.ndarray,
                                 length: float, determinant_b: np.ndarray, elem2node) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculates elements for the divgrad_operator with one constant material tensor per element.

    Calculates the contribution of the elements specified in `elements` to the divgrad matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered.
    value : np.ndarray
        (T,2,2) The value of the material.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9), np.int_)
    j = np.empty((num_elements, 9), np.int_)
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        b_mat = np.outer(b[element], b[element])
        c_mat = np.outer(c[element], c[element])
        bc_mat = np.outer(b[element], c[element])
        cb_mat = np.outer(c[element], b[element])

        mat_elem = length / 2 / determinant_b[element] * value * (c_mat + b_mat) * \
                   (b_mat * value[k, 0, 0] + cb_mat * value[k, 1, 0] + bc_mat * value[k, 0, 1] + c_mat * value[k, 1, 1])
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


# @njit_cache(parallel=True)
def calc_divgrad_function_scalar(elements: np.ndarray, weights: np.ndarray,
                                 evaluations: np.ndarray, b: np.ndarray, c: np.ndarray, length: float,
                                 determinant_b: np.ndarray, elem2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the divgrad_operator with a function as material.

    Calculates the contribution of the elements specified in `elements` to the divgrad matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    evaluations : np.ndarray
        (E,N) array. For every element the N evalutations of the material function at the evaluation points for the
        numerical integration. See :py:func:`evaluate_for_num_int_element`.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9))
    j = np.empty((num_elements, 9))
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        b_mat = np.outer(b[element], b[element])
        c_mat = np.outer(c[element], c[element])

        integral = np.dot(weights, evaluations[k])
        mat_elem = length / determinant_b[element] * (c_mat + b_mat) * integral
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)  # todo:docstring
def calc_divgrad_function_tensor(elements: np.ndarray, weights: np.ndarray,
                                 evaluations: np.ndarray, b: np.ndarray, c: np.ndarray, length: float,
                                 determinant_b: np.ndarray, elem2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the divgrad_operator with a function as material.

    Calculates the contribution of the elements specified in `elements` to the divgrad matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration. See :py:func:`evaluate_for_num_int_element`.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9))
    j = np.empty((num_elements, 9))
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        b_mat = np.outer(b[element], b[element])
        c_mat = np.outer(c[element], c[element])
        bc_mat = np.outer(b[element], c[element])

        first_integral = np.dot(weights, evaluations[k, :, 0, 0])
        second_integral = np.dot(weights, evaluations[k, :, 0, 1])
        third_integral = np.dot(weights, evaluations[k, :, 1, 0])
        fourth_integral = np.dot(weights, evaluations[k, :, 1, 1])

        sum_integrals = b_mat * first_integral + bc_mat * second_integral - \
                        bc_mat * third_integral + c_mat * fourth_integral

        mat_elem = length / determinant_b[element] * (c_mat + b_mat) * sum_integrals
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


# endregion


# region Functions for mass
@njit_cache(parallel=True)
def calc_mass_constant_scalar(elements: np.ndarray, value: Union[int, float], length: float, determinant_b: np.ndarray,
                              elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the mass matrix with one constant value of the material per element.

    Calculates the contribution of the elements specified in `elements` to the mass matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered
    value : np.ndarray
        (E,) array. One value per element.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9))
    j = np.empty((num_elements, 9))
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        mat_elem = length * value * determinant_b[element] / 24 * np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])

        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


def calc_mass_scalar_per_elem(elements: np.ndarray, value: np.ndarray, length: float, determinant_b: np.ndarray,
                              elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the mass matrix with one constant value of the material per element.

    Calculates the contribution of the elements specified in `elements` to the mass matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered
    value : np.ndarray
        (E,) array. One value per element.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.divgrad_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9))
    j = np.empty((num_elements, 9))
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        mat_elem = length * value[k] * determinant_b[element] / 24 * np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])

        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_mass_function_scalar(elements: np.ndarray, weights: np.ndarray, local_coordinates: np.ndarray,
                              evaluations: np.ndarray, length: float,
                              determinant_b: np.ndarray, elem2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the mass matrix with a function as material.

    Calculates the contribution of the elements specified in `elements` to the mass matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of elements that should be considered
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    evaluations : np.ndarray
        (E,N) array. For every element the N evalutations of the material function at the evaluation points for the
        numerical integration. See :py:func:`evaluate_for_num_int_element`.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.mass_matrix`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.mass_matrix`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.mass_matrix`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9), np.int_)
    j = np.empty((num_elements, 9), np.int_)
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        integral = np.zeros((3, 3))
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk, 0] - local_coordinates[kk, 1], local_coordinates[kk, 0],
                                 local_coordinates[kk, 1]])
            integral = integral + weight * evaluations[k, kk] * np.outer(m_values, m_values)

        mat_elem = length * determinant_b[element] * integral
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


# endregion


# region Functions for load vector

@njit_cache(parallel=True)
def calc_load_constant(elements: np.ndarray,
                       value: Union[int, float],
                       length: float,
                       determinant_b: np.ndarray,
                       elem2node) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates elements for the load vector with a constant load.

    Calculates the contribution of the elements specified in `elements` to the load vector. The calculated values and
    line information are written to v and i, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements :  np.ndarray
        (E,) array. The indices of elements that should be considered.
    value :  Union[int, float]
        The value of the material.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable `i_elem` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See the variable `v_elem` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    """
    num_elements = len(elements)
    i = np.empty((num_elements, 3), dtype=np.int_)
    v = np.empty((num_elements, 3), dtype=np.float_)

    for k in prange(num_elements):
        element = elements[k]
        vec_elem = length * determinant_b[element] * value / 6
        idx_node = elem2node[element, :]

        i[k] = idx_node
        v[k] = vec_elem

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_load_array(elements: np.ndarray,
                    value: np.ndarray,
                    length: float,
                    determinant_b: np.ndarray,
                    elem2node) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates elements for the load vector with a constant load.

    Calculates the contribution of the elements specified in `elements` to the load vector. The calculated values and
    line information are written to v and i, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements :  np.ndarray
        (E,) array. The indices of elements that should be considered.
    value :  np.ndarray
        The value of the material.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable `i_elem` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See the variable `v_elem` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    """
    num_elements = len(elements)
    i = np.empty((num_elements, 3), dtype=np.int_)
    v = np.empty((num_elements, 3), dtype=np.float_)

    for k in prange(num_elements):
        element = elements[k]
        vec_elem = length * determinant_b[element] * value[k] / 6
        idx_node = elem2node[element, :]

        i[k] = idx_node
        v[k] = vec_elem

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_load_function(elements: np.ndarray,
                       weights: np.ndarray,
                       local_coordinates: np.ndarray,
                       evaluations: np.ndarray,
                       length: float,
                       determinant_b: np.ndarray,
                       elem2node) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates elements for the load vector with load being a function.

    Calculates the contribution of the elements specified in `elements` to the load vector. The calculated values and
    line information are written to v and i, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 9T
        ======  =======

    Parameters
    ----------
    elements :  np.ndarray
        (E,) array. The indices of elements that should be considered.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    evaluations : np.ndarray
        (E,N) array. For every element the N evalutations of the material function at the evaluation points for the
        numerical integration. See :py:func:`evaluate_for_num_int_element`.
    length : float
        The length in z-direction
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable `i_elem` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See the variable  `v_elem` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    """
    num_elements = len(elements)

    i = np.zeros((num_elements, 3))
    v = np.zeros((num_elements, 3))
    for k in prange(num_elements):
        element = elements[k]

        integral = np.zeros(3)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk, 0] - local_coordinates[kk, 1], local_coordinates[kk, 0],
                                 local_coordinates[kk, 1]])
            integral = integral + weight * evaluations[k, kk] * m_values

        vec_elem = determinant_b[element] * length * integral
        idx_node = elem2node[element, :]

        i[k] = idx_node
        v[k] = vec_elem

    return i.flatten(), v.flatten()
# endregion


# region Functions for load grad vector
@njit_cache(parallel=True)
def calc_load_grad_constant(elements: np.ndarray, value: np.ndarray, abs_determinant_b: np.ndarray,
                            b_mtrans: np.ndarray, length: float, elem2node: np.ndarray):
    r"""Computes the load grad vector for a constant D field

    .. math::

        g_i := \int_\Omega \vec{D}_{\mathrm{s}} \cdot \nabla N_i \mathrm{d}V\,.

    Parameters
    ----------
    elements : np.ndarray
        (X,) array with the element indices to compute
    value : np.ndarray
        (2,1) array with a constant source D field
    abs_determinant_b : np.ndarray
        (E,) array with the absolute value of the determinant of the transformation matrix B on every element
    b_mtrans : np.ndarray
        (E,2,2) array with the transpose of the inverse of the transformation matrix on every element
    length : float
        The length of the domain
    elem2node : np.ndarray
        (E,3) array with the node indices per element

    Returns
    -------
    lines : np.ndarray
        Line numbers
    values : np.ndarray
        values to the line numbers of the entries
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 3), np.int_)
    v = np.empty((num_elements, 3))

    grads_bf = np.array([[-1., 1., 0.],
                         [-1., 0., 1.]])
    for k in prange(num_elements):
        element = elements[k]

        load_on_element = 0.5 * length * abs_determinant_b[element] * value.T @ b_mtrans[element].T @ grads_bf
        indices_nodes = elem2node[element, :]

        i[k] = indices_nodes
        v[k] = load_on_element

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_load_grad_function(elements: np.ndarray, weights: np.ndarray, evaluations: np.ndarray,
                            abs_determinant_b: np.ndarray, b_mtrans: np.ndarray, length: float, elem2node: np.ndarray):
    r"""Computes the load grad vector for a space dependent D field

    .. math::

        g_i := \int_\Omega \vec{D}_{\mathrm{s}} \cdot \nabla N_i \mathrm{d}V\,.

    Parameters
    ----------
    elements : np.ndarray
        (X,) array with the element indices to compute
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    evaluations : np.ndarray
        (E,N,2) array. E elements. For every element N evaluations. Every evaluation has 2 entries
    abs_determinant_b : np.ndarray
        (E,) array with the absolute value of the determinant of the transformation matrix B on every element
    b_mtrans : np.ndarray
        (E,2,2) array with the transpose of the inverse of the transformation matrix on every element
    length : float
        The length of the domain
    elem2node : np.ndarray
        (E,3) array with the node indices per element

    Returns
    -------
    lines : np.ndarray
        Line numbers
    values : np.ndarray
        values to the line numbers of the entries
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 3), np.int_)
    v = np.empty((num_elements, 3))

    grads_bf = np.array([[-1., 1., 0.],
                         [-1., 0., 1.]])
    weights_mat = np.ones((1, len(weights))) @ np.diag(weights)

    for k in prange(num_elements):
        element = elements[k]
        integral = weights_mat @ evaluations[k]
        load_on_element = length * abs_determinant_b[element] * integral @ b_mtrans[element].T @ grads_bf
        indices_nodes = elem2node[element, :]

        i[k] = indices_nodes
        v[k] = load_on_element

    return i.flatten(), v.flatten()


# endregion

@njit_cache(parallel=True)
def calc_neumann_term_constant(edges: np.ndarray, value: Union[int, float], length: float, node: np.ndarray,
                               edge2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates elements for the neumann term vector with a constant value.

    Calculates the contribution of the elements specified in `edges` to the neumann term vector. The calculated values
    and line information are written to v and i, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of edges in `edges`
        T       Number of edges in the mesh
        N       Number of evaluation points
        K       Size of i, v. Equal to 2*T
        ======  =======

    Parameters
    ----------
    edges : np.ndarray
        (E,) array. Indices of the edges the boundary condition is applied to.
    value : Union[int, float]
        The value of the boundary condition.
    node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See variable `i_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See variable `v_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    """
    num_edges = len(edges)
    i = np.empty((num_edges, 2))
    v = np.empty((num_edges, 2))
    for k in prange(num_edges):
        edge = edges[k]
        idx_node = edge2node[edge, :]
        coord_node1 = node[idx_node[0]]
        coord_node2 = node[idx_node[1]]
        length_edge = np.linalg.norm(coord_node2 - coord_node1)

        i[k] = idx_node
        v[k] = value * 0.5 * length_edge * length

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_neumann_term_array(edges: np.ndarray, value: np.ndarray, length: float, node: np.ndarray,
                            edge2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates elements for the neumann term vector with a constant value.

    Calculates the contribution of the elements specified in `edges` to the neumann term vector. The calculated values
    and line information are written to v and i, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of edges in `edges`
        T       Number of edges in the mesh
        N       Number of evaluation points
        K       Size of i, v. Equal to 2*T
        ======  =======

    Parameters
    ----------
    edges : np.ndarray
        (E,) array. Indices of the edges the boundary condition is applied to.
    value : np.ndarray
        The values of the boundary condition.
    node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See variable `i_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See variable `v_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    """
    num_edges = len(edges)

    i = np.empty((num_edges, 2))
    v = np.empty((num_edges, 2))
    for k in prange(num_edges):
        edge = edges[k]
        idx_node = edge2node[edge, :]
        coord_node1 = node[idx_node[0]]
        coord_node2 = node[idx_node[1]]
        length_edge = np.linalg.norm(coord_node2 - coord_node1)

        i[k] = idx_node
        v[k] = value[k] * 0.5 * length_edge * length

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_neumann_term_function(edges: np.ndarray, weights: np.ndarray, local_coordinates: np.ndarray,
                               evaluation_points: np.ndarray, evaluations: np.ndarray, node: np.ndarray,
                               edge2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates elements for the neumann term vector with a space dependant boundary condition.

    Calculates the contribution of the elements specified in `edges` to the neumann term vector. The calculated values
    and line information are written to v and i, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of edges in `edges`
        T       Number of edges in the mesh
        N       Number of evaluation points
        K       Size of i, v. Equal to 2*T
        ======  =======

    Parameters
    ----------
    edges : np.ndarray
        (E,) array. Indices of the edges the face current is on.
    i : np.ndarray
        (K,) array. See variable `i_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See variable `v_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_edge`.
    evaluations : np.ndarray
        (E,N) array. For every element the N evalutations of the material function at the evaluation points for the
        numerical integration. See :py:func:`evaluate_for_num_int_edge`.
    node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    None
    """
    num_edges = len(edges)

    i = np.zeros((num_edges, 2))
    v = np.zeros((num_edges, 2))
    for k in range(num_edges):
        edge = edges[k]
        length_edge = np.linalg.norm(node[edge2node[edge, 1]] - node[edge2node[edge, 0]])
        integral = np.zeros(2)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk], local_coordinates[kk]])
            integral = integral + weight * evaluations[k, kk] * m_values * length_edge

        idx_node = edge2node[edge, :]

        i[k] = idx_node
        v[k] = integral

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_robin_term_constant(edges: np.ndarray, value: Union[int, float],
                             node: np.ndarray, edge2node: np.ndarray) -> Tuple[np.ndarray,
                                                                               np.ndarray,
                                                                               np.ndarray]:
    """Calculates elements for the robin term matrix with a constant boundary condition.

    Calculates the contribution of the elements specified in `edges` to the robin term matrix. the calculated values are
    returned.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of edges in `edges`
        T       Number of edges in the mesh
        N       Number of evaluation points
        K       Size of i, v. Equal to 4*E
        ======  =======

    Parameters
    ----------
    edges : np.ndarray
        (E,) array. Indices of the edges the face current is on.
    value : Union[int, float]
        coefficient_dirichlet / coefficient_neumann
    node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    lines : np.ndarray
        (K,) array. Lines of the matrix elements
    columns : np.ndarray
        (K,) array. Columns of the matrix elements
    values : np.ndarray
        (K,) array. Values of the matrix elements
    """
    num_edges = len(edges)

    i_local = np.zeros((num_edges, 4))
    j_local = np.zeros((num_edges, 4))
    v_local = np.zeros((num_edges, 4))
    for k in prange(num_edges):
        edge = edges[k]
        idx_node = edge2node[edge, :]
        coord_node1 = node[idx_node[0]]
        coord_node2 = node[idx_node[1]]
        length_edge = np.linalg.norm(coord_node2 - coord_node1)

        mat_elem = 1 / 6 * length_edge * value * (coord_node1[0] * np.array([[3, 1], [1, 1]]) +
                                                  coord_node2[0] * np.array([[1, 1], [1, 3]]))  # TODO

        idx_node = edge2node[edge, :]
        tmp = np.stack((idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node))

        i_local[k] = np.reshape(tmp, (4,))
        j_local[k] = np.reshape(tmpt, (4,))
        v_local[k] = np.reshape(mat_elem, (4,))

    return i_local.flatten(), j_local.flatten(), v_local.flatten()


@njit_cache(parallel=True)
def calc_robin_term_array(edges: np.ndarray, value: np.ndarray,
                          node: np.ndarray, edge2node: np.ndarray) -> Tuple[np.ndarray,
                                                                            np.ndarray,
                                                                            np.ndarray]:
    """Calculates elements for the robin term matrix with a constant boundary condition.

    Calculates the contribution of the elements specified in `edges` to the robin term matrix. the calculated values are
    returned.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of edges in `edges`
        T       Number of edges in the mesh
        N       Number of evaluation points
        K       Size of i, v. Equal to 4*E
        ======  =======

    Parameters
    ----------
    edges : np.ndarray
        (E,) array. Indices of the edges the face current is on.
    value : np.ndarray
        coefficient_dirichlet / coefficient_neumann
    node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    lines : np.ndarray
        (K,) array. Lines of the matrix elements
    columns : np.ndarray
        (K,) array. Columns of the matrix elements
    values : np.ndarray
        (K,) array. Values of the matrix elements
    """
    num_edges = len(edges)

    i_local = np.zeros((num_edges, 4))
    j_local = np.zeros((num_edges, 4))
    v_local = np.zeros((num_edges, 4))
    for k in prange(num_edges):
        edge = edges[k]
        idx_node = edge2node[edge, :]
        coord_node1 = node[idx_node[0]]
        coord_node2 = node[idx_node[1]]
        length_edge = np.linalg.norm(coord_node2 - coord_node1)

        mat_elem = 1 / 6 * np.pi * length_edge * value[k] * (coord_node1[0] * np.array([[3, 1], [1, 1]]) +
                                                             coord_node2[0] * np.array([[1, 1], [1, 3]]))  # TODO

        idx_node = edge2node[edge, :]
        tmp = np.stack((idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node))

        i_local[k] = np.reshape(tmp, (4,))
        j_local[k] = np.reshape(tmpt, (4,))
        v_local[k] = np.reshape(mat_elem, (4,))

    return i_local.flatten(), j_local.flatten(), v_local.flatten()


@njit_cache(parallel=True)
def calc_robin_term_function(edges: np.ndarray, weights: np.ndarray, local_coordinates: np.ndarray,
                             evaluation_points: np.ndarray, evaluations: np.ndarray,
                             node_transformed: np.ndarray, edge2node: np.ndarray) -> Tuple[np.ndarray,
                                                                                           np.ndarray,
                                                                                           np.ndarray]:
    """Calculates elements for the robin term matrix with a space dependent boundary condition.

    Calculates the contribution of the elements specified in `edges` to the robin term matrix. the calculated values are
    returned.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of edges in `edges`
        T       Number of edges in the mesh
        N       Number of evaluation points
        K       Size of i, v. Equal to 4*E
        ======  =======

    Parameters
    ----------
    edges : np.ndarray
        (E,) array. Indices of the edges the face current is on.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all edges. See :py:func:`calc_evaluation_points_element`.
    evaluations : np.ndarray
        (E,N) array. For every element the N evalutations of the material function at the evaluation points for the
        numerical integration. See :py:func:`evaluate_for_num_int_element`.
    node_transformed : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    lines : np.ndarray
        (K,) array. Lines of the matrix elements
    columns : np.ndarray
        (K,) array. Columns of the matrix elements
    values : np.ndarray
        (K,) array. Values of the matrix elements
    """
    num_edges = len(edges)

    i_local = np.zeros((num_edges, 4))
    j_local = np.zeros((num_edges, 4))
    v_local = np.zeros((num_edges, 4))
    for k in prange(num_edges):
        edge = edges[k]

        coord_node1 = node_transformed[edge2node[edge, 0]]
        coord_node2 = node_transformed[edge2node[edge, 1]]
        length_edge = np.linalg.norm(coord_node2 - coord_node1)

        integral = np.zeros((2, 2))
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk], local_coordinates[kk]])
            integral = integral + weight * evaluations[k, kk] * \
                       evaluation_points[k, kk, 0] * np.outer(m_values, m_values) * length_edge

        mat_elem = 2 * np.pi * integral  # TODO
        idx_node = edge2node[edge, :]

        tmp = np.stack((idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node))

        i_local[k] = np.reshape(tmp, (4,))
        j_local[k] = np.reshape(tmpt, (4,))
        v_local[k] = np.reshape(mat_elem, (4,))

    return i_local.flatten(), j_local.flatten(), v_local.flatten()


@njit_cache(parallel=True)
def calc_gradient(val2node: np.ndarray, elem2node: np.ndarray, num_elem: int, b: np.ndarray,
                  c: np.ndarray, element_areas_double: np.ndarray) -> np.ndarray:
    r"""Performant implementation of gradient.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in the mesh
        N       Number of nodes in the mesh
        ======  =======

    Parameters
    ----------
    val2node : np.ndarray
        (N,) array. One value per edge, the edge functions are defined on, i.e. one value per node in the mesh.
    elem2node : np.ndarray
        (E,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    num_elem : int
        Total number of elements. See field in :py:class:`source.mesh.AxiMesh`.
    b : np.ndarray
        (E,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (E,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    element_areas_double : s : np.ndarray
        (E,) array. Vector with 2 times the oriented area of all elements. See the field __parallelogram_areas_oriented
        in :py:class:`TriAxisymmetricNodalShapeFunction`.

    Returns
    -------
    None
    """
    out = np.empty((num_elem, 2), dtype=val2node.dtype)
    for k in prange(num_elem):
        area_double = element_areas_double[k]
        nodes = elem2node[k]
        tmp = np.array([np.sum(b[k] * val2node[nodes]),
                        np.sum(c[k] * val2node[nodes])])
        out[k] = tmp / area_double
    return out


class TriCartesianNodalShapeFunction(NodalShapeFunction):
    """Class representing shape functions in axisymmetric geometries with a triangular mesh in the rz-plane."""

    def __init__(self, mesh: 'TriMesh', length: float = 1):
        """Constructor.

        Parameters
        ----------
        mesh : AxiMesh
            The mesh object.
        """
        super().__init__(mesh, dim=2, allocation_size=9 * mesh.num_elem)
        self.r1 = None
        self.__determinant_b = np.zeros(mesh.num_elem)
        self.__calc_coefficients()
        self.length = length

    def __calc_coefficients(self) -> None:
        """
        Calculates some coefficients that are needed in various methods of this class.

        Returns
        -------
        NoReturn
        """
        x1 = self.mesh.node[self.mesh.elem2node, 0]
        y1 = self.mesh.node[self.mesh.elem2node, 1]
        x2 = np.roll(x1, -1, axis=1)
        y2 = np.roll(y1, -1, axis=1)
        x3 = np.roll(x1, -2, axis=1)
        y3 = np.roll(y1, -2, axis=1)
        self.a = x2 * y3 - x3 * y2
        self.b = y2 - y3
        self.c = x3 - x2

        x1 = self.mesh.node[self.mesh.elem2node[:, 0], 0]
        x2 = self.mesh.node[self.mesh.elem2node[:, 1], 0]
        x3 = self.mesh.node[self.mesh.elem2node[:, 2], 0]
        y1 = self.mesh.node[self.mesh.elem2node[:, 0], 1]
        y2 = self.mesh.node[self.mesh.elem2node[:, 1], 1]
        y3 = self.mesh.node[self.mesh.elem2node[:, 2], 1]
        self.p1_to_p2 = np.c_[x2 - x1, y2 - y1]
        self.p1_to_p3 = np.c_[x3 - x1, y3 - y1]

        self.transform_coefficients = np.stack((self.p1_to_p2, self.p1_to_p3, np.c_[x1, y1]), axis=2)

        # Calculate the cross product of the vectors p1_to_p2 and p1_to_p3. The absolute value corresponds to the area
        # of the parallelogram spanned by the two vector (= twice the element area) and the sign depends on the
        # orientation of the triangle (ijk or ikj)
        self.__parallelogram_areas_oriented = self.p1_to_p2[:, 0] * self.p1_to_p3[:, 1] - \
                                              self.p1_to_p2[:, 1] * self.p1_to_p3[:, 0]
        # Calculate the absolute value of the determinant of the transformation matrix for every element
        self.__determinant_b = np.abs(self.__parallelogram_areas_oriented)

        matrix_b = np.empty((self.mesh.num_elem, 2, 2))
        matrix_b[:, :, 0] = self.p1_to_p2
        matrix_b[:, :, 1] = self.p1_to_p3
        self.inverse_b_transpose = np.linalg.inv(matrix_b)

    def _calc_evaluation_points_element(self, local_coordinates: np.ndarray, indices: np.ndarray) -> np.ndarray:
        return calc_evaluation_points_element(local_coordinates, self.transform_coefficients, indices)

    # region Calc matrix

    # region Calc matrix constant

    def _calc_matrix_constant_scalar(self, matrix_type: str, indices: np.ndarray, value: Number,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_constant_scalar(indices, value, self.b, self.c, self.length, self.__determinant_b,
                                                self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_constant_scalar(indices, value, self.length, self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_constant_scalar is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_constant_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs)\
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        return NotImplementedError(f"calc_matrix_constant_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_constant_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, *args, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_constant_tensor(indices, value, self.b, self.c, self.length, self.__determinant_b,
                                                self.mesh.elem2node)
        if matrix_type == "mass":
            raise NotImplementedError('Mass matrix does not support tensors.')

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix constant

    # region Calc matrix elementwise

    def _calc_matrix_elementwise_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_scalar_per_elem(indices, value, self.b, self.c, self.length,
                                                self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_scalar_per_elem(indices, value, self.length, self.__determinant_b,
                                             self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_scalar_per_elem is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_elementwise_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs)\
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_vector_per_elem is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_elementwise_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_tensor_per_elem(indices, value, self.b, self.c, self.length,
                                                self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            raise NotImplementedError('Mass matrix does not support tensors.')

        raise NotImplementedError(f"calc_matrix_tensor_per_elem is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix elementwise

    # region Calc matrix function

    def _calc_matrix_function_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_function_scalar(indices, weights, value,
                                                self.b, self.c, self.length, self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_function_scalar(indices, weights, local_coordinates, value,
                                             self.length, self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_function_scalar is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_function_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs)\
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_function_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_function_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_function_tensor(indices, weights, value,
                                                self.b, self.c, self.length, self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            raise NotImplementedError('Mass matrix does not support tensors.')

        raise NotImplementedError(f"calc_matrix_function_scalar is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix function

    # endregion Calc matrix

    # region Calc vector

    # region Calc vector constant

    def _calc_vector_constant_scalar(self, vector_type: str, indices: np.ndarray, value: Number, weights: np.ndarray,
                                     local_coordinates: np.ndarray, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_constant_scalar(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load":
            return calc_load_constant(indices, value, self.length, self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_vector_constant_scalar is not implemented for vector type: {vector_type}.")

    def _calc_vector_constant_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_constant_vector(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load_grad":
            return calc_load_grad_constant(indices, value, self.__determinant_b,
                                           self.inverse_b_transpose, self.length, self.mesh.elem2node)

        raise NotImplementedError(f"calc_vector_constant_vector is not implemented for vector type: {vector_type}.")

    def _calc_vector_constant_tensor(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_constant_tensor(vector_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_vector_constant_tensor is not implemented for vector type: {vector_type}.")

    # endregion Calc vector constant

    # region Calc vector elementwise

    def _calc_vector_elementwise_scalar(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_elementwise_scalar(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load":
            return calc_load_array(indices, value, self.length, self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_vector_elementwise_scalar is not implemented for vector type: {vector_type}.")

    def _calc_vector_elementwise_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_elementwise_vector(vector_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_vector_elementwise_vector is not implemented for vector type: {vector_type}.")

    def _calc_vector_elementwise_tensor(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_elementwise_tensor(vector_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_vector_elementwise_tensor is not implemented for vector type: {vector_type}.")

    # endregion Calc vector elementwise

    # region Calc vector function

    def _calc_vector_function_scalar(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_function_scalar(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load":
            return calc_load_function(indices, weights, local_coordinates, value, self.length, self.__determinant_b,
                                      self.mesh.elem2node)

        raise NotImplementedError(f"calc_vector_function_scalar is not implemented for vector type: {vector_type}.")

    def _calc_vector_function_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_function_vector(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load_grad":
            return calc_load_grad_function(indices, weights, value, self.__determinant_b,
                                                               self.inverse_b_transpose, self.length,
                                                               self.mesh.elem2node)

        raise NotImplementedError(f"calc_vector_function_vector is not implemented for vector type: {vector_type}.")

    def _calc_vector_function_tensor(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_function_tensor(vector_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_vector_function_tensor is not implemented for vector type: {vector_type}.")

    # endregion Calc vector function

    # endregion Calc vector

    def divgrad_operator(self, *material: Union[NumericalData, MaterialData], **kwargs) -> coo_matrix:
        assembly_iterator = self._process_input(*material, **kwargs)
        return self._matrix_routine("divgrad", assembly_iterator, **kwargs)

    def mass_matrix(self, *material: Union[NumericalData, MaterialData], **kwargs) -> coo_matrix:
        assembly_iterator = self._process_input(*material, **kwargs)
        return self._matrix_routine("mass", assembly_iterator, **kwargs)

    # pylint: disable=line-too-long
    def neumann_term(self, *args: Union[Tuple['Regions', 'BdryCond'],
                                        Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[..., float]], ...],
                                                             Callable[..., Tuple[float]]]]],
                     integration_order: int = 3) -> coo_matrix:
        r"""Compute the Neumann term on a part of the boundary (see the notes).

        Parameters
        ----------
        args : Union[Tuple[Regions, BdryCond], Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[...,
        float]], ...], Callable[..., Tuple[float]]]]]
            The following possibilities are:

            - **Regions, BdyCond**: Will search for instances of BCNeumann in BdryCond and use the value of these.
            - **Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[..., float]], ...], Callable[..., Tuple[float]]]]**:
              The first argument is an array of shape (N,) and contains the indices of the boundary elements. The second
              argument is the value of g at these elements.
        integration_order : int, optional
            The integration order for the case that a numerical integration is necessary. Default is 1

        Returns
        -------
        q : csr_matrix
            The vector :math:`\mathbf{q}` for the Neumann term.

        Notes
        -----
        The Neumann term for edge basis functions is a vector :math:`\mathbf{q}` where the elements are defined as

        .. math::

            q_i = \int_{\partial\Omega} \vec{w}_i\cdot\vec{g}\,\mathrm{d} S\,.

        In the finite element formulation it is :math:`\vec{g} = \vec{n}\times\vec{H}`.
        """
        flag_regions, flag_value = self._process_neumann(*args, allow_indices_tuple=True)

        weights, local_coordinates = gauss(integration_order)  # quadrature along unit line

        if flag_regions:  # We have regions and boundary_conditions
            i, v = [], []
            regions: Regions = args[0]
            boundary_conditions: BdryCond = args[1]
            for key in boundary_conditions.get_ids():
                bc = boundary_conditions.get_bc(key)
                if not isinstance(bc, BCNeumann):
                    continue

                indices_regions = regions.find_regions_of_boundary_condition(bc.ID)
                indices_edges = np.empty(0)  # Indices of all edges that are on the boundary bc
                for region_id in indices_regions:
                    indices_edges = np.r_[indices_edges, np.where(self.mesh.edge2regi == region_id)[0]]
                indices_edges = indices_edges.astype(int)

                if not bc.is_homogeneous:
                    evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node,
                                                                    indices_edges, self.mesh.edge2node)
                    evaluations = evaluate_for_num_int_edge(bc.value, evaluation_points)
                    i_tmp, v_tmp = calc_neumann_term_function(indices_edges, weights, local_coordinates,
                                                              evaluation_points, evaluations, self.mesh.node,
                                                              self.mesh.edge2node)

                elif bc.is_constant:
                    if isinstance(bc.value, (float, int)):
                        i_tmp, v_tmp = calc_neumann_term_constant(indices_edges, bc.value, self.length,
                                                                  self.mesh.node, self.mesh.edge2node)
                    elif isinstance(bc.value, ndarray):
                        i_tmp, v_tmp = calc_neumann_term_array(indices_edges, bc.value, self.length,
                                                               self.mesh.node, self.mesh.edge2node)
                    else:
                        raise Exception("Type not supported")
                else:
                    i_tmp, v_tmp = calc_neumann_term_constant(indices_edges, bc.value(), self.length,
                                                              self.mesh.node, self.mesh.edge2node)
                i.append(i_tmp)
                v.append(v_tmp)
            i = np.concatenate(i)
            v = np.concatenate(v)

        else:  # We have indices and value
            indices, value = args[0], args[1][0] if isinstance(args[1], Tuple) else args[1]

            if flag_value == 'callable':
                evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node, indices,
                                                                self.mesh.edge2node)
                evaluations = evaluate_for_num_int_edge(value, evaluation_points)
                i, v = calc_neumann_term_function(indices, weights, local_coordinates, evaluation_points, evaluations,
                                                  self.mesh.node, self.mesh.edge2node)
            elif flag_value == 'array':
                i, v = calc_neumann_term_array(indices, value, self.length, self.mesh.node, self.mesh.edge2node)
            elif flag_value == 'value':
                i, v = calc_neumann_term_constant(indices, value, self.length, self.mesh.node, self.mesh.edge2node)
        columns = np.zeros(len(i), dtype=int)
        neumann_vector = coo_matrix((v, (i, columns)), shape=(self.mesh.num_node, 1))
        return neumann_vector

    # pylint: disable=cell-var-from-loop
    def robin_terms(self, regions: 'Regions', boundary_condition: 'BdryCond', integration_order: int = 1) -> \
            Tuple[csr_matrix, csr_matrix]:
        raise NotImplementedError('Robin BC not implemented.')
        # TODO the robin BC are copied from TriAxisymmetricNodalShapeFunction and therefore not valid in Cartesian coord
        # to be implemented later

        # bc_keys = boundary_condition.get_ids()
        # weights, local_coordinates = gauss(integration_order)
        # values_list = []
        # lines_list = []
        # columns_list = []
        # robin_vector = coo_matrix((self.mesh.num_node, 1))

        # for bc_key in bc_keys:
        #    bc = boundary_condition.get_bc(bc_key)
        #    if not isinstance(bc, BCRobin):
        #        continue

        # Calculate the matrix
        #    indices_regions = regions.find_regions_of_boundary_condition(bc.ID)
        #    indices_edges = np.empty(0)  # Indices of all edges that are on the boundary bc
        #    for region_id in indices_regions:
        #        indices_edges = np.r_[indices_edges, np.where(self.mesh.edge2regi == region_id)[0]]
        #    indices_edges = indices_edges.astype('int')

        #    coef_dir = bc.coefficient_dirichlet
        #    coef_neum = bc.coefficient_neumann
        #    if isinstance(coef_neum, ndarray) or isinstance(coef_dir, ndarray):
        #        raise NotImplementedError
        #    value_bc = bc.value
        #    if callable(coef_dir):
        #        if callable(coef_neum):  # Both coefficients are functions
        #            evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node,
        #                                                            indices_edges, self.mesh.edge2node)
        #            evaluations = evaluate_for_num_int_edge(lambda x, y: coef_dir(x, y) / coef_neum(x, y),
        #                                                    evaluation_points)
        #            robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_function(
        #                indices_edges, weights, local_coordinates, evaluation_points, evaluations,
        #                self.mesh.node, self.mesh.edge2node)
        #        else:  # Only dirichlet coefficient is a function
        #            evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node,
        #                                                            indices_edges, self.mesh.edge2node)
        #            evaluations = evaluate_for_num_int_edge(lambda x, y: coef_dir(x, y) / coef_neum,
        #                                                    evaluation_points)
        #            robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_function(
        #                indices_edges, weights, local_coordinates, evaluation_points, evaluations,
        #                self.mesh.node, self.mesh.edge2node)
        #    else:
        #        if callable(coef_neum):  # Only coef_neum is a function
        #            evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node,
        #                                                            indices_edges, self.mesh.edge2node)
        #            evaluations = evaluate_for_num_int_edge(lambda x, y: coef_dir / coef_neum(x, y), evaluation_points)
        #            robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_function(
        #                indices_edges, weights, local_coordinates, evaluation_points, evaluations,
        #                self.mesh.node, self.mesh.edge2node)
        #        else:  # Both are no functions
        #            value = coef_dir / coef_neum
        #            robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_constant(
        #                indices_edges, value, self.mesh.node, self.mesh.edge2node)
        #    values_list.append(robin_values_per_bc)
        #    lines_list.append(robin_lines_per_bc)
        #    columns_list.append(robin_columns_per_bc)

        # Calculate the vector
        #    if callable(value_bc):
        #        if callable(coef_neum):
        #            # Both are functions
        #            robin_vector = robin_vector + self.neumann_term(indices_edges,
        #                                                            (lambda x, y: value_bc(x, y) / coef_neum(x, y),),
        #                                                            integration_order=integration_order)
        #        else:
        #            # only value_bc is a function
        #            if isinstance(coef_neum, np.ndarray):
        #                robin_vector = robin_vector + self.neumann_term(indices_edges,
        #                                                                (lambda x, y: value_bc(x, y) / coef_neum,),
        #                                                                integration_order=integration_order)
        #            elif isinstance(coef_neum, (float, int)):
        #                robin_vector = robin_vector + self.neumann_term(indices_edges,
        #                                                                (lambda x, y: value_bc(x, y) / coef_neum,),
        #                                                                integration_order=integration_order)
        #            else:
        #                raise Exception("Type of coef_neum is not supported.")
        #    else:
        #        if callable(coef_neum):
        #            # Only Neumann coefficient is a function
        #            if isinstance(value_bc, np.ndarray):
        #                robin_vector = robin_vector + self.neumann_term(indices_edges,
        #                                                                (lambda x, y: value_bc / coef_neum(x, y),),
        #                                                                integration_order=integration_order)
        #            elif isinstance(value_bc, (float, int)):
        #                robin_vector = robin_vector + self.neumann_term(indices_edges,
        #                                                                (lambda x, y: value_bc / coef_neum(x, y),),
        #                                                                integration_order=integration_order)
        #            else:
        #                raise Exception("Type of value not supported")

        #        else:
        #            value_tmp = value_bc / coef_neum
        #            if isinstance(value_tmp, np.ndarray):
        #                robin_vector = robin_vector + self.neumann_term(indices_edges, (value_tmp,),
        #                                                                integration_order=integration_order)
        #            elif isinstance(value_tmp, (float, int)):
        #                robin_vector = robin_vector + self.neumann_term(indices_edges, (value_tmp,),
        #                                                                integration_order=integration_order)
        #            else:
        #                raise Exception("Type not supported.")

        # robin_matrix = coo_matrix(
        #    (np.concatenate(values_list), (np.concatenate(lines_list), np.concatenate(columns_list))),
        #    shape=(self.mesh.num_node, self.mesh.num_node))
        # return robin_matrix, robin_vector.tocoo()

    def gradient(self, val2node: np.ndarray) -> np.ndarray:
        out = calc_gradient(val2node, self.mesh.elem2node, self.mesh.num_elem, self.b, self.c,
                            self.__parallelogram_areas_oriented)
        return out
