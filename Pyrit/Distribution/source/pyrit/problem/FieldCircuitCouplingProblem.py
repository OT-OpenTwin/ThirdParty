# coding=utf-8
# coding=utf-8
"""Classes for problems where a field circuit coupling should be performed

.. sectionauthor:: Bundschuh
"""

from abc import abstractmethod
from typing import List, TYPE_CHECKING, Iterable, Tuple

import numpy as np
from scipy import sparse

from pyrit import material
from pyrit.problem.MagneticProblemAxi import MagneticProblemAxiStatic, MagneticProblemAxiHarmonic, \
    MagneticProblemAxiTransient
from pyrit.problem.MagneticProblemCart import MagneticProblemCartStatic, MagneticProblemCartHarmonic, \
    MagneticProblemCartTransient
from pyrit.toolbox.CircuitSimulationToolbox import FEElement, Edge, CircuitSolution, CircuitSolutionStatic, \
    CircuitSolutionHarmonic, CircuitSolutionTransient
from pyrit.bdrycond import BCConductor
from pyrit.problem import Problem
from pyrit.solution import FieldCircuitCouplingSolution, FieldCircuitCouplingSolutionStatic, \
    FieldCircuitCouplingSolutionHarmonic, FieldCircuitCouplingSolutionTransient

from pyrit import get_logger

magnetic_problems = (MagneticProblemAxiStatic, MagneticProblemAxiHarmonic, MagneticProblemAxiTransient,
                     MagneticProblemCartStatic, MagneticProblemCartHarmonic, MagneticProblemCartTransient)

harmonic_problem = (MagneticProblemCartHarmonic, MagneticProblemAxiHarmonic)

if TYPE_CHECKING:
    from pyrit.problem import StaticProblem, HarmonicProblem, TransientProblem
    from pyrit.toolbox.CircuitSimulationToolbox import Circuit

logger = get_logger(__name__)


class FieldCircuitCouplingProblem:
    """Basic field-circuit coupling class"""

    associated_fe_solution_class = FieldCircuitCouplingSolution
    associated_circuit_solution_class = CircuitSolution

    def __init__(self, *problems: 'Problem'):
        self._problems = None
        self._circuits = None
        self._conductors = None
        self._conductors_names = None
        self._conductor_to_problem = None

        self.problems = list(problems)

    def _extract_conductors(self):
        """Get all conductors from all problems"""
        self._conductors = []
        self._conductors_names = []
        self._conductor_to_problem = []
        for k, problem in enumerate(self.problems):
            list_conductors = problem.boundary_conditions.dict_of_boundary_condition()['conductor']
            if len(list_conductors) == 0:
                logger.warning("There is a problem without any conductors.")
            for index in list_conductors:
                self._conductors.append(problem.boundary_conditions.get_bc(index))
                self._conductors_names.append(self._conductors[-1].name)
                self._conductor_to_problem.append(k)

    def _extract_circuits_from_problems(self):
        """Get all circuits from all problems."""
        if self._conductors is None:
            self._extract_conductors()

        circuits = set()
        circuits.update([conductor.circuit for conductor in self._conductors])

        self._circuits = list(circuits)

    @property
    def problems(self) -> List['Problem']:
        """A list of problems"""
        return list(self._problems)

    @problems.setter
    def problems(self, problems: Iterable['Problem']):
        """Set the list of problems.

        Parameters
        ----------
        problems : Iterable['Problem']
            An iterable of problems
        """
        self._problems = list(problems)

        self._extract_conductors()
        self._extract_circuits_from_problems()
        self.consistency_check()

    def consistency_check(self):
        """Check the consistency of the problem.

        Raises
        ------
        ValueError :
            If the problem is not consistent
        """
        for problem in self.problems:
            if not isinstance(problem, magnetic_problems):
                raise ValueError("Every problem has to be a magnetic problem")
        if not len(self._conductors_names) == len(set(self._conductors_names)):
            seen = set()
            duplicates = [x for x in self._conductors_names if x in seen or seen.add(x)]
            raise ValueError(f"The conductor names are not unique. Duplicates are {duplicates}")

    @abstractmethod
    def solve(self, *args, **kwargs):
        """Solve the field-circuit coupling problem."""

    @abstractmethod
    def create_solution(self, fe_solutions: List[np.ndarray], circuit_solutions: List[np.ndarray]):
        """Create the finite element and circuit solutions from the solution arrays"""
        if len(fe_solutions) != len(self.problems):
            raise ValueError("Number of fe solutions does not match the number of problems")

        if len(circuit_solutions) != len(self._circuits):
            raise ValueError("Number of circuit solutions dies not match the number of circuits")


