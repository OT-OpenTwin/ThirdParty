# coding=utf-8
"""Class representing anisotropic property.

.. sectionauthor:: Bundschuh, Thyssen
"""

from typing import Union, Callable, Tuple
import numpy as np
from pyrit.toolbox.TransformationToolbox import transform_constant_tensor
from pyrit.material import MatProperty


def _from_inhomogeneous_linear_2d_basis_constant(properties: Tuple[MatProperty, MatProperty],
                                                 local_basis: np.ndarray = None)\
        -> Callable[[float, float], np.ndarray]:
    """Method to get anisotropic material tensor for a 2d linear material where at least one property is inhomogeneous\
    and the basis is None or constant

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty]
        A maximum of two properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : np.ndarray, optional
        The local basis. Default is the global basis. Equivalent to identity tensor

    Returns
    -------
    calculate_from_inhomogeneous_linear_2d_basis_constant: Callable[[float, float], np.ndarray]
        callable that returns the anisotropic property tensor for the coordinates x and y
    """

    def calculate_from_inhomogeneous_linear_2d_basis_constant(x, y):
        tensor = np.zeros((2, 2))
        for i, prop in enumerate(properties):
            if not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y]]]))
            else:
                value = prop.evaluate()
            if value is not None:
                tensor[i, i] = value
        if isinstance(local_basis, np.ndarray):
            return transform_constant_tensor(tensor, local_basis)
        return tensor

    return calculate_from_inhomogeneous_linear_2d_basis_constant


def _from_inhomogeneous_linear_2d_basis_callable(properties: Tuple[MatProperty, MatProperty],
                                                 local_basis: Callable[[float, float], np.ndarray])\
        -> Callable[[float, float], np.ndarray]:
    """Method to get anisotropic material tensor for a 2d linear material where at least one property is inhomogeneous\
    and the basis is callable

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty]
        A maximum of two properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : Callable[[float, float], np.ndarray]
        The local basis. Accepts x and y arguments and returns the tensor of basis vectors.

    Returns
    -------
    calculate_from_inhomogeneous_linear_2d_basis_callable: Callable[[float, float], np.ndarray]
        callable that returns the anisotropic property tensor for the coordinates x and y
    """

    def calculate_from_inhomogeneous_linear_2d_basis_callable(x, y):
        tensor = np.zeros((2, 2))
        basis = local_basis(x, y)
        for i, prop in enumerate(properties):
            if not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y]]]))
            else:
                value = prop.evaluate()
            tensor[i, i] = value
        return transform_constant_tensor(tensor, basis)

    return calculate_from_inhomogeneous_linear_2d_basis_callable


def _from_inhomogeneous_linear_3d_basis_constant(properties: Tuple[MatProperty, MatProperty, MatProperty],
                                                 local_basis: np.ndarray)\
        -> Callable[[float, float, float], np.ndarray]:
    """Method to get anisotropic material tensor for a 3d linear material where at least one property is inhomogeneous\
    and the basis is None or constant

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty, MatProperty]
        A maximum of three properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : np.ndarray, optional
        The local basis. Default is the global basis. Equivalent to identity tensor

    Returns
    -------
    calculate_from_inhomogeneous_linear_3d_basis_constant: Callable[[float, float, float], np.ndarray]
        calllable that returns the anisotropic property tensor for the coordinates x, y and z
    """

    def calculate_from_inhomogeneous_linear_3d_basis_constant(x, y, z):
        tensor = np.zeros((3, 3))
        for i, prop in enumerate(properties):
            if not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y, z]]]))
            else:
                value = prop.evaluate()
            if value is not None:
                tensor[i, i] = value
        if isinstance(local_basis, np.ndarray):
            return transform_constant_tensor(tensor, local_basis)
        return tensor

    return calculate_from_inhomogeneous_linear_3d_basis_constant


def _from_inhomogeneous_linear_3d_basis_callable(properties: Tuple[MatProperty, MatProperty, MatProperty],
                                                 local_basis: Callable[[float, float, float], np.ndarray])\
        -> Callable[[float, float, float], np.ndarray]:
    """Method to get anisotropic material tensor for a 3d linear material where at least one property is inhomogeneous\
    and the basis is callable

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty, MatProperty]
        A maximum of three properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : Callable[[float, float, float], np.ndarray]
        The local basis. Accepts x, y and z arguments and returns the tensor of basis vectors.

    Returns
    -------
    calculate_from_inhomogeneous_linear_3d_basis_callable: Callable[[float, float, float], np.ndarray]
         callable that returns the anisotropic property tensor for the coordinates x, y and z
    """

    def calculate_from_inhomogeneous_linear_3d_basis_callable(x, y, z):
        tensor = np.zeros((3, 3))
        basis = local_basis(x, y, z)
        for i, prop in enumerate(properties):
            if not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y, z]]]))
            else:
                value = prop.evaluate()
            if value is not None:
                tensor[i, i] = value
        return transform_constant_tensor(tensor, basis)

    return calculate_from_inhomogeneous_linear_3d_basis_callable


