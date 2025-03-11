# coding=utf-8
"""Calculation of the reluctivity tensor of a layered composite material.

.. sectionauthor:: Thyssen
"""

from abc import ABC, abstractmethod
import numpy as np
from pyrit.material import Reluctivity
from pyrit.toolbox.TransformationToolbox import basis_from_constant_direction, transform_constant_tensor, \
    basis_from_function_direction, transform_function_tensor


class MixedReluctivity(Reluctivity, ABC):
    r"""Class that represents the reluctivity :math:`\nu=\mu^{-1}` of a layered composite material"""

    @abstractmethod
    def __init__(self, reluctivity_1, reluctivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """
        Parameters: reluctivity_1, reluctivity_2, direction and ratio and parameters inherited from Reluctivity class.

        Parameters
        ----------
        reluctivity_1: float
            reluctivity of material1
        reluctivity_2: float
            reluctivity of material2
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
        self.reluctivity_1 = reluctivity_1
        self.reluctivity_2 = reluctivity_2
        self.direction = direction
        self.ratio = ratio
        value = self._get_reluctivity_tensor()

        super().__init__(value, name, data)

    @property
    def _perpendicular_reluctivity(self):
        """Calculates the reluctivity perpendicular to the layers

        Returns
        -------
        perpendicular_reluctivity: float
            reluctivity value perpendicular to the material's layers
        """
        perpendicular_reluctivity = self.ratio * self.reluctivity_1 + (1 - self.ratio) * self.reluctivity_2
        return perpendicular_reluctivity

    @property
    def _parallel_reluctivity(self):
        """Calculates the reluctivity parallel to the layers

        Returns
        -------
        parallel_reluctivity: float
            reluctivity value parallel to the material's layers
        """
        parallel_reluctivity = 1 / ((self.ratio / self.reluctivity_1) + ((1 - self.ratio) / self.reluctivity_2))
        return parallel_reluctivity

    @abstractmethod
    def _get_reluctivity_tensor(self):
        """Calculate the reluctivity tensor in the reference coordinate system x

        Returns
        -------
        reluctivity_tensor: np.ndarray
            (N,N) reluctivity tensor rotated in a reference coordinate system x.
        """


class MixedReluctivityCart(MixedReluctivity):
    r"""Class that represents the reluctivity of a 2D layered composite material in a cartesian coordinate system"""

    def __init__(self, reluctivity_1, reluctivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of MixedReluctivity in a 2D cartesian coordinate system

        Parameters
        ----------
        reluctivity_1: float
            reluctivity of material1
        reluctivity_2: float
            reluctivity of material2
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
        super().__init__(reluctivity_1, reluctivity_2, direction, ratio, name, data)

    def _get_reluctivity_tensor(self):
        """Calculate the reluctivity tensor in the reference 2D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_reluctivity, 0], [0, self._parallel_reluctivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            reluctivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            reluctivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return reluctivity_tensor


class MixedReluctivityAxi(MixedReluctivity):
    r"""Class that represents the reluctivity of a 3D layered composite material in a axisymmetric coordinate system"""

    def __init__(self, reluctivity_1, reluctivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of MixedReluctivity in a 3D axisymmetric coordinate system

        Parameters
        ----------
        reluctivity_1: float
            reluctivity of material1
        reluctivity_2: float
            reluctivity of material2
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
        super().__init__(reluctivity_1, reluctivity_2, direction, ratio, name, data)

    def _get_reluctivity_tensor(self):
        """Calculate the reluctivity tensor in the reference axisymmetric coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_reluctivity, 0], [0, self._parallel_reluctivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            reluctivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            reluctivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return reluctivity_tensor


class MixedReluctivity3D(MixedReluctivity):
    """Class that represents the reluctivity of a 3D layered composite material in a cartesian coordinate system"""

    def __init__(self, reluctivity_1, reluctivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        r"""Calculation of MixedReluctivity in a 3D cartesian coordinate system

        Parameters
        ----------
        reluctivity_1: float
            reluctivity of material1
        reluctivity_2: float
            reluctivity of material2
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
        super().__init__(reluctivity_1, reluctivity_2, direction, ratio, name, data)

    def _get_reluctivity_tensor(self):
        """Calculate the reluctivity tensor in the reference 3D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_reluctivity, 0, 0],
                                  [0, self._parallel_reluctivity, 0],
                                  [0, 0, self._parallel_reluctivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            reluctivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            reluctivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return reluctivity_tensor
