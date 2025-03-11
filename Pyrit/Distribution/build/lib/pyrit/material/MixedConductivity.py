# coding=utf-8
"""Calculation of the conductivity tensor of a layered composite material.

.. sectionauthor:: Thyssen
"""

from abc import ABC, abstractmethod
import numpy as np
from pyrit.material import Conductivity
from pyrit.toolbox.TransformationToolbox import basis_from_constant_direction, transform_constant_tensor, \
    basis_from_function_direction, transform_function_tensor


class MixedConductivity(Conductivity, ABC):
    r"""Class that represents the conductivity :math:`\sigma=\rho^{-1}` of a layered composite material"""

    @abstractmethod
    def __init__(self, conductivity_1, conductivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """
        Parameters: conductivity_1, conductivity_2, direction and ratio and parameters inherited from conductivity class

        Parameters
        ----------
        conductivity_1: float
            conductivity of material1
        conductivity_2: float
            conductivity of material2
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
        self.conductivity_1 = conductivity_1
        self.conductivity_2 = conductivity_2
        self.direction = direction
        self.ratio = ratio
        value = self._get_conductivity_tensor()

        super().__init__(value, name, data)

    @property
    def _perpendicular_conductivity(self):
        """Calculates the conductivity perpendicular to the layers

        Returns
        -------
        perpendicular_conductivity: float
            conductivity value perpendicular to the material's layers
        """
        perpendicular_conductivity = 1 / ((self.ratio / self.conductivity_1) + ((1 - self.ratio) / self.conductivity_2))
        return perpendicular_conductivity

    @property
    def _parallel_conductivity(self):
        """Calculates the conductivity parallel to the layers

        Returns
        -------
        parallel_conductivity: float
            conductivity value parallel to the material's layers
        """
        parallel_conductivity = self.ratio * self.conductivity_1 + (1 - self.ratio) * self.conductivity_2
        return parallel_conductivity

    @abstractmethod
    def _get_conductivity_tensor(self):
        """Calculate the conductivity tensor in the reference coordinate system x

        Returns
        -------
        conductivity_tensor: np.ndarray
            (N,N) conductivity tensor rotated in a reference coordinate system x.
        """


class MixedConductivityCart(MixedConductivity):
    r"""Class that represents the conductivity of a 2D layered composite material in a cartesian coordinate system"""

    def __init__(self, conductivity_1, conductivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of MixedConductivity in a 2D cartesian coordinate system

        Parameters
        ----------
        conductivity_1: float
            conductivity of material1
        conductivity_2: float
            conductivity of material2
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
        super().__init__(conductivity_1, conductivity_2, direction, ratio, name, data)

    def _get_conductivity_tensor(self):
        """Calculate the conductivity tensor in the reference 2D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_conductivity, 0], [0, self._parallel_conductivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            conductivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            conductivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return conductivity_tensor


class MixedConductivityAxi(MixedConductivity):
    r"""Class that represents the conductivity of a 3D layered composite material in a axisymmetric coordinate system"""

    def __init__(self, conductivity_1, conductivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of Mixedconductivity in a 3D axisymmetric coordinate system

        Parameters
        ----------
        conductivity_1: float
            conductivity of material1
        conductivity_2: float
            conductivity of material2
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
        super().__init__(conductivity_1, conductivity_2, direction, ratio, name, data)

    def _get_conductivity_tensor(self):
        """Calculate the conductivity tensor in the reference axisymmetric coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_conductivity, 0], [0, self._parallel_conductivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            conductivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            conductivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return conductivity_tensor


class MixedConductivity3D(MixedConductivity):
    """Class that represents the conductivity of a 3D layered composite material in a cartesian coordinate system"""

    def __init__(self, conductivity_1, conductivity_2, direction, ratio, name: str = '', data: np.ndarray = None):
        r"""Calculation of MixedConductivity in a 3D cartesian coordinate system

        Parameters
        ----------
        conductivity_1: float
            conductivity of material1
        conductivity_2: float
            conductivity of material2
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
        super().__init__(conductivity_1, conductivity_2, direction, ratio, name, data)

    def _get_conductivity_tensor(self):
        """Calculate the conductivity tensor in the reference 3D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_conductivity, 0, 0],
                                  [0, self._parallel_conductivity, 0],
                                  [0, 0, self._parallel_conductivity]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            conductivity_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            conductivity_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return conductivity_tensor
