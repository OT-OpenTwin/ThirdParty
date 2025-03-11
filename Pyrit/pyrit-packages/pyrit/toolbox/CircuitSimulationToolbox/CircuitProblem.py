# coding=utf-8
"""A circuit simulation problem

.. sectionauthor:: Bundschuh
"""

from abc import ABC, abstractmethod

import numpy as np

from pyrit.toolbox.MiscellaneousToolbox import solve_linear_system

from pyrit.toolbox.CircuitSimulationToolbox.Circuit import Circuit, FEElement
from pyrit.toolbox.CircuitSimulationToolbox.CircuitSolution import CircuitSolution, CircuitSolutionStatic, \
    CircuitSolutionHarmonic, CircuitSolutionTransient

from pyrit import get_logger

logger = get_logger(__name__)


class CircuitSimulationException(Exception):
    """Exception for errors in the simulation of circuits."""


class CircuitProblem(ABC):
    """Class for the simulation of an electrical circuit"""

    corresponding_solution_class = CircuitSolution

    def __init__(self, circuit: Circuit, name: str = None):
        self._circuit = None
        self.circuit = circuit
        self.name = name

    def _circuit_consistency_check(self):
        # Check if there are no FEElements in the circuit
        if len(self.circuit.get_edges(FEElement)) != 0:
            logger.warning("The circuit contains at least one FEEelement. This cannot be simulation with this class")

    @property
    def circuit(self) -> Circuit:
        """The circuit"""
        return self._circuit

    @circuit.setter
    def circuit(self, circuit: Circuit):
        """Set the circuit"""
        if not isinstance(circuit, Circuit):
            raise ValueError("The given circuit is not of the right class")
        self._circuit = circuit
        self._circuit_consistency_check()

    @abstractmethod
    def generate_solution(self, solution: np.ndarray, **kwargs):
        """Generate a solution object of the corresponding solution class

        Parameters
        ----------
        solution : np.ndarray
            The solution of the circuit

        Returns
        -------
        solution : CircuitSolution
            The solution object
        """
        kwargs.setdefault('name', self.name)
        return kwargs

    @abstractmethod
    def get_system(self, *args, **kwargs):
        """Return the system of equations of the circuit problem."""

    @abstractmethod
    def solve(self, *args, **kwargs) -> CircuitSolution:
        """Solve the circuit"""


class CircuitProblemStatic(CircuitProblem):
    """Class for the static simulation of an electrical circuit"""

    corresponding_solution_class = CircuitSolutionStatic

    def _circuit_consistency_check(self):
        super()._circuit_consistency_check()
        if self.circuit.is_time_dependent:
            raise CircuitSimulationException("Circuit is time dependent")
        if self.circuit.is_frequency_domain:
            raise CircuitSimulationException("Circuit is in frequency domain")

    # pylint: disable=arguments-differ
    def get_system(self):
        matrix, _ = self.circuit.mna_matrices()
        rhs = self.circuit.mna_rhs()

        return matrix, rhs

    def solve(self, *args, **kwargs) -> CircuitSolutionStatic:
        matrix, rhs = self.get_system()

        mna_solution, _ = solve_linear_system(matrix, rhs, **kwargs)

        return self.generate_solution(mna_solution)

    def generate_solution(self, solution: np.ndarray, **kwargs):
        kwargs = super().generate_solution(solution, **kwargs)
        # noinspection PyArgumentList
        return self.corresponding_solution_class(solution, self.circuit, **kwargs)


class CircuitProblemHarmonic(CircuitProblem):
    """Class for the harmonic simulation of an electrical circuit"""

    corresponding_solution_class = CircuitSolutionHarmonic

    def __init__(self, circuit: Circuit, frequency: float, name: str = None):
        super().__init__(circuit, name)
        self._frequency = None
        self.frequency = frequency

    def _circuit_consistency_check(self):
        super()._circuit_consistency_check()
        if self.circuit.is_time_dependent:
            raise CircuitSimulationException("Circuit is time dependent")
        if not self.circuit.is_frequency_domain:
            raise CircuitSimulationException("Circuit is not in frequency domain")

    @property
    def frequency(self) -> float:
        """The frequency."""
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        """The frequency.

        Parameters
        ----------
        frequency : float
            The non-negative frequency.
        """
        if frequency <= 0:
            raise ValueError("The frequency must be greater or equal to 0")
        self._frequency = frequency

    @property
    def angular_frequency(self) -> float:
        """The angular frequency."""
        return 2 * np.pi * self.frequency

    omega = angular_frequency

    def get_system(self, *args, **kwargs):
        time_constant_matrix, time_derivative_matrix = self.circuit.mna_matrices()
        matrix = (time_constant_matrix + 1j * self.omega * time_derivative_matrix).tocoo()
        rhs = self.circuit.mna_rhs()

        return matrix, rhs

    def solve(self, *args, **kwargs):
        matrix, rhs = self.get_system()

        mna_solution, _ = solve_linear_system(matrix, rhs, **kwargs)

        return self.generate_solution(mna_solution)

    def generate_solution(self, solution: np.ndarray, **kwargs):
        kwargs = super().generate_solution(solution, **kwargs)
        # noinspection PyArgumentList
        return self.corresponding_solution_class(solution, self.circuit, self.frequency, **kwargs)


class CircuitProblemTransient(CircuitProblem):
    """Class for the transient simulation of an electrical circuit"""

    corresponding_solution_class = CircuitSolutionTransient

    def __init__(self, circuit: Circuit, name: str = None):
        super().__init__(circuit, name)

    def _circuit_consistency_check(self):
        super()._circuit_consistency_check()
        if not self.circuit.is_time_dependent:
            raise CircuitSimulationException("Circuit is not time dependent")

    def solve(self, *args, **kwargs):
        raise NotImplementedError

    def get_system(self, *args, **kwargs):
        raise NotImplementedError

    def generate_solution(self, solution: np.ndarray, **kwargs):
        kwargs = super().generate_solution(solution, **kwargs)
        # noinspection PyArgumentList
        return self.corresponding_solution_class(solution, self.circuit, **kwargs)
