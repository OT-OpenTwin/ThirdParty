# coding=utf-8
"""
Created on 21 June 2021

File containing the class TetCartesianNodalShapeFunction

.. sectionauthor:: christ
"""
from inspect import signature
from typing import Union, Callable, Tuple

import numpy as np
from scipy.sparse import coo_matrix
from numba import prange

from pyrit.bdrycond import BdryCond, BCNeumann, BCRobin
from pyrit.toolbox.NumbaToolbox import njit_cache
from pyrit.mesh import TetMesh
from pyrit.region import Regions
from pyrit.toolbox import QuadratureToolbox

from .ShapeFunction import Number, MaterialData, NumericalData
from .NodalShapeFunction import NodalShapeFunction


# region Functions for evaluation

@njit_cache(parallel=True)
def calc_evaluation_points_element(local_coordinates: np.ndarray, element_indices: np.ndarray,
                                   transformation_matrices: np.ndarray,
                                   transformation_vectors: np.ndarray) -> np.ndarray:
    """Calculate evaluation points on elements for given local coordinates.

    The local cooridnates are given on a reference element :math:`T`. This function calculates the corresponding
    evaluation points on elements :math:`t` in the mesh. The element :math:`t` is th image of the affine transformation
    defined by the transformation matrices and transformation vectors, with the reference element :math:`T` as domain.
    There is one transformation for each element :math:`t`.

    Parameters
    ----------
    local_coordinates : np.ndarray
        (N,3) array. Local coordinates on the reference element :math:`T`. N local points with 3 coordinates each.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    transformation_matrices : np.ndarray
        (X,3,3) array. Transformation matrix for each element :math:`t`.
    transformation_vectors : np.ndarray
        (X,3) array. Translation vector for each element :math:`t`.

    Returns
    -------
    evaluation_points : np.ndarray
        (E, N, 3) array. Evaluation points on each element :math:`t` for each local coordinate.
    """
    evaluation_points = np.empty((element_indices.shape[0], local_coordinates.shape[0], 3),
                                 dtype=np.float_)

    for index in prange(element_indices.shape[0]):
        element = element_indices[index]
        evaluation_points[index] = local_coordinates @ transformation_matrices[element].T + \
                                     transformation_vectors[element]
    return evaluation_points


# endregion


