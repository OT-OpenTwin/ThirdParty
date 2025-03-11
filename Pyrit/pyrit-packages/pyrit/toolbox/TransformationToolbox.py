# coding=utf-8
"""Toolbox for all kinds of coordinate transformations.

.. sectionauthor:: Thyssen, Bundschuh
"""
from typing import Callable, overload
from inspect import signature
import numpy as np


class TransformationException(Exception):
    """Exception for errors in the TransformationToolbox"""

    def __init__(self, vector, tensor):
        """Customized exception Class for errors in TransformationToolbox

        Parameters
        ----------
        vector: np.ndarray or callable
            input vector to calculate the basis or input vector to be transformed, depending on the case

        tensor: np.ndarray
            input tensor to be transformed
        """
        self.vector = vector
        self.tensor = tensor
        self.message = None

        if not callable(self.vector) and np.array_equal(self.vector, np.array([0, 0])):
            self.message = "Input vector may not be [0,0]"

        if callable(self.vector) and np.all(self.vector(1, 1) == 0):
            self.message = "Input vector may not return [0,0]"

        elif not callable(self.vector) and np.array_equal(self.vector, np.array([0, 0, 0])):
            self.message = "Input vector may not be [0,0,0]"

        elif callable(self.vector) and np.all(self.vector(1, 1, 1) == 0):
            self.message = "Input vector may not return [0,0,0]"

        elif isinstance(self.vector, np.ndarray) and self.vector.shape not in [(2,), (3,)]:
            self.message = "Vector must have shape (2,) or (3,)"

        elif isinstance(self.tensor, np.ndarray) and tensor.shape not in [(2, 2), (3, 3)]:
            self.message = "tensor must have shape (2, 2) or (3, 3)"

        elif self.vector is callable and len(signature(vector).parameters) not in [2, 3]:
            self.message = "Vector must have two or three positional arguments"

        super().__init__(self.message)


def _basis_from_constant_direction_3d(vector: np.ndarray) -> np.ndarray:
    """Get an orthonormal basis from one vector.

    Compute an orthonormal basis where the first basis vector is
    parallel to the given vector.

    Parameters
    ----------
    vector : np.ndarray
        (3,) array as a vector

    Returns
    -------
    basis_vectors : np.ndarray
        (3,3) array where in the i-th row there is the i-th basis vector.
        The basis vectors are orthonormal to each other
    """
    vector = np.array(vector)
    if np.all(vector == 0):
        raise TransformationException(vector, tensor=None)
    # normalize vector
    vector = vector / np.linalg.norm(vector)

    component_a = vector[0]
    component_b = vector[1]
    component_c = vector[2]
    perp_1 = np.array([component_b + component_c,
                       component_c - component_a,
                       -component_a - component_b])
    perp_1 = perp_1 / np.linalg.norm(perp_1)
    perp_2 = np.cross(vector, perp_1)
    perp_2 = perp_2 / np.linalg.norm(perp_2)

    basis_vectors = np.array([vector, perp_1, perp_2])
    return basis_vectors


def _basis_from_constant_direction_2d(vector: np.ndarray) -> np.ndarray:
    """Get an orthonormal basis from one vector.

    Compute an orthonormal basis where the first basis vector is
    parallel to the given vector.

    Parameters
    ----------
    vector : np.ndarray
        (2,) array as a vector

    Returns
    -------
    basis_vectors : np.ndarray
        (2,2) array where in the i-th row there is the i-th basis vector.
        The basis vectors are orthonormal to each other
    """
    vector = np.array(vector)
    if np.all(vector == 0):
        raise TransformationException(vector, tensor=None)
    # normalize vector
    vector = vector / np.linalg.norm(vector)

    component_a = vector[0]
    component_b = vector[1]
    if np.all(vector) == 0:
        perp_1 = np.array([component_b, component_a])
    else:
        perp_1 = np.array([-component_b, component_a])
        perp_1 = perp_1 / np.linalg.norm(perp_1)

    basis_vectors = np.array([vector, perp_1])
    return basis_vectors


