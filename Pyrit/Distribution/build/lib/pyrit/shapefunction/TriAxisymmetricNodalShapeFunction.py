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

from typing import Union, Callable, Tuple, NoReturn, TYPE_CHECKING

import numpy as np
from numpy import ndarray
from scipy.sparse import coo_matrix, csr_matrix
from numba import prange

from pyrit.region import Regions
from pyrit.bdrycond import BdryCond, BCNeumann, BCRobin
from pyrit.ValueHandler import evaluate_for_num_int_edge

from pyrit.toolbox.QuadratureToolbox import gauss
from pyrit.toolbox.NumbaToolbox import njit_cache

from .ShapeFunction import Number, NumericalData, MaterialData
from .NodalShapeFunction import NodalShapeFunction

if TYPE_CHECKING:
    from pyrit.mesh import AxiMesh


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
        (E,) array. Array with the indices of elements the evalutaion points should calculated for.

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
            coords[k, kk] = nodes[edge2node[edge, 0]] + local_coordinates[kk] * \
                (nodes[edge2node[edge, 1]] - nodes[edge2node[edge, 0]])

    return coords


# endregion


# region Functions for divgrad


@njit_cache(parallel=True)
def calc_divgrad_constant_scalar(elements: np.ndarray, value: Union[int, float], b: np.ndarray, c: np.ndarray,
                                 bmat_11: np.ndarray, bmat_12: np.ndarray, r1: np.ndarray, determinant_b: np.ndarray,
                                 elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    bmat_11: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
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

        mat_elem = 2 / determinant_b[element] * value * np.pi * \
                   ((bmat_11[element] + bmat_12[element]) / 6 + 0.5 * r1[element]) * (c_mat + b_mat)
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
                                 bmat_11: np.ndarray, bmat_12: np.ndarray, r1: np.ndarray, determinant_b: np.ndarray,
                                 elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    bmat_11: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
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

        mat_elem = 2 / determinant_b[element] * np.pi * \
                   ((bmat_11[element] + bmat_12[element]) / 6 + 0.5 * r1[element]) * \
                   (b_mat * value[0, 0] + cb_mat * value[1, 0] + bc_mat * value[0, 1] + c_mat * value[1, 1])
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_divgrad_scalar_per_elem(elements: np.ndarray, value: np.ndarray, b: np.ndarray, c: np.ndarray,
                                 bmat_11: np.ndarray, bmat_12: np.ndarray, r1: np.ndarray, determinant_b: np.ndarray,
                                 elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    bmat_11 : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12 : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1 : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
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

        mat_elem = 2 / determinant_b[element] * value[k] * np.pi * \
                   ((bmat_11[element] + bmat_12[element]) / 6 + 0.5 * r1[element]) * \
                   (c_mat + b_mat)

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
                                 bmat_11: np.ndarray, bmat_12: np.ndarray, r1: np.ndarray, determinant_b: np.ndarray,
                                 elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    bmat_11: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1: np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
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

        mat_elem = 2 / determinant_b[element] * np.pi * \
                   ((bmat_11[element] + bmat_12[element]) / 6 + 0.5 * r1[element]) * \
                   (b_mat * value[k, 0, 0] + cb_mat * value[k, 1, 0] + bc_mat * value[k, 0, 1] + c_mat * value[k, 1, 1])
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_divgrad_function_scalar(elements: np.ndarray, weights: np.ndarray, evaluation_points: np.ndarray,
                                 evaluations: np.ndarray, b: np.ndarray, c: np.ndarray, determinant_b: np.ndarray,
                                 elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
        index = elements[k]

        b_mat = np.outer(b[index], b[index])
        c_mat = np.outer(c[index], c[index])

        integral = np.dot(weights, evaluations[k] * evaluation_points[k, :, 0])
        mat_elem = 2 / determinant_b[index] * np.pi * (c_mat + b_mat) * integral
        idx_node = elem2node[index, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)  # todo:docstring
def calc_divgrad_function_tensor(elements: np.ndarray, weights: np.ndarray, evaluation_points: np.ndarray,
                                 evaluations: np.ndarray, b: np.ndarray, c: np.ndarray, determinant_b: np.ndarray,
                                 elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
        # cb_mat = np.outer(c[element], b[element])
        # ToDo: Check if cb_mat can always be replaced by bc_mat

        first_integral = np.dot(weights, evaluations[k, :, 0, 0] * evaluation_points[k, :, 0])
        second_integral = np.dot(weights, evaluations[k, :, 0, 1] * evaluation_points[k, :, 0])
        third_integral = np.dot(weights, evaluations[k, :, 1, 0] * evaluation_points[k, :, 0])
        fourth_integral = np.dot(weights, evaluations[k, :, 1, 1] * evaluation_points[k, :, 0])

        sum_integrals = b_mat * first_integral + bc_mat * second_integral - \
                        bc_mat * third_integral + c_mat * fourth_integral

        mat_elem = 2 / determinant_b[element] * np.pi * sum_integrals
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
def calc_mass_constant_scalar(elements: np.ndarray, value: Union[int, float], bmat_11: np.ndarray,
                              bmat_12: np.ndarray, r1: np.ndarray, determinant_b: np.ndarray, elem2node) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    bmat_11 : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12 : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1 : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
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

        mat_elem = determinant_b[element] * value * np.pi * \
                   (bmat_11[element] / 60 * np.array([[2, 2, 1], [2, 6, 2], [1, 2, 2]]) +
                    bmat_12[element] / 60 * np.array([[2, 1, 2], [1, 2, 2], [2, 2, 6]]) +
                    r1[element] / 12 * np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]]))

        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


def calc_mass_scalar_per_elem(elements: np.ndarray, value: np.ndarray,
                              bmat_11: np.ndarray, bmat_12: np.ndarray, r1: np.ndarray, determinant_b: np.ndarray,
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
    bmat_11 : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12 : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1 : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
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

        mat_elem = determinant_b[element] * value[k] * np.pi * \
                   (bmat_11[element] / 60 * np.array([[2, 2, 1], [2, 6, 2], [1, 2, 2]]) +
                    bmat_12[element] / 60 * np.array([[2, 1, 2], [1, 2, 2], [2, 2, 6]]) +
                    r1[element] / 12 * np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]]))

        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_mass_function_scalar(elements: np.ndarray, weights: np.ndarray, local_coordinates: np.ndarray,
                              evaluation_points: np.ndarray, evaluations: np.ndarray, determinant_b: np.ndarray,
                              elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
            integral = integral + weight * evaluations[k, kk] * evaluation_points[k, kk, 0] * np.outer(m_values,
                                                                                                       m_values)

        mat_elem = determinant_b[element] * 2 * np.pi * integral
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
                       bmat_11: np.ndarray,
                       bmat_12: np.ndarray,
                       r1: np.ndarray,
                       determinant_b: np.ndarray,
                       elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
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
    bmat_11 : np.ndarray
        (N,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12 : np.ndarray
        (N,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1 : np.ndarray
        (N,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
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
    v = np.empty((num_elements, 3))
    for k in prange(num_elements):
        element = elements[k]
        vec_elem = value / 12 * np.pi * determinant_b[element] * (bmat_11[element] * np.array([1, 2, 1]) +
                                                                  bmat_12[element] * np.array([1, 1, 2]) +
                                                                  r1[element] * np.array([4, 4, 4]))
        idx_node = elem2node[element, :]

        i[k] = idx_node
        v[k] = vec_elem

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_load_vector(elements: np.ndarray,
                     value: np.ndarray,
                     bmat_11: np.ndarray,
                     bmat_12: np.ndarray,
                     r1: np.ndarray,
                     determinant_b: np.ndarray,
                     elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
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
    bmat_11 : np.ndarray
        (N,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12 : np.ndarray
        (N,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1 : np.ndarray
        (N,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
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
    v = np.empty((num_elements, 3))
    for k in prange(num_elements):
        element = elements[k]
        vec_elem = value[k] / 12 * np.pi * determinant_b[element] * (bmat_11[element] * np.array([1, 2, 1]) +
                                                                     bmat_12[element] * np.array([1, 1, 2]) +
                                                                     r1[element] * np.array([4, 4, 4]))
        idx_node = elem2node[element, :]

        i[k] = idx_node
        v[k] = vec_elem

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_load_function(elements: np.ndarray,
                       weights: np.ndarray,
                       local_coordinates: np.ndarray,
                       evaluation_points: np.ndarray,
                       evaluations: np.ndarray,
                       determinant_b: np.ndarray,
                       elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
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

    i = np.empty((num_elements, 3))
    v = np.empty((num_elements, 3))
    for k in prange(num_elements):
        element = elements[k]

        integral = np.zeros(3)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk, 0] - local_coordinates[kk, 1], local_coordinates[kk, 0],
                                 local_coordinates[kk, 1]])
            integral = integral + weight * evaluations[k, kk] * evaluation_points[k, kk, 0] * m_values

        vec_elem = determinant_b[element] * 2 * np.pi * integral
        idx_node = elem2node[element, :]

        i[k] = idx_node
        v[k] = vec_elem

    return i.flatten(), v.flatten()


# endregion


@njit_cache(parallel=True)
def calc_curl(val2edge: np.ndarray, node: np.ndarray, elem2node: np.ndarray, num_elem: int, b: np.ndarray,
              c: np.ndarray, s: np.ndarray):
    """Performant implementation of curl.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in the mesh
        N       Number of nodes in the mesh
        ======  =======

    Parameters
    ----------
    val2edge : np.ndarray
        (N,) array. One value per edge, the edge functions are defined on, i.e. one value per node in the mesh.
    node : np.ndarray
        (N,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    elem2node : np.ndarray
        (E,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    num_elem : int
        Total number of elements. See field in :py:class:`source.mesh.AxiMesh`.
    b : np.ndarray
        (E,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (E,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    s : s : np.ndarray
        (E,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.

    Returns
    -------
    None
    """
    out = np.empty((num_elem, 2), dtype=val2edge.dtype)
    for k in prange(num_elem):
        nodes = elem2node[k]
        radius_mid = 1 / 3 * np.sum(node[nodes, 0])
        tmp = np.array([-1 / (2 * np.pi * s[k] * radius_mid) * np.sum(c[k] * val2edge[nodes]),
                        1 / (np.pi * s[k]) * np.sum(b[k] * val2edge[nodes])])
        out[k] = tmp
    return out


# @njit_cache(parallel=True)
def calc_neumann_term_constant(edges: np.ndarray, value: Union[int, float], node: np.ndarray, edge2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray]:
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
    i : np.ndarray
        (K,) array. See variable `i_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See variable `v_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    value : Union[int, float]
        The value of the boundary condition.
    node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    None
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
        v[k] = value * 2 * np.pi * length_edge * \
               np.array([coord_node1[0] / 3 + coord_node2[0] / 6, coord_node1[0] / 6 + coord_node2[0] / 3])

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_neumann_term_array(edges: np.ndarray, value: np.ndarray, node: np.ndarray, edge2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray]:
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
        v[k] = value[k] * 2 * np.pi * length_edge * \
               np.array([coord_node1[0] / 3 + coord_node2[0] / 6, coord_node1[0] / 6 + coord_node2[0] / 3])

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
    i : np.ndarray
        (K,) array. See variable `i_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See variable `v_face` in :py:func:`TriAxisymmetricNodalShapeFunction.load_vector`.
    """
    num_edges = len(edges)

    i = np.empty((num_edges, 2))
    v = np.empty((num_edges, 2))
    for k in range(num_edges):
        edge = edges[k]
        length_edge = np.linalg.norm(node[edge2node[edge, 1]] - node[edge2node[edge, 0]])
        integral = np.zeros(2)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk], local_coordinates[kk]])
            integral = integral + weight * evaluations[k, kk] * 2 * np.pi * \
                       evaluation_points[k, kk, 0] * m_values * length_edge

        idx_node = edge2node[edge, :]

        i[k] = idx_node
        v[k] = integral

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_robin_term_constant(edges: np.ndarray, value: Union[int, float],
                             node: np.ndarray, edge2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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

        mat_elem = 1 / 6 * np.pi * length_edge * value * (coord_node1[0] * np.array([[3, 1], [1, 1]]) +
                                                          coord_node2[0] * np.array([[1, 1], [1, 3]]))

        idx_node = edge2node[edge, :]
        tmp = np.stack((idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node))

        i_local[k] = np.reshape(tmp, (4,))
        j_local[k] = np.reshape(tmpt, (4,))
        v_local[k] = np.reshape(mat_elem, (4,))

    return i_local.flatten(), j_local.flatten(), v_local.flatten()


@njit_cache(parallel=True)
def calc_robin_term_array(edges: np.ndarray, value: np.ndarray,
                          node: np.ndarray, edge2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
                                                             coord_node2[0] * np.array([[1, 1], [1, 3]]))

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
                             node_transformed: np.ndarray, edge2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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

        mat_elem = 2 * np.pi * integral
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


@njit_cache(parallel=True)
def calc_div_array(values: np.ndarray, b: np.ndarray, c: np.ndarray,
                   bmat_11: np.ndarray, bmat_12: np.ndarray, r1: np.ndarray,
                   elem2node) -> np.ndarray:
    """Calculates the div-operator for a given array of values per element.

    Calculates the contribution of each element to the div matrix. The calculated values
    and line and column information are written to v, i and j, respectively.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in the mesh
        N       Number of nodes in the mesh
        ======  =======

    Parameters
    ----------
    values : np.ndarray
        (E,2) array. One material vector per element.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_11 : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    bmat_12 : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    r1 : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricNodalShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.div_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.div_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricNodalShapeFunction.div_operator`.
    """
    num_elements = elem2node.shape[0]

    i = np.empty((num_elements, 9))
    j = np.empty((num_elements, 9))
    v = np.empty((num_elements, 9))

    helper_1 = np.array([1 / 24, 1 / 12, 1 / 24])
    helper_2 = np.array([1 / 24, 1 / 24, 1 / 12])
    helper_3 = np.array([1 / 6, 1 / 6, 1 / 6])
    for element in prange(num_elements):
        b_elem = b[element]
        c_elem = c[element]
        values_elem = values[element]

        mat_elem = np.pi * np.outer(values_elem[0] * b_elem + values_elem[1] * c_elem,
                                    bmat_11[element] * helper_1 + bmat_12[element] * helper_2
                                    + r1[element] * helper_3)

        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        j[element] = np.reshape(tmp, (9,))  # 1 2 3 1 2 3
        i[element] = np.reshape(tmpt, (9,))  # 1 1 1 2 2 2 3 3 3
        v[element] = np.reshape(mat_elem, (9,))  #

    return i.flatten(), j.flatten(), v.flatten()


class TriAxisymmetricNodalShapeFunction(NodalShapeFunction):
    """Class representing shape functions in axisymmetric geometries with a triangular mesh in the rz-plane."""

    def __init__(self, mesh: 'AxiMesh'):
        """Constructor.

        Parameters
        ----------
        mesh : AxiMesh
            The mesh object.
        """
        super().__init__(mesh, dim=2, allocation_size=9 * mesh.num_elem)
        self.__determinant_b = np.zeros(mesh.num_elem)
        self.__calc_coefficients()

    def __calc_coefficients(self) -> NoReturn:
        """
        Calculates some coefficients that are needed in various methods of this class.

        Returns
        -------
        NoReturn
        """
        r1 = self.mesh.node[self.mesh.elem2node, 0]
        z1 = self.mesh.node[self.mesh.elem2node, 1]
        r2 = np.roll(r1, -1, axis=1)
        z2 = np.roll(z1, -1, axis=1)
        r3 = np.roll(r1, -2, axis=1)
        z3 = np.roll(z1, -2, axis=1)
        self.a = r2 * z3 - r3 * z2
        self.b = z2 - z3
        self.c = r3 - r2

        r1 = self.mesh.node[self.mesh.elem2node[:, 0], 0]
        r2 = self.mesh.node[self.mesh.elem2node[:, 1], 0]
        r3 = self.mesh.node[self.mesh.elem2node[:, 2], 0]
        z1 = self.mesh.node[self.mesh.elem2node[:, 0], 1]
        z2 = self.mesh.node[self.mesh.elem2node[:, 1], 1]
        z3 = self.mesh.node[self.mesh.elem2node[:, 2], 1]
        self.p1_to_p2 = np.c_[r2 - r1, z2 - z1]
        self.p1_to_p3 = np.c_[r3 - r1, z3 - z1]
        # (elements,2,3) array. For every element there are the 3 coefficients for s and z
        self.transform_coefficients = np.stack((self.p1_to_p2, self.p1_to_p3, np.c_[r1, z1]), axis=2)

        self.bmat_11 = self.p1_to_p2[:, 0]
        self.bmat_12 = self.p1_to_p3[:, 0]
        self.r1 = r1

        # Calculate the cross product of the vectors p1_to_p2 and p1_to_p3. The absolute value corresponds to the area
        # of the parallelogram spanned by the two vector (= twice the element area) and the sign depends on the
        # orientation of the triangle (ijk or ikj)
        self.__parallelogram_areas_oriented = self.p1_to_p2[:, 0] * self.p1_to_p3[:, 1] - \
                                              self.p1_to_p2[:, 1] * self.p1_to_p3[:, 0]
        # Calculate the absolute value of the determinant of the transformation matrix for every element
        self.__determinant_b = np.abs(self.__parallelogram_areas_oriented)

    def _calc_evaluation_points_element(self, local_coordinates: np.ndarray, indices: np.ndarray) -> np.ndarray:
        return calc_evaluation_points_element(local_coordinates, self.transform_coefficients, indices)

    # region Calc matrix

    # region Calc matrix constant

    def _calc_matrix_constant_scalar(self, matrix_type: str, indices: np.ndarray, value: Number,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_constant_scalar(indices, value, self.b, self.c, self.bmat_11, self.bmat_12,
                                                self.r1, self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_constant_scalar(indices, value, self.bmat_11, self.bmat_12, self.r1,
                                             self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_constant_scalar is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_constant_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        return NotImplementedError(f"calc_matrix_constant_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_constant_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, *args, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_constant_tensor(indices, value, self.b, self.c, self.bmat_11, self.bmat_12,
                                                self.r1, self.__determinant_b, self.mesh.elem2node)
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
            return calc_divgrad_scalar_per_elem(indices, value, self.b, self.c, self.bmat_11, self.bmat_12,
                                                self.r1, self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_scalar_per_elem(indices, value, self.bmat_11, self.bmat_12,
                                             self.r1, self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_scalar_per_elem is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_elementwise_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_vector_per_elem is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_elementwise_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_tensor_per_elem(indices, value, self.b, self.c, self.bmat_11, self.bmat_12,
                                                self.r1, self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            raise NotImplementedError('Mass matrix does not support tensors.')

        raise NotImplementedError(f"calc_matrix_tensor_per_elem is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix elementwise

    # region Calc matrix function

    def _calc_matrix_function_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        evaluation_points = kwargs.pop("evaluation_points", None)
        if evaluation_points is None:
            evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

        if matrix_type == "divgrad":
            return calc_divgrad_function_scalar(indices, weights, evaluation_points, value,
                                                self.b, self.c, self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_function_scalar(indices, weights, local_coordinates, evaluation_points, value,
                                             self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_function_scalar is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_function_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_function_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_function_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            evaluation_points = kwargs.pop("evaluation_points", None)
            if evaluation_points is None:
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

            return calc_divgrad_function_tensor(indices, weights, evaluation_points, value,
                                                self.b, self.c, self.__determinant_b, self.mesh.elem2node)
        if matrix_type == "mass":
            raise NotImplementedError('Mass matrix does not support tensors.')

        raise NotImplementedError(f"calc_matrix_function_scalar is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix function

    # endregion Calc matrix

    # region Calc vector

    # region Calc vector constant

    def _calc_vector_constant_scalar(self, vector_type: str, indices: np.ndarray, value: Number,
                                     weights: np.ndarray,
                                     local_coordinates: np.ndarray, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_constant_scalar(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load":
            return calc_load_constant(indices, value, self.bmat_11, self.bmat_12, self.r1, self.__determinant_b,
                                      self.mesh.elem2node)

        raise NotImplementedError(f"calc_vector_constant_scalar is not implemented for vector type: {vector_type}.")

    def _calc_vector_constant_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_constant_vector(vector_type, indices, value, weights, local_coordinates, **kwargs)

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
            return calc_load_vector(indices, value, self.bmat_11, self.bmat_12, self.r1, self.__determinant_b,
                                    self.mesh.elem2node)

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
            evaluation_points = kwargs.pop("evaluation_points", None)
            if evaluation_points is None:
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

            return calc_load_function(indices, weights, local_coordinates, evaluation_points, value,
                                      self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_vector_function_scalar is not implemented for vector type: {vector_type}.")

    def _calc_vector_function_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_function_vector(vector_type, indices, value, weights, local_coordinates, **kwargs)

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

    def fem_div_operator(self, values: np.ndarray):
        r"""Returns the discrete representation of the weak formulation of div-terms.

        Compute the discrete operator for terms of the form :math:`-\mathrm{div}(\phi * \vec{m})`,
        where :math:`\phi` the scalar solution field and :math:`\vec{m}` a known vector field.
        Needed e.g. for the adjoint method for coupled electrothermal problems.

        Parameters
        ----------
        values : np.ndarray
            (M,2)-array with two entries per element that represents the vector field :math:`\vec{m}`.
            (M is the number of elements in the mesh)

        Returns
        -------
        divgrad : (N,N) coo_matrix
            Sparse matrix representing the discrete fem-div operator for nodal shape functions on the underlying mesh.
            (N is the number of nodes in the mesh)
        """
        if values.shape[0] != self.mesh.num_elem or values.shape[1] != 2:
            raise ValueError('Expected (numelem, 2) as shape of values the shape, '
                             'but got' + values.shape + ' instead.')
        i, j, v = calc_div_array(values, self.b, self.c, self.bmat_11, self.bmat_12, self.r1,
                                 self.mesh.elem2node)
        return coo_matrix((v, (i, j)), shape=(self.mesh.num_node, self.mesh.num_node))

    def fem_grad_operator(self, values: np.ndarray):
        r"""Returns the discrete representation of the weak formulation of grad terms.

        Compute the discrete operator for terms of the form :math:`\mathrm{grad}(\phi) * \vec{m}`,
        where :math:`\phi` the scalar solution field and :math:`\vec{m}` a known vector field.
        Needed e.g. for the adjoint method for coupled electrothermal problems.

        Parameters
        ----------
        values : np.ndarray
            (M,2)-array with two entries per element that represents the vector field :math:`\vec{m}`.
            (M is the number of elements in the mesh)

        Returns
        -------
        fem_grad : (N,N) coo_matrix
            Sparse matrix representing the discrete fem-grad operator for nodal shape functions on the underlying mesh.
            (N is the number of nodes in the mesh)
        """
        if values.shape[0] != self.mesh.num_elem or values.shape[1] != 2:
            raise ValueError('Expected (numelem, 2) as shape of values the shape, '
                             'but got' + values.shape + ' instead.')
        i, j, v = calc_div_array(values, self.b, self.c, self.bmat_11, self.bmat_12, self.r1,
                                 self.mesh.elem2node)
        return coo_matrix((v, (j, i)), shape=(self.mesh.num_node, self.mesh.num_node))

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
                    i_tmp, v_tmp = calc_neumann_term_constant(indices_edges, bc.value, self.mesh.node,
                                                              self.mesh.edge2node)
                else:
                    i_tmp, v_tmp = calc_neumann_term_constant(indices_edges, bc.value(), self.mesh.node,
                                                              self.mesh.edge2node)
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
                i, v = calc_neumann_term_function(indices, weights, local_coordinates, evaluation_points,
                                                  evaluations, self.mesh.node, self.mesh.edge2node)
            elif flag_value == 'array':
                i, v = calc_neumann_term_array(indices, value, self.mesh.node, self.mesh.edge2node)
            elif flag_value == 'value':
                i, v = calc_neumann_term_constant(indices, value, self.mesh.node, self.mesh.edge2node)
        columns = np.zeros(len(i), dtype=int)
        neumann_vector = coo_matrix((v, (i, columns)), shape=(self.mesh.num_node, 1))
        return neumann_vector

    # pylint: disable=cell-var-from-loop
    def robin_terms(self, regions: 'Regions', boundary_condition: 'BdryCond', integration_order: int = 1) -> \
            Tuple[csr_matrix, csr_matrix]:
        bc_keys = boundary_condition.get_ids()
        weights, local_coordinates = gauss(integration_order)
        values_list = []
        lines_list = []
        columns_list = []
        robin_vector = coo_matrix((self.mesh.num_node, 1))

        for bc_key in bc_keys:
            bc = boundary_condition.get_bc(bc_key)
            if not isinstance(bc, BCRobin):
                continue

            # Calculate the matrix
            indices_regions = regions.find_regions_of_boundary_condition(bc.ID)
            indices_edges = np.empty(0)  # Indices of all edges that are on the boundary bc
            for region_id in indices_regions:
                indices_edges = np.r_[indices_edges, np.where(self.mesh.edge2regi == region_id)[0]]
            indices_edges = indices_edges.astype('int')

            coef_dir = bc.coefficient_dirichlet
            coef_neum = bc.coefficient_neumann
            if isinstance(coef_neum, ndarray) or isinstance(coef_dir, ndarray):
                raise NotImplementedError
            value_bc = bc.value
            if callable(coef_dir):
                if callable(coef_neum):  # Both coefficients are functions
                    evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node,
                                                                    indices_edges, self.mesh.edge2node)
                    evaluations = evaluate_for_num_int_edge(lambda r, z: coef_dir(r, z) / coef_neum(r, z),
                                                            evaluation_points)
                    robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_function(
                        indices_edges, weights, local_coordinates, evaluation_points, evaluations,
                        self.mesh.node, self.mesh.edge2node)
                else:  # Only dirichlet coefficient is a function
                    evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node,
                                                                    indices_edges, self.mesh.edge2node)
                    evaluations = evaluate_for_num_int_edge(lambda r, z: coef_dir(r, z) / coef_neum,
                                                            evaluation_points)
                    robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_function(
                        indices_edges, weights, local_coordinates, evaluation_points, evaluations,
                        self.mesh.node, self.mesh.edge2node)
            else:
                if callable(coef_neum):  # Only coef_neum is a function
                    evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node,
                                                                    indices_edges, self.mesh.edge2node)
                    evaluations = evaluate_for_num_int_edge(lambda r, z: coef_dir / coef_neum(r, z), evaluation_points)
                    robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_function(
                        indices_edges, weights, local_coordinates, evaluation_points, evaluations,
                        self.mesh.node, self.mesh.edge2node)
                else:  # Both are no functions
                    value = coef_dir / coef_neum
                    robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_constant(
                        indices_edges, value, self.mesh.node, self.mesh.edge2node)
            values_list.append(robin_values_per_bc)
            lines_list.append(robin_lines_per_bc)
            columns_list.append(robin_columns_per_bc)

            # Calculate the vector
            if callable(value_bc):
                if callable(coef_neum):
                    # Both are functions
                    robin_vector = robin_vector + self.neumann_term(indices_edges,
                                                                    (lambda r, z: value_bc(r, z) / coef_neum(r, z),),
                                                                    integration_order=integration_order)
                else:
                    # only value_bc is a function
                    if isinstance(coef_neum, np.ndarray):
                        robin_vector = robin_vector + self.neumann_term(indices_edges,
                                                                        (lambda r, z: value_bc(r, z) / coef_neum,),
                                                                        integration_order=integration_order)
                    elif isinstance(coef_neum, (float, int)):
                        robin_vector = robin_vector + self.neumann_term(indices_edges,
                                                                        (lambda r, z: value_bc(r, z) / coef_neum,),
                                                                        integration_order=integration_order)
                    else:
                        raise Exception("Type of coef_neum is not supported.")
            else:
                if callable(coef_neum):
                    # Only Neumann coefficient is a function
                    if isinstance(value_bc, np.ndarray):
                        robin_vector = robin_vector + self.neumann_term(indices_edges,
                                                                        (lambda r, z: value_bc / coef_neum(r, z),),
                                                                        integration_order=integration_order)
                    elif isinstance(value_bc, (float, int)):
                        robin_vector = robin_vector + self.neumann_term(indices_edges,
                                                                        (lambda r, z: value_bc / coef_neum(r, z),),
                                                                        integration_order=integration_order)
                    else:
                        raise Exception("Type of value not supported")

                else:
                    value_tmp = value_bc / coef_neum
                    if isinstance(value_tmp, np.ndarray):
                        robin_vector = robin_vector + self.neumann_term(indices_edges, (value_tmp,),
                                                                        integration_order=integration_order)
                    elif isinstance(value_tmp, (float, int)):
                        robin_vector = robin_vector + self.neumann_term(indices_edges, (value_tmp,),
                                                                        integration_order=integration_order)
                    else:
                        raise Exception("Type not supported.")

        robin_matrix = coo_matrix(
            (np.concatenate(values_list), (np.concatenate(lines_list), np.concatenate(columns_list))),
            shape=(self.mesh.num_node, self.mesh.num_node))
        return robin_matrix, robin_vector.tocoo()

    def gradient(self, val2node: np.ndarray) -> np.ndarray:
        out = calc_gradient(val2node, self.mesh.elem2node, self.mesh.num_elem, self.b, self.c,
                            self.__parallelogram_areas_oriented)
        return out
