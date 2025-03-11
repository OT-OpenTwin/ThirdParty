# coding=utf-8
"""Calculation of the permeability tensor of a layered composite material.

.. sectionauthor:: Thyssen
"""

from abc import ABC, abstractmethod
import numpy as np
from pyrit.material import Permeability
from pyrit.toolbox.TransformationToolbox import basis_from_constant_direction, transform_constant_tensor, \
    basis_from_function_direction, transform_function_tensor


class MixedPermeability(Permeability, ABC):
    r"""Class that represents the permeability :math:`\mu=\nu^{-1}` of a layered composite material"""

    @abstractmethod
    def __init__(self, permeability_1, permeability_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """
        Parameters: permeability_1, permeability_2, direction and ratio and parameters inherited from permeability class

        Parameters
        ----------
        permeability_1: float
            permeability of material1
        permeability_2: float
            permeability of material2
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
        self.permeability_1 = permeability_1
        self.permeability_2 = permeability_2
        self.direction = direction
        self.ratio = ratio
        value = self._get_permeability_tensor()

        super().__init__(value, name, data)

    @property
    def _perpendicular_permeability(self):
        """Calculates the permeability perpendicular to the layers

        Returns
        -------
        perpendicular_permeability: float
            permeability value perpendicular to the material's layers
        """
        perpendicular_permeability = 1 / ((self.ratio / self.permeability_1) + ((1 - self.ratio) / self.permeability_2))
        return perpendicular_permeability

    @property
    def _parallel_permeability(self):
        """Calculates the permeability parallel to the layers

        Returns
        -------
        parallel_permeability: float
            permeability value parallel to the material's layers
        """
        parallel_permeability = self.ratio * self.permeability_1 + (1 - self.ratio) * self.permeability_2
        return parallel_permeability

    @abstractmethod
    def _get_permeability_tensor(self):
        """Calculate the permeability tensor in the reference coordinate system x

        Returns
        -------
        permeability_tensor: np.ndarray
            (N,N) permeability tensor rotated in a reference coordinate system x.
        """


class MixedPermeabilityCart(MixedPermeability):
    r"""Class that represents the permeability of a 2D layered composite material in a cartesian coordinate system"""

    def __init__(self, permeability_1, permeability_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of MixedPermeability in a 2D cartesian coordinate system

        Parameters
        ----------
        permeability_1: float
            permeability of material1
        permeability_2: float
            permeability of material2
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
        super().__init__(permeability_1, permeability_2, direction, ratio, name, data)

    def _get_permeability_tensor(self):
        """Calculate the permeability tensor in the reference 2D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_permeability, 0], [0, self._parallel_permeability]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            permeability_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            permeability_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return permeability_tensor


class MixedPermeabilityAxi(MixedPermeability):
    r"""Class that represents the permeability of a 3D layered composite material in a axisymmetric coordinate system"""

    def __init__(self, permeability_1, permeability_2, direction, ratio, name: str = '', data: np.ndarray = None):
        """Calculation of Mixedpermeability in a 3D axisymmetric coordinate system

        Parameters
        ----------
        permeability_1: float
            permeability of material1
        permeability_2: float
            permeability of material2
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
        super().__init__(permeability_1, permeability_2, direction, ratio, name, data)

    def _get_permeability_tensor(self):
        """Calculate the permeability tensor in the reference axisymmetric coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_permeability, 0], [0, self._parallel_permeability]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            permeability_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            permeability_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return permeability_tensor


class MixedPermeability3D(MixedPermeability):
    """Class that represents the permeability of a 3D layered composite material in a cartesian coordinate system"""

    def __init__(self, permeability_1, permeability_2, direction, ratio, name: str = '', data: np.ndarray = None):
        r"""Calculation of Mixedpermeability in a 3D cartesian coordinate system

        Parameters
        ----------
        permeability_1: float
            permeability of material1
        permeability_2: float
            permeability of material2
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
        super().__init__(permeability_1, permeability_2, direction, ratio, name, data)

    def _get_permeability_tensor(self):
        """Calculate the permeability tensor in the reference 3D coordinate system x"""
        charac_matrix = np.array([[self._perpendicular_permeability, 0, 0],
                                  [0, self._parallel_permeability, 0],
                                  [0, 0, self._parallel_permeability]])
        if isinstance(self.direction, np.ndarray):
            basis_vectors = basis_from_constant_direction(self.direction)
            permeability_tensor = transform_constant_tensor(charac_matrix, basis_vectors)
        elif callable(self.direction):
            basis_vectors = basis_from_function_direction(self.direction)
            permeability_tensor = transform_function_tensor(charac_matrix, basis_vectors)
        else:
            raise TypeError(f"Direction must be np.ndarray or callable, got '{type(self.direction).__name__}' instead.")
        return permeability_tensor
