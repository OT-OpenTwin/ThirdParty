# coding=utf-8
# coding=utf-8
"""Solid conductor

.. sectionauthor:: Bundschuh
"""

from typing import Tuple, TYPE_CHECKING
import numpy as np
from scipy.sparse import coo_matrix

from pyrit.material import Conductivity
from pyrit.bdrycond.BCConductor import BCConductor

if TYPE_CHECKING:
    from pyrit.toolbox.CircuitSimulationToolbox import Circuit
    from pyrit.problem import Problem


class BCSolidConductor(BCConductor):
    """Class representing a solid conductor.

    The current density is allowed to redistribute inside a solid conductor.
    """

    # Name of the attribute that is temporarily saved in problem
    __mass_name = 'fcc_solid_conductor_mass_conductivity'

    def __init__(self, name: str, circuit: 'Circuit'):
        super().__init__(name, circuit)

        self.voltage_distribution_function = None

        self.base_coupling_matrix: coo_matrix = None
        self.bottom_coupling_matrix: coo_matrix = None
        self.right_coupling_matrix: coo_matrix = None
        self.coupling_value = None

    @property
    def additional_dofs(self) -> int:
        return 2

    @property
    def voltage_index(self) -> int:
        return 0

    @property
    def current_index(self) -> int:
        return 1

    def get_coupling_values(self, problem: 'Problem') -> Tuple[coo_matrix, coo_matrix, coo_matrix, coo_matrix]:
        if self.bottom_coupling_matrix is None or self.right_coupling_matrix is None or self.coupling_value is None:
            self.compute_coupling_values(problem)

        bottom_matrix: coo_matrix = self.bottom_coupling_matrix.copy()

        right_matrix: coo_matrix = self.right_coupling_matrix.copy()
        right_matrix.resize((self.right_coupling_matrix.shape[0], 2))

        diagonal_matrix = coo_matrix(np.array([[self.coupling_value, -1], ]))
        rhs_matrix = coo_matrix((1, 1))

        return bottom_matrix, right_matrix, diagonal_matrix, rhs_matrix

    def compute_coupling_values(self, problem: 'Problem'):
        """Computes matrices needed for the coupling and stored them internally.

        Parameters
        ----------
        problem : ShrinkInflateProblem
            A problem instance.
        """
        if len(problem.regions.find_regions_of_boundary_condition(self.ID)) != 1:
            raise Exception("This conductor is defined on more than one region. This does not make sense.")

        if hasattr(problem, self.__mass_name):
            mass = problem.__getattribute__(self.__mass_name)
        else:
            mass = problem.shape_function.mass_matrix(problem.regions, problem.materials, Conductivity)
            problem.__setattr__(self.__mass_name, mass)

        if self.voltage_distribution_function is None:
            self.compute_voltage_distribution_function(problem)
        self.compute_coupling_matrix(mass, problem.omega)
        self.compute_coupling_value(mass)

    def compute_coupling_matrix(self, mass: coo_matrix, omega: float) -> None:
        """Compute the coupling matrix and save it internally.

        Parameters
        ----------
        mass : coo_matrix
            The mass matrix.
        omega : float
            Angular frequency.
        """
        if self.base_coupling_matrix is None:
            self.base_coupling_matrix = mass @ self.voltage_distribution_function
            self.base_coupling_matrix = self.base_coupling_matrix.tocoo()
        self.bottom_coupling_matrix = -1j * omega * self.base_coupling_matrix.transpose()
        self.right_coupling_matrix = -1 * self.base_coupling_matrix

    def compute_coupling_value(self, mass: coo_matrix) -> None:
        """Compute the coupling value und save it internally.

        Parameters
        ----------
        mass : coo_matrix
            The mass matrix.
        """
        if self.right_coupling_matrix is None:
            coupling_value = self.voltage_distribution_function.transpose() @ mass @ self.voltage_distribution_function
        else:
            coupling_value = -1 * self.voltage_distribution_function.transpose() @ self.right_coupling_matrix
        self.coupling_value = coupling_value.data[0]

    def compute_voltage_distribution_function(self, problem: 'Problem') -> None:
        """Compute the voltage distribution function and save it internally.

        Parameters
        ----------
        problem : pyrit.excitation.FieldCircuitCoupling.ShrinkInflateProblem
            A problem object.
        """
        self.voltage_distribution_function = problem.shape_function.voltage_distribution_function(problem.regions, self)

    def cleanup(self, problem: 'Problem'):
        self.base_coupling_matrix = None
        self.bottom_coupling_matrix = None
        self.right_coupling_matrix = None
        self.coupling_value = None
        self.voltage_distribution_function = None

        if hasattr(problem, self.__mass_name):
            problem.__delattr__(self.__mass_name)