def _from_homogeneous_nonlinear_basis_constant(properties: Union[Tuple[MatProperty, MatProperty],
                                                                 Tuple[MatProperty, MatProperty, MatProperty]],
                                               local_basis: np.ndarray = None) -> Callable[[np.ndarray], np.ndarray]:
    """Method to get anisotropic material tensor for a homogeneous material where at least one property is nonlinear

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty] or Tuple[MatProperty, MatProperty, MatProperty]
        A maximum of three properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : np.ndarray, optional
        The local basis. Default is the global basis. Equivalent to identity tensor

    Returns
    -------
    calculate_from_homogeneous_nonlinear_basis_constant: Callable[[np.ndarray], np.ndarray]
         callable that returns the anisotropic property tensor for the specified element
    """

    def calculate_from_homogeneous_nonlinear_basis_constant(element=None):
        if element is None:
            element = np.array([1])  # needed for isotrop check
        dimension = len(properties)
        number_of_elements = element.size
        tensor = np.zeros((number_of_elements, dimension, dimension))
        for i, prop in enumerate(properties):
            if not prop.is_linear:
                value = prop.evaluate(elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,), (N, 2, 2) for 2D case or (N, 3, 3)"
                                     f"for 3D case can be handeled in homogeneous nonlinear case. The current shape is"
                                     f"{value.shape}.")
            else:
                value = prop.evaluate()
                tensor[:, i, i] = value
        if isinstance(local_basis, np.ndarray):
            for i in range(tensor.shape[0]):
                tensor[i] = transform_constant_tensor(tensor[i], local_basis)
        return tensor

    return calculate_from_homogeneous_nonlinear_basis_constant


def _from_homogeneous_nonlinear_2d_basis_callable(properties: Tuple[MatProperty, MatProperty],
                                                  local_basis: Callable[[float, float], np.ndarray])\
        -> Callable[[float, float, np.ndarray], np.ndarray]:
    """Method to get anisotropic material tensor for a 2d homogeneous material where at least one property is nonlinear\
    and the basis is callable

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty]
        A maximum of two properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : Callable[[float, float], np.ndarray]
        The local basis. Accepts x and y arguments and returns the tensor of basis vectors.

    Returns
    -------
    calculate_from_homogeneous_nonlinear_2d_basis_callable: Callable[[float, float, np.ndarray], np.ndarray]
        callable that returns the anisotropic property tensor for the specified element
    """

    def calculate_from_homogeneous_nonlinear_2d_basis_callable(x, y, element=None):
        if element is None:
            element = np.array([1])  # needed for isotrop check
        dimension = len(properties)
        number_of_elements = element.size
        tensor = np.zeros((number_of_elements, dimension, dimension))
        basis = local_basis(x, y)
        for i, prop in enumerate(properties):
            if not prop.is_linear:
                value = prop.evaluate(elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 2, 2) can be handeled in"
                                     f"homogeneous nonlinear 2D case. The current shape is {value.shape}.")
            else:
                value = prop.evaluate()
                tensor[:, i, i] = value
        for i in range(tensor.shape[0]):
            tensor[i] = transform_constant_tensor(tensor[i], basis)
        return tensor

    return calculate_from_homogeneous_nonlinear_2d_basis_callable


