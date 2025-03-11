# coding=utf-8
"""Ferromagnetic material based Brauer model.

.. sectionauthor:: Thyssen
"""
from typing import Callable, List
import numpy as np
from scipy.optimize import curve_fit
from pyrit.material import MatProperty


class Value:
    """Class used for nonlinear material properties."""

    def __init__(self, nonlinear_material_property: Callable[[float], float]):
        self.nonlinear_material_property = nonlinear_material_property
        self.solution = None

    def __call__(self, element, solution=None):
        if solution is None:
            solution = self.solution

        flux_density = solution.b_field[element]

        return self.nonlinear_material_property(flux_density)


class BrauerModel:
    """Class representing ferromagnetic material based on Brauer model"""

    def __init__(self, k_1: float, k_2: float, k_3: float):
        """Constructor of BrauerModel

        Parameters
        ----------
        k_1: float
            parameter determining the shape of Brauer curve
        k_2: float
            parameter determining the shape of Brauer curve
        k_3: float
            parameter determining the shape of Brauer curve
        """
        if k_1 <= 0:
            raise ValueError("Invalid k_1. k_1 must be >0.")
        if k_2 <= 0:
            raise ValueError("Invalid k_2. k_2 must be >0.")
        if k_3 <= -k_1:
            raise ValueError("Invalid k_3. It must be k_3>-k_1.")
        self.k_1 = k_1
        self.k_2 = k_2
        self.k_3 = k_3

    def material_properties(self) -> List[MatProperty]:
        """Return all material properties of the Brauer model"""
        return [Value(self.reluctivity), Value(self.differential_reluctivity)]

    @property
    def reluctivity(self) -> Callable[[float], float]:
        """Return reluctivity of the Brauer model"""
        return type(self).compute_reluctivity(self.k_1, self.k_2, self.k_3)

    @property
    def differential_reluctivity(self) -> Callable[[float], float]:
        """Return differential reluctivity of the Brauer model"""
        return type(self).compute_differential_reluctivity(self.k_1, self.k_2, self.k_3)

    @staticmethod
    def compute_reluctivity(k_1: float, k_2: float, k_3: float) -> Callable[[float], float]:
        """Calculation of reluctivity following Brauer model"""

        def reluctivity(flux_density):
            return k_1 * np.exp(k_2 * flux_density ** 2) + k_3

        return reluctivity

    @staticmethod
    def compute_differential_reluctivity(k_1: float, k_2: float, k_3: float) -> Callable[[float], float]:
        """Calculation of differential reluctivity following Brauer model"""

        def differential_reluctivity(flux_density):
            return k_1 * k_2 * np.exp(k_2 * flux_density ** 2)

        return differential_reluctivity

    @classmethod
    def from_data(cls, flux_density_data: np.ndarray, magnetic_field_data: np.ndarray):
        """Calculation of parameters k_1, k_2 and k_3 if not given

        Parameters
        ----------
        flux_density_data: np.ndarray
            np.ndarray containing experimental or simulated flux density data.
        magnetic_field_data: np.ndarray
            np.ndarray containing experimental or simulated magnetic field data.

        Returns
        -------
        brauer_model : BrauerModel
            Instance of the BrauerModel class with the calculated parameters k_1, k_2 and k_3.
        """
        sorted_indices = np.argsort(flux_density_data)
        b_1 = flux_density_data[sorted_indices[0]]
        b_2 = flux_density_data[sorted_indices[1]]
        b_3 = flux_density_data[sorted_indices[-2]]
        b_4 = flux_density_data[sorted_indices[-1]]
        h_1 = magnetic_field_data[sorted_indices[0]]
        h_2 = magnetic_field_data[sorted_indices[1]]
        h_3 = magnetic_field_data[sorted_indices[-2]]
        h_4 = magnetic_field_data[sorted_indices[-1]]

        k_3 = (h_2 - h_1) / (b_2 - b_1)
        k_2 = np.log((h_4 * b_3) / (h_3 * b_4)) / (b_4 ** 2 - b_3 ** 2)
        k_1 = h_3 / (b_3 * np.exp(k_2 * b_3 ** 2))

        initial_guess = [k_1, k_2, k_3]

        def brauer_curve(flux_density, k_1_, k_2_, k_3_):
            return cls.compute_reluctivity(k_1_, k_2_, k_3_)(flux_density) * flux_density

        fitted_params = curve_fit(brauer_curve, flux_density_data, magnetic_field_data, initial_guess)

        return cls(*fitted_params[0])