@njit_cache()
def gradient_nodal_basis() -> np.ndarray:
    """Returns an array with the gradients of the nodal basis functions.

    Returns
    -------
    gradient_nodal_basis : np.ndarray
        (4,3) array. Gradient of the nodal basis functions.
    """
    return np.array([[-1, -1, -1], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float_)


@njit_cache
def evaluate_nodal_basis_functions(evaluation_points: np.ndarray) -> np.ndarray:
    """Evaluate nodal basis functions at given evaluation points.

    Parameters
    ----------
    evaluation_points : np.ndarray
        (N,3) array. Evaluation points for the numerical integration on the reference element.

    Returns
    -------
    nodal_basis_functions : np.ndarray
        (4,N) array. Nodal basis functions evaluated at the evaluation points.
    """
    evaluations = np.empty((4, evaluation_points.shape[0]), dtype=np.float_)

    for k in range(evaluation_points.shape[0]):
        evaluations[0, k] = 1 - np.sum(evaluation_points[k])
        evaluations[1, k] = evaluation_points[k, 0]
        evaluations[2, k] = evaluation_points[k, 1]
        evaluations[3, k] = evaluation_points[k, 2]

    return evaluations


@njit_cache
def multiplication_nodal_basis_over_reference():
    """Returns the integral of the multiplication of two nodal basis functions over the reference element.

    Returns
    -------
    multiplication_nodal_basis_over_reference : np.ndarray
        (4,4) array. Integral of the multiplication of two nodal basis functions over the reference element.
    """
    return 1 / 120 * np.array([[2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 2, 1], [1, 1, 1, 2]])


@njit_cache
def nodal_basis_over_reference():
    """Returns the integral of a nodal basis function over the reference element.

    Returns
    -------
    nodal_basis_over_reference : np.ndarray
        (4,) array. Integral of a nodal basis function over the reference element.
    """
    return 1 / 24 * np.array([1, 1, 1, 1], dtype=np.float_)


# region Calc divgrad matrices

@njit_cache(parallel=True)
def calc_divgrad_function_tensor(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                                 weights: np.ndarray,
                                 abs_determinant_transformation_matrix: np.ndarray,
                                 inverse_transpose_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the divgrad matrix for a space dependent tensor.

    Parameters
    ----------
    values : np.ndarray
        (E, N, 3, 3) array. Values of the tensor for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    weights : np.ndarray
        (N,) array. Weights for numerical integration.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.
    inverse_transpose_transformation_matrix : np.ndarray
        (X, 3, 3) array. Inverse and transpose of the transformation matrix for all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    grad_nodal_basis = gradient_nodal_basis()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        integral_value = np.sum(weights[:, np.newaxis, np.newaxis] * values[element], axis=0)

        value[element] = abs_determinant_transformation_matrix[element_index] * grad_nodal_basis @ \
                         inverse_transpose_transformation_matrix[element_index].T @ integral_value.T @ \
                         inverse_transpose_transformation_matrix[element_index] @ grad_nodal_basis.T

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_divgrad_constant_tensor(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                                 abs_determinant_transformation_matrix: np.ndarray,
                                 inverse_transpose_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the divgrad matrix for a constant tensor.

    Parameters
    ----------
    values : np.ndarray
        (3, 3) array. Values of the tensor for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.
    inverse_transpose_transformation_matrix : np.ndarray
        (X, 3, 3) array. Inverse and transpose of the transformation matrix for all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    grad_nodal_basis = gradient_nodal_basis()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        value[element] = 1 / 6 * abs_determinant_transformation_matrix[element_index] * grad_nodal_basis @ \
                         inverse_transpose_transformation_matrix[element_index].T @ values.T @ \
                         inverse_transpose_transformation_matrix[element_index] @ grad_nodal_basis.T

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_divgrad_elementwise_tensor(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                                    abs_determinant_transformation_matrix: np.ndarray,
                                    inverse_transpose_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the divgrad matrix for an elementwise tensor.

    Parameters
    ----------
    values : np.ndarray
        (E, 3, 3) array. Values of the tensor for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.
    inverse_transpose_transformation_matrix : np.ndarray
        (X, 3, 3) array. Inverse and transpose of the transformation matrix for all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    grad_nodal_basis = gradient_nodal_basis()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        value[element] = 1 / 6 * abs_determinant_transformation_matrix[element_index] * grad_nodal_basis @ \
                         inverse_transpose_transformation_matrix[element_index].T @ values[element].T @ \
                         inverse_transpose_transformation_matrix[element_index] @ grad_nodal_basis.T

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_divgrad_function_scalar(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                                 weights: np.ndarray,
                                 abs_determinant_transformation_matrix: np.ndarray,
                                 inverse_transpose_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the divgrad matrix for a space dependent scalar.

    Parameters
    ----------
    values : np.ndarray
        (E, N) array. Values of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    weights : np.ndarray
        (N,) array. Weights for numerical integration.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.
    inverse_transpose_transformation_matrix : np.ndarray
        (X, 3, 3) array. Inverse and transpose of the transformation matrix for all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    grad_nodal_basis = gradient_nodal_basis()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        integral_value = np.sum(weights * values[element])

        value[element] = abs_determinant_transformation_matrix[element_index] * integral_value * grad_nodal_basis @ \
                         inverse_transpose_transformation_matrix[element_index].T @ \
                         inverse_transpose_transformation_matrix[element_index] @ grad_nodal_basis.T

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_divgrad_constant_scalar(values: Number, element_indices: np.ndarray, elem2node: np.ndarray,
                                 abs_determinant_transformation_matrix: np.ndarray,
                                 inverse_transpose_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the divgrad matrix for a constant scalar.

    Parameters
    ----------
    values : Number
        Value of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.
    inverse_transpose_transformation_matrix : np.ndarray
        (X, 3, 3) array. Inverse and transpose of the transformation matrix for all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    grad_nodal_basis = gradient_nodal_basis()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        value[element] = 1 / 6 * abs_determinant_transformation_matrix[element_index] * values * grad_nodal_basis @ \
                         inverse_transpose_transformation_matrix[element_index].T @ \
                         inverse_transpose_transformation_matrix[element_index] @ grad_nodal_basis.T

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_divgrad_elementwise_scalar(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                                    abs_determinant_transformation_matrix: np.ndarray,
                                    inverse_transpose_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the divgrad matrix for an elementwise scalar.

    Parameters
    ----------
    values : np.ndarray
        (E,) array. Values of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.
    inverse_transpose_transformation_matrix : np.ndarray
        (X, 3, 3) array. Inverse and transpose of the transformation matrix for all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    grad_nodal_basis = gradient_nodal_basis()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        value[element] = (1 / 6 * abs_determinant_transformation_matrix[element_index] * values[element] *
                          grad_nodal_basis @ inverse_transpose_transformation_matrix[element_index].T @
                          inverse_transpose_transformation_matrix[element_index] @ grad_nodal_basis.T)

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


# endregion Calc divgrad matrices


# region Calc mass matrix

@njit_cache(parallel=True)
def calc_mass_function_scalar(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                              weights: np.ndarray, local_coordinates: np.ndarray,
                              abs_determinant_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the mass matrix for a space dependent scalar.

    Parameters
    ----------
    values : np.ndarray
        (E, N) array. Values of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    weights : np.ndarray
        (N,) array. Weights for numerical integration.
    local_coordinates : np.ndarray
        (N,3) array. Evaluation points for the numerical integration on the reference element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    num_elements = len(element_indices)
    num_integration_points = len(weights)
    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    evaluations_nodal_basis = evaluate_nodal_basis_functions(local_coordinates)
    evaluations_multiplication = np.empty((local_coordinates.shape[0], 4, 4), dtype=np.float_)
    for k in range(local_coordinates.shape[0]):
        evaluations_multiplication[k] = np.outer(evaluations_nodal_basis[:, k], evaluations_nodal_basis[:, k])

    for element in prange(num_elements):
        element_index = element_indices[element]
        integral_value = 0.
        for k in range(num_integration_points):
            integral_value += weights[k] * values[element, k] * evaluations_multiplication[k]

        value[element] = abs_determinant_transformation_matrix[element_index] * integral_value

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_mass_elementwise_scalar(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                                 abs_determinant_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the mass matrix for an elementwise scalar.

    Parameters
    ----------
    values : np.ndarray
        (E,) array. Values of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    mul_nodal_basis_over_ref = multiplication_nodal_basis_over_reference()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        value[element] = (abs_determinant_transformation_matrix[element_index] * mul_nodal_basis_over_ref *
                          values[element])

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_mass_constant_scalar(values: Number, element_indices: np.ndarray, elem2node: np.ndarray,
                              abs_determinant_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate contributions to the mass matrix for an elementwise scalar.

    Parameters
    ----------
    values : Number
        Value of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.

    Returns
    -------
    row : np.ndarray
        (16*E,) array. Row-Index-Vector for sparse creation.
    column : np.ndarray
        (16*E,) array. Column-Index-Vector for sparse creation.
    value : np.ndarray
        (16*E,) array. Value-Vector for sparse creation.
    """
    mul_nodal_basis_over_ref = multiplication_nodal_basis_over_reference()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4, 4), np.int_)
    column = np.empty((num_elements, 4, 4), np.int_)
    value = np.empty((num_elements, 4, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        value[element] = abs_determinant_transformation_matrix[element_index] * mul_nodal_basis_over_ref * values

        indices_nodes_of_element = elem2node[element_index]
        row[element] = np.column_stack((indices_nodes_of_element, indices_nodes_of_element,
                                        indices_nodes_of_element, indices_nodes_of_element))
        column[element] = np.stack((indices_nodes_of_element, indices_nodes_of_element,
                                    indices_nodes_of_element, indices_nodes_of_element))

    return row.flatten(), column.flatten(), value.flatten()


# endregion Calc mass matrix


# region Calc load vector

@njit_cache(parallel=True)
def calc_load_function_scalar(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                              weights: np.ndarray, local_coordinates: np.ndarray,
                              abs_determinant_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray]:
    """Calculate contributions to the load vector for a space dependent scalar.

    Parameters
    ----------
    values : np.ndarray
        (E, N) array. Values of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    weights : np.ndarray
        (N,) array. Weights for numerical integration.
    local_coordinates : np.ndarray
        (N,3) array. Evaluation points for the numerical integration on the reference element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.

    Returns
    -------
    row : np.ndarray
        (4*E,) array. Row-Index-Vector for sparse creation.
    value : np.ndarray
        (4*E,) array. Value-Vector for sparse creation.
    """
    num_elements = len(element_indices)

    row = np.empty((num_elements, 4), np.int_)
    value = np.empty((num_elements, 4))

    evaluations_nodal_basis = evaluate_nodal_basis_functions(local_coordinates)

    for element in prange(num_elements):
        element_index = element_indices[element]
        integral_value = evaluations_nodal_basis @ (weights[:, np.newaxis] * values[element][:, np.newaxis])

        value[element] = abs_determinant_transformation_matrix[element_index] * integral_value.flatten()

        row[element] = elem2node[element_index]

    return row.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_load_elementwise_scalar(values: np.ndarray, element_indices: np.ndarray, elem2node: np.ndarray,
                                 abs_determinant_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray]:
    """Calculate contributions to the load vector for an elementwise scalar.

    Parameters
    ----------
    values : np.ndarray
        (E,) array. Values of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.

    Returns
    -------
    row : np.ndarray
        (4*E,) array. Row-Index-Vector for sparse creation.
    value : np.ndarray
        (4*E,) array. Value-Vector for sparse creation.
    """
    nodal_basis_over_ref = nodal_basis_over_reference()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4), np.int_)
    value = np.empty((num_elements, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        value[element] = abs_determinant_transformation_matrix[element_index] * values[element] * nodal_basis_over_ref

        row[element] = elem2node[element_index]

    return row.flatten(), value.flatten()


@njit_cache(parallel=True)
def calc_load_constant_scalar(values: Number, element_indices: np.ndarray, elem2node: np.ndarray,
                              abs_determinant_transformation_matrix: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray]:
    """Calculate contributions to the load vector for a constant scalar.

    Parameters
    ----------
    values : Number
        Value of the scalar for each element and each evaluation point.
    element_indices : np.ndarray
        (E,) array. Indices of mesh elements.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    abs_determinant_transformation_matrix : np.ndarray
        (X,) array. Absolute value of the determinant of the transformation matrix all elements.

    Returns
    -------
    row : np.ndarray
        (4*E,) array. Row-Index-Vector for sparse creation.
    value : np.ndarray
        (4*E,) array. Value-Vector for sparse creation.
    """
    nodal_basis_over_ref = nodal_basis_over_reference()

    num_elements = len(element_indices)

    row = np.empty((num_elements, 4), np.int_)
    value = np.empty((num_elements, 4))

    for element in prange(num_elements):
        element_index = element_indices[element]
        value[element] = abs_determinant_transformation_matrix[element_index] * values * nodal_basis_over_ref

        row[element] = elem2node[element_index]

    return row.flatten(), value.flatten()


# endregion Calc load vector

@njit_cache(parallel=True)
def calc_gradient_per_element(value_per_node: np.ndarray, elem2node: np.ndarray,
                              inverse_transpose_transformation_matrix: np.ndarray) -> np.ndarray:
    """Calculates the gradient for each element.

    Parameters
    ----------
    value_per_node : np.ndarray
        (N,) array. Values for each node.
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each mesh element.
    inverse_transpose_transformation_matrix : np.ndarray
        (E,3,3) array. Inverse and transpose of the transformation matrix for all elements.

    Returns
    -------
    gradient_per_element : np.ndarray
        (E,3) array. Gradient for each element.
    """
    num_elements = elem2node.shape[0]
    grad_nodal_basis_T = gradient_nodal_basis().T

    gradient_per_element = np.empty((num_elements, 3), dtype=np.float_)

    for element in range(num_elements):
        gradient_per_element[element] = (inverse_transpose_transformation_matrix[element] @ grad_nodal_basis_T @
                                         value_per_node[elem2node[element]])

    return gradient_per_element


@njit_cache(parallel=True)
def calc_transformations(node: np.ndarray, elem2node: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""Calculate the transformations from each element to the reference element.

    With :math:`t` being an element in the mesh and :math:`T` being the reference element, this function calculates the
    transformation

    .. math::

        F_t(x', y', z') = \mathbf{B}_t \left(x', y', z' \right)^T + \mathbf{b}_t

    for each element.

    Parameters
    ----------
    node : np.ndarray
        (N,3) array. Node coordinates (x, y, z).
    elem2node : np.ndarray
        (E,4) array. Indices of the nodes for each element.

    Returns
    -------
    transformation_matrices : np.ndarray
        (E,3,3) array. Transformation matrix for each element.
    transformation_vectors : np.ndarray
        (E,3) array. Translation vector for each element.
    """
    transformation_matrices = np.empty((elem2node.shape[0], 3, 3), dtype=np.float_)
    transformation_vectors = np.empty((elem2node.shape[0], 3), dtype=np.float_)

    for element in prange(elem2node.shape[0]):
        transformation_vectors[element] = node[elem2node[element, 0]]
        transformation_matrix = np.column_stack((node[elem2node[element, 1]] - node[elem2node[element, 0]],
                                                 node[elem2node[element, 2]] - node[elem2node[element, 0]],
                                                 node[elem2node[element, 3]] - node[elem2node[element, 0]]))
        transformation_matrices[element, :, :] = transformation_matrix

    return transformation_matrices, transformation_vectors


@njit_cache(parallel=True)
def calc_absolute_determinant(matrices: np.ndarray) -> Tuple[np.ndarray]:
    """Calc the absolute values of the determinants of the given matrices.

    Parameters
    ----------
    matrices : np.ndarray
        (N,3,3) array. Matrices to calculate the determinant of.

    Returns
    -------
    absolute_determinant : np.ndarray
        (N,) array. Absolute values of the determinants.
    """
    absolute_determinant = np.empty(matrices.shape[0], dtype=float)

    for element in prange(matrices.shape[0]):
        absolute_determinant[element] = np.abs(np.linalg.det(matrices[element]))

    return absolute_determinant


@njit_cache(parallel=True)
def calc_inverse_matrix_transpose(matrices: np.ndarray) -> Tuple[np.ndarray]:
    """Calc the inverse transpose of the given matrices.

    Parameters
    ----------
    matrices : np.ndarray
        (N,3,3) array. Matrices to calculate the inverse transpose of.

    Returns
    -------
    inverse_transpose : np.ndarray
        (N,3,3) array. Inverse transpose of the given matrices.
    """
    inverse_transpose = np.empty(matrices.shape, dtype=np.float_)

    for element in prange(matrices.shape[0]):
        inverse_transpose[element, :, :] = np.linalg.inv(matrices[element]).T

    return inverse_transpose


class TetCartesianNodalShapeFunction(NodalShapeFunction):
    """Class describing tetrahedral nodal shape functions on 3D cartesian meshes"""

    dphi1 = np.array([[-1], [-1], [-1]])
    dphi2 = np.array([[1], [0], [0]])
    dphi3 = np.array([[0], [1], [0]])
    dphi4 = np.array([[0], [0], [1]])

    @staticmethod
    def issingleint(x) -> bool:
        """Workaround: check whether it is either an array with single integer or integer only."""
        if isinstance(x, (int, np.int_)):
            return True
        if isinstance(x, np.ndarray):
            if len(x.shape) == 1 and np.round(x) == x:
                return True
        return False

    @staticmethod
    def base1(x: float, y: float, z: float) -> float:
        """
        First basis function on reference element.

        Parameters
        ----------
        x : float
            x coordinate
        y : float
            y coordinate
        z : float
            z coordinate

        Returns
        -------
        float : value of function at given coordinates

        Notes
        -----
        Explained in info/Ansatzfunktionen/ansatzfunktionen.pdf (German)
        """
        coord = np.array([x, y, z])
        if np.all(coord >= 0) and np.all(coord <= 1):
            return 1 - x - y - z
        return 0

    @staticmethod
    def base2(x: float, y: float, z: float) -> float:
        """
        Second basis function on reference element.

        Parameters
        ----------
        x : float
            x coordinate
        y : float
            y coordinate
        z : float
            z coordinate

        Returns
        -------
        float : value of function at given coordinates

        Notes
        -----
        Explained in info/Ansatzfunktionen/ansatzfunktionen.pdf (German)
        """
        coord = np.array([x, y, z])
        if np.all(coord >= 0) and np.all(coord <= 1):
            return x
        return 0

    @staticmethod
    def base3(x: float, y: float, z: float) -> float:
        """
        Third basis function on reference element.

        Parameters
        ----------
        x : float
            x coordinate
        y : float
            y coordinate
        z : float
            z coordinate

        Returns
        -------
        float : value of function at given coordinates

        Notes
        -----
        Explained in info/Ansatzfunktionen/ansatzfunktionen.pdf (German)
        """
        coord = np.array([x, y, z])
        if np.all(coord >= 0) and np.all(coord <= 1):
            return y
        return 0

    @staticmethod
    def base4(x: float, y: float, z: float) -> float:
        """
        Fourth basis function on reference element.

        Parameters
        ----------
        x : float
            x coordinate
        y : float
            y coordinate
        z : float
            z coordinate

        Returns
        -------
        float : value of function at given coordinates

        Notes
        -----
        Explained in info/Ansatzfunktionen/ansatzfunktionen.pdf (German)
        """
        coord = np.array([x, y, z])
        if np.all(coord >= 0) and np.all(coord <= 1):
            return z
        return 0

    def __init__(self, mesh: TetMesh):
        super().__init__(mesh, dim=3, allocation_size=16 * mesh.num_elem)
        self._transformation_matrices, self._transformation_vectors = calc_transformations(mesh.node, mesh.elem2node)
        self._abs_det_transformation_matrix = calc_absolute_determinant(self._transformation_matrices)
        self._inverse_transpose_transformation_matrix = calc_inverse_matrix_transpose(self._transformation_matrices)

    def _calc_evaluation_points_element(self, local_coordinates: np.ndarray, indices: np.ndarray) -> np.ndarray:
        return calc_evaluation_points_element(local_coordinates, indices,
                                              self._transformation_matrices, self._transformation_vectors)

    # region Calc matrix

    # region Calc matrix constant

    def _calc_matrix_constant_scalar(self, matrix_type: str, indices: np.ndarray, value: Number,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_constant_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_constant_scalar(value, indices, self.mesh.elem2node,
                                                self._abs_det_transformation_matrix,
                                                self._inverse_transpose_transformation_matrix)
        if matrix_type == "mass":
            return calc_mass_constant_scalar(value, indices, self.mesh.elem2node, self._abs_det_transformation_matrix)

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
            return calc_divgrad_constant_tensor(value, indices, self.mesh.elem2node,
                                                self._abs_det_transformation_matrix,
                                                self._inverse_transpose_transformation_matrix)

        raise NotImplementedError("Anisotrop materials are not implemented in TetCartesianNodalShapeFunction.")

    # endregion Calc matrix constant

    # region Calc matrix elementwise

    def _calc_matrix_elementwise_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_elementwise_scalar(value, indices, self.mesh.elem2node,
                                                   self._abs_det_transformation_matrix,
                                                   self._inverse_transpose_transformation_matrix)
        if matrix_type == "mass":
            return calc_mass_elementwise_scalar(value, indices, self.mesh.elem2node,
                                                self._abs_det_transformation_matrix)

        raise NotImplementedError(f"calc_matrix_scalar_per_elem is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_elementwise_vector(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_vector(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        raise NotImplementedError(f"calc_matrix_elementwise_vector is not implemented for matrix type: {matrix_type}.")

    def _calc_matrix_elementwise_tensor(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                        weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_elementwise_tensor(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_elementwise_tensor(value, indices, self.mesh.elem2node,
                                                   self._abs_det_transformation_matrix,
                                                   self._inverse_transpose_transformation_matrix)

        raise NotImplementedError("Anisotrop materials are not implemented in TetCartesianNodalShapeFunction.")

    # endregion Calc matrix elementwise

    # region Calc matrix function

    def _calc_matrix_function_scalar(self, matrix_type: str, indices: np.ndarray, value: np.ndarray,
                                     weights: np.ndarray, local_coordinates: np.ndarray, **kwargs) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        super()._calc_matrix_function_scalar(matrix_type, indices, value, weights, local_coordinates, **kwargs)

        if matrix_type == "divgrad":
            return calc_divgrad_function_scalar(value, indices, self.mesh.elem2node, weights,
                                                self._abs_det_transformation_matrix,
                                                self._inverse_transpose_transformation_matrix)
        if matrix_type == "mass":
            return calc_mass_function_scalar(value, indices, self.mesh.elem2node, weights, local_coordinates,
                                             self._abs_det_transformation_matrix)

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
            return calc_divgrad_function_tensor(value, indices, self.mesh.elem2node, weights,
                                                self._abs_det_transformation_matrix,
                                                self._inverse_transpose_transformation_matrix)
        raise NotImplementedError("Anisotrop materials are not implemented in TetCartesianNodalShapeFunction.")

    # endregion Calc matrix function

    # endregion Calc matrix

    # region Calc vector

    # region Calc vector constant

    def _calc_vector_constant_scalar(self, vector_type: str, indices: np.ndarray, value: Number,
                                     weights: np.ndarray,
                                     local_coordinates: np.ndarray, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        super()._calc_vector_constant_scalar(vector_type, indices, value, weights, local_coordinates, **kwargs)

        if vector_type == "load":
            return calc_load_constant_scalar(value, indices, self.mesh.elem2node, self._abs_det_transformation_matrix)

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
            return calc_load_elementwise_scalar(value, indices, self.mesh.elem2node,
                                                self._abs_det_transformation_matrix)

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
            return calc_load_function_scalar(value, indices, self.mesh.elem2node, weights, local_coordinates,
                                             self._abs_det_transformation_matrix)

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

    def gradient(self, val2node: np.ndarray) -> np.ndarray:
        if not isinstance(val2node, np.ndarray):
            raise ValueError("Gradient is calculated only for array inputs.")
        if val2node.size != self.mesh.num_node:
            raise ValueError("Provided scalar field needs to provide one value for each node.")
        return calc_gradient_per_element(val2node, self.mesh.elem2node, self._inverse_transpose_transformation_matrix)

    def _calc_neumann_term_on_face_function(self, face_number, value, weights, int_points) -> np.ndarray:
        """
        Calculates the local neumann term vector for element k when a function is given.

        Parameters
        ----------
        face_number : int
            Index of element in mesh
        value : Callable[[float, float, float], float]
            Function of neumann term in element k in the format f(x,y,z)
        weights : np.ndarray
            (m,) weights for numerical integration of order m over reference triangle. See notes.
        int_points : np.ndarray
            (m, 2) integration points  of order m in reference triangle. See notes.

        Returns
        -------
        vec_elem : np.ndarray
            (3,) array containing the neumann vector values for the three nodes of face face_number

        Notes
        -----
        For derivation, see info/Ansatzfunktionen/ansatzfunktionen.
        weights and int_points can be directly provided by pyrit.toolbox.quadraturetoolbox.gauss_triangle
        """
        vec_elem = np.zeros(4)
        face_nodes = self.mesh.face2node[face_number, :]
        matrix_b = np.c_[self.mesh.node[face_nodes[1], :] - self.mesh.node[face_nodes[0], :],
                         self.mesh.node[face_nodes[2], :] - self.mesh.node[face_nodes[0], :],
                         np.ones((3,))]  # local transformation matrix
        nm_values = np.zeros(weights.size)
        for idx in range(int_points.shape[0]):
            # iterate over integration points and find coordinates in real mesh
            local_coord = np.r_[int_points[idx, :], 0]
            real_coord = (matrix_b @ local_coord) + self.mesh.node[face_nodes[0]]
            nm_values[idx] = value(*real_coord)

        dummyz = np.zeros(int_points[:, 0].shape)
        vec_elem[0] = np.sum(weights * nm_values * self.base1(int_points[:, 0], int_points[:, 1], dummyz))
        vec_elem[1] = np.sum(weights * nm_values * self.base2(int_points[:, 0], int_points[:, 1], dummyz))
        vec_elem[2] = np.sum(weights * nm_values * self.base3(int_points[:, 0], int_points[:, 1], dummyz))
        vec_elem = vec_elem * np.abs(np.linalg.det(matrix_b))
        return vec_elem

    def _calc_neumann_term_on_face_constant(self, face_number, value) -> np.ndarray:
        return np.ones(3) * self.mesh.face_area[face_number] * value / 3

    # pylint: disable=cell-var-from-loop
    def neumann_term(self, *args: Union[Tuple[Regions, BdryCond],
                                        Tuple[np.ndarray, Union[Callable[..., float], np.ndarray, float]]],
                     integration_order: int = 1) -> coo_matrix:
        # note complete similarity to implementation in TriCartesianNodalShapeFunction
        flag_regions, flag_value = self._process_neumann(*args)

        weights, int_points = QuadratureToolbox.gauss_triangle(int(integration_order))

        neumann_vector = np.zeros((self.mesh.num_node, 1))
        if flag_regions:  # We have regions and boundary_conditions
            regions, boundary_conditions = args
            regions: Regions
            boundary_conditions: BdryCond
            for key in boundary_conditions.get_ids():
                bc = boundary_conditions.get_bc(key)
                if isinstance(bc, BCNeumann):
                    bc_value = bc.value
                    indices_regions = regions.find_regions_of_boundary_condition(bc.ID)
                    indices_faces = np.empty(0)  # Indices of all faces that are on the boundary bc
                    for region_id in indices_regions:
                        indices_faces = np.r_[indices_faces, np.where(self.mesh.face2regi == region_id)[0]]
                    indices_faces = indices_faces.astype('int')
                    if not bc.is_homogeneous:
                        for face in indices_faces:
                            face_values = self._calc_neumann_term_on_face_function(face, bc_value, weights, int_points)
                            neumann_vector[self.mesh.face2node[face, 0], 0] += face_values[0]
                            neumann_vector[self.mesh.face2node[face, 1], 0] += face_values[1]
                            neumann_vector[self.mesh.face2node[face, 2], 0] += face_values[2]
                    if bc.is_constant:
                        for k, face in enumerate(indices_faces):
                            if isinstance(bc_value, np.ndarray):
                                face_values = self._calc_neumann_term_on_face_constant(face, bc_value[k])
                            elif isinstance(bc_value, (float, int, complex)):
                                face_values = self._calc_neumann_term_on_face_constant(face, bc_value)
                            else:
                                raise Exception("Type not supported")
                            neumann_vector[self.mesh.face2node[face, 0], 0] += face_values[0]
                            neumann_vector[self.mesh.face2node[face, 1], 0] += face_values[1]
                            neumann_vector[self.mesh.face2node[face, 2], 0] += face_values[2]
        else:  # We have indices and value
            indices, value = args
            for k, index in enumerate(indices):
                if flag_value == 'callable':
                    node_test = self.mesh.node[self.mesh.face2node[index, 0], :]
                    if isinstance(value(*node_test), np.ndarray):
                        # noinspection PyCallingNonCallable
                        face_values = self._calc_neumann_term_on_face_function(index, lambda x, y, z: value(x, y, z)[k],
                                                                               weights, int_points)
                    else:
                        face_values = self._calc_neumann_term_on_face_function(index, value, weights, int_points)
                elif flag_value == 'array':
                    face_values = self._calc_neumann_term_on_face_constant(index, value[k])
                elif flag_value == 'value':
                    face_values = self._calc_neumann_term_on_face_constant(index, value)
                # noinspection PyUnboundLocalVariable
                neumann_vector[self.mesh.face2node[index, 0], 0] += face_values[0]
                neumann_vector[self.mesh.face2node[index, 1], 0] += face_values[1]
                neumann_vector[self.mesh.face2node[index, 2], 0] += face_values[2]
        return coo_matrix(neumann_vector)

    def _calc_robin_term_function(self, face_number, value, weights, int_points):
        """Calculates the local Robin matrix vector for a surface when a function is given.

        Parameters
        ----------
        face_number : int
            Index of element in mesh
        value : Callable[[float, float, float], float]
            Function of Robin alpha/beta term in element k in the format f(x,y,z)
        weights : np.ndarray
            (m,) weights for numerical integration of order m over reference triangle. See notes.
        int_points : np.ndarray
            (m, 2) integration points  of order m in reference triangle. See notes.


        Returns
        -------
        vec_elem : np.ndarray
            (9,) array containing the Robin matrix values for the three nodes of face face_number

        Notes
        -----
        Compare the 2D TriCartesian Mass matrix.
        weights and int_points can be directly provided by pyrit.toolbox.quadraturetoolbox.gauss_triangle
        """
        face_nodes = self.mesh.face2node[face_number, :]
        matrix_b = np.c_[self.mesh.node[face_nodes[1], :] - self.mesh.node[face_nodes[0], :],
                         self.mesh.node[face_nodes[2], :] - self.mesh.node[face_nodes[0], :],
                         np.ones((3,))]  # local transformation matrix
        # compare TriCart Mass-Matrix
        integral = np.zeros((3, 3))
        for kk, weight in enumerate(weights):
            m_values = np.array(
                [1 - int_points[kk, 0] - int_points[kk, 1], int_points[kk, 0],
                 int_points[kk, 1]])
            local_coord = np.array(int_points[kk, :], ndmin=2).T
            tmp = (matrix_b[:, 0:2] @ local_coord).flatten() + self.mesh.node[face_nodes[0]]
            # noinspection PyCallingNonCallable
            evaluation = value(x=tmp[0], y=tmp[1], z=tmp[2])
            integral = integral + weight * evaluation * np.outer(m_values, m_values)
        return np.abs(np.linalg.det(matrix_b)) * integral.reshape(9)

    def _calc_robin_term_constant(self, face_number, value):
        """Calculates the local Robin matrix vector for a surface when a constant is given.

        Parameters
        ----------
        face_number : int
            Index of element in mesh
        value : float
            Constant value alpha / beta

        Returns
        -------
        vec_elem : np.ndarray
            (9,) array containing the Robin matrix values for the three nodes of face face_number

        Notes
        -----
        Compare the 2D TriCartesian Mass matrix.
        """
        return self.mesh.face_area[face_number] * value / 12 * np.array([2, 1, 1, 1, 2, 1, 1, 1, 2])

    # pylint: disable=unnecessary-lambda-assignment
    def robin_terms(self, regions: Regions, boundary_condition: 'BdryCond', integration_order: int = 1) -> \
            Tuple[coo_matrix, coo_matrix]:

        # simple input check: arguments are of correct class
        if not (isinstance(regions, Regions) and isinstance(boundary_condition, BdryCond)):
            raise ValueError("Input arguments have wrong types. Did you mix up the order?")

        bc_keys = boundary_condition.get_ids()

        values_list = []
        lines_list = []
        columns_list = []
        robin_vector = coo_matrix((self.mesh.num_node, 1))
        weights, int_points = QuadratureToolbox.gauss_triangle(int(integration_order))

        def check_valid_function(arg, numargs):
            if callable(arg):
                if len(signature(arg).parameters) != numargs:
                    raise ValueError(f"The function has not the expected number of {str(numargs)} "
                                     f"arguments")

        for bc_key in bc_keys:
            bc = boundary_condition.get_bc(bc_key)
            if not isinstance(bc, BCRobin):
                continue

            # Calculate the matrix
            indices_regions = regions.find_regions_of_boundary_condition(bc.ID)
            indices_faces = np.empty(0)  # Indices of all faces that are on the boundary bc
            for region_id in indices_regions:
                indices_faces = np.r_[indices_faces, np.where(self.mesh.face2regi == region_id)[0]]
            indices_faces = indices_faces.astype('int')
            robin_values_per_bc = np.zeros(9 * len(indices_faces))
            robin_lines_per_bc = np.zeros(9 * len(indices_faces), dtype=int)
            robin_columns_per_bc = np.zeros(9 * len(indices_faces), dtype=int)

            coef_dir = bc.coefficient_dirichlet
            coef_neum = bc.coefficient_neumann
            if np.any(coef_neum == 0):
                raise ValueError("Neumann coefficient must not be zero.")
            value_bc = bc.value
            if callable(coef_dir):
                check_valid_function(coef_dir, 3)
                if callable(coef_neum):
                    check_valid_function(coef_neum, 3)
                    # Both coefficients are functions
                    for k, face in enumerate(indices_faces):
                        idx_node = np.kron(np.ones((3, 1), dtype=int), self.mesh.face2node[face])
                        tmp_values = self._calc_robin_term_function(face,
                                                                    lambda x, y, z: coef_dir(x, y, z) / coef_neum(x, y,
                                                                                                                  z),
                                                                    weights, int_points)
                        robin_values_per_bc[9 * k:9 * (k + 1)] = tmp_values
                        robin_lines_per_bc[9 * k:9 * (k + 1)] = np.reshape(idx_node, 9)
                        robin_columns_per_bc[9 * k:9 * (k + 1)] = np.reshape(idx_node.T, 9)
                else:
                    # Only dirichlet coefficient is a function
                    if isinstance(coef_neum, np.ndarray):
                        if len(indices_faces) != coef_neum.size:
                            raise ValueError("Provided array-valued coefficient does not have the same number of "
                                             "elements as there are surface elements for the Robin BC.")
                    for k, face in enumerate(indices_faces):
                        idx_node = np.kron(np.ones((3, 1), dtype=int), self.mesh.face2node[face])
                        if isinstance(coef_neum, np.ndarray):
                            tmp_values = self._calc_robin_term_function(face,
                                                                        lambda x, y, z: coef_dir(x, y, z) / coef_neum[
                                                                            k], weights, int_points)
                        elif isinstance(coef_neum, (float, int)):
                            tmp_values = self._calc_robin_term_function(face,
                                                                        lambda x, y, z: coef_dir(x, y, z) / coef_neum,
                                                                        weights, int_points)
                        else:
                            raise Exception("Type of coef_neum is not supported")
                        robin_values_per_bc[9 * k:9 * (k + 1)] = tmp_values
                        robin_lines_per_bc[9 * k:9 * (k + 1)] = np.reshape(idx_node, 9)
                        robin_columns_per_bc[9 * k:9 * (k + 1)] = np.reshape(idx_node.T, 9)
            else:
                if callable(coef_neum):
                    check_valid_function(coef_neum, 3)
                    if isinstance(coef_dir, np.ndarray):
                        if len(indices_faces) != coef_dir.size:
                            raise ValueError("Provided array-valued coefficient does not have the same number of "
                                             "elements as there are surface elements for the Robin BC.")
                    # Only coef_neum is a function
                    for k, face in enumerate(indices_faces):
                        idx_node = np.kron(np.ones((3, 1), dtype=int), self.mesh.face2node[face])
                        if isinstance(coef_dir, np.ndarray):
                            tmp_values = self._calc_robin_term_function(face,
                                                                        lambda x, y, z: coef_dir[k] / coef_neum(x, y,
                                                                                                                z),
                                                                        weights, int_points)
                        elif isinstance(coef_dir, (float, int)):
                            tmp_values = self._calc_robin_term_function(face,
                                                                        lambda x, y, z: coef_dir / coef_neum(x, y, z),
                                                                        weights, int_points)
                        else:
                            raise Exception("Type of coef_dir is not supported")
                        robin_values_per_bc[9 * k:9 * (k + 1)] = tmp_values
                        robin_lines_per_bc[9 * k:9 * (k + 1)] = np.reshape(idx_node, 9)
                        robin_columns_per_bc[9 * k:9 * (k + 1)] = np.reshape(idx_node.T, 9)
                else:
                    # Both are no functions
                    value = coef_dir / coef_neum
                    if isinstance(value, np.ndarray):
                        if len(indices_faces) != value.size:
                            raise ValueError("Provided array-valued coefficient does not have the same number of "
                                             "elements as there are surface elements for the Robin BC.")
                    for k, face in enumerate(indices_faces):
                        idx_node = np.kron(np.ones((3, 1), dtype=int), self.mesh.face2node[face])
                        if isinstance(value, np.ndarray):
                            tmp_values = self._calc_robin_term_constant(face, value[k])
                        elif isinstance(value, (float, int)):
                            tmp_values = self._calc_robin_term_constant(face, value)
                        else:
                            raise Exception("Type of value not supported")
                        robin_values_per_bc[9 * k:9 * (k + 1)] = tmp_values
                        robin_lines_per_bc[9 * k:9 * (k + 1)] = np.reshape(idx_node, 9)
                        robin_columns_per_bc[9 * k:9 * (k + 1)] = np.reshape(idx_node.T, 9)
            values_list.append(robin_values_per_bc)
            lines_list.append(robin_lines_per_bc)
            columns_list.append(robin_columns_per_bc)

            # Calculate the vector
            if not bc.is_homogeneous:
                if callable(coef_neum):
                    check_valid_function(coef_neum, 3)
                    check_valid_function(value_bc, 3)
                    # Both are functions
                    if callable(value_bc):
                        fun = lambda x, y, z: value_bc(x, y, z) / coef_neum(x, y, z)
                    else:
                        fun = lambda x, y, z: value_bc / coef_neum(x, y, z)
                    robin_vector = robin_vector + self.neumann_term(indices_faces, fun,
                                                                    integration_order=integration_order)
                else:
                    # only value_bc is a function
                    check_valid_function(value_bc, 3)
                    if callable(value_bc):
                        fun = lambda x, y, z: value_bc(x, y, z) / coef_neum
                    else:
                        fun = value_bc / coef_neum
                    robin_vector = robin_vector + self.neumann_term(indices_faces, fun,
                                                                    integration_order=integration_order)
            else:
                if callable(coef_neum):
                    check_valid_function(coef_neum, 3)
                    # Only Neumann coefficient is a function
                    if isinstance(value_bc, np.ndarray):
                        robin_vector = robin_vector + self.neumann_term(indices_faces,
                                                                        lambda x, y, z: value_bc / coef_neum(x, y, z),
                                                                        integration_order=integration_order)
                    elif isinstance(value_bc, (float, int)):
                        robin_vector = robin_vector + self.neumann_term(indices_faces,
                                                                        lambda x, y, z: value_bc / coef_neum(x, y, z),
                                                                        integration_order=integration_order)
                    else:
                        raise Exception("Type of value not supported")

                else:
                    value_tmp = value_bc / coef_neum
                    if isinstance(value_tmp, np.ndarray):
                        robin_vector = robin_vector + self.neumann_term(indices_faces, value_tmp,
                                                                        integration_order=integration_order)
                    elif isinstance(value_tmp, (float, int)):
                        robin_vector = robin_vector + self.neumann_term(indices_faces, value_tmp,
                                                                        integration_order=integration_order)
                    else:
                        raise Exception("Type not supported.")

        if len(values_list) != 0:
            robin_matrix = coo_matrix(
                (np.concatenate(values_list), (np.concatenate(lines_list), np.concatenate(columns_list))),
                shape=(self.mesh.num_node, self.mesh.num_node))
        else:
            robin_matrix = coo_matrix((self.mesh.num_node, self.mesh.num_node)).tocoo()
        return robin_matrix, robin_vector.tocoo()
