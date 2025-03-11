# coding=utf-8
"""
File containing class TriCartesianEdgeShapeFunctions.

.. sectionauthor:: leissner
"""
import itertools
from typing import Union, Callable, Tuple, TYPE_CHECKING, NewType, Iterator
import numpy as np
from scipy.sparse import coo_matrix
from numba import prange

from pyrit.bdrycond import BCNeumann, BCDirichlet
from pyrit.shapefunction.EdgeShapeFunction import EdgeShapeFunction, NumericalData, MaterialData
from pyrit.toolbox.NumbaToolbox import njit_cache
from pyrit.toolbox.QuadratureToolbox import gauss
from pyrit import get_logger
from pyrit import ValueHandler

if TYPE_CHECKING:
    from pyrit.bdrycond import BdryCond
    from pyrit.excitation import Excitations, FieldCircuitCoupling, Exci
    from pyrit.mesh import TriMesh
    from pyrit.material import Materials, MatProperty
    from pyrit.region import Regions

Number = NewType('Number', Union[int, float, complex])
AssemblyIterator = NewType('AssemblyIterator', Iterator[Tuple[np.ndarray, ValueHandler, int]])

logger = get_logger(__name__)


# region General functions
@njit_cache(parallel=True)
def calc_evaluation_points_element(local_coordinates: np.ndarray,
                                   matrix_b: np.ndarray,
                                   offset: np.ndarray,
                                   elements: np.ndarray) -> np.ndarray:
    r"""
    Compute the coordinates at which a function needs to be evaluated if numerical integration is needed.

    Returns a three-dimensional array with the evaluation coordinates for all elements specified. The returned array is
    of dimensions (N,E,T) with [n,e,0] being the x coordinates and [n,e,1] being the y coordinates. Mathematically
    the transformation can be expressed as :math:`(x,\,y)^T  = \mathbf{B}\,(\hat{x},\,\hat{y})^T + offset`.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements
        T       Number of mesh elements
        ======  =======

    Parameters
    ----------
    local_coordinates : np.ndarray
        (N,2) array. x and y coordinates for each evaluation point.
    matrix_b : np.ndarray
        (T,2,2) array. Matrix that maps local coordinates to global coordinates.
    offset : np.ndarray
        (T,2) array. Offset transformation to global coordinates.
    elements : np.ndarray
        (E,) array. Array with indices of considered elements.

    Returns
    -------
    coord : np.ndarray
        (N,E,2) array.
    """
    coord = np.empty((len(elements), local_coordinates.shape[0], 2))
    for counter in prange(len(elements)):
        idx = elements[counter]
        coord[counter, :, :] = (matrix_b[idx] @ local_coordinates.T).T + offset[idx]
    return coord


@njit_cache(parallel=True)
def calc_evaluation_points_edge(local_coordinates: np.ndarray,
                                nodes: np.ndarray,
                                edges: np.ndarray,
                                edge2node: np.ndarray) -> np.ndarray:
    """
    Calculates the coordinates (x, y) needed for the evaluation of the numerical integration on an edge.

    Returns a three-dimensional array with the evaluation coordinates for all edges specified. The return values is
    a (E,N,2) array. It is `out[e,n,0]` and `out[e,n,1]` the x and < coordinate on edge e and evaluation point n,
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
    nodes : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.TriMesh`.
    edges : np.ndarray
        (E,) array. Array with the indices of edges the evaluation points are calculated for.
    edge2node : np.ndarray
        (T,2) array. See field in :py:class:`source.mesh.TriMesh`.

    Returns
    -------
    out : np.ndarray
        (E,N,2) array.
    """
    coords = np.empty((len(edges), len(local_coordinates), 2))

    for k in prange(len(edges)):
        edge = edges[k]
        first_node, second_node = nodes[edge2node[edge]]
        for kk, local_coord in enumerate(local_coordinates):
            coords[k, kk] = (second_node - first_node) * local_coord + first_node

    return coords


def check_integration_order(integration_order) -> None:
    """Typecheck for integration_order argument."""
    if not isinstance(integration_order, int):
        raise ValueError(f"integration order is of type {type(integration_order)} but has to be an int.")


def __eval_inhom_lin_iso_vectorized(fun: Callable[[float, float], float], evaluation_points: np.ndarray) -> np.ndarray:
    """Evaluate an inhomogeneous, linear and isotropic function using a vectorization."""
    return np.vectorize(fun)(evaluation_points[:, :, 0], evaluation_points[:, :, 1])


def __eval_inhom_lin_iso_loop(fun: Callable[[float, float], float], evaluation_points: np.ndarray) -> np.ndarray:
    """Evaluate a linear function for given evaluation points using a loop."""
    values = np.zeros((evaluation_points.shape[0], evaluation_points.shape[1]))
    for k in range(evaluation_points.shape[0]):
        values[k, :] = fun(evaluation_points[k, :, 0], evaluation_points[k, :, 1])
    return values


def eval_inhom_lin_iso(fun: Callable[[float, float], float], evaluation_points: np.ndarray) -> np.ndarray:
    """
    Evaluate an inhomogeneous, linear and isotropic function.

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
    try:
        return __eval_inhom_lin_iso_vectorized(fun, evaluation_points)
    except ValueError:
        pass
    return __eval_inhom_lin_iso_loop(fun, evaluation_points)


# endregion


# region Functions curlcurl_operator

def calc_curlcurl_constant_scalar(indices: np.ndarray,
                                  value: float,
                                  length: float,
                                  determinant_b: np.ndarray,
                                  inverse_b_transpose: np.ndarray,
                                  mesh_elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the elements of the curlcurl_matrix for a constant reluctivity.

    Parameters
    ----------
    indices : np.ndarray
        Indices of mesh elements.
    length : float
        Length in z-direction.
    value : float
        Reluctivity of the elements.
    determinant_b : np.ndarray
        Determinant of B-matrix.
    inverse_b_transpose : np.ndarray
        Inverse and transpose of B-matrix.
    mesh_elem2node : np.ndarray
        Indices of the nodes for each mesh element.

    Returns
    -------
    i : np.ndarray
        Row-Index-Vector for sparse creation.
    j : np.ndarray
        Column-Index-Vector for sparse creation.
    v : np.ndarray
        Value-Vector for sparse creation.
    """
    return calc_curlcurl_scalar_per_elem(indices, value * np.ones(len(indices), dtype=float), length, determinant_b,
                                         inverse_b_transpose, mesh_elem2node)