def basis_from_constant_direction(vector: np.ndarray) -> np.ndarray:
    """Get an orthonormal basis from one vector.

    Compute an orthonormal basis where the first basis vector is
    parallel to the given vector.

    Parameters
    ----------
    vector : np.ndarray
        (N,) array with N=2 or N=3 as a vector

    Returns
    -------
    basis_vectors : np.ndarray
        (N,N) array where in the i-th row there is the i-th basis vector.
        The basis vectors are orthonormal to each other
    """
    vector = np.array(vector)
    if vector.shape == (2,):
        basis_vectors = _basis_from_constant_direction_2d(vector)

    elif vector.shape == (3,):
        basis_vectors = _basis_from_constant_direction_3d(vector)

    else:
        raise TransformationException(vector, tensor=None)

    return basis_vectors


def transform_constant_vector(vector: np.ndarray, basis_vectors: np.ndarray) -> np.ndarray:
    r"""Transform a vector to another coordinate system.

    There are two coordinate systems x and u. The basis vectors of the latter one can be expressed
    as a linear combination of the former one.
    The input vector is known in coordinate system u.
    This function transforms the input vector to the coordinate system x.

    Parameters
    ----------
    vector: np.ndarray
        (N,) array as a vector in the coordinate system u.
    basis_vectors : np.ndarray
        (N,N) array where in the i-th row there is the i-th basis vector of coordinate system u
        expressed in the basis vectors of a coordinate system x.

    Returns
    -------
    transformed_vector: np.ndarray
        (N,) array. The input vector expressed in the coordinate system x

    Examples
    --------
    Let the 2D cartesian coordinate system be coordinate system x and the basis vectors of
    coordinate system u be :math:`\vec{e}_u = 2 \vec{e}_x` and
    :math:`\vec{e}_u = 1 \vec{e}_x + 1 \vec{e}_y`.
    Let :math:`a` be a vector with :math:`a_x` being this vector expressed in the
    coordinate system x and :math:`a_u` being this vector expressed in the coordinate system u.
    With :math:`a_u` known, :math:`a_x` can be computed via:

        >>> a_u = np.array([1, 2])
        >>> basis_vectors = np.array([[2, 0],
        >>>                           [1, 1]])
        >>> transform_vector(a_u, basis_vectors)
        array([4, 2])
    """
    transformed_vector = np.dot(basis_vectors.transpose(), vector)
    return transformed_vector


def transform_constant_tensor(tensor: np.ndarray, basis_vectors: np.ndarray) -> np.ndarray:
    r"""Transform a tensor to another coordinate system

    There are two coordinate systems x and u. The basis vectors of the latter one can be expressed
    as a linear combination of the former one.
    The input tensor in known in coordinate system u.
    This function transforms the input tensor to the coordinate system x.

    Parameters
    ----------
    tensor : np.ndarray
        (N,N) array as a tensor in the coordinate system u.
    basis_vectors : np.ndarray
        (N,N) array where in the i-th row there is the i-th basis vector of coordinate system u
        expressed in the basis vectors of a coordinate system x.

    Returns
    -------
    transformed_tensor: np.ndarray
        (N,N) array. The input tensor expressed in the coordinate system x
    """
    transp_basis_vectors = basis_vectors.transpose()
    transformed_tensor = np.dot(np.dot(transp_basis_vectors, tensor), basis_vectors)
    return transformed_tensor


