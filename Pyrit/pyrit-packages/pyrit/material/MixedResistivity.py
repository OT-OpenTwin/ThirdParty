# coding=utf-8
"""Calculation of the resistivity tensor of a layered composite material.

.. sectionauthor:: Thyssen
"""

from abc import ABC, abstractmethod
import numpy as np
from pyrit.material import Resistivity
from pyrit.toolbox.TransformationToolbox import basis_from_constant_direction, transform_constant_tensor, \
    basis_from_function_direction, transform_function_tensor


class MixedResistivity(Resistivity, ABC):
    r"""Class that represents the resistivity :math:`\rho=\sigma^{-1}` of a layered composite material"""

    @abstractmethod
    def __init__(self, resistivity_1, resistivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """
        Parameters: resistivity_1, resistivity_2, direction and ratio and parameters inherited from resistivity class.

        Parameters
        ----------
        resistivity_1: float
            resistivity of material1
        resistivity_2: float
            resistivity of material2
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
        self.resistivity_1 = resistivity_1
        self.resistivity_2 = resistivity_2
        self.direction = direction
        self.ratio = ratio
        value = self._get_resistivity_tensor()

        super().__init__(value, name, data)

    @property
    def _perpendicular_resistivity(self):
        """Calculates the resistivity perpendicular to the layers

        Returns
        -------
        perpendicular_resistivity: float
            resistivity value perpendicular to the material's layers
        """
        perpendicular_resistivity = self.ratio * self.resistivity_1 + (1 - self.ratio) * self.resistivity_2
        return perpendicular_resistivity

    @property
    def _parallel_resistivity(self):
        """Calculates the resistivity parallel to the layers

        Returns
        -------
        parallel_resistivity: float
            resistivity value parallel to the material's layers
        """
        parallel_resistivity = 1 / ((self.ratio / self.resistivity_1) + ((1 - self.ratio) / self.resistivity_2))
        return parallel_resistivity

    @abstractmethod
    def _get_resistivity_tensor(self):
        """Calculate the resistivity tensor in the reference coordinate system x

        Returns
        -------
        resistivity_tensor: np.ndarray
            (N,N) resistivity tensor rotated in a reference coordinate system x.
        """


class MixedResistivityCart(MixedResistivity):
    r"""Class that represents the resistivity of a 2D layered composite material in a cartesian coordinate system"""

    def __init__(self, resistivity_1, resistivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of MixedResistivity in a 2D cartesian coordinate system

        Parameters
        ----------
        resistivity_1: float
            resistivity of material1
        resistivity_2: float
            resistivity of material2
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
        super().__init__(resistivity_1, resistivity_2, direction, ratio, name, data)

    def _get_resistivity_tensor(self):
        """Calculate the resistivity tensor in the reference 2D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_resistivity, 0], [0, self._parallel_resistivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            resistivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            resistivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return resistivity_tensor


class MixedResistivityAxi(MixedResistivity):
    r"""Class that represents the resistivity of a 3D layered composite material in a axisymmetric coordinate system"""

    def __init__(self, resistivity_1, resistivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of MixedResistivity in a 3D axisymmetric coordinate system

        Parameters
        ----------
        resistivity_1: float
            resistivity of material1
        resistivity_2: float
            resistivity of material2
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
        super().__init__(resistivity_1, resistivity_2, direction, ratio, name, data)

    def _get_resistivity_tensor(self):
        """Calculate the resistivity tensor in the reference axisymmetric coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_resistivity, 0], [0, self._parallel_resistivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            resistivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            resistivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return resistivity_tensor


class MixedResistivity3D(MixedResistivity):
    """Class that represents the resistivity of a 3D layered composite material in a cartesian coordinate system"""

    def __init__(self, resistivity_1, resistivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        r"""Calculation of MixedResistivity in a 3D cartesian coordinate system

        Parameters
        ----------
        resistivity_1: float
            resistivity of material1
        resistivity_2: float
            resistivity of material2
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
        super().__init__(resistivity_1, resistivity_2, direction, ratio, name, data)

    def _get_resistivity_tensor(self):
        """Calculate the resistivity tensor in the reference 3D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_resistivity, 0, 0],
                                  [0, self._parallel_resistivity, 0],
                                  [0, 0, self._parallel_resistivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            resistivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            resistivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return resistivity_tensor