def _from_homogeneous_nonlinear_3d_basis_callable(properties: Tuple[MatProperty, MatProperty, MatProperty],
                                                  local_basis: Callable[[float, float, float], np.ndarray])\
        -> Callable[[float, float, float, np.ndarray], np.ndarray]:
    """Method to get anisotropic material tensor for a 3d homogeneous material where at least one property is nonlinear\
    and the basis is callable

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty, MatProperty]
        A maximum of three properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : Callable[[float, float, float], np.ndarray]
        The local basis. Accepts x, y and z arguments and returns the tensor of basis vectors.

    Returns
    -------
    calculate_from_homogeneous_nonlinear_3d_basis_callable: Callable[[float, float, float, np.ndarray], np.ndarray]
        callable that returns the anisotropic property tensor for the specified element
    """

    def calculate_from_homogeneous_nonlinear_3d_basis_callable(x, y, z, element=None):
        if element is None:
            element = np.array([1])  # needed for isotrop check
        dimension = len(properties)
        number_of_elements = element.size
        tensor = np.zeros((number_of_elements, dimension, dimension))
        basis = local_basis(x, y, z)

        for i, prop in enumerate(properties):
            if not prop.is_linear:
                value = prop.evaluate(elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 3, 3) can be handeled in"
                                     f"homogeneous nonlinear 3D case. The current shape is {value.shape}.")
            else:
                value = prop.evaluate()
                tensor[:, i, i] = value
        for i in range(tensor.shape[0]):
            tensor[i] = transform_constant_tensor(tensor[i], basis)
        return tensor
    return calculate_from_homogeneous_nonlinear_3d_basis_callable


def _from_homogeneous_linear_basis_constant(properties: Union[Tuple[MatProperty, MatProperty],
                                                              Tuple[MatProperty, MatProperty, MatProperty]],
                                            local_basis: np.ndarray = None) -> Callable[[], np.ndarray]:
    """Method to get anisotropic material tensor for a linear and homogeneous material and a constant basis

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty] or Tuple[MatProperty, MatProperty, MatProperty]
        A maximum of three properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : np.ndarray, optional
        The local basis. Default is the global basis. Equivalent to identity tensor

    Returns
    -------
    calculate_from_homogeneous_linear_basis_constant: Callable[[], np.ndarray]
        callable that that returns the anisotropic property tensor of the material
    """
    dimension = len(properties)
    tensor = np.zeros((dimension, dimension))
    for i, prop in enumerate(properties):
        value = prop.evaluate()
        if value is not None:
            tensor[i, i] = value
    if isinstance(local_basis, np.ndarray):
        tensor = transform_constant_tensor(tensor, local_basis)

    def calculate_from_homogeneous_linear_basis_constant():
        return tensor

    return calculate_from_homogeneous_linear_basis_constant()


def _from_homogeneous_linear_2d_basis_callable(properties: Tuple[MatProperty, MatProperty],
                                               local_basis: Callable[[float, float], np.ndarray])\
        -> Callable[[float, float], np.ndarray]:
    """Method to get anisotropic material tensor for a 2d linear and homogeneous material and a callable basis

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty]
        A maximum of two properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : Callable[[float, float], np.ndarray]
        The local basis. Accepts x and y arguments and returns the tensor of basis vectors.

    Returns
    -------
    calculate_from_homogeneous_linear_2d_basis_callable: Callable[[float, float], np.ndarray]
        Callable that returns the anisotropic property tensor for the coordinates x, y
    """

    def calculate_from_homogeneous_linear_2d_basis_callable(x, y):
        basis = local_basis(x, y)
        tensor = np.zeros((2, 2))
        for i, prop in enumerate(properties):
            value = prop.evaluate()
            if value is not None:
                tensor[i, i] = value
        return transform_constant_tensor(tensor, basis)

    return calculate_from_homogeneous_linear_2d_basis_callable


def _from_homogeneous_linear_3d_basis_callable(properties: Tuple[MatProperty, MatProperty, MatProperty],
                                               local_basis: Callable[[float, float, float], np.ndarray])\
        -> Callable[[float, float, float], np.ndarray]:
    """Method to get anisotropic material tensor for a 3d linear and homogeneous material with a callable basis

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty, MatProperty]
        A Maximum of three properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : Callable[[float, float, float], np.ndarray]
        The local basis. Accepts x, y and z arguments and returns the tensor of basis vectors.

    Returns
    -------
    calculate_from_homogeneous_linear_3d_basis_callable: Callable[[float, float, float], np.ndarray]
        Callable that returns the anisotropic property tensor for the coordinates x, y and z
    """

    def calculate_from_homogeneous_linear_3d_basis_callable(x, y, z):
        basis = local_basis(x, y, z)
        tensor = np.zeros((3, 3))
        for i, prop in enumerate(properties):
            value = prop.evaluate()
            if value is not None:
                tensor[i, i] = value
        return transform_constant_tensor(tensor, basis)

    return calculate_from_homogeneous_linear_3d_basis_callable