class FieldCircuitCouplingProblemStatic(FieldCircuitCouplingProblem):
    """Field-circuit coupling class for static problems"""

    associated_fe_solution_class = FieldCircuitCouplingSolutionStatic
    associated_circuit_solution_class = CircuitSolutionStatic

    def __init__(self, *problems: 'StaticProblem'):
        super().__init__(*problems)
        raise NotImplementedError

    def solve(self, *args, **kwargs):
        pass

    def create_solution(self, fe_solutions: List[np.ndarray], circuit_solutions: List[np.ndarray]):
        pass

    # def create_solution(self, fe_solutions: List[np.ndarray], circuit_solutions: List[np.ndarray]):
    #     super().create_solution(fe_solutions, circuit_solutions)
    #
    #     solutions_fe = [problem.create_solution(fe_solution) for problem, fe_solution in
    #                     zip(self.problems, fe_solutions)]
    #     solutions_circuit = [self.associated_circuit_solution_class(circuit_solution, circuit) for
    #                          circuit, circuit_solution in zip(self._circuits, circuit_solutions)]
    #     return self.associated_fe_solution_class(solutions_fe, solutions_circuit)


class FieldCircuitCouplingProblemHarmonic(FieldCircuitCouplingProblem):
    """Field-circuit coupling class for static problems"""

    associated_fe_solution_class = FieldCircuitCouplingSolutionHarmonic
    associated_circuit_solution_class = CircuitSolutionHarmonic

    def __init__(self, *problems: 'HarmonicProblem'):
        self._circuits = None
        super().__init__(*problems)

        self._problems: List['HarmonicProblem']
        self.shrunk_matrices = []
        self.shrunk_rhs = []

    @property
    def frequency(self):
        """Frequency of the problems"""
        return self._problems[0].frequency

    @property
    def angular_frequency(self):
        """Angular frequency of the problems"""
        return self._problems[0].omega

    omega = angular_frequency

    def consistency_check(self):
        super().consistency_check()

        for problem in self.problems:
            if not isinstance(problem, harmonic_problem):
                raise ValueError("Every problem has to be a harmonic problem")

        frequencies = [problem.frequency for problem in self.problems]
        if len(frequencies) > 1 and not np.allclose(*frequencies):
            raise ValueError("Not all frequencies are equal")

        if any(circuit.is_time_dependent for circuit in self._circuits):
            raise ValueError("All circuits must not be time dependent")

    @staticmethod
    def get_shrunk_system(problem: Problem, integration_order: int = 1) -> Tuple[sparse.coo_matrix, sparse.coo_matrix]:
        """Get the shrunk system for a magnetic problem.

        Parameters
        ----------
        problem : Problem
        integration_order : int, optional
            The integration order used for shrinking.

        Returns
        -------
        matrix_shrink : sparse.coo_matrix
            The shrunk system matrix
        rhs_shrink : sparse.coo_matrix
            The shrunk system right-hand side
        """
        curlcurl = problem.shape_function.curlcurl_operator(problem.regions, problem.materials, material.Reluctivity)
        mass = problem.shape_function.mass_matrix(problem.regions, problem.materials, material.Conductivity)

        matrix = curlcurl + 1j * problem.omega * mass
        load = problem.shape_function.load_vector(problem.regions, problem.excitations)

        matrix_shrink, rhs_shrink, _, _, _ = problem.shape_function.shrink_fcc(matrix, load, problem, integration_order)
        return matrix_shrink, rhs_shrink

    def calc_shrunk_systems(self):
        """Calculate the shrunk systems of all problems"""
        for problem in self.problems:
            matrix_shrink, rhs_shrink = self.get_shrunk_system(problem)
            self.shrunk_matrices.append(matrix_shrink)
            self.shrunk_rhs.append(rhs_shrink)

    def _get_column_number_voltage(self, conductor: BCConductor, problem_index):
        """Get the column number of the voltage of the component that is in the problem with given index"""
        return conductor.voltage_index_in_dof + sum(mat.shape[1] for mat in self.shrunk_matrices[:problem_index])

    def _get_column_number_current(self, conductor: BCConductor, problem_index):
        """Get the column number of the current of the component that is in the problem with given index"""
        return conductor.current_index_in_dof + sum(mat.shape[1] for mat in self.shrunk_matrices[:problem_index])

    def build_system(self) -> Tuple[sparse.coo_matrix, sparse.coo_matrix]:
        """Build the large system that couples all FE systems with all circuit systems.

        Returns
        -------
        system_matrix : sparse.coo_matrix
            The system matrix of the field-circuit coupling problem
        system_rhs : sparse.coo_matrix
            The right-hand side vector of the field-circuit coupling problem
        """
        self.calc_shrunk_systems()

        fe_system_matrices: sparse.coo_matrix = sparse.block_diag(self.shrunk_matrices, format='coo')
        fe_rhs_matrices: sparse.coo_matrix = sparse.vstack(self.shrunk_rhs, format='coo')

        conductors = {name: (conductor, self._conductor_to_problem[k]) for k, (name, conductor) in
                      enumerate(zip(self._conductors_names, self._conductors))}

        circuit_matrices = []
        coupling_matrices = []
        circuit_rhses = []
        for circuit in self._circuits:
            time_constant_matrix, time_derivative_matrix = circuit.mna_matrices()
            rhs: sparse.coo_matrix = circuit.mna_rhs()
            A_F: sparse.coo_matrix = circuit.A_F  # pylint: disable=invalid-name
            A_F, _ = circuit.split_incidence_matrix(A_F)  # pylint: disable=invalid-name
            len_lv = circuit.A_L.shape[1] + circuit.A_V.shape[1]

            voltage_column_numbers = []
            current_column_numbers = []
            for fe_edge in circuit.get_edges(FEElement):
                fe_edge: Edge
                conductor, problem = conductors[fe_edge.component.name]
                voltage_column_numbers.append(self._get_column_number_voltage(conductor, problem))
                current_column_numbers.append(self._get_column_number_current(conductor, problem))

            if not A_F.shape[1] == len(voltage_column_numbers):
                raise ValueError("Internal error")

            A_F_inflated = A_F.copy()  # pylint: disable=invalid-name
            A_F_inflated.resize((A_F.shape[0], fe_system_matrices.shape[1]))
            mul_mat = sparse.coo_matrix(
                (np.ones(len(current_column_numbers)), (np.arange(A_F.shape[1]), current_column_numbers)),
                shape=(fe_system_matrices.shape[1], fe_system_matrices.shape[1]))
            matrix_current = A_F_inflated @ mul_mat
            # matrix_current = sparse.coo_matrix((A_F.data, (A_F.row, current_column_numbers)),
            #                                    shape=(A_F.shape[0], fe_system_matrices.shape[1]))
            tmp = A_F.shape[1]
            matrix_voltage = sparse.coo_matrix((np.ones(tmp), (np.arange(tmp), voltage_column_numbers)),
                                               shape=(tmp, fe_system_matrices.shape[1]))

            coupling_matrices.append(sparse.vstack([matrix_current,
                                                    sparse.coo_matrix((len_lv, fe_system_matrices.shape[1])),
                                                    matrix_voltage]))
            circuit_matrices.append(time_constant_matrix + 1j * self.omega * time_derivative_matrix)
            circuit_rhses.append(rhs)

        coupling_matrix = sparse.vstack(coupling_matrices, format='coo')
        circuit_matrix = sparse.block_diag(circuit_matrices, format='coo')
        circuit_rhs = sparse.vstack(circuit_rhses, format='coo')

        system_matrix = sparse.bmat([[fe_system_matrices, None],
                                     [coupling_matrix, circuit_matrix]])
        system_rhs = sparse.vstack([fe_rhs_matrices, circuit_rhs])

        return system_matrix, system_rhs

    def disassemble_system_solution(self, system_solution: np.ndarray) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """Disassemble the solution of the big system.

        Parameters
        ----------
        system_solution : np.ndarray
            The solution of the big coupled system.

        Returns
        -------
        fe_solution : List[np.ndarray]
            A list with the solutions of the single FE problems
        circuit_solutions : List[np.ndarray]
            A list with the solutions of the single circuit problems
        """
        conductors = {name: (conductor, self._conductor_to_problem[k]) for k, (name, conductor) in
                      enumerate(zip(self._conductors_names, self._conductors))}

        # Get the solution fo each circuit (includes the voltage over and the current through the FE element)
        tmp = len(system_solution)
        circuit_solutions = []
        for circuit in reversed(self._circuits):
            current_column_numbers = []
            for fe_edge in circuit.get_edges(FEElement):
                fe_edge: Edge
                conductor, problem = conductors[fe_edge.component.name]
                current_column_numbers.append(self._get_column_number_current(conductor, problem))

            # Write circuit solution to the circuit
            num_dof = circuit.num_dof - len(current_column_numbers)
            circuit_solutions.append(system_solution[np.ix_(np.concatenate([np.arange(tmp - num_dof, tmp),
                                                                            current_column_numbers]))])

            tmp -= num_dof

        fe_solutions = []
        # Get the solution of each FE problem
        for problem, system_matrix in zip(reversed(self.problems), reversed(self.shrunk_matrices)):
            problem_dof = system_matrix.shape[1]
            fe_solutions.append(
                problem.shape_function.inflate_fcc(system_solution[tmp - problem_dof:tmp], problem, None))
            tmp -= problem_dof

        return list(reversed(fe_solutions)), list(reversed(circuit_solutions))

    def create_solution(self, fe_solutions: List[np.ndarray], circuit_solutions: List[np.ndarray]):
        super().create_solution(fe_solutions, circuit_solutions)

        solutions_fe = [problem.create_solution(fe_solution) for problem, fe_solution in
                        zip(self.problems, fe_solutions)]
        solutions_circuit = [
            self.associated_circuit_solution_class(circuit_solution, circuit, self.frequency, circuit.name) for
            circuit, circuit_solution in zip(self._circuits, circuit_solutions)]
        return self.associated_fe_solution_class(solutions_fe, solutions_circuit)

    def solve(self, *args, **kwargs):
        system_matrix, system_rhs = self.build_system()

        system_solution, _ = Problem.solve_linear_system(system_matrix, system_rhs, **kwargs)

        fe_solutions, circuit_solutions = self.disassemble_system_solution(system_solution)

        return self.create_solution(fe_solutions, circuit_solutions)


class FieldCircuitCouplingProblemTransient(FieldCircuitCouplingProblem):
    """Field-circuit coupling class for static problems"""

    associated_fe_solution_class = FieldCircuitCouplingSolutionTransient
    associated_circuit_solution_class = CircuitSolutionTransient

    def __init__(self, *problems: 'TransientProblem'):
        super().__init__(*problems)
        raise NotImplementedError

    def solve(self, *args, **kwargs):
        pass

    def create_solution(self, fe_solutions: List[np.ndarray], circuit_solutions: List[np.ndarray]):
        pass
