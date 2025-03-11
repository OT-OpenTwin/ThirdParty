# coding=utf-8
"""
File containing the class TriAxisymmetricEdgeShapeFunction.

Numba is used with a lot of functions to get a good performance. The data types of the arguments of the numa functions
can be given in the decorator. If one of these functions is called with another data type it does not work anymore.
Because different data types of some arguments should be supported the data types are not indicated in the decorator.
Anyway, the code is written such that the data types of the arguments are as equal as possible for different user input
parameters. So the number of compilations with numba should be at a minimum.

.. sectionauthor:: bundschuh
"""
# pylint: disable=duplicate-code

from typing import Union, Callable, Tuple, NoReturn, TYPE_CHECKING, Dict, Any

import numpy as np
from numpy import ndarray, log
from scipy.sparse import coo_matrix, csr_matrix, vstack
from scipy.sparse import linalg as splinalg
from numba import prange

from pyrit.region import Regions
from pyrit.bdrycond import BdryCond, BCNeumann, BCRobin, BCDirichlet

from pyrit.toolbox.QuadratureToolbox import gauss
from pyrit.toolbox.NumbaToolbox import njit_cache
from pyrit import get_logger

from pyrit.shapefunction.EdgeShapeFunction import EdgeShapeFunction, NumericalData, MaterialData, ExcitationData
from pyrit.shapefunction.ShapeFunction import Number

if TYPE_CHECKING:
    from .ShapeFunction import ShrinkInflateProblemShapeFunction
    from pyrit.mesh import AxiMesh
    from pyrit.excitation import FieldCircuitCoupling

logger = get_logger(__name__)


# region General functions

@njit_cache(parallel=True)
def calc_evaluation_points_element(local_coordinates: np.ndarray, transform_coefficcients: np.ndarray,
                                   elements: np.ndarray) -> np.ndarray:
    """Calculates the coordinates (s,z) needed for the evaluation of the numerical integration on an element.

    Returns a three dimensional array with the evaluation coordinates for all elements specified. The return values is
    a (E,N,2) array. It is `out[e,n,0]` and `out[e,n,1]` the s and z coordinate on element e and evaluation point
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
    transform_coefficcients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
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
        tc = transform_coefficcients[element]  # (2,3) array
        tct = tc.T
        coords[k] = local_cds @ tct
    return coords


@njit_cache(parallel=True)
def calc_evaluation_points_edge(local_coordinates: np.ndarray, node_transformed: np.ndarray,
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
        first_node = edge2node[edge, 0]
        second_node = edge2node[edge, 1]

        for kk in range(num_coordinates):
            coords[k, kk] = node_transformed[first_node] + local_coordinates[kk] * (
                node_transformed[second_node] - node_transformed[first_node])

    return coords


def eval_inhom_lin_iso(fun: Callable[[float, float], float], evaluation_points: np.ndarray):
    """Evaluate an inhomogeneous, linear and isotropic function.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Callable[[float, float], float]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.

    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of an arbitrary function is
    necessary, can be computed.
    """
    evaluations = np.vectorize(fun)(np.sqrt(evaluation_points[:, :, 0]), evaluation_points[:, :, 1])
    # evaluations.astype(float, copy=False)  #change: why make it float?
    return evaluations


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
        (E,N) array with evaluations.
    """
    vfun = np.vectorize(fun, signature='(),()->(i,i)')
    evaluations = vfun(np.sqrt(evaluation_points[:, :, 0]), evaluation_points[:, :, 1])
    # evaluations.astype(float, copy=False)  #change: why make it float?
    return evaluations


def eval_inhom_nonlin_iso(fun: Callable[[float, float, int], float], evaluation_points: np.ndarray,
                          elements: np.ndarray):
    """Evaluates an inhomogeneous, nonlinear and isotropic function

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Callable[[float, float], float]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    elements : np.ndarray
        Array of the considered elements.

    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of an arbitrary function is
    necessary, can be computed.
    """
    indices = np.kron(np.ones((evaluation_points.shape[1], 1), dtype=int), elements).transpose()
    evaluations = np.vectorize(fun)(np.sqrt(evaluation_points[:, :, 0]), evaluation_points[:, :, 1], indices)
    # evaluations.astype(float, copy=False)  #change: why make it float?
    return evaluations


def eval_inhom_nonlin_aniso(fun: Callable[[float, float, int], np.ndarray], evaluation_points: np.ndarray,
                            elements: np.ndarray):
    """Evaluates an inhomogeneous, nonlinear and anisotropic function

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Callable[[float, float], float]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    elements : np.ndarray
        Array of the considered elements.

    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of an arbitrary function is
    necessary, can be computed.
    """
    indices = np.kron(np.ones((evaluation_points.shape[1], 1), dtype=int), elements).transpose()
    vfun = np.vectorize(fun, signature='(),(),()->(i,i)')
    evaluations = vfun(np.sqrt(evaluation_points[:, :, 0]), evaluation_points[:, :, 1], indices)
    # evaluations.astype(float, copy=False)  #change: why make it float?
    return evaluations


def eval_neumann_hom_lin(indices: np.ndarray, value: np.ndarray, mesh: 'AxiMesh', weights: np.ndarray):
    """Evaluate a homogeneous and linear value for Neumann boundary conditions.

    Parameters
    ----------
    indices : np.ndarray
        The indices of the edges
    value : np.ndarray
        A (2,) array with r and z component
    mesh : AxiMesh
        The AxiMesh
    weights : np.ndarray
        The weights of the numerical integration

    Returns
    -------
    evaluation : np.ndarray
    """
    evaluations = np.empty((len(indices), len(weights)))
    for k, edge in enumerate(indices):
        nv = mesh.calc_normal_vector(edge)
        for kk in range(len(weights)):
            evaluations[k, kk] = np.dot(value, [nv[1], -nv[0]])
    return evaluations


def eval_neumann_hom_nonlin(indices: np.ndarray, value: Callable[[], np.ndarray], mesh: 'AxiMesh', weights: np.ndarray):
    """Evaluate a homogeneous and nonlinear value for Neumann boundary conditions.

    Parameters
    ----------
    indices : np.ndarray
        The indices of the edges
    value : Callable[[], np.ndarray]
        Returns a (2,) array with r and z component
    mesh : AxiMesh
        The AxiMesh
    weights : np.ndarray
        The weights of the numerical integration

    Returns
    -------
    evaluation : np.ndarray
    """
    evaluations = np.empty((len(indices), len(weights)))
    for k, edge in enumerate(indices):
        nv = mesh.calc_normal_vector(edge)
        for kk in range(len(weights)):
            # noinspection PyArgumentList
            evaluations[k, kk] = np.dot(value(element=k), [nv[1], -nv[0]])
    return evaluations


def eval_neumann_inhom_lin(indices: np.ndarray, value: Callable[[float, float], np.ndarray], mesh: 'AxiMesh',
                           weights: np.ndarray, evaluation_points: np.ndarray):
    """Evaluate an inhomogeneous and linear value for Neumann boundary conditions.

    Parameters
    ----------
    indices : np.ndarray
        The indices of the edges
    value : Callable[[float, float], np.ndarray]
        Returns a (2,) array with r and z component
    mesh : AxiMesh
        The AxiMesh
    weights : np.ndarray
        The weights of the numerical integration
    evaluation_points : np.ndarray
        The evaluation points.

    Returns
    -------
    evaluation : np.ndarray
    """
    evaluations = np.empty((len(indices), len(weights)))
    for k, edge in enumerate(indices):
        nv = mesh.calc_normal_vector(edge)
        for kk in range(len(weights)):
            evaluations[k, kk] = np.dot(value(np.sqrt(evaluation_points[k, kk, 0]), evaluation_points[k, kk, 1]),
                                        [nv[1], -nv[0]])
    return evaluations