def _from_inhomogeneous_nonlinear_2d_basis_constant(properties: Tuple[MatProperty, MatProperty],
                                                    local_basis: np.ndarray = None)\
        -> Callable[[float, float, np.ndarray], np.ndarray]:
    """Method to get anisotropic material tensor for a 2d material which is at least in one direction nonlinear and at\
    least in one direction inhomogeneous with a constant basis

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty]
        A Maximum of two properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : np.ndarray, optional
        The local basis. Default is the global basis. Equivalent to identity tensor

    Returns
    -------
    calculate_from_inhomogeneous_nonlinear_2d_basis_constant: Callable[[float, float, np.ndarray], np.ndarray]
    Callable returning anisotropic property tensor for 2d material for the coordinates x, y and element
    """

    def calculate_from_inhomogeneous_nonlinear_2d_basis_constant(x, y, element=None):
        if element is None:
            element = np.array([1])  # needed for isotrop check
        dimension = len(properties)
        number_of_elements = element.size
        tensor = np.zeros((number_of_elements, dimension, dimension))
        for i, prop in enumerate(properties):
            if not prop.is_linear and not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y]]]), elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 2, 2) can be handeled in"
                                     f"inhomogeneous nonlinear 2D case. The current shape is {value.shape}.")
            if not prop.is_linear and prop.is_homogeneous:
                value = prop.evaluate(elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 2, 2) can be handeled in"
                                     f"inhomogeneous nonlinear 2D case. The current shape is {value.shape}.")
            if prop.is_linear and not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y]]]))
                tensor[:, i, i] = value
            if prop.is_linear and prop.is_homogeneous:
                value = prop.evaluate()
                tensor[:, i, i] = value
        if isinstance(local_basis, np.ndarray):
            for i in range(tensor.shape[0]):
                tensor[i] = transform_constant_tensor(tensor[i], local_basis)
        return tensor

    return calculate_from_inhomogeneous_nonlinear_2d_basis_constant


def _from_inhomogeneous_nonlinear_2d_basis_callable(properties: Tuple[MatProperty, MatProperty],
                                                    local_basis: Callable[[float, float], np.ndarray])\
        -> Callable[[float, float, np.ndarray], np.ndarray]:
    """Method to get anisotropic material tensor for a 2d material which is at least in one direction nonlinear and at\
    least in one direction inhomogeneous with a callable basis

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty]
        A maximum of two properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : Callable[[float, float], np.ndarray]
        The local basis. Accepts x and y arguments and returns the tensor of basis vectors.

    Returns
    -------
    calculate_from_inhomogeneous_nonlinear_2d_basis_callable: Callable[[float, float, np.ndarray], np.ndarray]
        callable returning anisotropic property tensor for 2d material for the coordinates x, y and element
    """

    def calculate_from_inhomogeneous_nonlinear_2d_basis_callable(x, y, element=None):
        if element is None:
            element = np.array([1])  # needed for isotrop check
        dimension = len(properties)
        number_of_elements = element.size
        tensor = np.zeros((number_of_elements, dimension, dimension))
        basis = local_basis(x, y)

        for i, prop in enumerate(properties):
            if not prop.is_linear and not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y]]]), elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 2, 2) can be handeled in"
                                     f"inhomogeneous nonlinear 2D case. The current shape is {value.shape}.")
            if not prop.is_linear and prop.is_homogeneous:
                value = prop.evaluate(elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 2, 2) can be handeled in"
                                     f"inhomogeneous nonlinear 2D case. The current shape is {value.shape}.")
            if prop.is_linear and not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y]]]))
                tensor[:, i, i] = value
            if prop.is_linear and prop.is_homogeneous:
                value = prop.evaluate()
                tensor[:, i, i] = value
        for i in range(tensor.shape[0]):
            tensor[i] = transform_constant_tensor(tensor[i], basis)
        return tensor
    return calculate_from_inhomogeneous_nonlinear_2d_basis_callable