@njit_cache(parallel=True)
def calc_curlcurl_scalar_per_elem(indices: np.ndarray,
                                  value: np.ndarray,
                                  length: float,
                                  determinant_b: np.ndarray,
                                  inverse_b_transpose: np.ndarray,
                                  mesh_elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the elements of the curlcurl_matrix for a constant reluctivity.

    Parameters
    ----------
    indices : np.ndarray
        Indices of mesh elements.
    length : float
        Length in z-direction.
    value : np.ndarray
        Reluctivity of the elements.
    determinant_b : np.ndarray
        Determinant of B-matrix.
    inverse_b_transpose : np.ndarray
        Inverse and transpose of B-matrix.
    mesh_elem2node : np.ndarray
        Indices of the nodes for each mesh element.

    Returns
    -------
    i : np.ndarray
        Row-Index-Vector for sparse creation.
    j : np.ndarray
        Column-Index-Vector for sparse creation.
    v : np.ndarray
        Value-Vector for sparse creation.
    """
    grad_base = np.array([[-1, 1, 0], [-1, 0, 1]], dtype=np.float_)  # gradients of the base functions N1, N2, N3

    i = np.empty((9 * len(indices)), dtype=np.int_)
    j = np.empty_like(i, dtype=np.int_)
    v = np.empty_like(i, dtype=np.float_)

    for count in prange(len(indices)):  # iterate over each given mesh element
        idx = indices[count]
        b_inv_t_grad_base = inverse_b_transpose[idx] @ grad_base
        # compute a 3x3 matrix for each element: reluctivity is constant for a single mesh element
        # --> analytical integration over reference triangle gives factor 0.5
        integral = 0.5 / length * value[count] * determinant_b[idx] * (b_inv_t_grad_base.T @ b_inv_t_grad_base)
        idx_node = mesh_elem2node[idx, :]
        idx_ijv = np.arange(9 * count, 9 * count + 9)
        i[idx_ijv] = np.column_stack((idx_node, idx_node, idx_node)).flatten()
        j[idx_ijv] = np.hstack((idx_node, idx_node, idx_node))
        v[idx_ijv] = integral.flatten()

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=False)
def calc_curlcurl_function_scalar(indices: np.ndarray,
                                  weights: np.ndarray,
                                  evaluations: np.ndarray,
                                  length: float,
                                  determinant_b: np.ndarray,
                                  inverse_b_transpose: np.ndarray,
                                  mesh_elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the elements of the curlcurl matrix if the material (reluctivity) is a function.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points per element
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    indices : np.ndarray
        (E,) array. Indices of mesh elements.
    length : float
        Length in z-direction.
    evaluations : np.ndarray
        (E,N) array. Array with the evaluated values at all evaluation points.
    determinant_b : np.ndarray
        (E,) array. Determinant of B-matrix.
    inverse_b_transpose : np.ndarray
        (E,2,2) array. Inverse and transpose of B-matrix.
    mesh_elem2node : np.ndarray
        (E,3) array. Indices of the nodes for each mesh element.
    weights : np.ndarray
        (N,) array. Weights for numerical integration.

    Returns
    -------
    i : np.ndarray
        (E,) array. Row-Index-Vector for sparse creation.
    j : np.ndarray
        (E,) array. Column-Index-Vector for sparse creation.
    v : np.ndarray
        (E,) array. Value-Vector for sparse creation.
    """
    grad_base = np.array([[-1, 1, 0], [-1, 0, 1]], dtype=np.float_)  # gradients of the base functions N1, N2, N3

    i = np.empty((9 * len(indices)), dtype=np.int_)
    j = np.empty_like(i, dtype=np.int_)
    v = np.empty_like(i, dtype=np.float_)

    for count in prange(len(indices)):  # iterate over each given mesh element
        idx = indices[count]
        b_inv_t_grad_base = inverse_b_transpose[idx] @ grad_base

        constant = (1 / length) * determinant_b[idx] * (b_inv_t_grad_base.T @ b_inv_t_grad_base)
        integral = constant * (evaluations[count, :] * weights)

        idx_node = mesh_elem2node[idx, :]
        idx_ijv = np.arange(9 * count, 9 * count + 9)
        i[idx_ijv] = np.column_stack((idx_node, idx_node, idx_node)).flatten()
        j[idx_ijv] = np.hstack((idx_node, idx_node, idx_node))
        v[idx_ijv] = integral.flatten()

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_curlcurl_constant_tensor(indices: np.ndarray,
                                  value: np.ndarray,
                                  length: np.ndarray,
                                  determinant_b: np.ndarray,
                                  inverse_b_transpose: np.ndarray,
                                  mesh_elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the elements of the curlcurl_matrix for a constant reluctivity.

    Parameters
    ----------
    indices : np.ndarray
        Indices of mesh elements.
    length : float
        Length in z-direction.
    value : np.ndarray
        Reluctivity of the elements.
    determinant_b : np.ndarray
        Determinant of B-matrix.
    inverse_b_transpose : np.ndarray
        Inverse and transpose of B-matrix.
    mesh_elem2node : np.ndarray
        Indices of the nodes for each mesh element.

    Returns
    -------
    i : np.ndarray
        Row-Index-Vector for sparse creation.
    j : np.ndarray
        Column-Index-Vector for sparse creation.
    v : np.ndarray
        Value-Vector for sparse creation.
    """
    grad_base = np.array([[-1, 1, 0], [-1, 0, 1]], dtype=np.float_)  # gradients of the base functions N1, N2, N3

    i = np.empty((9 * len(indices)), dtype=np.int_)
    j = np.empty_like(i, dtype=np.int_)
    v = np.empty_like(i, dtype=np.float_)

    skew_matrix = np.array([[0, 1], [-1, 0]], dtype=np.float_)
    for count in prange(len(indices)):  # iterate over each given mesh element
        idx = indices[count]
        skew_b_inv_t_grad_base = skew_matrix @ inverse_b_transpose[idx] @ grad_base

        integral = 0.5 / length * determinant_b[idx] * skew_b_inv_t_grad_base.T @ value.T @ skew_b_inv_t_grad_base
        idx_node = mesh_elem2node[idx, :]
        idx_ijv = np.arange(9 * count, 9 * count + 9)
        i[idx_ijv] = np.column_stack((idx_node, idx_node, idx_node)).flatten()
        j[idx_ijv] = np.hstack((idx_node, idx_node, idx_node))
        v[idx_ijv] = integral.flatten()

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_curlcurl_tensor_per_elem(indices: np.ndarray,
                                  value: np.ndarray,
                                  length: np.ndarray,
                                  determinant_b: np.ndarray,
                                  inverse_b_transpose: np.ndarray,
                                  mesh_elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the elements of the curlcurl_matrix for a constant reluctivity.

    Parameters
    ----------
    indices : np.ndarray
        Indices of mesh elements.
    length : float
        Length in z-direction.
    value : np.ndarray
        Reluctivity of the elements.
    determinant_b : np.ndarray
        Determinant of B-matrix.
    inverse_b_transpose : np.ndarray
        Inverse and transpose of B-matrix.
    mesh_elem2node : np.ndarray
        Indices of the nodes for each mesh element.

    Returns
    -------
    i : np.ndarray
        Row-Index-Vector for sparse creation.
    j : np.ndarray
        Column-Index-Vector for sparse creation.
    v : np.ndarray
        Value-Vector for sparse creation.
    """
    grad_base = np.array([[-1, 1, 0], [-1, 0, 1]], dtype=np.float_)  # gradients of the base functions N1, N2, N3

    i = np.empty((9 * len(indices)), dtype=np.int_)
    j = np.empty_like(i, dtype=np.int_)
    v = np.empty_like(i, dtype=np.float_)

    skew_matrix = np.array([[0, 1], [-1, 0]], dtype=np.float_)
    for count in prange(len(indices)):  # iterate over each given mesh element
        idx = indices[count]
        skew_b_inv_t_grad_base = skew_matrix @ inverse_b_transpose[idx] @ grad_base

        integral = (0.5 / length * determinant_b[idx] *
                    skew_b_inv_t_grad_base.T @ value[count].T @ skew_b_inv_t_grad_base)
        idx_node = mesh_elem2node[idx, :]
        idx_ijv = np.arange(9 * count, 9 * count + 9)
        i[idx_ijv] = np.column_stack((idx_node, idx_node, idx_node)).flatten()
        j[idx_ijv] = np.hstack((idx_node, idx_node, idx_node))
        v[idx_ijv] = integral.flatten()

    return i.flatten(), j.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_curlcurl_function_tensor(indices: np.ndarray,
                                  weights: np.ndarray,
                                  evaluations: np.ndarray,
                                  length: np.ndarray,
                                  determinant_b: np.ndarray,
                                  inverse_b_transpose: np.ndarray,
                                  mesh_elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the elements of the curlcurl_matrix for a constant reluctivity.

    Parameters
    ----------
    indices : np.ndarray
        Indices of mesh elements.
    weights : np.ndarray
        (N,) array. Weights for numerical integration.
    evaluations : np.ndarray
        (E,N) array. Array with the evaluated values at all evaluation points.
    length : float
        Length in z-direction.
    determinant_b : np.ndarray
        Determinant of B-matrix.
    inverse_b_transpose : np.ndarray
        Inverse and transpose of B-matrix.
    mesh_elem2node : np.ndarray
        Indices of the nodes for each mesh element.

    Returns
    -------
    i : np.ndarray
        Row-Index-Vector for sparse creation.
    j : np.ndarray
        Column-Index-Vector for sparse creation.
    v : np.ndarray
        Value-Vector for sparse creation.
    """
    grad_base = np.array([[-1, 1, 0], [-1, 0, 1]], dtype=np.float_)  # gradients of the base functions N1, N2, N3

    i = np.empty((9 * len(indices)), dtype=np.int_)
    j = np.empty_like(i, dtype=np.int_)
    v = np.empty_like(i, dtype=np.float_)

    num_integration_points = len(weights)
    skew_matrix = np.array([[0, 1], [-1, 0]], dtype=np.float_)
    for count in prange(len(indices)):  # iterate over each given mesh element
        idx = indices[count]
        skew_b_inv_t_grad_base = skew_matrix @ inverse_b_transpose[idx] @ grad_base

        integral_value = np.zeros((2, 2), dtype=np.float_)
        for k in range(num_integration_points):
            integral_value += weights[k] * evaluations[count, k]
        integral = (1 / length * determinant_b[idx] *
                    skew_b_inv_t_grad_base.T @ integral_value.T @ skew_b_inv_t_grad_base)

        idx_node = mesh_elem2node[idx, :]
        idx_ijv = np.arange(9 * count, 9 * count + 9)
        i[idx_ijv] = np.column_stack((idx_node, idx_node, idx_node)).flatten()
        j[idx_ijv] = np.hstack((idx_node, idx_node, idx_node))
        v[idx_ijv] = integral.flatten()

    return i.flatten(), j.flatten(), v.flatten()


# endregion


# region Functions load_vector

@njit_cache(parallel=True)
def calc_load_constant(elements: np.ndarray,
                       value: Union[int, float],
                       determinant_b: np.ndarray,
                       elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Calculate the elements for the load vector if the load is constant.

    Calculates the contribution of the elements specified in `elements` to the load vector. The calculated values and
    line information are written to v and i, respectively. The integration is performed analytically. For a single mesh
    element the load for each node :math:`i` is calculated as follows:
    :math:`q_i = J \, \vert \mathrm{det} \, B \vert \, \int_{\hat{T}} \, \hat{N}_i \, \mathrm{d}\hat{A}` with the
    integration performed over the reference triangle. The integral
    :math:`\int_{\hat{T}} \, \hat{N}_i \, \mathrm{d}\hat{A}` gives :math:`(1/6, 1/6, 1/6)`.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 3T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of considered elements.
    value : Union[int, float]
        The value of the load.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriCartesianEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the field in :py:class:`source.mesh.TriMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. Indices for sparse creation.
    v : np.ndarray
        (K,) array. Values for sparse creation.
    """
    num_elements = len(elements)
    integral_ref_triangle = np.array([1 / 6, 1 / 6, 1 / 6])

    det_b = determinant_b[elements].reshape((num_elements, 1))

    v = value * det_b * integral_ref_triangle
    i = elem2node[elements, :]

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_load_array(elements: np.ndarray,
                    value: np.ndarray,
                    determinant_b: np.ndarray,
                    elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Calculate the elements for the load vector if the load is a vector.

    Calculates the contribution of the elements specified in `elements` to the load vector. The calculated values and
    line information are written to v and i, respectively. The integration is performed analytically. For a single mesh
    element the load for each node :math:`i` is calculated as follows:
    :math:`q_i = J \, \vert \mathrm{det} \, B \vert \, \int_{\hat{T}} \, \hat{N}_i \, \mathrm{d}\hat{A}` with the
    integration performed over the reference triangle. The integral
    :math:`\int_{\hat{T}} \, \hat{N}_i \, \mathrm{d}\hat{A}` gives :math:`(1/6, 1/6, 1/6)`. :math:`J` is constant for
    a single mesh element.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 3T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of considered elements.
    value : np.ndarray
        (E,) array. Vector with value of load for each element in elements.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriCartesianEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the field in :py:class:`source.mesh.TriMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. Indices for sparse creation.
    v : np.ndarray
        (K,) array. Values for sparse creation.
    """
    num_elements = len(elements)
    integral_ref_triangle = np.array([1 / 6, 1 / 6, 1 / 6])

    det_b = (determinant_b[elements] * value).reshape((num_elements, 1))

    v = det_b * integral_ref_triangle
    i = elem2node[elements, :]

    return i.flatten(), v.flatten()


@njit_cache(parallel=True)
def calc_load_function(elements: np.ndarray,
                       weights: np.ndarray,
                       local_coordinates: np.ndarray,
                       evaluations: np.ndarray,
                       determinant_b: np.ndarray,
                       elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Calculate the elements for the load vector if the load is a function.

    Calculates the contribution of the elements specified in `elements` to the load vector. The calculated values and
    line information are written to v and i, respectively. The integration is performed numerically.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        E       Number of elements in `elements`
        T       Number of elements in the mesh
        N       Number of evaluation points
        K       Size of i, j, v. Equal to 3T
        ======  =======

    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of the considered elements.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates within the reference triangle for each evaluation point (and weight, respectively)
    evaluations : np.ndarray
        (E,N) array. The load function evaluated for every evaluation point N and for every element E.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriCartesianEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the field in :py:class:`source.mesh.TriMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. Indices for sparse creation.
    v : np.ndarray
        (K,) array. Values for sparse creation.
    """
    num_elements = len(elements)

    v = np.empty((num_elements, 3), dtype=np.float_)
    i = elem2node[elements, :]

    for k in prange(num_elements):
        element = elements[k]
        integral = np.zeros(3)
        for kk, weight in enumerate(weights):
            m_values = np.array([1 - local_coordinates[kk, 0] - local_coordinates[kk, 1], local_coordinates[kk, 0],
                                 local_coordinates[kk, 1]])  # (1, 3) array. (N_1, N_2, N_3)
            integral += evaluations[k, kk] * weight * m_values  # (1, 3) array. (J*N_1, J*N_2, J*N_3) * weight
        v[k] = integral * determinant_b[element]

    return i.flatten(), v.flatten()


# endregion


# region Functions load vector curl

# @njit_cache(parallel=True)
def calc_load_vector_curl_vector(elements: np.ndarray,
                                 value: np.ndarray,
                                 length: float,
                                 determinant_b: np.ndarray,
                                 elem2node: np.ndarray,
                                 inverse_b_transpose: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""Calculate the elements for the load vector curl if the load is a vector.

    The contribution of one element :math:`T` is

    .. math::

        x_j^T = \frac{1}{\ell_z^2}\lvert\mathrm{det}\,B\rvert F(T)\cdot\left(\mathbf{B}^{-T} m_j\right)\mathrm{d}S\,.

    Herein, :math:`F(T)` represents the value on element :math:`T` and :math:`m_j` represents the curl of the edge
    shape functions. This is

    .. math::

        m_1 = [-1,1]^T\quad m_2 = [0, -1]^T\quad m_3 = [1 0]^T\,.


    Parameters
    ----------
    elements : np.ndarray
        (E,) array. The indices of considered elements.
    value : np.ndarray
        (E,2) array. Vector with value of the function for each element in elements. x and y component.
    length : float
        Length of the domain
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriCartesianEdgeShapeFunction`.
    inverse_b_transpose : np.ndarray
        (E,2,2) array. Inverse and transpose of B-matrix.

    Returns
    -------
    i : np.ndarray
        (K,) array. Indices for sparse creation.
    v : np.ndarray
        (K,) array. Values for sparse creation.
    """
    num_elements = len(elements)

    i = elem2node[elements, :]
    v = np.empty((num_elements, 3), dtype=value.dtype)

    m_global = np.array([[-1., 1., 0.], [-1., 0., 1.]], )
    matrix_s = np.array([[0., 1.], [-1., 0.]])
    for k in prange(num_elements):
        element = elements[k]
        v[k] = 0.5 * determinant_b[element] * value[k] @ matrix_s @ inverse_b_transpose[element] @ m_global

    return i.flatten(), v.flatten()


# endregion


# region curl_operator
@njit_cache(parallel=True)
def calc_curl(val2node: np.ndarray,
              elem2node: np.ndarray,
              inverse_b_transposed: np.ndarray,
              length: float) -> np.ndarray:
    """
    Calculate elements of the curl_operator.

    Parameters
    ----------
    val2node : np.ndarray
    elem2node : np.ndarray
    inverse_b_transposed : np.ndarray
    length : float

    Returns
    -------
    curl : np.ndarray
    """
    # num_elem = elem2node.shape[0]
    #
    # b = np.empty((num_elem, 3, 2))
    # b[:, 0, 0] = - inv_b_t[:, 1, 0] - inv_b_t[:, 1, 1]
    # b[:, 1, 0] = inv_b_t[:, 1, 0]
    # b[:, 2, 0] = inv_b_t[:, 1, 1]
    # b[:, 0, 1] = inv_b_t[:, 0, 0] + inv_b_t[:, 0, 1]
    # b[:, 1, 1] = - inv_b_t[:, 0, 0]
    # b[:, 2, 1] = - inv_b_t[:, 0, 1]
    #
    # curl = np.empty((num_elem, 2))  # only x and y components
    # for k in range(num_elem):
    #     a = val2node[elem2node[k, :]]
    #     curl[k, :] = a[np.newaxis, :] @ b[k, :, :]
    #
    # return curl / length
    num_elem = elem2node.shape[0]
    out = np.empty((num_elem, 2))

    permute = np.array([[0, 1], [-1, 0]], dtype=np.float_)
    grads = np.array([[[-1], [-1]], [[1], [0]], [[0], [1]]], dtype=np.float_)
    for elem in prange(num_elem):
        nodes = elem2node[elem]
        value = permute @ inverse_b_transposed[elem] @ (val2node[nodes[0]] * grads[0] + val2node[nodes[1]] * grads[1]
                                                        + val2node[nodes[2]] * grads[2])
        out[elem, :] = value.flatten()
    out = out / length
    return out


# endregion


# region mass_matrix

@njit_cache(parallel=True)
def calc_mass_constant_scalar(elements: np.ndarray,
                              value: float,
                              length: float,
                              determinant_b: np.ndarray,
                              elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    length : float
        Model length.
    value : Union[int, float]
        The value of the material.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriCartesianEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    """
    i = np.empty((9 * len(elements)), dtype=np.int_)
    j = np.empty_like(i, dtype=np.int_)
    v = np.empty_like(i, dtype=np.float_)

    for count in prange(len(elements)):  # iterate over each given mesh element
        idx = elements[count]
        integral = value * determinant_b[idx] / length / 24 * np.array([2, 1, 1, 1, 2, 1, 1, 1, 2])
        idx_node = elem2node[idx, :]
        idx_ijv = np.arange(9 * count, 9 * count + 9)
        i[idx_ijv] = np.column_stack((idx_node, idx_node, idx_node)).flatten()
        j[idx_ijv] = np.hstack((idx_node, idx_node, idx_node))
        v[idx_ijv] = integral.flatten()

    return i.flatten(), j.flatten(), v.flatten()


def calc_mass_scalar_per_elem(elements: np.ndarray,
                              value: np.ndarray,
                              length: float,
                              determinant_b: np.ndarray,
                              elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    length : float
        Model length.
    value : Union[int, float]
        The value of the material.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriCartesianEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    """
    if elements.shape != value.shape:
        raise ValueError(f"elements is of shape {elements.shape} and reluctivity is of shape {value.shape}.")

    det_b_new = value * determinant_b[elements]

    return calc_mass_constant_scalar(elements, 1, length, det_b_new, elem2node)


@njit_cache(parallel=True)
def calc_mass_function_scalar(elements: np.ndarray,
                              evaluations: np.ndarray,
                              length: float,
                              determinant_b: np.ndarray,
                              elem2node: np.ndarray,
                              weights: np.ndarray,
                              local_coordinates: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    length : float
        Model length.
    evaluations : np.ndarray
        (E,N) array. For every element the N evalutations of the material function at the evaluation points for the
        numerical integration. See :py:func:`evaluate_for_num_int_element`.
    determinant_b : np.ndarray
        (T,) array. See the field in :py:class:`TriCartesianEdgeShapeFunction`.
    elem2node : np.ndarray
        (T,3) array. See the filed in :py:class:`source.mesh.AxiMesh`.
    weights : np.ndarray
        (N,) array. The weights of the numerical integration.
    local_coordinates : np.ndarray
        (N,2) array. Two coordinates for each evaluation point.

    Returns
    -------
    i : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    j : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    v : np.ndarray
        (K,) array. See the variable in :py:func:`TriCartesianEdgeShapeFunction.mass_matrix`.
    """
    i = np.empty((9 * len(elements)), dtype=np.int_)
    j = np.empty_like(i, dtype=np.int_)
    v = np.empty_like(i, dtype=np.float_)

    for count in prange(len(elements)):  # iterate over each given mesh element
        idx = elements[count]
        integral = np.zeros(9)
        for kk, weight in enumerate(weights):
            x, y = local_coordinates[kk, :]
            matrix = np.array([(1 - x - y) ** 2, x * (1 - x - y), y * (1 - x - y), x * (1 - x - y), x ** 2, x * y,
                               y * (1 - x - y), x * y, y ** 2])
            integral += (evaluations[idx, kk] * weight) * matrix

        idx_node = elem2node[idx, :]
        idx_ijv = np.arange(9 * count, 9 * count + 9)
        i[idx_ijv] = np.column_stack((idx_node, idx_node, idx_node)).flatten()
        j[idx_ijv] = np.hstack((idx_node, idx_node, idx_node))
        v[idx_ijv] = determinant_b[idx] / length * integral

    return i.flatten(), j.flatten(), v.flatten()


# endregion


# region neumann_term
def calc_neumann_constant_array(edge_length: Union[float, np.ndarray],
                                value: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate the neumann term if the provided boundary condition is a constant or an array.

    Parameters
    ----------
    edge_length : np.ndarray
        (n,) array. Length of each edge belonging to the considered boundary.
    value : Union[float, np.ndarray]
        Either a constant value for the boundary or a value for each edge.

    Returns
    -------
    np.ndarray
        (n, 2) array. Values.
    """
    tmp = value * edge_length / 2
    return np.vstack((tmp, tmp)).T


def calc_neumann_term_function(evaluations: np.ndarray,
                               weights: np.ndarray,
                               local_coordinates: np.ndarray,
                               edge_lengths: np.ndarray) -> np.ndarray:
    """
    Calculate the neumann term if the provided boundary condition is a function.

    Parameters
    ----------
    evaluations : np.ndarray
        Function evaluated for the local_coordinates.
    weights : np.ndarray
        Weights for numerical integration.
    local_coordinates : np.ndarray
        Local coordinates for numerical integration.
    edge_lengths : np:ndarray
        Length of each edge belonging to the considered boundary.

    Returns
    -------
    values : np.ndarray
    """
    values = np.zeros((len(edge_lengths), 2))
    for k, edge_length in enumerate(edge_lengths):
        for kk, weight, local_coord in zip(itertools.count(), weights, local_coordinates):
            tmp_val = weight * evaluations[k, kk] * edge_length
            values[k, 0] += tmp_val * local_coord
            values[k, 1] += tmp_val * (1 - local_coord)
    return values


# endregion


class TriCartesianEdgeShapeFunction(EdgeShapeFunction):
    """Class representing edge-shape-functions in cartesian coordinates with a triangular mesh."""

    def __init__(self,
                 mesh: 'TriMesh',
                 length: float = 1):
        """
        Constructor.

        Parameters
        ----------
        mesh : TriMesh
            The mesh object.

        length : float
            Length in z-direction.
        """
        super().__init__(mesh, dim=2, allocation_size=9 * mesh.num_elem)
        self.matrix_b, self.determinant_b, self.inverse_b_transpose = self.__calc_transformation_matrices()
        self.length = length

    def __calc_transformation_matrices(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        x1 = self.mesh.node[self.mesh.elem2node, 0]
        y1 = self.mesh.node[self.mesh.elem2node, 1]
        x2 = np.roll(x1, -1, axis=1)
        y2 = np.roll(y1, -1, axis=1)
        x3 = np.roll(x1, -2, axis=1)
        y3 = np.roll(y1, -2, axis=1)
        # self.a = x2 * y3 - x3 * y2  # currently not needed
        self.b = y2 - y3
        self.c = x3 - x2
        self.s = np.sum(x2 * y3 - x3 * y2, axis=1)

        p1 = self.mesh.node[self.mesh.elem2node[:, 0]]
        p2 = self.mesh.node[self.mesh.elem2node[:, 1]]
        p3 = self.mesh.node[self.mesh.elem2node[:, 2]]
        p1_to_p2 = p2 - p1
        p1_to_p3 = p3 - p1
        matrix_b = np.empty((self.mesh.num_elem, 2, 2))
        matrix_b[:, :, 0] = p1_to_p2
        matrix_b[:, :, 1] = p1_to_p3
        determinant_b = np.abs(np.linalg.det(matrix_b))
        inverse_b_transpose = np.linalg.inv(np.transpose(matrix_b, axes=(0, 2, 1)))
        return matrix_b, determinant_b, inverse_b_transpose

    def _calc_evaluation_points_element(self, local_coordinates: np.ndarray, indices: np.ndarray) -> np.ndarray:
        return calc_evaluation_points_element(local_coordinates, self.matrix_b,
                                              self.mesh.node[self.mesh.elem2node[:, 0]], indices)

    # region Calc matrix

    # region Calc matrix constant

    def _calc_matrix_constant_scalar(self,
                                     matrix_type: str,
                                     indices: np.ndarray,
                                     value: Number,
                                     weights: np.ndarray,
                                     local_coordinates: np.ndarray,
                                     **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            return calc_curlcurl_constant_scalar(indices,
                                                 value,
                                                 self.length,
                                                 self.determinant_b,
                                                 self.inverse_b_transpose,
                                                 self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_constant_scalar(indices,
                                             value,
                                             self.length,
                                             self.determinant_b,
                                             self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_constant_scalar is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_constant_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_constant_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_constant_tensor(self,
                                     matrix_type: str,
                                     indices: np.ndarray,
                                     value: np.ndarray,
                                     weights: np.ndarray,
                                     local_coordinates: np.ndarray,
                                     **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            return calc_curlcurl_constant_tensor(indices,
                                                 value,
                                                 self.length,
                                                 self.determinant_b,
                                                 self.inverse_b_transpose,
                                                 self.mesh.elem2node)

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix constant

    # region Calc matrix elementwise

    def _calc_matrix_elementwise_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            return calc_curlcurl_scalar_per_elem(indices,
                                                 value,
                                                 self.length,
                                                 self.determinant_b,
                                                 self.inverse_b_transpose,
                                                 self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_scalar_per_elem(indices,
                                             value,
                                             self.length,
                                             self.determinant_b,
                                             self.mesh.elem2node)

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

        if matrix_type == "curlcurl":
            return calc_curlcurl_tensor_per_elem(indices,
                                                 value,
                                                 self.length,
                                                 self.determinant_b,
                                                 self.inverse_b_transpose,
                                                 self.mesh.elem2node)
        raise NotImplementedError(f"calc_matrix_tensor_per_elem is not implemented for matrix type: {matrix_type}.")

    # endregion Calc matrix elementwise

    # region Calc matrix function

    def _calc_matrix_function_scalar(self,
                                     matrix_type: str,
                                     indices: np.ndarray,
                                     value: np.ndarray,
                                     weights: np.ndarray,
                                     local_coordinates: np.ndarray,
                                     **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            return calc_curlcurl_function_scalar(indices,
                                                 weights,
                                                 value,
                                                 self.length,
                                                 self.determinant_b,
                                                 self.inverse_b_transpose,
                                                 self.mesh.elem2node)
        if matrix_type == "mass":
            return calc_mass_function_scalar(indices,
                                             value,
                                             self.length,
                                             self.determinant_b,
                                             self.mesh.elem2node,
                                             weights,
                                             local_coordinates)

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_function_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_constant_tensor is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_function_tensor(self,
                                     matrix_type: str,
                                     indices: np.ndarray,
                                     value: np.ndarray,
                                     weights: np.ndarray,
                                     local_coordinates: np.ndarray,
                                     **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "curlcurl":
            return calc_curlcurl_function_tensor(indices,
                                                 weights,
                                                 value,
                                                 self.length,
                                                 self.determinant_b,
                                                 self.inverse_b_transpose,
                                                 self.mesh.elem2node)

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
            return calc_load_constant(indices, value, self.determinant_b, self.mesh.elem2node)

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
            return calc_load_array(indices, value, self.determinant_b, self.mesh.elem2node)

        raise NotImplementedError(f"calc_vector_elementwise_scalar is not implemented for vector type: {vector_type}.")

    def _calc_vector_elementwise_vector(self, vector_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_elementwise_vector(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load_curl":
            return calc_load_vector_curl_vector(indices, value, self.length, self.determinant_b, self.mesh.elem2node,
                                                self.inverse_b_transpose)

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
            return calc_load_function(indices, weights, local_coordinates, value, self.determinant_b,
                                      self.mesh.elem2node)

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

    def curlcurl_operator(self, *material: Union[NumericalData, MaterialData], **kwargs) -> coo_matrix:
        assembly_iterator = self._process_input(*material, **kwargs)
        return self._matrix_routine("curlcurl", assembly_iterator, **kwargs)

    def mass_matrix(self, *material: Union[NumericalData, MaterialData], **kwargs) -> coo_matrix:
        assembly_iterator = self._process_input(*material, **kwargs)
        return self._matrix_routine("mass", assembly_iterator, **kwargs)

    def curl(self, val2edge: np.ndarray) -> np.ndarray:
        return calc_curl(val2edge, self.mesh.elem2node, self.inverse_b_transpose, self.length)

    def _calc_neumann_term_inhom_lin_iso(self,
                                         indices_edges: np.ndarray,
                                         value: Callable,
                                         integration_order: int) -> np.ndarray:
        weights, local_coords = gauss(integration_order)
        eval_points = calc_evaluation_points_edge(local_coords,
                                                  self.mesh.node,
                                                  indices_edges,
                                                  self.mesh.edge2node)
        evals = eval_inhom_lin_iso(value, eval_points)
        return calc_neumann_term_function(evals,
                                          weights,
                                          local_coords,
                                          self.mesh.edge_length[indices_edges])

    def neumann_term(self, *args: Union[Tuple['Regions', 'BdryCond'],
                                        Tuple[np.ndarray,
                                              Union[Tuple[Union[float, np.ndarray, Callable[..., float]], ...],
                                                    Callable[..., Tuple[float]]]]],
                     integration_order: int = 1) -> coo_matrix:
        flag_regions, flag_value = self._process_neumann(*args)
        if flag_regions:
            regions, boundary_conditions = args
            indices_nodes = np.array([])
            values = np.array([])

            for key in boundary_conditions.get_ids():
                bc = boundary_conditions.get_bc(key)
                if not isinstance(bc, BCNeumann):
                    continue
                indices_regions = regions.find_regions_of_boundary_condition(bc.ID)
                indices_edges = [np.where(self.mesh.edge2regi == regi)[0] for regi in indices_regions][0].astype('int')

                if bc.is_homogeneous:
                    if bc.is_linear:  # homogeneous, linear
                        if bc.is_time_dependent:  # homogeneous, linear, time dependent
                            raise NotImplementedError
                        # bc.is_constant: homogeneous, linear, time independent
                        edge_values = calc_neumann_constant_array(self.mesh.edge_length[indices_edges], bc.value)
                    else:  # homogeneous, nonlinear
                        raise NotImplementedError
                else:  # inhomogeneous
                    if bc.is_linear:  # inhomogeneous, linear
                        edge_values = self._calc_neumann_term_inhom_lin_iso(indices_edges,
                                                                            bc.value,
                                                                            integration_order)
                    else:  # inhomogeneous, nonlinear
                        raise NotImplementedError
                indices_nodes = np.hstack((indices_nodes, self.mesh.edge2node[indices_edges, :].flatten()))
                values = np.hstack((values, edge_values.flatten()))

        else:
            indices_edges: np.ndarray = args[0]
            value: Union[Callable, np.ndarray, float] = args[1]

            if flag_value == "callable":
                weights, local_coords = gauss(integration_order)
                eval_points = calc_evaluation_points_edge(local_coords,
                                                          self.mesh.node,
                                                          indices_edges,
                                                          self.mesh.edge2node)
                evals = eval_inhom_lin_iso(value, eval_points)
                edge_values = calc_neumann_term_function(evals,
                                                         weights,
                                                         local_coords,
                                                         self.mesh.edge_length[indices_edges])
            elif flag_value in ("array", "value"):
                edge_values = calc_neumann_constant_array(self.mesh.edge_length[indices_edges], value)
            else:
                raise ValueError(f"flag_value: {flag_value} is unknown")
            indices_nodes = self.mesh.edge2node[indices_edges, :].flatten()
            values = edge_values.flatten()
        return coo_matrix((values, (indices_nodes, np.zeros_like(indices_nodes, dtype=int))),
                          shape=(self.mesh.num_node, 1))

    def robin_terms(self,
                    regions: 'Regions',
                    boundary_condition: 'BdryCond',
                    integration_order: int = 1) -> Tuple[coo_matrix, coo_matrix]:
        raise NotImplementedError("The robin_terms method in class TriCartesianEdgeShapeFunction is not implemented.")

    def __fcc2elements_nodes(self,
                             regions: 'Regions',
                             fcc: 'FieldCircuitCoupling') -> Tuple[np.ndarray, np.ndarray]:
        """Get the elements and nodes belonging to a FieldCircuitCoupling object."""
        keys = []  # All IDs of regions having my fcc as excitation
        for key in regions.get_keys():
            regi = regions.get_regi(key)
            if regi.bc == fcc.ID:
                keys.append(key)
        elements = np.concatenate([np.where(self.mesh.elem2regi == key)[0] for key in keys])  # all elements of fcc
        nodes = np.unique(self.mesh.elem2node[elements]).flatten()
        return elements, nodes

    def current_distribution_function(self,
                                      regions: 'Regions',
                                      fcc: 'FieldCircuitCoupling') -> coo_matrix:
        elements, nodes = self.__fcc2elements_nodes(regions, fcc)

        area = np.sum(self.mesh.elem_area[elements])

        values = 1 / area * np.ones(len(nodes))
        return coo_matrix((values, (nodes, np.zeros(len(nodes), dtype=int))), shape=(self.mesh.num_node, 1))

    def dirichlet_equations(self,
                            regions: 'Regions',
                            boundary_conditions: 'BdryCond') -> Tuple[coo_matrix, coo_matrix]:
        i, j, v, rhs = [], [], [], []
        max_line = 0
        for bc_key in boundary_conditions.get_ids():
            bc = boundary_conditions.get_bc(bc_key)
            if not isinstance(bc, BCDirichlet):
                continue

            indices_regions = regions.find_regions_of_boundary_condition(bc.ID)
            indices_edges = np.array([])
            for region_id in indices_regions:
                indices_edges = np.hstack((indices_edges, np.where(self.mesh.edge2regi == region_id)[0]))
            indices_edges = indices_edges.astype('int')

            i_bc = np.c_[np.arange(max_line, max_line + len(indices_edges)),
                         np.arange(max_line, max_line + len(indices_edges))].flatten()
            j_bc = np.empty(2 * len(indices_edges), dtype=int)
            v_bc = np.empty(2 * len(indices_edges))
            max_line += len(indices_edges)

            if bc.is_constant:
                if isinstance(bc.value, (int, float, complex)):
                    rhs_bc = bc.value * np.ones((len(indices_edges), 1))
                elif isinstance(bc.value, np.ndarray):
                    if len(bc.value) != len(indices_edges):
                        raise ValueError("The vector of the boundary condition has not the right length.")
                    rhs_bc = np.array(bc.value, ndmin=2).T
                else:
                    raise NotImplementedError("The type of value of the boundary condition is not supported.")
            else:  # boundary conditions is a function
                weights, local_coordinates = gauss(1)
                eval_points = calc_evaluation_points_edge(local_coordinates,
                                                          self.mesh.node,
                                                          indices_edges,
                                                          self.mesh.edge2node)
                evaluations = eval_inhom_lin_iso(bc.value, eval_points)
                rhs_bc = (evaluations @ np.atleast_2d(weights).T)

            for k, edge in enumerate(indices_edges):
                element = self.mesh.edge2elem[edge][0]
                nodes = self.mesh.edge2node[edge]
                first_node_in_element = np.nonzero(self.mesh.elem2node[element] == nodes[0])[0][0]
                second_node_in_element = np.nonzero(self.mesh.elem2node[element] == nodes[1])[0][0]

                normal_vector = self.mesh.calc_normal_vector(edge)
                v_bc[2 * k] = 1 / (self.s[element] * self.length) * np.dot(
                    [self.c[element, first_node_in_element], -self.b[element, first_node_in_element]], normal_vector)
                v_bc[2 * k + 1] = 1 / (self.s[element] * self.length) * np.dot(
                    [self.c[element, second_node_in_element], -self.b[element, second_node_in_element]], normal_vector)
                j_bc[2 * k:2 * k + 2] = nodes

            i.append(i_bc)
            j.append(j_bc)
            v.append(v_bc)
            rhs.append(rhs_bc)

        vector = coo_matrix(np.concatenate(rhs))
        matrix = coo_matrix((np.concatenate(v).flatten(), (np.concatenate(i), np.concatenate(j))),
                            shape=(vector.shape[0], self.mesh.num_node))
        return matrix, vector

    def voltage_distribution_function(self,
                                      regions: 'Regions',
                                      fcc: 'FieldCircuitCoupling') -> coo_matrix:
        _, nodes = self.__fcc2elements_nodes(regions, fcc)

        return coo_matrix((np.ones(len(nodes)), (nodes, np.zeros(len(nodes), dtype=int))),
                          shape=(self.mesh.num_node, 1))