def eval_neumann_inhom_nonlin(indices: np.ndarray, value: Callable[[float, float], np.ndarray], mesh: 'AxiMesh',
                              weights: np.ndarray, evaluation_points: np.ndarray):
    """Evaluate an inhomogeneous and nonlinear value for Neumann boundary conditions.

    Parameters
    ----------
    indices : np.ndarray
        The indices of the edges
    value : Callable[[float, float], np.ndarray]
        Returns a (2,) array with r and z component
    mesh : AxiMesh
        The AxiMesh
    weights : np.ndarray
        The weights of the numerical integration
    evaluation_points : np.ndarray
        The evaluation points.

    Returns
    -------
    evaluation : np.ndarray
    """
    evaluations = np.empty((len(indices), len(weights)))
    for k, edge in enumerate(indices):
        nv = mesh.calc_normal_vector(edge)
        for kk in range(len(weights)):
            # noinspection PyArgumentList
            evaluations[k, kk] = np.dot(value(np.sqrt(evaluation_points[k, kk, 0]),
                                              evaluation_points[k, kk, 1], element=k), [nv[1], -nv[0]])
    return evaluations


def evaluate_for_num_int_edge(fun: Callable[[float, float], float], evaluation_points: np.ndarray):
    """Evaluates the function `fun` for numerical integration on edges.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified edges.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of edges in `edges`
        ======  =======

    Parameters
    ----------
    fun : Callable[[float, float], float]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_edge`.

    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evalutations of the material function at the evaluation points for the
        numerical integration.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of a arbitrary funtion is
    necessary, can be computed.
    """
    evaluations = np.vectorize(fun)(np.sqrt(evaluation_points[:, :, 0]), evaluation_points[:, :, 1])
    evaluations.astype(float, copy=False)
    return evaluations


evaluation_functions = {'eval_inhom_lin_iso': eval_inhom_lin_iso,
                        'eval_inhom_lin_aniso': eval_inhom_lin_aniso,
                        'eval_inhom_nonlin_iso': eval_inhom_nonlin_iso,
                        'eval_inhom_nonlin_aniso': eval_inhom_nonlin_aniso,
                        'evaluate_for_num_int_edge': evaluate_for_num_int_edge}


# endregion


# region Functions for curlcurl

@njit_cache
def calc_integral(alpha: float, beta: float, gamma: float):
    r"""Calculates the value of an integral needed for the curlcurl operator.

    Parameters
    ----------
    alpha : float
    beta : float
    gamma : float

    Returns
    -------
    out : float64
        The value of the integral

    Notes
    -----
    The following integral is computed

    .. math::

        \int_0^1\int_0^{1-\xi}\frac{1}{\alpha \xi + \beta \eta + \gamma}\mathrm{d}\eta\mathrm{d}\xi\,.
    """
    if (alpha == 0 and gamma == 0) or (beta == 0 and gamma == 0):
        return 0
    if alpha == 0:
        if beta + gamma == 0:
            return -1 / beta
        return (-beta + (beta + gamma) * log((beta + gamma) / gamma)) / beta ** 2
    if beta == 0:
        if alpha + gamma == 0:
            return -1 / alpha
        return (-alpha + (alpha + gamma) * log((alpha + gamma) / gamma)) / alpha ** 2
    if gamma == 0:
        if alpha == beta:
            return 1 / alpha
        return (log(alpha) - log(beta)) / (alpha - beta)
    if alpha == beta:
        return (alpha + gamma * log(gamma / (alpha + gamma))) / alpha ** 2
    if alpha + gamma == 0:
        return -1 / alpha
    return (alpha * (beta + gamma) * log((alpha + gamma) / (beta + gamma)) + gamma * (alpha - beta) * log(
        gamma / (alpha + gamma))) / (alpha * beta * (alpha - beta))