def _from_inhomogeneous_nonlinear_3d_basis_constant(properties: Tuple[MatProperty, MatProperty, MatProperty],
                                                    local_basis: np.ndarray = None)\
        -> Callable[[float, float, float, np.ndarray], np.ndarray]:
    """Method to get anisotropic material tensor for a 3d material which is at least in one direction nonlinear and at\
    least in one direction inhomogeneous with a constant basis

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty, MatProperty]
        A Maximum of two properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : np.ndarray, optional
        The local basis. Default is the global basis. Equivalent to identity tensor

    Returns
    -------
    calculate_from_inhomogeneous_nonlinear_3d_basis_constant: Callable[[float, float, float, np.ndarray], np.ndarray]
        Callable returning anisotropic propertytensor for 3d material for the coordinates x, y, z and element
    """

    def calculate_from_inhomogeneous_nonlinear_3d_basis_constant(x, y, z, element=None):
        if element is None:
            element = np.array([1])  # needed for isotrop check
        dimension = len(properties)
        number_of_elements = element.size
        tensor = np.zeros((number_of_elements, dimension, dimension))
        for i, prop in enumerate(properties):
            if not prop.is_linear and not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y, z]]]), elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 3, 3) can be handeled in"
                                     f"inhomogeneous nonlinear 3D case. The current shape is {value.shape}.")
            if not prop.is_linear and prop.is_homogeneous:
                value = prop.evaluate(elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 3, 3) can be handeled in"
                                     f"inhomogeneous nonlinear 3D case. The current shape is {value.shape}.")
            if prop.is_linear and not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y, z]]]))
                tensor[:, i, i] = value
            if prop.is_linear and prop.is_homogeneous:
                value = prop.evaluate()
                tensor[:, i, i] = value
        if isinstance(local_basis, np.ndarray):
            for i in range(tensor.shape[0]):
                tensor[i] = transform_constant_tensor(tensor[i], local_basis)
        return tensor

    return calculate_from_inhomogeneous_nonlinear_3d_basis_constant


def _from_inhomogeneous_nonlinear_3d_basis_callable(properties: Tuple[MatProperty, MatProperty, MatProperty],
                                                    local_basis: Callable[[float, float, float], np.ndarray])\
        -> Callable[[float, float, float, np.ndarray], np.ndarray]:
    """Method to get anisotropic material tensor for a 3d material which is at least in one direction nonlinear and at\
    least in one direction inhomogeneous

    Parameters
    ----------
    properties : Tuple[MatProperty, MatProperty, MatProperty]
        A Maximum of three properties. One for each direction. They must be of the same type and not be anisotropic
    local_basis : Callable[[float, float, float], np.ndarray]
        The local basis. Accepts x, y and z arguments and returns the tensor of basis vectors.

    Returns
    -------
    calculate_from_inhomogeneous_nonlinear_3d_basis_callable: Callable[[float, float, float, np.ndarray], np.ndarray]
        Callable returning anisotropic property tensor for 3d material for the coordinates x, y, z and element
    """

    def calculate_from_inhomogeneous_nonlinear_3d_basis_callable(x, y, z, element=None):
        if element is None:
            element = np.array([1])  # needed for isotrop check
        dimension = len(properties)
        number_of_elements = element.size
        tensor = np.zeros((number_of_elements, dimension, dimension))
        basis = local_basis(x, y, z)
        for i, prop in enumerate(properties):
            if not prop.is_linear and not prop.is_homogeneous:
                value = prop.evaluate(np.array([[x, y, z]]), elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 3, 3) can be handeled in"
                                     f"inhomogeneous nonlinear 3D case. The current shape is {value.shape}.")
            if not prop.is_linear and prop.is_homogeneous:
                value = prop.evaluate(elements=element)
                if len(value.shape) == 1:
                    tensor[:, i, i] = value
                elif len(value.shape) == 3:
                    for j in range(dimension):
                        for k in range(dimension):
                            tensor[:, j, k] += value[:, j, k] / dimension
                else:
                    raise ValueError(f"Only values that return arrays of shape (N,) or (N, 3, 3) can be handeled in"
                                     f"inhomogeneous nonlinear 3D case. The current shape is {value.shape}.")
            if prop.is_linear and not prop.is_homogeneous:
                value = prop.evaluate(np.array([[[x, y, z]]]))
                tensor[:, i, i] = value
            if prop.is_linear and prop.is_homogeneous:
                value = prop.evaluate()
                tensor[:, i, i] = value
        for i in range(tensor.shape[0]):
            tensor[i] = transform_constant_tensor(tensor[i], basis)
        return tensor

    return calculate_from_inhomogeneous_nonlinear_3d_basis_callable