def _basis_from_function_direction_3d(vector: Callable[[float, float, float], np.ndarray])\
        -> Callable[[float, float, float], np.ndarray]:
    """Get a function that returns an orthonormal basis for each vector given by the input vector.

    Compute an orthonormal basis where the first basis vector is
    parallel to the given vector.

    Parameters
    ----------
    vector : Callable[[float, float, float], np.ndarray]
        A callable that takes three positional float arguments and returns a (3,) array as a vector.

    Returns
    -------
    basis_vectors : Callable[[float, float, float], np.ndarray]
        A callable that takes three positional float arguments and returns a (3,3) array where in the i-th row there is
        the i-th basis vector. The basis vectors are orthonormal to each other.
    """
    def basis_vectors3d(vector: Callable[[float, float, float], np.ndarray], x: float, y: float, z: float):
        """Calculate basis vectors as a function of vector"""
        input_vector = np.array(vector(x, y, z))
        if np.all(input_vector == 0):
            raise TransformationException(vector, tensor=None)
        # normalize vector
        input_vector = input_vector / np.linalg.norm(input_vector)

        component_a = input_vector[0]
        component_b = input_vector[1]
        component_c = input_vector[2]
        perp_1 = np.array([component_b + component_c,
                           component_c - component_a,
                           -component_a - component_b])
        perp_1 = perp_1 / np.linalg.norm(perp_1)
        perp_2 = np.cross(input_vector, perp_1)
        perp_2 = perp_2 / np.linalg.norm(perp_2)
        return np.array([input_vector, perp_1, perp_2])
    return lambda x, y, z: basis_vectors3d(vector, x, y, z)


def _basis_from_function_direction_2d(vector: Callable[[float, float], np.ndarray])\
        -> Callable[[float, float], np.ndarray]:
    """Get a function that returns an orthonormal basis for each vector given by the input vector.

    Compute an orthonormal basis where the first basis vector is
    parallel to the given vector.

    Parameters
    ----------
    vector : Callable[[float, float], np.ndarray]
        A callable that takes two positional float arguments and returns a (3,) array as a vector.

    Returns
    -------
    basis_vectors : Callable[[float, float], np.ndarray]
        A callable that takes three positional float arguments and returns a (3,3) array where in the i-th row there is
        the i-th basis vector. The basis vectors are orthonormal to each other.
    """
    def basis_vectors2d(vector: Callable[[float, float], np.ndarray], x: float, y: float):
        """Calculate basis vectors as a function of vector"""
        input_vector = np.array(vector(x, y))
        if np.all(input_vector == 0):
            raise TransformationException(vector, tensor=None)
        # normalize vector
        input_vector = input_vector / np.linalg.norm(input_vector)

        component_a = input_vector[0]
        component_b = input_vector[1]
        if np.all(input_vector) == 0:
            perp_1 = np.array([component_b, component_a])
        else:
            perp_1 = np.array([-component_b, component_a])
            perp_1 = perp_1 / np.linalg.norm(perp_1)

        return np.array([input_vector, perp_1])
    return lambda x, y: basis_vectors2d(vector, x, y)


@overload
def basis_from_function_direction(vector: Callable[[float, float], np.ndarray]) -> Callable[[float, float], np.ndarray]:
    pass


@overload
def basis_from_function_direction(vector: Callable[[float, float, float], np.ndarray])\
        -> Callable[[float, float, float], np.ndarray]:
    pass


def basis_from_function_direction(vector):
    """Get a function that returns an orthonormal basis for each vector given by the input vector.

    Compute an orthonormal basis where the first basis vector is
    parallel to the given vector.

    Parameters
    ----------
    vector : Callable[[float, float], np.ndarray] or Callable[[float, float, float], np.ndarray]
        A callable that takes two or three positional float arguments and returns respectively a (2,) or
        (3,) array as a vector.

    Returns
    -------
    basis_vectors : Callable[[float, float], np.ndarray] or Callable[[float, float, float], np.ndarray]
        A callable that takes two or three positional float arguments and returns respectively a (2,2) or
        (3,3) array where in the i-th row there is the i-th basis vector.
        The basis vectors are orthonormal to each other.
    """
    sig = signature(vector)
    parameters = sig.parameters
    number_parameters = len(parameters)
    if number_parameters == 2:
        basis_vectors = _basis_from_function_direction_2d(vector)

    elif number_parameters == 3:
        basis_vectors = _basis_from_function_direction_3d(vector)

    else:
        raise TransformationException(vector, tensor=None)

    return basis_vectors


@overload
def transform_function_vector(vector: np.ndarray, basis_vectors: Callable[[float, float], np.ndarray])\
        -> Callable[[float, float], np.ndarray]:
    pass


@overload
def transform_function_vector(vector: np.ndarray, basis_vectors: Callable[[float, float, float], np.ndarray]) \
        -> Callable[[float, float, float], np.ndarray]:
    pass