@njit_cache(parallel=True)
def calc_curlcurl_constant_scalar(elements: np.ndarray, value: Union[int, float], b: np.ndarray, c: np.ndarray,
                                  transform_coefficcients: np.ndarray, determinant_b: np.ndarray,
                                  s: np.ndarray, elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the curlcurl_operator with a constant material.

    Calculates the contribution of the elements specified in `elements` to the curlcurl matrix. The calculated values
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
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    transform_coefficcients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    s : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9), np.int_)
    j = np.empty((num_elements, 9), np.int_)
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        b_mat = np.outer(b[element], b[element])
        c_mat = np.outer(c[element], c[element])

        integral = calc_integral(transform_coefficcients[element, 0, 0], transform_coefficcients[element, 0, 1],
                                 transform_coefficcients[element, 0, 2])

        mat_elem = determinant_b[element] * value / (np.pi * s[element] ** 2) * (c_mat * integral / 4 + b_mat / 2)
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_curlcurl_constant_tensor(elements: np.ndarray, weights: np.ndarray, evaluation_points: np.ndarray,
                                  value: np.ndarray, b: np.ndarray, c: np.ndarray,
                                  transform_coefficcients: np.ndarray, determinant_b: np.ndarray,
                                  s: np.ndarray, elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculates elements for the curlcurl_operator with a constant material.

    Calculates the contribution of the elements specified in `elements` to the curlcurl matrix. The calculated values
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
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    value : Union[int, float]
        The value of the material.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    transform_coefficcients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    s : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
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

        integral_off_diagonal = np.dot(weights, 1 / np.sqrt(evaluation_points[k, :, 0]))

        integral = calc_integral(transform_coefficcients[element, 0, 0], transform_coefficcients[element, 0, 1],
                                 transform_coefficcients[element, 0, 2])
        sum_integrals = c_mat * 0.25 * integral * value[0, 0] + \
                        b_mat * 0.5 * value[1, 1] - \
                        bc_mat * 0.5 * integral_off_diagonal * value[0, 1] - \
                        cb_mat * 0.5 * integral_off_diagonal * value[1, 0]
        mat_elem = 1 / (np.pi * s[element] ** 2) * determinant_b[element] * sum_integrals
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_curlcurl_scalar_per_elem(elements: np.ndarray, value: np.ndarray, b: np.ndarray, c: np.ndarray,
                                  transform_coefficients: np.ndarray, determinant_b: np.ndarray, s: np.ndarray,
                                  elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the curlcurl_operator with one constant value of the material per element.

    Calculates the contribution of the elements specified in `elements` to the curlcurl matrix. The calculated values
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
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    transform_coefficients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    s : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
     i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 9))
    j = np.empty((num_elements, 9))
    v = np.empty((num_elements, 9))
    for k in prange(num_elements):
        element = elements[k]

        b_mat = np.outer(b[element], b[element])
        c_mat = np.outer(c[element], c[element])

        integral = calc_integral(transform_coefficients[element, 0, 0], transform_coefficients[element, 0, 1],
                                 transform_coefficients[element, 0, 2])

        mat_elem = determinant_b[element] * value[k] / (np.pi * s[element] ** 2) * (c_mat * integral / 4 + b_mat / 2)
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_curlcurl_tensor_per_elem(elements: np.ndarray, weights: np.ndarray, evaluation_points: np.ndarray,
                                  value: np.ndarray, b: np.ndarray, c: np.ndarray,
                                  transform_coefficients: np.ndarray, determinant_b: np.ndarray, s: np.ndarray,
                                  elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the curlcurl_operator with one constant tensor of the material per element.

    Calculates the contribution of the elements specified in `elements` to the curlcurl matrix. The calculated values
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
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    value : np.ndarray
        (E,2) array. One tensor per element.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    transform_coefficients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    s : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
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

        integral_off_diagonal = np.dot(weights, 1 / np.sqrt(evaluation_points[k, :, 0]))

        integral = calc_integral(transform_coefficients[element, 0, 0], transform_coefficients[element, 0, 1],
                                 transform_coefficients[element, 0, 2])
        sum_integrals = c_mat * 0.25 * integral * value[k, 0, 0] + \
                        b_mat * 0.5 * value[k, 1, 1] - \
                        bc_mat * 0.5 * integral_off_diagonal * value[k, 0, 1] - \
                        cb_mat * 0.5 * integral_off_diagonal * value[k, 1, 0]
        mat_elem = 1 / (np.pi * s[element] ** 2) * determinant_b[element] * sum_integrals
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    # Write results to i, j, v
    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_curlcurl_function_scalar(elements: np.ndarray, weights: np.ndarray, evaluation_points: np.ndarray,
                                  evaluations: np.ndarray, b: np.ndarray, c: np.ndarray,
                                  determinant_b: np.ndarray, s: np.ndarray, elem2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the curlcurl_operator with a function as material.

    Calculates the contribution of the elements specified in `elements` to the curlcurl matrix. The calculated values
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
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    s : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    """
    num_elements = len(elements)

    i_local = np.empty((num_elements, 9))
    j_local = np.empty((num_elements, 9))
    v_local = np.empty((num_elements, 9))
    for k in prange(num_elements):
        index = elements[k]

        b_mat = np.outer(b[index], b[index])
        c_mat = np.outer(c[index], c[index])

        first_integral = np.dot(weights, evaluations[k] / evaluation_points[k, :, 0])
        second_integral = np.sum(weights * evaluations[k])

        mat_elem = determinant_b[index] / (np.pi * s[index] ** 2) * \
                   (c_mat * first_integral / 4 + b_mat * second_integral)
        idx_node = elem2node[index, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i_local[k] = np.reshape(tmp, (9,))
        j_local[k] = np.reshape(tmpt, (9,))
        v_local[k] = np.reshape(mat_elem, (9,))

    return i_local.flatten(), j_local.flatten(), v_local.flatten()


@njit_cache(parallel=True)  # todo:docstring
def calc_curlcurl_function_tensor(elements: np.ndarray, weights: np.ndarray, evaluation_points: np.ndarray,
                                  evaluations: np.ndarray, b: np.ndarray, c: np.ndarray,
                                  determinant_b: np.ndarray, s: np.ndarray, elem2node: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the curlcurl_operator with a function as material.

    Calculates the contribution of the elements specified in `elements` to the curlcurl matrix. The calculated values
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
        (E,N,2,2) array. For every element the N evalutations of the material function at the evaluation points for the
        numerical integration. See :py:func:`evaluate_for_num_int_element`.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    s : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
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
        cb_mat = np.outer(c[element], b[element])

        first_integral = np.dot(weights, evaluations[k, :, 0, 0] / evaluation_points[k, :, 0])
        second_integral = np.sum(weights * evaluations[k, :, 1, 1])
        third_integral = np.dot(weights, evaluations[k, :, 0, 1] / np.sqrt(evaluation_points[k, :, 0]))
        fourth_integral = np.dot(weights, evaluations[k, :, 1, 0] / np.sqrt(evaluation_points[k, :, 0]))

        sum_integrals = c_mat * 0.25 * first_integral + b_mat * second_integral - \
                        bc_mat * 0.5 * third_integral - cb_mat * 0.5 * fourth_integral

        mat_elem = 1 / (np.pi * s[element] ** 2) * determinant_b[element] * sum_integrals
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
def calc_mass_constant_scalar(elements: np.ndarray, value: Union[int, float], weights: np.ndarray,
                              local_coordinates: np.ndarray, transform_coefficcients: np.ndarray,
                              determinant_b: np.ndarray, elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the mass matrix with a constant material.

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
        (E,) array. The indices of elements that should be considered.
    value : Union[int, float]
        The value of the material.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    transform_coefficcients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    """
    evaluation_points = calc_evaluation_points_element(local_coordinates, transform_coefficcients, elements)
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
            integral = integral + weight / evaluation_points[k, kk, 0] * np.outer(m_values, m_values)

        mat_elem = value * determinant_b[element] / (4 * np.pi) * integral
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_mass_scalar_per_elem(elements: np.ndarray, value: np.ndarray, weights: np.ndarray,
                              local_coordinates: np.ndarray, transform_coefficcients: np.ndarray,
                              determinant_b: np.ndarray, elem2node) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates elements for the mass matrix with value being a vector.

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
        (E,) array. The indices of elements that should be considered.
    value : Union[int, float]
        The value of the material.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    transform_coefficcients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    """
    evaluation_points = calc_evaluation_points_element(local_coordinates, transform_coefficcients, elements)
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
            integral = integral + weight / evaluation_points[k, kk, 0] * np.outer(m_values, m_values)

        mat_elem = value[k] * determinant_b[element] / (4 * np.pi) * integral
        idx_node = elem2node[element, :]

        tmp = np.stack((idx_node, idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node, idx_node))

        i[k] = np.reshape(tmp, (9,))
        j[k] = np.reshape(tmpt, (9,))
        v[k] = np.reshape(mat_elem, (9,))

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_mass_function_scalar(elements: np.ndarray, weights: np.ndarray, local_coordinates: np.ndarray,
                              evaluation_points: np.ndarray, evaluations: np.ndarray,
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
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriAxisymmetricEdgeShapeFunction.curlcurl_operator`.
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
            integral = integral + weight * evaluations[k, kk] / evaluation_points[k, kk, 0] * np.outer(m_values,
                                                                                                       m_values)

        mat_elem = determinant_b[element] / (4 * np.pi) * integral
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
                       weights: np.ndarray,
                       local_coordinates: np.ndarray,
                       evaluation_points: np.ndarray,
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
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    transform_coefficcients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable `i_elem` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See the variable `v_elem` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    """
    # evaluation_points = calc_evaluation_points_element(local_coordinates, transform_coefficcients, elements)
    num_elements = len(elements)

    i = np.empty((num_elements, 3), np.int_)
    v = np.empty((num_elements, 3))
    for k in prange(num_elements):
        element = elements[k]

        integral = np.zeros(3)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk, 0] - local_coordinates[kk, 1], local_coordinates[kk, 0],
                                 local_coordinates[kk, 1]])
            integral = integral + weight / np.sqrt(evaluation_points[k, kk, 0]) * m_values

        vec_elem = value * determinant_b[element] / 2 * integral
        idx_node = elem2node[element, :]

        i[k] = idx_node
        v[k] = vec_elem

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_load_array(elements: np.ndarray,
                    value: np.ndarray,
                    weights: np.ndarray,
                    local_coordinates: np.ndarray,
                    evaluation_points: np.ndarray,
                    determinant_b: np.ndarray,
                    elem2node) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates elements for the load vector with a constant load per element.

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
    value : np.ndarray
        (E,) array. One value per element specified in `elements`.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    transform_coefficcients : np.ndarray
        (T,3,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable `i_elem` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See the variable `v_elem` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    """
    # evaluation_points = calc_evaluation_points_element(local_coordinates, transform_coefficcients, elements)
    num_elements = len(elements)

    i = np.empty((num_elements, 3), np.int_)
    v = np.empty((num_elements, 3))
    for k in prange(num_elements):
        element = elements[k]

        integral = np.zeros(3)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk, 0] - local_coordinates[kk, 1], local_coordinates[kk, 0],
                                 local_coordinates[kk, 1]])
            integral = integral + weight / np.sqrt(evaluation_points[k, kk, 0]) * m_values

        vec_elem = value[k] * determinant_b[element] / 2 * integral
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
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable `i_elem` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See the variable  `v_elem` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 3), np.int_)
    v = np.empty((num_elements, 3))
    for k in prange(num_elements):
        element = elements[k]

        integral = np.zeros(3)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk, 0] - local_coordinates[kk, 1], local_coordinates[kk, 0],
                                 local_coordinates[kk, 1]])
            integral = integral + weight * evaluations[k, kk] / np.sqrt(evaluation_points[k, kk, 0]) * m_values

        vec_elem = determinant_b[element] / 2 * integral
        idx_node = elem2node[element, :]

        i[k] = idx_node
        v[k] = vec_elem

    return i.flatten(), v.flatten()


# endregion


# region Functions load vector curl

@njit_cache(parallel=True)
def calc_load_vector_curl_vector(elements: np.ndarray,
                                 value: np.ndarray,
                                 b: np.ndarray,
                                 c: np.ndarray,
                                 s: np.ndarray,
                                 weights: np.ndarray,
                                 evaluation_points: np.ndarray,
                                 determinant_b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""Calculate the elements for the load vector curl if the load is a vector.

    The contribution of one element :math:`T` is

    .. math::

        x_j^T = \frac{\lvert B_t\rvert}{2d}\left(-c_jF_r\int_0^1\int_0^{1-\xi}\frac{1}{\sqrt{s(\xi,\eta)}}+b_jF_z\right)

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
        (E,) array. The indices of considered elements.
    value : np.ndarray
        (E,2) array. Vector with value of load for each element in elements. r and z coordinate.
    b : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    c : np.ndarray
        (T,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    s : np.ndarray
        (T,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    evaluation_points : np.ndarray
        (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriCartesianEdgeShapeFunction`.

    Returns
    -------
    i : np.ndarray
        (K,) array. Indices for sparse creation.
    v : np.ndarray
        (K,) array. Values for sparse creation.
    """
    num_elements = len(elements)

    i = np.empty((num_elements, 3), np.int32)
    v = np.empty((num_elements, 3))

    for k in prange(num_elements):
        element = elements[k]

        first_integral = -c[element] * value[k, 0] * np.dot(weights, 1 / np.sqrt(evaluation_points[k, :, 0]))
        second_integral = b[element] * value[k, 1]

        i[k] = np.arange(3 * element, 3 * element + 3, 1)
        v[k] = determinant_b[element] / (2 * s[element]) * (first_integral + second_integral)

    return i, v


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
        (E,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    c : np.ndarray
        (E,2) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.
    s : s : np.ndarray
        (E,) array. See the field in :py:class:`TriAxisymmetricEdgeShapeFunction`.

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


@njit_cache(parallel=True)
def calc_neumann_term_constant(edges: np.ndarray, value: Union[int, float], weights: np.ndarray,
                               local_coordinates: np.ndarray, node_transformed: np.ndarray, edge2node: np.ndarray) \
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
        (E,) array. Indices of the edges the face current is on.
    value : Union[int, float]
        The value of the face current.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
    node_transformed : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See variable `i_face` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See variable `v_face` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    """
    evaluation_points = calc_evaluation_points_edge(local_coordinates, node_transformed, edges, edge2node)
    num_edges = len(edges)

    i = np.empty((num_edges, 2))
    v = np.empty((num_edges, 2))
    for k in prange(num_edges):
        edge = edges[k]

        first_node = edge2node[edge, 0]
        second_node = edge2node[edge, 1]
        del_s = (node_transformed[second_node, 0] - node_transformed[first_node, 0]) ** 2
        del_z = (node_transformed[second_node, 1] - node_transformed[first_node, 1]) ** 2

        integral = np.zeros(2)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk], local_coordinates[kk]])
            integral = integral + weight * np.sqrt(del_s / (4 * evaluation_points[k, kk, 0]) + del_z) * m_values

        idx_node = edge2node[edge, :]

        i[k] = idx_node
        v[k] = value * integral

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_neumann_term_function(edges: np.ndarray, weights: np.ndarray, local_coordinates: np.ndarray,
                               evaluation_points: np.ndarray, evaluations: np.ndarray, node_transformed: np.ndarray,
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
    node_transformed : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See variable `i_face` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    v : np.ndarray
        (K,) array. See variable `v_face` in :py:func:`TriAxisymmetricEdgeShapeFunction.load_vector`.
    """
    num_edges = len(edges)

    i_local = np.empty((num_edges, 2))
    v_local = np.empty((num_edges, 2))
    for k in range(num_edges):
        edge = edges[k]

        first_node = edge2node[edge, 0]
        second_node = edge2node[edge, 1]
        del_s = (node_transformed[second_node, 0] - node_transformed[first_node, 0]) ** 2
        del_z = (node_transformed[second_node, 1] - node_transformed[first_node, 1]) ** 2

        integral = np.zeros(2)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk], local_coordinates[kk]])
            integral = integral + weight * evaluations[k, kk] * np.sqrt(
                del_s / (4 * evaluation_points[k, kk, 0]) + del_z) * m_values

        idx_node = edge2node[edge, :]

        i_local[k] = idx_node
        v_local[k] = integral

    return i_local.flatten(), v_local.flatten()