class AnisotropicProperty:
    """Class constructing an anisotropic property tensor from different MatProperties in different spatial directions"""

    def __init__(self, *properties, local_basis=None):
        """Constructor

        Parameters
        ----------
        properties : MatProperty
            A maximum of three properties. One for each direction. They must be of the same type and not be anisotropic.
        local_basis : np.ndarray or Callable
            The local basis. Default is the global basis. Equivalent to identity tensor.

        Examples
        --------
        One defines the single properties for the directions:

        >>> conductivity_x = Conductivity(1e7)
        >>> conductivity_y = Conductivity(1e6)
        >>> conductivity_z = Conductivity(1e5)

        Then, they are combined into an anisotropic property:

        >>> anisotropic_conductivity = AnisotropicProperty(conductivity_x, conductivity_y, conductivity_z)

        This acts as input for the Property that is used in the simulation.

        >>> conductivity = Conductivity(anisotropic_conductivity.get_property())

        In this case, since all conductivities in the tree direction were constant and the basis was constant, the
        property is a constant tensor.
        """
        if not all(isinstance(prop, MatProperty) for prop in properties):
            raise TypeError("All properties must be instances of MatProperty.")

        if local_basis is not None and not isinstance(local_basis, (np.ndarray, Callable)):
            raise TypeError("local_basis must be either None, a np.ndarray, or a callable function.")
        self.properties = properties
        self.local_basis = local_basis

    def get_property(self) -> Union[np.ndarray, Callable[[float, float, float], np.ndarray],
                                    Callable[[float, float], np.ndarray], Callable[[np.ndarray], np.ndarray],
                                    Callable[[float, float, float], np.ndarray],
                                    Callable[[float, float, np.ndarray], np.ndarray]]:
        """Return the property

        Returns
        -------
        Union[np.ndarray, Callable]
            - A constant tensor (numpy.ndarray)
            - A function returning a tensor. The function can depend on:
                - The space coordinates, either (float, float) for 2D or (float, float, float) for 3D
                - The field (np.ndarray)
                - Both the space coordinates and the field

        """
        # nonlinear and inhomogeneous possible, three kind of bases
        if any(not prop.is_linear for prop in self.properties) and \
                any(not prop.is_homogeneous for prop in self.properties):
            if self.local_basis is None or isinstance(self.local_basis, np.ndarray):
                if len(self.properties) == 2:
                    return _from_inhomogeneous_nonlinear_2d_basis_constant(self.properties, self.local_basis)
                if len(self.properties) == 3:
                    return _from_inhomogeneous_nonlinear_3d_basis_constant(self.properties, self.local_basis)
            if callable(self.local_basis):
                if len(self.properties) == 2:
                    return _from_inhomogeneous_nonlinear_2d_basis_callable(self.properties, self.local_basis)
                if len(self.properties) == 3:
                    return _from_inhomogeneous_nonlinear_3d_basis_callable(self.properties, self.local_basis)

        # nonlinear possible, homogeneous, three kind of bases
        if any(not prop.is_linear for prop in self.properties) and all(prop.is_homogeneous for prop in self.properties):
            if self.local_basis is None or isinstance(self.local_basis, np.ndarray):
                return _from_homogeneous_nonlinear_basis_constant(self.properties, self.local_basis)
            if callable(self.local_basis):
                if len(self.properties) == 2:
                    return _from_homogeneous_nonlinear_2d_basis_callable(self.properties, self.local_basis)
                if len(self.properties) == 3:
                    return _from_homogeneous_nonlinear_3d_basis_callable(self.properties, self.local_basis)

        # inhomogeneous possible, linear, three kind of bases
        if any(not prop.is_homogeneous for prop in self.properties) and all(prop.is_linear for prop in self.properties):
            if self.local_basis is None or isinstance(self.local_basis, np.ndarray):
                if len(self.properties) == 2:
                    return _from_inhomogeneous_linear_2d_basis_constant(self.properties, self.local_basis)
                if len(self.properties) == 3:
                    return _from_inhomogeneous_linear_3d_basis_constant(self.properties, self.local_basis)
            if callable(self.local_basis):
                if len(self.properties) == 2:
                    return _from_inhomogeneous_linear_2d_basis_callable(self.properties, self.local_basis)
                if len(self.properties) == 3:
                    return _from_inhomogeneous_linear_3d_basis_callable(self.properties, self.local_basis)

        # homogeneous and linear, three kind of bases
        else:
            if self.local_basis is None or isinstance(self.local_basis, np.ndarray):
                return _from_homogeneous_linear_basis_constant(self.properties, self.local_basis)
            if callable(self.local_basis):
                if len(self.properties) == 2:
                    return _from_homogeneous_linear_2d_basis_callable(self.properties, self.local_basis)
                if len(self.properties) == 3:
                    return _from_homogeneous_linear_3d_basis_callable(self.properties, self.local_basis)

        raise ValueError("Properties or local_basis are not defined correctly. The local_basis should be none, a "
                         "constant np.ndarray or a callable accepting two or three spatial coordinates. The "
                         "properties should be Property objects inheriting from the MatProperty class")