def transform_function_vector(vector, basis_vectors):
    """Transform a vector to another coordinate system.

    There are two coordinate systems x and u. The position dependent basis vectors of the latter one can be expressed
    as a linear combination of the former one.
    The input vector is known in coordinate system u.
    This function transforms the input vector to the coordinate system x.

    Parameters
    ----------
    vector: np.ndarray
        (N,) array as a vector in the coordinate system u.
    basis_vectors : Callable[[float, float], np.ndarray] or Callable[[float, float, float], np.ndarray]
        A callable that takes two or three positional float arguments (a, b, c) and returns respectively a (2,2) or
        (3,3) array where in the i-th row there is the i-th basis vector of coordinate system u at the position (a, b)
        or (a, b, c) expressed in the basis vectors of a coordinate system x.

    Returns
    -------
    transformed_vector: Callable[[float, float], np.ndarray] or Callable[[float, float, float], np.ndarray]
        A callable that takes two or three positional float arguments and returns respectively a (2,) or (3,) array that
        represents the input vector expressed in the coordinate system x.
    """

    def transformed_vector(*args):
        if vector.shape == (2,):
            def transformed_vector2d(x, y):
                input_basis_vectors = np.array(basis_vectors(x, y))
                transf_vector = np.dot(input_basis_vectors.transpose(), vector)
                return transf_vector
            return transformed_vector2d(*args)

        if vector.shape == (3,):
            def transformed_vector3d(x, y, z):
                input_basis_vectors = np.array(basis_vectors(x, y, z))
                transf_vector = np.dot(input_basis_vectors.transpose(), vector)
                return transf_vector
            return transformed_vector3d(*args)

        raise TransformationException(vector, None)
    return transformed_vector


@overload
def transform_function_tensor(tensor: np.ndarray, basis_vectors: Callable[[float, float], np.ndarray], x, y)\
        -> Callable[[float, float], np.ndarray]:
    pass


@overload
def transform_function_tensor(tensor: np.ndarray, basis_vectors: Callable[[float, float, float], np.ndarray], x, y, z) \
        -> Callable[[float, float, float], np.ndarray]:
    pass


def transform_function_tensor(tensor, basis_vectors):
    """Transform a tensor to another coordinate system

    There are two coordinate systems x and u. The position dependent basis vectors of the latter one can be expressed
    as a linear combination of the former one.
    The input tensor in known in coordinate system u.
    This function transforms the input tensor to the coordinate system x.

    Parameters
    ----------
    tensor : np.ndarray
        (N,N) array as a tensor in the coordinate system u.
    basis_vectors : Callable[[float, float], np.ndarray] or Callable[[float, float, float], np.ndarray]
        A callable that takes two or three positional float arguments (a, b, c) and returns respectively a (2,2) or
        (3,3) array where in the i-th row there is the i-th basis vector of coordinate system u at the position (a, b)
        or (a, b, c) expressed in the basis vectors of a coordinate system x.

    Returns
    -------
    transformed_tensor: Callable[[float, float], np.ndarray] or Callable[[float, float, float], np.ndarray]
    The input tensor expressed in the coordinate system x is returned.
    It is a callable that takes two or three positional float arguments and returns respectively a (2,2) or (3,3)
    array that represents the input tensor expressed in the coordinate system x.
    """
    def transformed_tensor(*args):
        if tensor.shape == (2, 2):
            def transformed_tensor2d(x, y):
                input_basis_vectors = np.array(basis_vectors(x, y))
                transf_tensor = np.dot(np.dot(input_basis_vectors.transpose(), tensor), input_basis_vectors)
                return transf_tensor
            return transformed_tensor2d(*args)

        if tensor.shape == (3, 3):
            def transformed_tensor3d(x, y, z):
                input_basis_vectors = np.array(basis_vectors(x, y, z))
                transf_tensor = np.dot(np.dot(input_basis_vectors.transpose(), tensor), input_basis_vectors)
                return transf_tensor
            return transformed_tensor3d(*args)

        raise TransformationException(None, tensor)
    return transformed_tensor