@njit_cache(parallel=True)
def calc_robin_term_constant(edges: np.ndarray, value: Union[int, float],
                             weights: np.ndarray, local_coordinates: np.ndarray,
                             node_transformed: np.ndarray, edge2node: np.ndarray) \
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
        The value of the face current.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.
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
    evaluation_points = calc_evaluation_points_edge(local_coordinates, node_transformed, edges, edge2node)
    num_edges = len(edges)

    i_local = np.zeros((num_edges, 4))
    j_local = np.zeros((num_edges, 4))
    v_local = np.zeros((num_edges, 4))
    for k in prange(num_edges):
        edge = edges[k]

        first_node = edge2node[edge, 0]
        second_node = edge2node[edge, 1]
        del_s = (node_transformed[second_node, 0] - node_transformed[first_node, 0]) ** 2
        del_z = (node_transformed[second_node, 1] - node_transformed[first_node, 1]) ** 2

        integral = np.zeros((2, 2))
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk], local_coordinates[kk]])
            integral = integral + weight * np.sqrt(del_s / (4 * evaluation_points[k, kk, 0]) + del_z) / np.sqrt(
                evaluation_points[k, kk, 0]) * np.outer(m_values, m_values)

        mat_elem = 1 / (2 * np.pi) * value * integral
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
                             node_transformed: np.ndarray, edge2node: np.ndarray)\
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

        first_node = edge2node[edge, 0]
        second_node = edge2node[edge, 1]
        del_s = (node_transformed[second_node, 0] - node_transformed[first_node, 0]) ** 2
        del_z = (node_transformed[second_node, 1] - node_transformed[first_node, 1]) ** 2

        integral = np.zeros((2, 2))
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk], local_coordinates[kk]])
            integral = integral + weight * evaluations[k, kk] * np.sqrt(
                del_s / (4 * evaluation_points[k, kk, 0]) + del_z) / np.sqrt(evaluation_points[k, kk, 0]) * np.outer(
                m_values, m_values)

        mat_elem = 1 / (2 * np.pi) * integral
        idx_node = edge2node[edge, :]

        tmp = np.stack((idx_node, idx_node))
        tmpt = np.column_stack((idx_node, idx_node))

        i_local[k] = np.reshape(tmp, (4,))
        j_local[k] = np.reshape(tmpt, (4,))
        v_local[k] = np.reshape(mat_elem, (4,))

    return i_local.flatten(), j_local.flatten(), v_local.flatten()


