# coding=utf-8
"""Calculation of the permittivity tensor of a layered composite material.

.. sectionauthor:: Thyssen
"""

from abc import ABC, abstractmethod
import numpy as np
from pyrit.material import Permittivity
from pyrit.toolbox.TransformationToolbox import basis_from_constant_direction, transform_constant_tensor, \
    basis_from_function_direction, transform_function_tensor


class MixedPermittivity(Permittivity, ABC):
    r"""Class that represents the permittivity :math:`\epsilon` of a layered composite material"""

    @abstractmethod
    def __init__(self, permittivity_1, permittivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """
        Parameters: permittivity_1, permittivity_2, direction and ratio and parameters inherited from permittivity class

        Parameters
        ----------
        permittivity_1: float
            permittivity of material1
        permittivity_2: float
            permittivity of material2
        direction: np.ndarray or callable[[float, float], np.ndarray] or Callable[[float, float, float], np.ndarray]
            (N,) array with N=2 or N=3 as a vector which describes the direction perpendicular to a layer
            of the composite material or callable that takes two or three positional arguments and returns a (2,) or
            (3,) array as a vector which describes the direction perpendicular to a layer of the composite material
        ratio: float
            ratio of material1, as it is a layered material where each layer is constant in length, width and thickness,
            the total thickness of all layers belonging to material1 :math:`(x_1)` or material2 :math:`(x_2)`
            respectively can be used to calculate the ratio of material1 to the total material by
            :math:`ratio = x_1 / {(x_1 + x_2)}`.
        name: str
            name of the material
        data: np.ndarray, optional
            Data for a data-driven material.

        Returns
        -------
        None.

        """
        self.permittivity_1 = permittivity_1
        self.permittivity_2 = permittivity_2
        self.direction = direction
        self.ratio = ratio
        value = self._get_permittivity_tensor()

        super().__init__(value, name, data)

    @property
    def _perpendicular_permittivity(self):
        """Calculates the permittivity perpendicular to the layers

        Returns
        -------
        perpendicular_permittivity: float
            permittivity value perpendicular to the material's layers
        """
        perpendicular_permittivity = 1 / ((self.ratio / self.permittivity_1) + ((1 - self.ratio) / self.permittivity_2))
        return perpendicular_permittivity

    @property
    def _parallel_permittivity(self):
        """Calculates the permittivity parallel to the layers

        Returns
        -------
        parallel_permittivity: float
            permittivity value parallel to the material's layers
        """
        parallel_permittivity = self.ratio * self.permittivity_1 + (1 - self.ratio) * self.permittivity_2
        return parallel_permittivity

    @abstractmethod
    def _get_permittivity_tensor(self):
        """Calculate the permittivity tensor in the reference coordinate system x

        Returns
        -------
        permittivity_tensor: np.ndarray
            (N,N) permittivity tensor rotated in a reference coordinate system x.
        """


class MixedPermittivityCart(MixedPermittivity):
    r"""Class that represents the permittivity of a 2D layered composite material in a cartesian coordinate system"""

    def __init__(self, permittivity_1, permittivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of MixedPermittivity in a 2D cartesian coordinate system

        Parameters
        ----------
        permittivity_1: float
            permittivity of material1
        permittivity_2: float
            permittivity of material2
        direction: np.ndarray or callable[[float, float], np.ndarray]
            (2,) array as a vector which describes the direction perpendicular to a layer of the composite material
            or callable that takes two positional arguments and returns a (2,) array as a vector which describes the
            direction perpendicular to a layer of the composite material
        ratio: float
            ratio of material1, as it is a layered material where each layer is constant in length, width and thickness,
            the total thickness of all layers belonging to material1 :math:`(x_1)` or material2 :math:`(x_2)`
            respectively can be used to calculate the ratio of material1 to the total material by
            :math:`ratio = x_1 / {(x_1 + x_2)}`.
        name: str
            name of the material
        data: np.ndarray, optional
            Data for a data-driven material.
        """
        super().__init__(permittivity_1, permittivity_2, direction, ratio, name, data)

    def _get_permittivity_tensor(self):
        """Calculate the permittivity tensor in the reference 2D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_permittivity, 0], [0, self._parallel_permittivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            permittivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            permittivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return permittivity_tensor


class MixedPermittivityAxi(MixedPermittivity):
    r"""Class that represents the permittivity of a 3D layered composite material in a axisymmetric coordinate system"""

    def __init__(self, permittivity_1, permittivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of MixedPermittivity in a 3D axisymmetric coordinate system

        Parameters
        ----------
        permittivity_1: float
            permittivity of material1
        permittivity_2: float
            permittivity of material2
        direction: np.ndarray or callable[[float, float], np.ndarray]
            (2,) array as a vector which describes the direction perpendicular to a layer of the composite material
            or callable that takes two positional arguments and returns a (2,) array as a vector which describes the
            direction perpendicular to a layer of the composite material
        ratio: float
            ratio of material1, as it is a layered material where each layer is constant in length, width and thickness,
            the total thickness of all layers belonging to material1 :math:`(x_1)` or material2 :math:`(x_2)`
            respectively can be used to calculate the ratio of material1 to the total material by
            :math:`ratio = x_1 / {(x_1 + x_2)}`.
        name: str
            name of the material
        data: np.ndarray, optional
            Data for a data-driven material.
        """
        super().__init__(permittivity_1, permittivity_2, direction, ratio, name, data)

    def _get_permittivity_tensor(self):
        """Calculate the permittivity tensor in the reference axisymmetric coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_permittivity, 0], [0, self._parallel_permittivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            permittivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            permittivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return permittivity_tensor


class MixedPermittivity3D(MixedPermittivity):
    """Class that represents the permittivity of a 3D layered composite material in a cartesian coordinate system"""

    def __init__(self, permittivity_1, permittivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        r"""Calculation of MixedPermittivity in a 3D cartesian coordinate system

        Parameters
        ----------
        permittivity_1: float
            permittivity of material1
        permittivity_2: float
            permittivity of material2
        direction: np.ndarray or callable[[float, float, float], np.ndarray]
            (3,) array as a vector which describes the direction perpendicular to a layer of the composite material
            or callable that takes three positional arguments and returns a (3,) array as a vector which describes the
            direction perpendicular to a layer of the composite material
        ratio: float
            ratio of material1, as it is a layered material where each layer is constant in length, width and thickness,
            the total thickness of all layers belonging to material1 :math:`(x_1)` or material2 :math:`(x_2)`
            respectively can be used to calculate the ratio of material1 to the total material by
            :math:`ratio = x_1 / {(x_1 + x_2)}`.
        name: str
            name of the material
        data: np.ndarray, optional
            Data for a data-driven material
        """
        super().__init__(permittivity_1, permittivity_2, direction, ratio, name, data)

    def _get_permittivity_tensor(self):
        """Calculate the permittivity tensor in the reference 3D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_permittivity, 0, 0],
                                  [0, self._parallel_permittivity, 0],
                                  [0, 0, self._parallel_permittivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            permittivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            permittivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return permittivity_tensor
