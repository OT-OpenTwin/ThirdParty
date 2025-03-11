# coding=utf-8
"""Solution classes for field-circuit coupling problems

.. sectionauthor:: Bundschuh
"""

from typing import TYPE_CHECKING, Iterable, Tuple, Union

from pyrit.toolbox.IOToolbox import save, load
from pyrit.solution.Solution import Solution, StaticSolution, HarmonicSolution, TransientSolution
from pyrit.toolbox.CircuitSimulationToolbox import CircuitSolution, CircuitSolutionStatic, CircuitSolutionHarmonic, \
    CircuitSolutionTransient

from pyrit import get_logger

if TYPE_CHECKING:
    from pathlib import Path


logger = get_logger(__name__)


class FieldCircuitCouplingSolution:
    """General field-circuit coupling solution class"""

    solution_identifier: str = 'General field-circuit coupling solution'
    solution_class = Solution
    circuit_solution_class = CircuitSolution

    def __init__(self, solutions: Iterable[Solution], circuit_solutions: Iterable[CircuitSolution]):
        self._solutions = None
        self._circuit_solutions = None

        self.solutions = solutions
        self.circuit_solutions = circuit_solutions

    @property
    def solutions(self) -> Tuple[Solution]:
        """A tuple of all finite element solutions."""
        return tuple(self._solutions)

    @solutions.setter
    def solutions(self, solutions: Iterable[Solution]):
        """Set finite element solutions

        Parameters
        ----------
        solutions : Iterable[Solution]
            An iterable of finite element solutions.
        """
        for solution in solutions:
            if not isinstance(solution, self.solution_class):
                raise ValueError("Every solution must be a Solution")

        self._solutions = tuple(solutions)

    @property
    def circuit_solutions(self) -> Tuple[CircuitSolution]:
        """A tuple of all circuit solutions."""
        return self._circuit_solutions

    @circuit_solutions.setter
    def circuit_solutions(self, circuit_solutions: Iterable[CircuitSolution]):
        """Set circuit solutions

        Parameters
        ----------
        circuit_solutions : Iterable['CircuitSolutions']
            An iterable of circuit solutions
        """
        for circuit_solution in circuit_solutions:
            if not isinstance(circuit_solution, self.circuit_solution_class):
                raise ValueError("Every circuit solution must be a CircuitSolution")

        self._circuit_solutions = tuple(circuit_solutions)

    def get_solution_from_name(self, name: str) -> Solution:
        """Get a solution from its name.

        Parameters
        ----------
        name : str
            Name of the solution.

        Returns
        -------
        solution : Solution
            The specified solution

        Raises
        ------
        IndexError : When there is not exactly one solution with this name
        """
        indices = [index for index, solution in enumerate(self.solutions) if solution.description == name]

        if len(indices) > 1:
            raise IndexError(f"More than one solution with the name '{name}'")
        if len(indices) == 0:
            raise IndexError(f"No solution exists with the name '{name}'")

        return self.solutions[indices[0]]

    def get_circuit_solution_from_name(self, name: str) -> CircuitSolution:
        """Get a circuit solution from its name.

        Parameters
        ----------
        name : str
            Name of the circuit solution

        Returns
        -------
        circuit_solution : CircuitSolution
            The specified circuit solution

        Raises
        ------
        IndexError : When there is not exactly one solution with this name
        """
        indices = [index for index, circuit in enumerate(self._circuit_solutions) if circuit.name == name]

        if len(indices) > 1:
            raise Exception(f"More than one circuit solution with the name '{name}'")
        if len(indices) == 0:
            raise IndexError(f"No circuit solution exists with the name '{name}'")

        return self.circuit_solutions[indices[0]]

    def save(self, path: Union[str, 'Path'], **kwargs) -> 'Path':
        """Save the object.

        Parameters
        ----------
        path : Union[str, 'Path']
        kwargs :
            Passed to :py:func:`pyrit.toolbox.IOToolbox.save`.

        Returns
        -------
        path : Path
            The path where the object is saved
        """
        return save(self, path, **kwargs)

    @classmethod
    def load(cls, path: Union[str, 'Path'], **kwargs):
        """Load a field-circuit coupling object.

        Parameters
        ----------
        path : Union[str, 'Path']
            The path where the object is saved.
        kwargs :
            Passed to :py:func:`pyrit.toolbox.IOToolbox.load`

        Returns
        -------
        obj :
            The field-circuit coupling object.
        """
        obj = load(path, **kwargs)
        if not isinstance(obj, cls):
            raise TypeError("The loaded object has has to wring type")


class FieldCircuitCouplingSolutionStatic(FieldCircuitCouplingSolution):
    """Solution class for static field-circuit coupling problems."""

    solution_identifier: str = 'Static field-circuit coupling solution'
    solution_class = StaticSolution
    circuit_solution_class = CircuitSolutionStatic

    def __init__(self, solutions: Iterable[StaticSolution], circuit_solutions: Iterable[CircuitSolutionStatic]):
        super().__init__(solutions, circuit_solutions)


class FieldCircuitCouplingSolutionHarmonic(FieldCircuitCouplingSolution):
    """Solution class for harmonic field-circuit coupling problems."""

    solution_identifier: str = 'Harmonic field-circuit coupling solution'
    solution_class = HarmonicSolution
    circuit_solution_class = CircuitSolutionHarmonic

    def __init__(self, solutions: Iterable[HarmonicSolution], circuit_solutions: Iterable[CircuitSolutionHarmonic]):
        super().__init__(solutions, circuit_solutions)


class FieldCircuitCouplingSolutionTransient(FieldCircuitCouplingSolution):
    """Solution class for transient field-circuit coupling problems."""

    solution_identifier: str = 'Transient field-circuit coupling solution'
    solution_class = TransientSolution
    circuit_solution_class = CircuitSolutionTransient

    def __init__(self, solutions: Iterable[TransientSolution], circuit_solutions: Iterable[CircuitSolutionTransient]):
        super().__init__(solutions, circuit_solutions)