class TriAxisymmetricEdgeShapeFunction(EdgeShapeFunction):
    """Class representing shape functions in axisymmetric geometries with a triangular mesh in the rz-plane."""

    def __init__(self, mesh: 'AxiMesh'):
        """Constructor.

        Parameters
        ----------
        mesh : AxiMesh
            The mesh object.
        """
        super().__init__(None, dim=2, allocation_size=9 * mesh.num_elem)
        self._mesh: 'AxiMesh' = mesh
        self.__determinant_b = np.zeros(mesh.num_elem)
        self.__calc_coefficients()

    @property
    def mesh(self) -> 'AxiMesh':
        """Returns the mesh."""
        return self._mesh

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

        self.a = r2 ** 2 * z3 - r3 ** 2 * z2
        self.b = z2 - z3
        self.c = r3 ** 2 - r2 ** 2
        self.s = np.sum(r2 ** 2 * z3 - r3 ** 2 * z2, axis=1)

        s1 = self.mesh.node[self.mesh.elem2node[:, 0], 0] ** 2
        s2 = self.mesh.node[self.mesh.elem2node[:, 1], 0] ** 2
        s3 = self.mesh.node[self.mesh.elem2node[:, 2], 0] ** 2
        z1 = self.mesh.node[self.mesh.elem2node[:, 0], 1]
        z2 = self.mesh.node[self.mesh.elem2node[:, 1], 1]
        z3 = self.mesh.node[self.mesh.elem2node[:, 2], 1]
        self.p1_to_p2 = np.c_[s2 - s1, z2 - z1]
        self.p1_to_p3 = np.c_[s3 - s1, z3 - z1]
        # (elements,2,3) array. For every element there are the 3 coefficients for s and z
        self.transform_coefficcients = np.stack((self.p1_to_p2, self.p1_to_p3, np.c_[s1, z1]), axis=2)

        # Calculate the absolute value of the determinant of the transformation matrix for every element
        self.__determinant_b = np.abs(
            self.p1_to_p2[:, 0] * self.p1_to_p3[:, 1] - self.p1_to_p2[:, 1] * self.p1_to_p3[:, 0])

    def _calc_evaluation_points_element(self, local_coordinates: np.ndarray, indices: np.ndarray) -> np.ndarray:
        return calc_evaluation_points_element(local_coordinates, self.transform_coefficcients, indices)

    # region Calc matrix

    # region Calc matrix constant

    def _calc_matrix_constant_scalar(self, matrix_type: str, indices: np.ndarray, value: Union[Number, np.ndarray],
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            return calc_curlcurl_constant_scalar(indices, value, self.b, self.c,
                                                 self.transform_coefficcients, self.__determinant_b,
                                                 self.s, self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_constant_scalar(indices, value, weights, local_coordinates, self.transform_coefficcients,
                                             self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_constant_scalar is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_constant_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs)\
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_constant_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_constant_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, *args, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            evaluation_points = kwargs.pop("evaluation_points", None)
            if evaluation_points is None:
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

            return calc_curlcurl_constant_tensor(indices, weights, evaluation_points, value,
                                                 self.b, self.c, self.transform_coefficcients,
                                                 self.__determinant_b, self.s, self.mesh.elem2node)
        if matrix_type == "mass":
            raise ValueError("For axisymmetric edge functions it does not make sense to have an anisotropic "
                             "material property for the mass matrix.")

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix constant

    # region Calc matrix elementwise

    def _calc_matrix_elementwise_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            return calc_curlcurl_scalar_per_elem(indices, value, self.b, self.c,
                                                 self.transform_coefficcients, self.__determinant_b,
                                                 self.s, self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_scalar_per_elem(indices, value, weights, local_coordinates,
                                             self.transform_coefficcients, self.__determinant_b,
                                             self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_elementwise_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_constant_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_elementwise_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            evaluation_points = kwargs.pop("evaluation_points", None)
            if evaluation_points is None:
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

            return calc_curlcurl_tensor_per_elem(indices, weights, evaluation_points, value,
                                                 self.b, self.c, self.transform_coefficcients,
                                                 self.__determinant_b, self.s, self.mesh.elem2node)
        if matrix_type == "mass":
            raise ValueError("For axisymmetric edge functions it does not make sense to have an anisotropic "
                             "material property for the mass matrix.")

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix elementwise

    # region Calc matrix function

    def _calc_matrix_function_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        evaluation_points = kwargs.pop("evaluation_points", None)
        if evaluation_points is None:
            evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

        if matrix_type == "curlcurl":
            return calc_curlcurl_function_scalar(indices, weights, evaluation_points,
                                                 value, self.b, self.c, self.__determinant_b, self.s,
                                                 self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_function_scalar(indices, weights, local_coordinates, evaluation_points,
                                             value, self.__determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_function_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_constant_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_function_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        evaluation_points = kwargs.pop("evaluation_points", None)
        if evaluation_points is None:
            evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

        if matrix_type == "curlcurl":
            evaluation_points = calc_evaluation_points_element(local_coordinates, self.transform_coefficcients,
                                                               indices)
            return calc_curlcurl_function_tensor(indices, weights, evaluation_points, value,
                                                 self.b, self.c, self.__determinant_b, self.s, self.mesh.elem2node)
        if matrix_type == "mass":
            raise ValueError("For axisymmetric edge functions it does not make sense to have an anisotropic "
                             "material property for the mass matrix.")

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix function

    # endregion Calc matrix

    # region Calc vector

    # region Calc vector constant

    def _calc_vector_constant_scalar(self, vector_type: str, indices: np.ndarray, value: Number,
                                     weights: np.ndarray,
                                     local_coordinates: np.ndarray, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_constant_scalar(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load":
            evaluation_points = kwargs.pop("evaluation_points", None)
            if evaluation_points is None:
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

            return calc_load_constant(indices, value, weights, local_coordinates, evaluation_points,
                                      self.__determinant_b, self.mesh.elem2node)
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

        raise NotImplementedError

    # endregion Calc vector constant

    # region Calc vector elementwise

    def _calc_vector_elementwise_scalar(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_elementwise_scalar(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load":
            evaluation_points = kwargs.pop("evaluation_points", None)
            if evaluation_points is None:
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

            return calc_load_array(indices, value, weights, local_coordinates, evaluation_points,
                                   self.__determinant_b, self.mesh.elem2node)
        raise NotImplementedError(
            f"calc_vector_elementwise_scalar is not implemented for vector type: {vector_type}.")

    def _calc_vector_elementwise_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_elementwise_vector(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load_curl":
            evaluation_points = kwargs.pop("evaluation_points", None)
            if evaluation_points is None:
                evaluation_points = self._calc_evaluation_points_element(local_coordinates, indices)

            return calc_load_vector_curl_vector(indices, value, self.b, self.c, self.s, weights,
                                                evaluation_points, self.__determinant_b)
        raise NotImplementedError

    def _calc_vector_elementwise_tensor(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_elementwise_tensor(vector_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError

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

        raise NotImplementedError

    # endregion Calc vector function

    # endregion Calc vector

    def curlcurl_operator(self, *material: Union[NumericalData, MaterialData], **kwargs) -> coo_matrix:
        kwargs.setdefault("integration_order", 3)
        assembly_iterator = self._process_input(*material, **kwargs)
        return self._matrix_routine("curlcurl", assembly_iterator, evaluation_functions=evaluation_functions, **kwargs)

    def mass_matrix(self, *material: Union[NumericalData, MaterialData], **kwargs) -> coo_matrix:
        kwargs.setdefault("integration_order", 3)
        assembly_iterator = self._process_input(*material, **kwargs)
        return self._matrix_routine("mass", assembly_iterator, evaluation_functions=evaluation_functions, **kwargs)

    def load_vector(self, *load: Union[NumericalData, ExcitationData], **kwargs) -> coo_matrix:
        kwargs.setdefault("integration_order", 3)
        return super().load_vector(*load, evaluation_functions=evaluation_functions, **kwargs)

    def load_vector_curl(self, *load: Union[NumericalData, ExcitationData], **kwargs) -> coo_matrix:
        kwargs.setdefault("integration_order", 3)
        return super().load_vector_curl(*load, evaluation_functions=evaluation_functions, **kwargs)

    def curl(self, val2edge: ndarray) -> ndarray:
        return calc_curl(val2edge, self.mesh.node, self.mesh.elem2node, self.mesh.num_elem, self.b, self.c, self.s)

    # pylint: disable=line-too-long
    def neumann_term(self, *args: Union[Tuple['Regions', 'BdryCond'],
                                        Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[..., float]], ...],
                                                             Callable[..., Tuple[float]]]]],
                     integration_order: int = 3) -> coo_matrix:
        r"""Compute the Neumann term on a part of the boundary (see the notes).

        Parameters
        ----------
        args : Union[Tuple[Regions, BdryCond], Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[..., float]], ...], Callable[..., Tuple[float]]]]]
            The following possibilities are:

            - **Regions, BdyCond**: Will search for instances of BCNeumann in BdryCond and use the value of these.
              The value of the instances of BCNeumann needs two components that represent the tangential H field at the
              boundary. The first one is considered as the :math:`\rho`-component and the second one as the
              :math:`z`-component of the tangential H-field. If the value is a function, it has to return a (2,)
              ndarray. If it is not a function, is has to be a tuple with two entries.
            - **Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[..., float]], ...], Callable[..., Tuple[float]]]]**:
              The first argument is an array of shape (N,) and contains the indices of the boundary elements. The second
              argument is the value of :math:`\vec{g}` at these elements. Since the basis functions only have an
              :math:`\varphi`-component, the second argument also only contains the :math:`\varphi`-component, i.e. a
              tuple with one entry.
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

        weights, local_coordinates = gauss(integration_order)
        # i = np.zeros(2 * self.mesh.num_edge, dtype=np.int32)
        # v = np.zeros(2 * self.mesh.num_edge)

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

                evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node_transformed,
                                                                indices_edges, self.mesh.edge2node)

                if bc.is_homogeneous:
                    if bc.is_linear:
                        # homogenous, linear
                        if bc.is_time_dependent:  # homogeneous, linear, time dependent
                            value = bc.value()
                        else:  # homogeneous, linear, time independent
                            value = bc.value
                        if not isinstance(value, tuple) and len(value) == 2:
                            raise Exception("Type not supported")
                        evaluations = eval_neumann_hom_lin(indices_edges, value, self.mesh, weights)

                    # value is a constant
                    else:  # nonlinear
                        evaluations = eval_neumann_hom_lin(indices_edges, bc.value, self.mesh, weights)
                # homogenous, nonlinear
                else:  # inhomogeneous
                    if bc.is_linear:
                        # inhomogeneous, linear
                        evaluations = eval_neumann_inhom_lin(indices_edges, bc.value, self.mesh, weights,
                                                             evaluation_points)
                    else:  # nonlinear
                        # inhomogeneous, nonlinear
                        evaluations = eval_neumann_inhom_nonlin(indices_edges, bc.value, self.mesh, weights,
                                                                evaluation_points)
                # Change: evaluations.astype(float, copy=False)

                i_tmp, v_tmp = calc_neumann_term_function(indices_edges, weights, local_coordinates,
                                                          evaluation_points, evaluations, self.mesh.node_transformed,
                                                          self.mesh.edge2node)
                i.append(i_tmp)
                v.append(v_tmp)
            i = np.concatenate(i)
            v = np.concatenate(v)
        else:  # We have indices and value
            indices, value = args[0], args[1][0] if isinstance(args[1], Tuple) else args[1]
            evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node_transformed, indices,
                                                            self.mesh.edge2node)
            if flag_value == 'callable':
                x_test, y_test = self.mesh.node[self.mesh.edge2node[indices[0]][0]]
                # noinspection PyCallingNonCallable
                if isinstance(value(x_test, y_test), np.ndarray):
                    raise NotImplementedError

                evaluations = evaluate_for_num_int_edge(value, evaluation_points)

                i, v = calc_neumann_term_function(indices, weights, local_coordinates, evaluation_points, evaluations,
                                                  self.mesh.node_transformed, self.mesh.edge2node)
            elif flag_value == 'array':
                evaluations = np.outer(value, np.ones(len(weights)))
                # Change: evaluations.astype(float, copy=False)

                i, v = calc_neumann_term_function(indices, weights, local_coordinates, evaluation_points, evaluations,
                                                  self.mesh.node_transformed, self.mesh.edge2node)
            elif flag_value == 'value':
                i, v = calc_neumann_term_constant(indices, value, weights, local_coordinates,
                                                  self.mesh.node_transformed, self.mesh.edge2node)
        columns = np.zeros(len(i), dtype=int)
        neumann_vector = coo_matrix((v, (i, columns)), shape=(self.mesh.num_node, 1))
        return neumann_vector

    # pylint: disable=cell-var-from-loop,unnecessary-lambda-assignment
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

            if bc.is_homogenous_dirichlet and bc.is_homogeneous_neumann:
                if bc.is_linear_dirichlet and bc.is_linear_neumann:
                    # homogenous, linear
                    if bc.is_time_dependent_dirichlet:  # homogeneous, linear, time dependent
                        coef_dir = bc.coefficient_dirichlet()
                    else:  # homogeneous, linear, time independent
                        coef_dir = bc.coefficient_dirichlet
                    if bc.is_time_dependent_neumann:
                        coef_neum = bc.coefficient_neumann()
                    else:
                        coef_neum = bc.coefficient_neumann

                    if isinstance(coef_neum, ndarray) or isinstance(coef_dir, ndarray):
                        raise NotImplementedError

                    value = coef_dir / coef_neum
                    robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_constant(
                        indices_edges, value, weights, local_coordinates, self.mesh.node_transformed,
                        self.mesh.edge2node)
                # value is a constant
                else:  # nonlinear
                    raise NotImplementedError
            # homogenous, nonlinear
            else:  # inhomogeneous
                if bc.is_linear_dirichlet and bc.is_linear_neumann:
                    # inhomogeneous, linear
                    evaluation_points = calc_evaluation_points_edge(local_coordinates, self.mesh.node_transformed,
                                                                    indices_edges, self.mesh.edge2node)
                    if not bc.is_homogenous_dirichlet and not bc.is_homogeneous_neumann:
                        fun = lambda r, z: coef_dir(r, z) / coef_neum(r, z)
                    elif bc.is_homogenous_dirichlet and not bc.is_homogeneous_neumann:
                        if bc.is_time_dependent_dirichlet:
                            coef_dir = bc.coefficient_dirichlet()
                        else:
                            coef_dir = bc.coefficient_dirichlet
                        fun = lambda r, z: coef_dir / coef_neum(r, z)
                    elif not bc.is_homogenous_dirichlet and bc.is_homogeneous_neumann:
                        if bc.is_time_dependent_neumann:
                            coef_neum = bc.coefficient_neumann()
                        else:
                            coef_neum = bc.coefficient_neumann
                        fun = lambda r, z: coef_dir(r, z) / coef_neum
                    else:
                        raise Exception('Internal Error')

                    evaluations = evaluate_for_num_int_edge(fun, evaluation_points)
                    robin_lines_per_bc, robin_columns_per_bc, robin_values_per_bc = calc_robin_term_function(
                        indices_edges, weights, local_coordinates, evaluation_points, evaluations,
                        self.mesh.node_transformed, self.mesh.edge2node)
                else:  # nonlinear
                    # inhomogeneous, nonlinear
                    raise NotImplementedError
            values_list.append(robin_values_per_bc)
            lines_list.append(robin_lines_per_bc)
            columns_list.append(robin_columns_per_bc)

            value_bc = bc.value
            # Calculate the vector
            if bc.is_homogeneous_value and bc.is_homogeneous_neumann:
                if bc.is_linear_value and bc.is_linear_neumann:
                    # homogenous, linear
                    if bc.is_time_dependent_value:  # homogeneous, linear, time dependent
                        value = bc.value()
                    else:  # homogeneous, linear, time independent
                        value = bc.value
                    if bc.is_time_dependent_neumann:
                        coef_neum = bc.coefficient_neumann()
                    else:
                        coef_neum = bc.coefficient_neumann

                    if isinstance(coef_neum, ndarray) or isinstance(coef_dir, ndarray):
                        raise NotImplementedError
                    robin_vector = robin_vector + self.neumann_term(indices_edges, value / coef_neum,
                                                                    integration_order=integration_order)
                # value is a constant
                else:  # nonlinear
                    raise NotImplementedError
            # homogenous, nonlinear
            else:  # inhomogeneous
                if bc.is_linear_value and bc.is_linear_neumann:
                    # inhomogeneous, linear
                    if not bc.is_homogeneous_value and not bc.is_homogeneous_neumann:
                        fun = lambda r, z: value_bc(r, z) / coef_neum(r, z)
                    elif bc.is_homogeneous_value and not bc.is_homogeneous_neumann:
                        if bc.is_time_dependent_value:
                            value_bc = bc.value()
                        else:
                            value_bc = bc.value
                        fun = lambda r, z: value_bc / coef_neum(r, z)
                    else:
                        if bc.is_time_dependent_neumann:
                            coef_neum = bc.coefficient_neumann()
                        else:
                            coef_neum = bc.coefficient_neumann
                        fun = lambda r, z: value_bc(r, z) / coef_neum

                    robin_vector = robin_vector + self.neumann_term(indices_edges, fun,
                                                                    integration_order=integration_order)
                else:  # nonlinear
                    # inhomogeneous, nonlinear
                    raise NotImplementedError

        robin_matrix = coo_matrix(
            (np.concatenate(values_list), (np.concatenate(lines_list), np.concatenate(columns_list))),
            shape=(self.mesh.num_node, self.mesh.num_node))
        return robin_matrix, robin_vector.tocoo()

    def dirichlet_equations(self, regions: 'Regions', boundary_conditions: 'BdryCond') -> Tuple[coo_matrix, coo_matrix]:
        i, j, v, rhs = [], [], [], []
        max_line = 0
        for bc_key in boundary_conditions.get_ids():
            bc = boundary_conditions.get_bc(bc_key)
            if not isinstance(bc, BCDirichlet):
                continue

            # Calculate the matrix
            indices_regions = regions.find_regions_of_boundary_condition(bc.ID)
            indices_edges = np.empty(0)  # Indices of all edges that are on the boundary bc
            for region_id in indices_regions:
                indices_edges = np.r_[indices_edges, np.where(self.mesh.edge2regi == region_id)[0]]
            indices_edges = indices_edges.astype('int')

            i_bc = np.reshape(np.vstack((np.arange(max_line, max_line + len(indices_edges)),
                                         np.arange(max_line, max_line + len(indices_edges)))).T, (-1,)).astype(int)
            j_bc = np.empty(2 * len(indices_edges), dtype=int)
            v_bc = np.empty(2 * len(indices_edges))
            max_line += len(indices_edges)

            flag_bc_is_function = False
            if bc.is_constant:
                if isinstance(bc.value, (int, float, complex)):
                    rhs_bc = bc.value * np.ones((len(indices_edges), 1))
                elif isinstance(bc.value, np.ndarray):
                    if len(bc.value) != len(indices_edges):
                        raise ValueError("The vector of the boundary condition has not the right length.")
                    rhs_bc = np.array(bc.value, ndmin=2).T
                else:
                    raise NotImplementedError("The type of value of the boundary condition is not supported.")
            else:
                flag_bc_is_function = True
                rhs_bc = np.empty((len(indices_edges), 1))

            for k, edge in enumerate(indices_edges):
                element = self.mesh.edge2elem[edge][0]
                nodes = self.mesh.edge2node[edge]
                first_node_in_element = np.nonzero(self.mesh.elem2node[element] == nodes[0])[0][0]
                second_node_in_element = np.nonzero(self.mesh.elem2node[element] == nodes[1])[0][0]
                avg_radius = np.mean(self.mesh.node[nodes, 0])
                if avg_radius == 0:
                    raise Exception("There are no boundary conditions on the z axis allowed.")

                normal_vector = self.mesh.calc_normal_vector(edge)
                v_bc[2 * k] = 1 / (np.pi * self.s[element]) * np.dot(
                    [-self.c[element, first_node_in_element] / (2 * avg_radius),
                     self.b[element, first_node_in_element]], normal_vector)
                v_bc[2 * k + 1] = 1 / (np.pi * self.s[element]) * np.dot(
                    [-self.c[element, second_node_in_element] / (2 * avg_radius),
                     self.b[element, second_node_in_element]], normal_vector)
                j_bc[2 * k:2 * k + 2] = nodes

                if flag_bc_is_function:
                    if bc.is_homogeneous:
                        rhs_bc[k, 0] = bc.value()
                    else:
                        rhs_bc[k, 0] = bc.value(avg_radius, np.mean(self.mesh.node[nodes, 1]))

            i.append(i_bc)
            j.append(j_bc)
            v.append(v_bc)
            rhs.append(rhs_bc)
        vector = coo_matrix(np.concatenate(rhs))
        matrix = coo_matrix((np.concatenate(v), (np.concatenate(i), np.concatenate(j))),
                            shape=(vector.shape[0], self.mesh.num_node))

        return matrix, vector

    def voltage_distribution_function(self, regions: 'Regions', fcc: 'FieldCircuitCoupling') -> coo_matrix:
        keys = []  # All IDs of regions that have my fcc as excitation
        for key in regions.get_keys():
            regi = regions.get_regi(key)
            if regi.bc == fcc.ID:
                keys.append(key)
        elements = np.concatenate(
            [np.where(self.mesh.elem2regi == key)[0] for key in keys])  # all elements of fcc
        nodes = np.unique(self.mesh.elem2node[elements]).flatten()

        return coo_matrix((np.ones(len(nodes)), (nodes, np.zeros(len(nodes), dtype=int))),
                          shape=(self.mesh.num_node, 1))

    def current_distribution_function(self, regions: 'Regions', fcc: 'FieldCircuitCoupling') -> coo_matrix:
        keys = []  # All IDs of regions that have my fcc as excitation
        for key in regions.get_keys():
            regi = regions.get_regi(key)
            if regi.bc == fcc.ID:
                keys.append(key)
        elements = np.concatenate([np.where(self.mesh.elem2regi == key)[0] for key in keys])  # all elements of fcc
        nodes = np.unique(self.mesh.elem2node[elements]).flatten()

        area = np.sum(self.mesh.elem_area[elements])

        values = 1 / area * np.ones(len(nodes)) * 2 * np.pi * self.mesh.node[nodes, 0]
        return coo_matrix((values, (nodes, np.zeros(len(nodes), dtype=int))), shape=(self.mesh.num_node, 1))

    def _compute_data_dirichlet(self, dict_of_bc, groups, problem):
        values_all_nodes = []
        indices_all_nodes = []

        only_dirichlet = False
        if len(groups) == 1:
            # check if there are only dirichlet bcs
            for key, val in dict_of_bc.items():
                if key not in ("dirichlet", "conductor") and len(val) > 0:  # There exists a non-Dirichlet BC
                    break
            else:
                only_dirichlet = True

        nodes_on_axis = set(self.mesh.nodes_on_axis)
        covered_axis_indices = set()
        if only_dirichlet:
            # There must be two nodes in the list of nodes on the axis
            b_mat, b_vec = self.dirichlet_equations(problem.regions, problem.boundary_conditions)

            indices_for_a = np.unique(b_mat.col)

            intersection_nodes = nodes_on_axis.intersection(set(indices_for_a))
            if not len(intersection_nodes) == 2:
                raise Exception("An internal error occured")
            first_node_on_axis = intersection_nodes.pop()
            second_node_on_axis = intersection_nodes.pop()
            index_first_node_on_axis = np.where(indices_for_a == first_node_on_axis)[0]
            index_second_node_on_axis = np.where(indices_for_a == second_node_on_axis)[0]
            if not len(index_first_node_on_axis) == 1:
                raise Exception("An internal error occured")
            if not len(index_second_node_on_axis) == 1:
                raise Exception("An internal error occured")
            index_first_node_on_axis = index_first_node_on_axis[0]
            index_second_node_on_axis = index_second_node_on_axis[0]
            covered_axis_indices.update([first_node_on_axis, second_node_on_axis])

            b_mat: csr_matrix = b_mat.tocsr()
            b_mat = b_mat[:, b_mat.getnnz(0) > 0]
            b_mat.resize(b_mat.shape[0] - 1, b_mat.shape[1])  # remove one condition
            b_mat = vstack([b_mat, csr_matrix(([1, 1], ([0, 1], [index_first_node_on_axis,
                                                                 index_second_node_on_axis])),
                                              shape=(2, b_mat.shape[1]))])
            b_vec.resize(b_mat.shape[1], 1)
            a_on_bound = splinalg.spsolve(b_mat, b_vec)

            values_all_nodes.append(a_on_bound)
            indices_all_nodes.append(indices_for_a)
        else:
            for group in groups:
                tmp_boundary_condition = BdryCond(*[problem.boundary_conditions.get_bc(i) for i in group[0]])
                b_mat, b_vec = self.dirichlet_equations(problem.regions, tmp_boundary_condition)

                indices_for_a = np.unique(b_mat.col)

                intersection_nodes = nodes_on_axis.intersection(set(indices_for_a))
                if not len(intersection_nodes) < 2:
                    raise Exception("An internal error occured")
                if len(intersection_nodes) == 1:
                    node_on_axis = intersection_nodes.pop()
                    covered_axis_indices.update([node_on_axis, ])
                    index_node_on_axis = np.where(indices_for_a == node_on_axis)[0]
                    if not len(index_node_on_axis) == 1:
                        raise Exception("An internal error occured")
                    index_node_on_axis = index_node_on_axis[0]
                else:
                    index_node_on_axis = 0
                b_mat = b_mat.tocsr()
                b_mat = b_mat[:, b_mat.getnnz(0) > 0]
                b_mat = vstack([b_mat, csr_matrix(([1, ], ([0, ], [index_node_on_axis, ])), shape=(1, b_mat.shape[1]))])
                b_vec.resize(b_mat.shape[1], 1)
                a_on_bound = splinalg.spsolve(b_mat, b_vec)

                values_all_nodes.append(a_on_bound)
                indices_all_nodes.append(indices_for_a)

        remaining_axis_nodes = np.array(list(nodes_on_axis.difference(covered_axis_indices)))
        indices_all_nodes.append(remaining_axis_nodes)
        values_all_nodes.append(np.zeros(len(remaining_axis_nodes)))

        values_on_dirichlet = np.concatenate(values_all_nodes)
        indices_on_dirichlet = np.concatenate(indices_all_nodes)

        return indices_on_dirichlet, values_on_dirichlet

    def shrink(self, matrix: 'coo_matrix', rhs: 'coo_matrix', problem: 'ShrinkInflateProblemShapeFunction',
               integration_order: int = 1) -> Tuple['coo_matrix', 'coo_matrix', ndarray, int, Dict['str', Any]]:
        bc_by_type = problem.boundary_conditions.dict_of_boundary_condition()

        if bc_by_type['binary']:
            logger.warning("The boundary condition type 'binary' is not supported. It is going to be ignored.")

        if bc_by_type['floating']:
            logger.warning("The boundary condition type 'floating' is not supported. It is going to be ignored.")

        if bc_by_type['neumann']:
            rhs = self.shrink_neumann(rhs, problem, integration_order)

        if bc_by_type['robin']:
            matrix, rhs = self.shrink_robin(matrix, rhs, problem, integration_order)

        matrix, rhs, ind_on_dir, ind_not_on_dir, val_on_dir = self.shrink_dirichlet(matrix, rhs, problem, bc_by_type)

        support_data = {'indices_on_dirichlet': ind_on_dir,
                        'indices_not_on_dirichlet': ind_not_on_dir,
                        'values_on_dirichlet': val_on_dir}

        return matrix, rhs, ind_on_dir, 0, support_data

    def shrink_dirichlet(self, matrix: coo_matrix, rhs: coo_matrix, problem: 'ShrinkInflateProblemShapeFunction',
                         dict_of_bc: Dict[str, Any]) -> Tuple[coo_matrix, coo_matrix, ndarray, ndarray, ndarray]:
        edges_on_axis = self.mesh.edges_on_axis

        for edge in edges_on_axis:
            regi = self.mesh.edge2regi[edge]
            if regi != -1:
                if problem.regions.get_regi(regi).bc is not None:
                    logger.error("A boundary condition is defined on the axis. That is not allowed. Edge index: %d, "
                                 "Boundary condition index: %d", edge, problem.regions.get_regi(regi).bc)
                    raise ValueError("A boundary condition is defined on the axis. That is not allowed.")

        return super().shrink_dirichlet(matrix, rhs, problem, dict_of_bc)

    def inflate(self, solution: ndarray, problem: 'ShrinkInflateProblemShapeFunction',
                support_data: Dict[str, Any] = None) -> ndarray:
        bc_by_type = problem.boundary_conditions.dict_of_boundary_condition()
        if support_data:  # If support data is given, use its data
            required_keys = ['indices_on_dirichlet', 'indices_not_on_dirichlet', 'values_on_dirichlet']
            for key in required_keys:
                if key not in support_data.keys():
                    logger.warning("The given support data is incomplete. The key 'num_lagrange_mul' is missing. "
                                   "It will be computed.")
                    support_data = self.compute_support_data(bc_by_type, len(solution), problem)
        else:
            support_data = self.compute_support_data(bc_by_type, len(solution), problem)

        ind_on_dir = support_data['indices_on_dirichlet']
        ind_not_on_dir = support_data['indices_not_on_dirichlet']
        val_on_dir = support_data['values_on_dirichlet']
        solution_inflated = self.inflate_dirichlet(solution, ind_on_dir, val_on_dir, ind_not_on_dir)
        return solution_inflated

    def compute_support_data(self, dict_of_bc: Dict[str, Any], size_solution: int,
                             problem: 'ShrinkInflateProblemShapeFunction') -> Dict[str, Any]:
        groups = self._compute_groups_dirichlet(problem, dict_of_bc)
        indices_on_dirichlet, values_on_dirichlet = self._compute_data_dirichlet(dict_of_bc, groups, problem)
        indices_not_on_dirichlet = np.setdiff1d(np.arange(size_solution + len(indices_on_dirichlet)),
                                                indices_on_dirichlet)
        support_data = dict(indices_on_dirichlet=indices_on_dirichlet,
                            indices_not_on_dirichlet=indices_not_on_dirichlet,
                            values_on_dirichlet=values_on_dirichlet)
        return support_data
