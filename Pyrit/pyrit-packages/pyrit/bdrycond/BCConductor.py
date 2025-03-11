# coding=utf-8
"""Implementaion of BCConductor

.. sectionauthor:: Bundschuh
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple, Generator

import numpy as np
from scipy.sparse import coo_matrix

from pyrit.bdrycond.BC import BC

if TYPE_CHECKING:
    from pyrit.toolbox.CircuitSimulationToolbox import Circuit
    from pyrit.problem import Problem
    from pyrit.bdrycond import BdryCond


class BCConductor(BC, ABC):
    """Abstract class for a conductor. Used with a field-circuit coupling"""

    def __init__(self, name: str, circuit: 'Circuit'):
        super().__init__(None, name)

        self.circuit = circuit

        self._voltage = None
        self._current = None

        self.first_index_in_dof_vector = None

    @property
    def voltage(self):
        """Voltage of the conductor"""
        return self._voltage

    @property
    def current(self):
        """Current of the conductor"""
        return self._current

    @property
    @abstractmethod
    def additional_dofs(self) -> int:
        """Returns the number of equations added to the standard finite element model."""

    @property
    @abstractmethod
    def voltage_index(self) -> int:
        """The index within the additional equations where the voltage is."""

    @property
    @abstractmethod
    def current_index(self) -> int:
        """The index within the additional equations where the current is."""

    @property
    def voltage_index_in_dof(self):
        """The index of the voltage in the vector of degrees of freedom"""
        return self.first_index_in_dof_vector + self.voltage_index

    @property
    def current_index_in_dof(self):
        """The index of the current in the vector of degrees of freedom"""
        return self.first_index_in_dof_vector + self.current_index

    @classmethod
    def iter_fcc(cls, boundary_conditions: 'BdryCond') -> Generator['BCConductor', None, None]:
        """A generator for iterating over all boundary conditions in boundary_conditions of the same class.

        Parameters
        ----------
        boundary_conditions : BdryCond
            An boundary condition object.

        Yields
        ------
        fcc : cls
            An instance of the current class.
        """
        for fcc in boundary_conditions:
            if isinstance(fcc, cls):
                yield fcc

    @abstractmethod
    def get_coupling_values(self, problem: 'Problem') -> \
            Tuple[coo_matrix, coo_matrix, coo_matrix, coo_matrix]:
        r"""Return all matrices and values needed for the field circuit coupling.

        Let :math:`\mathbf{A}\mathbf{x} = \mathbf{b}` the system to shrink. Let furthermore be :math:`\mathbf{B}` the
        *bottom matrix*, :math:`\mathbf{R}` the *right matrix*, :math:`c` the *coupling value* and :math:`r` the
        *right-hand-side value*. Then the new matrix is of the form

        .. math::

            \begin{pmatrix} \mathbf{A} & \mathbf{R}\\\mathbf{B} & c\end{pmatrix}
            \begin{pmatrix}\mathbf{x}\\\xi\end{pmatrix}=\begin{pmatrix}\mathbf{b}\\r\end{pmatrix}

        Parameters
        ----------
        problem : ShrinkInflateProblem

        Returns
        -------
        bottom_matrix : coo_matrix
            The matrix that goes below the original matrix.
        right_matrix : coo_matrix
            The matrix that goes right of the original matrix.
        coupling value : coo_matrix
            The matrix that goes in the bottom right corner.
        rhs_value : coo_matrix
            The matrix for the right-hand-side.
        """

    def set_solution(self, solution: np.ndarray):
        """Get the solution for the component and processes it

        Parameters
        ----------
        solution : np.ndarray
            An array of length 2.
        """
        if not len(solution) == self.additional_dofs:
            raise ValueError(f"There must be {self.additional_dofs} solutions.")
        self._voltage = solution[self.voltage_index]
        self._current = solution[self.current_index]

    @abstractmethod
    def cleanup(self, problem: 'Problem') -> None:
        """Delete the added temporary fields in problem.

        Parameters
        ----------
        problem : ShrinkInflateProblem
            A problem object.
        """
