# coding=utf-8
"""Axisymmetric capacitive-resistive-thermal problems.

.. sectionauthor:: Ruppert
"""

from typing import Dict, Union, Tuple, Iterable, List
from dataclasses import dataclass, field
from scipy import sparse
import numpy as np

from pyrit import get_logger
from pyrit.solution import CurrentFlowSolutionAxiStatic, ThermalSolutionAxiStatic, CurrentFlowSolutionAxiTransient, \
    ThermalSolutionAxiTransient

from .Problem import StaticProblem, TransientProblem
from .CurrentFlowProblemAxi import CurrentFlowProblemAxiStatic, CurrentFlowSolverInfoAxiStatic, \
    CurrentFlowSolverInfoAxiTransient, CurrentFlowProblemAxiTransient
from .ThermalProblemAxi import ThermalProblemAxiStatic, ThermalSolverInfoAxiStatic, ThermalSolverInfoAxiTransient, \
    ThermalProblemAxiTransient
from ..material import DiffConductivityParameter, DiffThermalConductivityParameter, DiffPermittivityParameter, \
    DiffVolumetricHeatCapacityParameter
from ..solution.CurrentFlowSolutionAxi import CurrentFlowSolutionAxiIntermediate
from ..solution.ThermalSolutionAxi import ThermalSolutionAxiIntermediate
from ..toolbox.QuantitiesOfInterestToolbox import QuantitiesOfInterest

logger = get_logger(__name__)


@dataclass()
class ElectrothermalSolverInfoAxiStatic:
    """Class for passing solver options to ElectrothermalProblemAxiStatic"""

    # region Options for the solve()-routine
    # Options for the solve()-method of the electric subproblem
    solver_info_el: CurrentFlowSolverInfoAxiStatic = CurrentFlowSolverInfoAxiStatic()
    kwargs_el: Dict = field(
        default_factory=dict)  # key word arguments passed to the solve routine of CurrentFlowProblemAxiStatic

    # Options for the solve()-method of the thermal subproblem
    solver_info_th: ThermalSolverInfoAxiStatic = ThermalSolverInfoAxiStatic()
    kwargs_th: Dict = field(
        default_factory=dict)  # key word arguments passed to the solve routine of ThermalProblemAxiStatic

    # Options for the successive substitution algorithm of the coupled problem
    tolerance_coupled: float = 1e-8
    max_iter_coupled: int = 100
    relaxation_coupled: float = 0.7
    # endregion

    # region Options for the direct_sensitivity_method()-routine
    # Options for the successive substitution algorithm for the sensitivity problem
    tolerance_dsm: float = 1e-8
    max_iter_dsm: int = 100
    relaxation_dsm: float = 0.7
    # endregion

    # region Options for the adjoint_method()-routine
    # Options for the successive substitution algorithm of the adjoint problem
    tolerance_adj: float = 1e-8
    max_iter_adj: int = 100
    relaxation_adj: float = 0.7
    # endregion


@dataclass()
class ElectrothermalSolverInfoAxiTransient:
    """Class for passing solver options to ElectrothermalProblemAxiStatic"""

    # region Options for the solve()-routine
    # Options for the coupling mechanism
    coupling_mechanism = 'weak'  # alternative 'successive_substitution'

    # region Options for the solve()-method of the electric subproblem
    solver_info_el: CurrentFlowSolverInfoAxiTransient = CurrentFlowSolverInfoAxiTransient()
    kwargs_el: Dict = field(
        default_factory=dict)  # key word arguments passed to the solve routine of CurrentFlowProblemAxiStatic
    linear_interpolation_potential_coupled: bool = True  # If true, the electric solution is interpolated
    # linearly during the solution of the thermal subproblem
    # endregion

    # region Options for the solve()-method of the thermal subproblem
    solver_info_th: ThermalSolverInfoAxiTransient = ThermalSolverInfoAxiTransient()
    kwargs_th: Dict = field(
        default_factory=dict)  # key word arguments passed to the solve routine of ThermalProblemAxiStatic
    linear_interpolation_temperature_coupled: bool = True  # If true, the thermal solution is interpolated
    # linearly during the solution of the electric subproblem
    # endregion

    # region Options for the successive substitution algorithm of the coupled problem
    tolerance_coupled: float = 1e-8
    max_iter_coupled: int = 100
    relaxation_coupled: float = 0.7
    # endregion
    # endregion

    # region Options for the direct_sensitivity_method()-routine
    # Options for the successive substitution algorithm for the sensitivity problem
    tolerance_dsm: float = 1e-8
    max_iter_dsm: int = 100
    relaxation_dsm: float = 0.7
    linear_interpolation_potential_dsm: bool = True
    linear_interpolation_temperature_dsm: bool = True
    # endregion

    # region Options for the adjoint_method()-routine
    # Options for the successive substitution algorithm of the adjoint problem
    tolerance_adj: float = 1e-8
    max_iter_adj: int = 100
    relaxation_adj: float = 0.7
    linear_interpolation_potential_adj: bool = True
    linear_interpolation_adj_1: bool = True
    linear_interpolation_adj_2: bool = True
    linear_interpolation_temperature_adj: bool = True
    # endregion


class ElectrothermalProblemAxiStatic(StaticProblem):
    """A two-dimensional stationary axisymmetric coupled electrothermal problem."""

    problem_identifier = 'Stationary electrothermal 2D problem, axisymmetric'

    def __init__(self, description: str, subproblem_el: CurrentFlowProblemAxiStatic,
                 subproblem_th: ThermalProblemAxiStatic):
        """Constructor.

        Parameters
        ----------
        description : str
            A description of the problem
        stationary_current_problem: CurrentFlowProblemAxiStatic
            electric subproblem
        stationary_heat_conduction_problem: ThermalProblemAxiStatic
            thermal subproblem
        solver_info: ElectrothermalSolverInfoAxiStatic
            Settings for coupled successive substitution solver
        """
        super().__init__(description, None, None, None, None, None, None)
        self.subproblem_el: CurrentFlowProblemAxiStatic = subproblem_el
        self.subproblem_th: ThermalProblemAxiStatic = subproblem_th

    def get_system(self, **kwargs) -> Tuple[Tuple[sparse.spmatrix, sparse.spmatrix]]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> Tuple[CurrentFlowSolutionAxiStatic, ThermalSolutionAxiStatic]:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> Tuple[CurrentFlowSolutionAxiStatic, ThermalSolutionAxiStatic]:
        raise NotImplementedError

    def create_solution(self, solution: np.ndarray, description: str = None, **kwargs) \
            -> Tuple[CurrentFlowSolutionAxiStatic, ThermalSolutionAxiStatic]:
        raise NotImplementedError

    def solve(self, initial_guess_potential: Union[np.ndarray, CurrentFlowSolutionAxiStatic] = None,
              initial_guess_temperature: Union[np.ndarray, ThermalSolutionAxiStatic] = None,
              solver_info: ElectrothermalSolverInfoAxiStatic = None) \
            -> Tuple[CurrentFlowSolutionAxiStatic, ThermalSolutionAxiStatic]:
        # pylint: disable=arguments-differ
        """Solve the coupled problem using the successive substitution method.

        Parameters
        ----------
        initial_guess_potential:
            Initial guess for the potential used for the successive substitution method.
        initial_guess_temperature:
            Initial guess for the temperature used for the successive substitution method.
        solver_info:
            Solver settings for the successive substitution algorithm.

        Returns
        -------
        solution_el: CurrentFlowSolutionAxiStatic
            The electric solution of the coupled problem.
        solution_th: ThermalSolutionAxiStatic
            The thermal solution of the coupled problem.
        """
        # Initialize the solver settings
        if solver_info is None:
            solver_info = ElectrothermalSolverInfoAxiStatic()

        # region Case that the stationary current problem is temperature-independent.
        # -> no iteration between the problems needed
        if not self.subproblem_el.is_temperature_dependent:
            solution_el = self.subproblem_el.solve(initial_guess_potential, solver_info.solver_info_el,
                                                   **solver_info.kwargs_el)
            self.subproblem_th.electromagnetic_heat_source = solution_el
            solution_th = self.subproblem_th.solve(initial_guess_temperature, solver_info.solver_info_th,
                                                   **solver_info.kwargs_th)
            return solution_el, solution_th
        # endregion

        # Initialize successive substitution method for coupled problem
        iter_no = 0

        # region Set initial guesses for potential and temperature
        # region Set initial_guess_potential
        if initial_guess_potential is None:
            # make sure all temperature dependent quantities are initialized
            if initial_guess_temperature is None:  # if no initial temperature is given, assume 293.15K everywhere
                self.subproblem_el.temperature_coupling = np.ones((self.subproblem_th.mesh.num_node,)) * 293.15
            else:
                self.subproblem_el.temperature_coupling = initial_guess_temperature
            solution_el = self.subproblem_el.solve(solver_info=solver_info.solver_info_el, **solver_info.kwargs_el)
        else:
            solution_el = CurrentFlowSolutionAxiStatic.solution_from_problem(
                self.subproblem_el.description, self.subproblem_el, initial_guess_potential)

        self.subproblem_th.electromagnetic_heat_source = solution_el
        # endregion

        # region Set initial_guess_temperature
        if initial_guess_temperature is None:
            solution_th = self.subproblem_th.solve(solver_info=solver_info.solver_info_th, **solver_info.kwargs_th)
        else:
            solution_th = ThermalSolutionAxiStatic.solution_from_problem(self.subproblem_th.description,
                                                                         self.subproblem_th, initial_guess_temperature)
        self.subproblem_el.temperature_coupling = solution_th.temperature
        # endregion
        # endregion

        # Successive substitution iteration between the electric and the thermal subproblems
        while True:
            # region Update iteration variables
            iter_no += 1
            electric_losses_prev = solution_el.joule_loss_power
            thermal_loss_prev = solution_th.thermal_loss_power
            potential_prev = solution_el.potential
            temperature_prev = solution_th.temperature
            # endregion

            # region Solve electric subproblem
            solution_el = self.subproblem_el.solve(initial_guess_potential=potential_prev,
                                                   solver_info=solver_info.solver_info_el,
                                                   **solver_info.kwargs_el)
            # endregion

            # region Insert relaxation
            if solver_info.relaxation_coupled != 1:
                solution_el.potential = solver_info.relaxation_coupled * solution_el.potential \
                    + (1 - solver_info.relaxation_coupled) * potential_prev
            self.subproblem_th.electromagnetic_heat_source = solution_el
            # endregion

            # region Solve thermal subproblem
            solution_th = self.subproblem_th.solve(temperature_prev, solver_info=solver_info.solver_info_th,
                                                   **solver_info.kwargs_th)
            self.subproblem_el.temperature_coupling = solution_th.temperature
            # endregion

            # region Compute relative error
            relative_error_el = np.abs(
                (electric_losses_prev - solution_el.joule_loss_power) / solution_el.joule_loss_power)
            relative_error_th = np.abs((thermal_loss_prev - solution_th.thermal_loss_power)
                                       / solution_th.thermal_loss_power)
            # endregion

            logger.info('Iteration: %d, rel. error: %e', iter_no, np.max([relative_error_el, relative_error_th]))

            # region Terminate algorithm
            # region Check for convergence
            if relative_error_el <= solver_info.tolerance_coupled and \
                    relative_error_th <= solver_info.tolerance_coupled:
                logger.info('Convergence after %d iterations. Relative error in el. losses: %e',
                            iter_no, np.max([relative_error_el, relative_error_th]))
                return solution_el, solution_th
            # endregion

            # region Check if maximum number of iterations is exceeded.
            if iter_no == solver_info.max_iter_coupled:
                logger.info('Maximum number of iterations %d exceeded. Relative error: %e',
                            iter_no, np.max([relative_error_el, relative_error_th]))
                return solution_el, solution_th
            # endregion
            # endregion

    @staticmethod
    def adjoint_method(solution_el: CurrentFlowSolutionAxiStatic,
                       solution_th: ThermalSolutionAxiStatic,
                       qois: QuantitiesOfInterest,
                       save_adj: bool = False,
                       solver_info: ElectrothermalSolverInfoAxiStatic = None,
                       **kwargs):
        """Compute the sensitivities of quantities of interest using the adjoint method.

        Parameters
        ----------
        solution_el: CurrentFlowProblemAxiStatic
            The electric solution of the coupled problem.
        solution_th: ThermalSolutionAxiStatic
            The thermal solution of the coupled problem.
        qois: QuantitiesOfInterest
            The quantities of interest
        save_adj: bool
            Boolean that indicates whether the adjoint variables should be saved. If not, an empty dictionary is
            returned.
        solver_info: ElectrothermalSolverInfoAxiStatic
            Solver settings for the successive substitution algorithm.
        kwargs:
            Are all passed to the function :py:func:`solve_linear_system`.

        Returns
        -------
        sensitivities: Dict[str: float]
            Dictionary with the sensitivities of the quantities of interests. The keys are tuples of the form
            (<name of the quantity of interest>,<name of the parameter>).
        adj_variables_1: Dict[str, np.ndarray]
            Dictionary containing the adjoint variables of the first subproblem (el). The keys are the names of the
            quantities of interest. If save_adj is false, an empty dictionary is returned.
        adj_variables_2: Dict[str, np.ndarray]
            Dictionary containing the adjoint variables of the second subproblem (th). The keys are the names of the
            quantities of interest. If save_adj is false, an empty dictionary is returned.
        """
        # region Initializations and pre-processing
        adj_variables_1 = {}
        adj_variables_2 = {}
        sensitivities = {}

        if solver_info is None:
            solver_info = ElectrothermalSolverInfoAxiStatic()

        solution_el = CurrentFlowSolutionAxiIntermediate.extend_solution(solution_el)
        solution_th = ThermalSolutionAxiIntermediate.extend_solution(solution_th)
        # endregion

        # region Generate adjoint boundary conditions from boundary conditions of original problems
        bdrycond_am_1 = solution_el.boundary_conditions.zero_dirichlet()
        bdrycond_am_2 = solution_th.boundary_conditions.zero_dirichlet()
        # endregion

        # region Compute all system matrices
        # The monolithic system is of the form [[lhs11 lhs12], [lhs21, lhs22]] [[w1],[w2]] = [[rhs1],[rhs2]]
        # lhs_11
        lhs_11 = solution_el.divgrad_matrix_sigmad

        # lhs_12
        tmp = solution_el.e_field * solution_el.differential_conductivity_per_element[:, :, 0] + \
              solution_el.e_field * solution_el.differential_conductivity_per_element[:, :, 1] + \
              solution_el.current_density
        lhs_12 = solution_el.shape_function.fem_div_operator(tmp)

        # lhs_21
        tmp = np.column_stack((solution_el.diff_conductivity_temperature_per_element * solution_el.e_field[:, 0],
                               solution_el.diff_conductivity_temperature_per_element * solution_el.e_field[:, 1]))
        lhs_21 = - solution_el.shape_function.fem_grad_operator(tmp)

        # lhs_22
        tmp1 = np.column_stack((solution_th.diff_thermal_conductivity_temperature_per_element
                                  * solution_th.temperature_gradient[:, 0],
                                  solution_th.diff_thermal_conductivity_temperature_per_element
                                  * solution_th.temperature_gradient[:, 1]))
        tmp2 = solution_el.e_field_abs ** 2 * solution_el.diff_conductivity_temperature_per_element
        lhs_22 = - solution_th.shape_function.fem_grad_operator(tmp1) \
                 + solution_th.divgrad_matrix_lambda \
                 - solution_th.shape_function.mass_matrix(tmp2)
        # endregion

        for qoi in qois:
            # region Compute right-hand sides
            rhs_1 = qoi.evaluate_diff_qoi_dof('potential', [solution_el, solution_th])
            if rhs_1.shape[0] != solution_el.mesh.num_node:
                rhs_1 = rhs_1.transpose()

            rhs_2 = qoi.evaluate_diff_qoi_dof('temperature', [solution_el, solution_th])
            if rhs_2.shape[0] != solution_el.mesh.num_node:
                rhs_2 = rhs_2.transpose()
            # endregion

            # region Successive substitution
            # region Initializations
            iter_no = 0
            adj_1_prev = np.zeros((solution_el.mesh.num_node,))  # needed to insert relaxation
            adj_2 = np.zeros((solution_el.mesh.num_node,))
            integral_value_1 = 0
            integral_value_2 = 0
            relative_error_1 = 0
            relative_error_2 = 0
            # endregion

            while True:
                # region Update iteration variables
                iter_no += 1
                integral_value_prev_1 = integral_value_1
                integral_value_prev_2 = integral_value_2
                # endregion

                # region 1st subproblem (el): Shrink, solve, inflate
                lhs_shrink, rhs_shrink = bdrycond_am_1.shrink(
                    solution_el.mesh, solution_el.shape_function, solution_el.regions,
                    lhs_11.tocoo(), sparse.coo_matrix((rhs_1 - lhs_12 @ adj_2)).transpose(), 1)

                adj_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                rhs_shrink.todense(),
                                                                                **kwargs)
                adj_1 = bdrycond_am_1.inflate(solution_el.mesh, solution_el.shape_function, solution_el.regions,
                                              adj_shrink)
                # endregion

                # region Insert relaxation
                if solver_info.relaxation_adj != 1:
                    adj_1 = solver_info.relaxation_adj * adj_1 + (1 - solver_info.relaxation_adj) * adj_1_prev
                # endregion

                # region 2nd subproblem (th): Shrink, solve, inflate
                lhs_shrink, rhs_shrink = bdrycond_am_2.shrink(solution_th.mesh, solution_th.shape_function,
                                                              solution_th.regions,
                                                              lhs_22.tocoo(),
                                                              sparse.coo_matrix(rhs_2 - lhs_21 @ adj_1).transpose(), 1)

                adj_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                rhs_shrink.todense(),
                                                                                **kwargs)
                adj_2 = bdrycond_am_2.inflate(solution_th.mesh, solution_th.shape_function, solution_th.regions,
                                              adj_shrink)
                # endregion

                # region Check for convergence
                integral_value_1 = adj_1 @ solution_el.divgrad_matrix_sigmad @ adj_1
                integral_value_2 = adj_2 @ solution_th.divgrad_matrix_lambda @ adj_2
                if iter_no > 1:
                    if integral_value_prev_1 != 0:
                        relative_error_1 = np.abs((integral_value_1 - integral_value_prev_1) / integral_value_prev_1)
                    else:
                        relative_error_1 = 0
                    if integral_value_prev_2 != 0:
                        relative_error_2 = np.abs((integral_value_2 - integral_value_prev_2) / integral_value_prev_2)
                    else:
                        relative_error_2 = 0

                    # Check for convergence
                    if relative_error_1 <= solver_info.tolerance_adj and \
                            relative_error_2 <= solver_info.tolerance_adj:
                        logger.info('Convergence after %d iterations. Relative error: %e',
                                    iter_no, max(relative_error_1, relative_error_2))
                        break
                # endregion

                # region Check if maximum number of iterations is exceeded.
                if iter_no == solver_info.max_iter_adj:
                    logger.info('Maximum number of iterations %d exceeded. Relative error: %e',
                                iter_no, max(relative_error_1, relative_error_2))
                    break
                # endregion

                adj_1_prev = adj_1

            # endregion

            if save_adj:
                adj_variables_1[qoi.name] = adj_1
                adj_variables_2[qoi.name] = adj_2

            # region Sensitivity computation
            for param in qoi.get_parameter_names():
                # region Select parameter in materials
                for mat in solution_el.materials:
                    prop: DiffConductivityParameter = mat.get_property(DiffConductivityParameter)
                    prop.parameter_key = param
                for mat in solution_th.materials:
                    prop: DiffThermalConductivityParameter = mat.get_property(DiffThermalConductivityParameter)
                    prop.parameter_key = param
                # endregion

                # region Compute sensitivity
                d_qoi_d_param = qoi.evaluate_diff_qoi_param(param, [solution_el, solution_th])
                sensitivities[(qoi.name, param)] = (
                    d_qoi_d_param - solution_el.potential @ solution_el.compute_Ksigmap() @ adj_1
                    - solution_th.temperature @ solution_th.compute_Klambdap() @ adj_2
                    + adj_2 @ solution_th.shape_function.load_vector(solution_el.dsigmadp_per_element()
                                                                     * solution_el.e_field_abs ** 2))[0]
                # endregion
            # endregion
        return sensitivities, adj_variables_1, adj_variables_2

    @staticmethod
    def direct_sensitivity_method(solution_el: CurrentFlowSolutionAxiStatic,
                                  solution_th: ThermalSolutionAxiStatic,
                                  qois: QuantitiesOfInterest,
                                  save_solution_sensitivities: bool = False,
                                  solver_info: ElectrothermalSolverInfoAxiStatic = None,
                                  **kwargs):
        """Compute the sensitivities of quantities of interest using the direct sensitivity method.

        Parameters
        ----------
        solution_el: CurrentFlowProblemAxiStatic
            The electric solution of the coupled problem.
        solution_th: ThermalSolutionAxiStatic
            The thermal solution of the coupled problem.
        qois: QuantitiesOfInterest
            The quantities of interest
        save_solution_sensitivities: bool
            Boolean that indicates whether the sensitivities of the potential/temperature should be saved.
            If not, empty dictionaries are returned.
        solver_info: ElectrothermalSolverInfoAxiStatic
            Solver settings for the successive substitution algorithm.
        kwargs:
            Are all passed to the function :py:func:`solve_linear_system`.

        Returns
        -------
        sensitivities: Dict[str: float]
            Dictionary with the sensitivities of the quantities of interests. The keys are tuples of the form
            (<name of the quantity of interest>,<name of the parameter>).
        sensitivities_potential: Dict[str, np.ndarray]
            Dictionary containing the sensitivities of the electric potential. The keys are the names of the
            parameters. If save_solution_sensitivities is false, an empty dictionary is returned.
        sensitivities_temperature: Dict[str, np.ndarray]
            Dictionary containing the sensitivities of the temperature. The keys are the names of the
            parameters. If save_solution_sensitivities is false, an empty dictionary is returned.
        """
        # region Initializations and pre-processing
        sensitivities_potential = {}
        sensitivities_temperature = {}
        sensitivities = {}

        if solver_info is None:
            solver_info = ElectrothermalSolverInfoAxiStatic()

        solution_el = CurrentFlowSolutionAxiIntermediate.extend_solution(solution_el)
        solution_th = ThermalSolutionAxiIntermediate.extend_solution(solution_th)
        # endregion

        # region Generate boundary conditions for the sensitivity formulation from bdry conditions of original problem
        bdrycond_dsm_el = solution_el.boundary_conditions.zero_dirichlet()
        bdrycond_dsm_th = solution_th.boundary_conditions.zero_dirichlet()
        # endregion

        # region Compute all system matrices
        lhs_11 = solution_el.divgrad_matrix_sigmad

        tmp = np.column_stack((solution_el.diff_conductivity_temperature_per_element * solution_el.e_field[:, 0],
                               solution_el.diff_conductivity_temperature_per_element * solution_el.e_field[:, 1]))
        lhs_12 = - solution_el.shape_function.fem_div_operator(tmp)

        tmp = solution_el.e_field * solution_el.differential_conductivity_per_element[:, :, 0] + \
              solution_el.e_field * solution_el.differential_conductivity_per_element[:, :, 1] + \
              solution_el.current_density
        lhs_21 = solution_el.shape_function.fem_grad_operator(tmp)

        tmp1 = np.column_stack(
            (solution_th.diff_thermal_conductivity_temperature_per_element * solution_th.temperature_gradient[:, 0],
             solution_th.diff_thermal_conductivity_temperature_per_element * solution_th.temperature_gradient[:, 1]))
        tmp2 = solution_el.e_field_abs ** 2 * solution_el.diff_conductivity_temperature_per_element
        lhs_22 = - solution_th.shape_function.fem_div_operator(tmp1) \
                 + solution_th.divgrad_matrix_lambda \
                 - solution_th.shape_function.mass_matrix(tmp2)
        # endregion

        for param_name in qois.get_parameter_names():
            # region Select parameter in materials
            for mat in solution_el.materials:
                prop: DiffConductivityParameter = mat.get_property(DiffConductivityParameter)
                prop.parameter_key = param_name
            for mat in solution_th.materials:
                prop: DiffThermalConductivityParameter = mat.get_property(DiffThermalConductivityParameter)
                prop.parameter_key = param_name
            # endregion

            # region Compute right-hand sides
            rhs_1 = - solution_el.compute_Ksigmap() @ solution_el.potential
            rhs_2 = np.expand_dims(- solution_th.compute_Klambdap() @ solution_th.temperature, axis=1) \
                    + solution_el.shape_function.load_vector(solution_el.dsigmadp_per_element()
                                                             * solution_el.e_field_abs ** 2)
            # endregion

            # region Successive substitution
            # region Initializations
            iter_no = 0
            sens_potential_prev = np.zeros((solution_el.mesh.num_node,))
            sens_temperature_prev = np.zeros((solution_el.mesh.num_node,))
            integral_value_1 = 0
            integral_value_2 = 0
            # endregion

            while True:
                # region Update iteration variables
                iter_no += 1
                integral_value_prev_1 = integral_value_1
                integral_value_prev_2 = integral_value_2
                # endregion

                # region 1st subproblem (el): Shrink, solve, inflate
                lhs_shrink, rhs_shrink = bdrycond_dsm_el.shrink(solution_el.mesh, solution_el.shape_function,
                                                                solution_el.regions,
                                                                lhs_11.tocoo(),
                                                                sparse.coo_matrix(
                                                                    rhs_1 - lhs_12 @ sens_temperature_prev).transpose(),
                                                                1)

                sens_potential_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                           rhs_shrink.todense(),
                                                                                           **kwargs)
                sens_potential = bdrycond_dsm_el.inflate(solution_el.mesh, solution_el.shape_function,
                                                         solution_el.regions, sens_potential_shrink)
                # endregion

                # region Insert relaxation
                if solver_info.relaxation_dsm != 1:
                    sens_potential = solver_info.relaxation_dsm * sens_potential \
                        + (1 - solver_info.relaxation_dsm) * sens_potential_prev
                # endregion

                # region 2nd subproblem (th): Shrink, solve, inflate
                lhs_shrink, rhs_shrink = bdrycond_dsm_th.shrink(solution_th.mesh, solution_th.shape_function,
                                                                solution_th.regions,
                                                                lhs_22.tocoo(),
                                                                sparse.coo_matrix(
                                                                    rhs_2 - np.expand_dims(lhs_21 @ sens_potential,
                                                                                           axis=1)), 1)

                sens_temperature_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                             rhs_shrink.todense(),
                                                                                             **kwargs)
                sens_temperature_prev = bdrycond_dsm_th.inflate(solution_th.mesh, solution_th.shape_function,
                                                                solution_th.regions,
                                                                sens_temperature_shrink)
                # endregion

                # region Check for convergence
                integral_value_1 = sens_potential @ solution_el.divgrad_matrix_sigmad @ sens_potential
                integral_value_2 = sens_temperature_prev @ solution_th.divgrad_matrix_lambda @ sens_temperature_prev
                if iter_no > 1:
                    if integral_value_prev_1 != 0:
                        relative_error_1 = np.abs((integral_value_1 - integral_value_prev_1) / integral_value_prev_1)
                    else:
                        relative_error_1 = 0
                    if integral_value_prev_2 != 0:
                        relative_error_2 = np.abs((integral_value_2 - integral_value_prev_2) / integral_value_prev_2)
                    else:
                        relative_error_2 = 0

                    # Check for convergence
                    if relative_error_1 <= solver_info.tolerance_dsm and \
                            relative_error_2 <= solver_info.tolerance_dsm:
                        logger.info('Convergence after %d iterations. Relative error: %e',
                                    iter_no, max(relative_error_1, relative_error_2))
                        break
                # endregion

                # region Check if maximum number of iterations is exceeded.
                if iter_no == solver_info.max_iter_dsm:
                    logger.info('Maximum number of iterations %d exceeded. Relative error: %e',
                                iter_no, max(relative_error_1, relative_error_2))
                    break
                # endregion

                sens_potential_prev = sens_potential

            # endregion

            if save_solution_sensitivities:
                sensitivities_potential[param_name] = sens_potential
                sensitivities_temperature[param_name] = sens_temperature_prev

            # region Sensitivity computation
            for qoi in qois.get_qois_from_parameter_name(param_name):
                d_qoi_d_param = qoi.evaluate_diff_qoi_param(param_name, [solution_el, solution_th])
                q_1 = qoi.evaluate_diff_qoi_dof('potential', [solution_el, solution_th])
                q_2 = qoi.evaluate_diff_qoi_dof('temperature', [solution_el, solution_th])
                sensitivities[(qoi.name, param_name)] = d_qoi_d_param \
                    + q_1 @ sens_potential + q_2 @ sens_temperature_prev
            # endregion
        return sensitivities, sensitivities_potential, sensitivities_temperature


class ElectrothermalProblemAxiTransient(TransientProblem):
    """A two-dimensional Transient axisymmetric coupled electrothermal problem."""

    problem_identifier = 'Transient electrothermal 2D problem, axisymmetric'

    def __init__(self, description: str, eqs_problem: CurrentFlowProblemAxiTransient,
                 heat_conduction_problem: ThermalProblemAxiTransient):
        """Constructor

        Parameters
        ----------
        description : str
            A description of the problem
        eqs_problem: CurrentFlowProblemAxiTransient
            The electric subproblem
        heat_conduction_problem: ThermalProblemAxiTransient
            The thermal subproblem
        """
        super().__init__(description, None, None, None, None, None, None, None)
        self.subproblem_el: CurrentFlowProblemAxiTransient = eqs_problem
        self.subproblem_th: ThermalProblemAxiTransient = heat_conduction_problem

        if self.subproblem_el.mesh.num_node != self.subproblem_th.mesh.num_node:
            raise ValueError("The meshes of the thermal and electric subproblem are not compatible!")

    def get_system(self, time: float, **kwargs) \
            -> Tuple[Tuple[List[sparse.spmatrix], List[sparse.spmatrix]],
                     Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> Tuple[CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient]:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> Tuple[CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient]:
        raise NotImplementedError

    def create_solution(self, solutions, time_steps, description: str = None,
                        **kwargs) -> Tuple[CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient]:
        raise NotImplementedError

    @staticmethod
    def create_time_axes_from_step_size(event_times: np.ndarray,
                                        max_step_size_el: Union[float, np.ndarray],
                                        max_step_size_th: Union[float, np.ndarray]):
        """Method to define time axes for both subproblems for given max. step sizes.

        The method ensures that the step sizes in each subinterval are multiples of each other to ensure enough coupling
        checkpoints.

        Parameters
        ----------
        event_times: np.ndarray
            Time instances that must be included in the time discretization :math:`[t_1,t_2,...,t_{N-1}]`.
        max_step_size_el:
            Maximum step size for the electric time discretizaton. It is possible to pass an individual max step size
            for each subinterval :math:`[t_i,t_{i+1}]` defined by the event times.
        max_step_size_th:
            Maximum step size for the thermal time discretizaton. It is possible to pass an individual max step size
            for each subinterval :math:`[t_i,t_{i+1}]` defined by the event times.

        Returns
        -------
        time_steps_el: np.ndarray
            The time discretization of the electric subproblem
        time_steps_th: np.ndarray
            The time discretization of the thermal subproblem
        """
        # Sort event_times
        event_times = np.sort(event_times)

        # region Define maximum step size for each subinterval
        if isinstance(max_step_size_el, float):
            max_step_size_el = np.ones((len(event_times) - 1,))
        elif len(max_step_size_el) != len(event_times) - 1:
            raise ValueError("The given number of maximum step sizes for the electric problem does not match the "
                             "number of intervals.")

        if isinstance(max_step_size_th, float):
            max_step_size_th = np.ones((len(event_times) - 1,))
        elif len(max_step_size_th) != len(event_times) - 1:
            raise ValueError("The given number of maximum step sizes for the thermal problem does not match the "
                             "number of intervals.")
        # endregion

        for cp in range(0, len(event_times) - 1):
            # region Make sure the bigger maximum step size is a multiple of the smaller maximum step size
            # (such that coupling at checkpoints is possible)
            dt_el = max_step_size_el[cp]
            dt_th = max_step_size_th[cp]
            if dt_el < dt_th:
                dt_th = (dt_th // dt_el) * dt_el
            else:
                dt_el = (dt_el // dt_th) * dt_th
            # endregion

            # region Create time axes
            if cp == 0:
                time_steps_el = np.arange(event_times[cp], event_times[cp + 1], dt_el)
                time_steps_th = np.arange(event_times[cp], event_times[cp + 1], dt_th)
            else:
                time_steps_el = np.append(time_steps_el, np.arange(event_times[cp], event_times[cp + 1], dt_el))
                time_steps_th = np.append(time_steps_th, np.arange(event_times[cp], event_times[cp + 1], dt_th))
            # endregion

        # Add last time instance
        time_steps_el = np.append(time_steps_el, event_times[-1])
        time_steps_th = np.append(time_steps_th, event_times[-1])

        return time_steps_el, time_steps_th

    @staticmethod
    def create_time_axes_from_numbers_of_time_steps(event_times: np.ndarray,
                                                    number_of_time_steps_el: Union[int, np.ndarray],
                                                    number_of_time_steps_th):
        """Method to define time axes for both subproblems for given numbers of time steps.

        The method ensures that the step sizes in each subinterval are multiples of each other to ensure enough coupling
        checkpoints.

        Parameters
        ----------
        event_times: np.ndarray
            Time instances that must be included in the time discretization :math:`[t_1,t_2,...,t_{N-1}]`.
        number_of_time_steps_el:
            Number of time steps for the electric time discretizaton. It is possible to pass an individual number of
            time steps for each subinterval :math:`[t_i,t_{i+1}]` defined by the event times.
        number_of_time_steps_th:
            Number of time steps for the thermal time discretizaton. It is possible to pass an individual number of
            time steps for each subinterval :math:`[t_i,t_{i+1}]` defined by the event times.

        Returns
        -------
        time_steps_el: np.ndarray
            The time discretization of the electric subproblem
        time_steps_th: np.ndarray
            The time discretization of the thermal subproblem
        """
        if isinstance(number_of_time_steps_el, int):
            number_of_time_steps_el = number_of_time_steps_el * np.ones((len(event_times) - 1,))

        if isinstance(number_of_time_steps_th, int):
            number_of_time_steps_th = number_of_time_steps_th * np.ones((len(event_times) - 1,))

        # Ensure each interval has at least two time steps (start and end time)
        number_of_time_steps_el = np.where(number_of_time_steps_el <= 1, 2, number_of_time_steps_el)
        number_of_time_steps_th = np.where(number_of_time_steps_th <= 1, 2, number_of_time_steps_th)

        # Convert number of time steps into max. step sizes
        max_step_size_el = np.diff(event_times) / (number_of_time_steps_el - 1)
        max_step_size_th = np.diff(event_times) / (number_of_time_steps_th - 1)

        return ElectrothermalProblemAxiTransient.create_time_axes_from_step_size(event_times,
                                                                                 max_step_size_el, max_step_size_th)

    @staticmethod
    def _find_coupling_indices(time_steps_el: np.ndarray, time_steps_th: np.ndarray) \
            -> (np.ndarray, np.ndarray):
        """Method that finds the common time instances of two given time discretizations.

        Returns the indices of these instances for both time vectors.
        """
        common_values = np.intersect1d(time_steps_el, time_steps_th)
        indices_coupling_el = np.searchsorted(time_steps_el, common_values)
        indices_coupling_th = np.searchsorted(time_steps_th, common_values)

        # Make sure the time discretizations not only have start and end value in common.
        if len(indices_coupling_el) == 2:
            logger.warning('Only two coupling indices were found. Consider using the methods '
                           '\'create_time_axes_from_numbers_of_time_steps\' or '
                           '\'create_time_axes_from_step_size\' to create the time axes for the subproblems.')

        return indices_coupling_el, indices_coupling_th

    @staticmethod
    def _prepare_solution_monitor(solution_monitor: Union[int, Iterable[int]], time_steps: np.ndarray) \
            -> Iterable[int]:
        # Pre-process solution_monitors
        if isinstance(solution_monitor, int):
            solution_monitor = np.arange(start=0, stop=len(time_steps), step=solution_monitor)
            if solution_monitor[-1] != len(time_steps) - 1:
                solution_monitor = np.concatenate([solution_monitor, np.array([len(time_steps) - 1])])
        return solution_monitor

    @staticmethod
    def _solution_monitors_on_interval(coupling_indices: np.ndarray, interval_idx: int, solution_monitor: np.ndarray) \
            -> np.ndarray:
        """Find the solution monitors of a subproblem on a given interval.

        Parameters
        ----------
        coupling_indices:
            Coupling indices of a subproblem.
        interval_idx:
            Index of the subinterval.
        solution_monitor:
            Solution monitors of a subproblem.

        Returns
        -------
        np.ndarray
            Solution monitors for a solution of the subproblem solved on the specified subinterval.

        """
        return np.extract(np.logical_and(coupling_indices[interval_idx] <= solution_monitor,
                                         coupling_indices[interval_idx + 1] >= solution_monitor), solution_monitor) \
               - coupling_indices[interval_idx]

    @staticmethod
    def _concatenate_solutions(solution: Union[CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient],
                               solution_interval: Union[CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient]):
        # Append a solution on an interval to a given solution (including monitors)

        # If solution is None, directly return solution_interval
        if solution is None:
            return solution_interval

        # Set solution
        tmp = solution_interval.get_solution()[1:, :]
        solution.set_solution(np.vstack((solution.get_solution(), tmp)))

        # Set time_steps
        solution.time_steps = (np.hstack((solution.time_steps, solution_interval.time_steps[1:])))

        # Append monitors
        for key in solution.monitor_solutions.keys():
            skip_first_entry = 0
            if solution.monitor_solutions[key][0][-1] == solution_interval.monitor_solutions[key][0][0]:
                skip_first_entry = 1
            if solution_interval.monitor_solutions[key][1].ndim == 1:
                solution.monitor_solutions[key] = (np.hstack((solution.monitor_solutions[key][0],
                                                              solution_interval.monitor_solutions[key][0][
                                                              skip_first_entry:])),
                                                   np.hstack((solution.monitor_solutions[key][1],
                                                              solution_interval.monitor_solutions[key][1][
                                                              skip_first_entry:])))
            else:
                solution.monitor_solutions[key] = (np.hstack((solution.monitor_solutions[key][0],
                                                              solution_interval.monitor_solutions[key][0][
                                                              skip_first_entry:])),
                                                   np.vstack((solution.monitor_solutions[key][1],
                                                              solution_interval.monitor_solutions[key][1][
                                                              skip_first_entry:])))

        return solution

    def _weak_coupling(self, initial_value_potential: Union[np.ndarray, CurrentFlowSolutionAxiStatic],
                       initial_value_temperature: Union[np.ndarray, ThermalSolutionAxiStatic],
                       time_steps_el: np.ndarray, time_steps_th: np.ndarray,
                       solution_monitor: Tuple[Union[int, Iterable[int]], Union[int, Iterable[int]]] = (1, 1),
                       solver_info: ElectrothermalSolverInfoAxiTransient = None) \
            -> Tuple[CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient]:
        """Solve coupled problem using weak coupling.

        Parameters
        ----------
        initial_value_potential:
            Initial condition for the electric potential
        initial_value_temperature:
            Initial condition for the temperature
        time_steps_el:
            Time axis of electric subproblem
        time_steps_th:
            Time axis of thermal subproblem
        solution_monitor : Union[int, np.ndarray]
            Determines at which time steps the solution should be stored in the solution object. If it is an integer
            :math:`n`, the solution is stored at every :math:`n`-th time step (including the first and the last one).
            If it is an array, store at the indicated time steps.
        solver_info:
            Solver settings.

        """
        # region Pre-process time axes
        coupling_indices_el, coupling_indices_th = self._find_coupling_indices(time_steps_el, time_steps_th)

        solution_monitor_el = ElectrothermalProblemAxiTransient._prepare_solution_monitor(solution_monitor[0],
                                                                                          time_steps_el)
        solution_monitor_th = ElectrothermalProblemAxiTransient._prepare_solution_monitor(solution_monitor[1],
                                                                                          time_steps_th)
        # endregion

        # region Initialization
        potential_prev = initial_value_potential
        temperature_prev = initial_value_temperature
        sol_el = None
        sol_th = None
        # endregion

        for interval_idx in range(0, len(coupling_indices_el) - 1):  # Loop over all subintervals
            # region Find monitor steps on interval
            solution_monitor_interval_el = ElectrothermalProblemAxiTransient._solution_monitors_on_interval(
                coupling_indices_el, interval_idx, solution_monitor_el)
            solution_monitor_interval_th = ElectrothermalProblemAxiTransient._solution_monitors_on_interval(
                coupling_indices_th, interval_idx, solution_monitor_th)
            # endregion

            # region Solve electric subproblem:
            self.subproblem_el.temperature_coupling = temperature_prev
            self.subproblem_el.time_steps = time_steps_el[coupling_indices_el[interval_idx]:
                                                          coupling_indices_el[interval_idx + 1] + 1]
            sol_interval_el = self.subproblem_el.solve(potential_prev, solution_monitor=solution_monitor_interval_el,
                                                       solver_info=solver_info.solver_info_el,
                                                       **solver_info.kwargs_el)
            sol_interval_el.linear_interpolation = solver_info.linear_interpolation_potential_coupled
            # endregion

            # region Solve thermal subproblem:
            self.subproblem_th.time_steps = time_steps_th[
                coupling_indices_th[interval_idx]:coupling_indices_th[interval_idx + 1] + 1]
            self.subproblem_th.electromagnetic_heat_source = sol_interval_el
            # ToDo: Question: For weak coupling, the thermal problem should only see the em_heat_source at the coupling
            #  indices --> waste of information
            sol_interval_th = self.subproblem_th.solve(temperature_prev, solution_monitor=solution_monitor_interval_th,
                                                       solver_info=solver_info.solver_info_th,
                                                       **solver_info.kwargs_th)
            sol_interval_th.linear_interpolation = solver_info.linear_interpolation_temperature_coupled
            # endregion

            # region Define initial conditions for the next subinterval
            potential_prev = sol_interval_el.potential(index=sol_interval_el.time_steps.size - 1)
            temperature_prev = sol_interval_th.temperature(index=sol_interval_th.time_steps.size - 1)
            # endregion

            # region Append solution of current interval to output
            sol_el = ElectrothermalProblemAxiTransient._concatenate_solutions(sol_el, sol_interval_el)
            sol_th = ElectrothermalProblemAxiTransient._concatenate_solutions(sol_th, sol_interval_th)
            # endregion

        return sol_el, sol_th

    def _successive_substitution_coupling(self,
                                          initial_value_potential: Union[np.ndarray, CurrentFlowSolutionAxiStatic],
                                          initial_value_temperature: Union[np.ndarray, ThermalSolutionAxiStatic],
                                          time_steps_el: np.ndarray, time_steps_th: np.ndarray,
                                          solution_monitor: Tuple[
                                              Union[int, Iterable[int]], Union[int, Iterable[int]]] = (1, 1),
                                          solver_info: ElectrothermalSolverInfoAxiTransient = None) \
            -> Tuple[CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient]:
        """Solve coupled problem using successive substitution coupling.

        Parameters
        ----------
        initial_value_potential:
            Initial condition for the electric potential
        initial_value_temperature:
            Initial condition for the temperature
        time_steps_el:
            Time axis of electric subproblem
        time_steps_th:
            Time axis of thermal subproblem
        solution_monitor : Union[int, np.ndarray]
            Determines at which time steps the solution should be stored in the solution object. If it is an integer
            :math:`n`, the solution is stored at every :math:`n`-th time step (including the first and the last one).
            If it is an array, store at the indicated time steps.
        solver_info:
            Solver settings.

        """
        # region Pre-process time axes
        coupling_indices_el, coupling_indices_th = self._find_coupling_indices(time_steps_el, time_steps_th)

        solution_monitor_el = ElectrothermalProblemAxiTransient._prepare_solution_monitor(solution_monitor[0],
                                                                                          time_steps_el)
        solution_monitor_th = ElectrothermalProblemAxiTransient._prepare_solution_monitor(solution_monitor[1],
                                                                                          time_steps_th)
        # endregion

        # region Initialization
        potential_prev = initial_value_potential
        temperature_prev = initial_value_temperature
        sol_el = None
        sol_th = None
        # endregion

        # Loop over all sub-intervals
        for interval_idx in range(0, len(coupling_indices_el) - 1):
            # region Find monitor steps of current interval
            solution_monitor_interval_el = ElectrothermalProblemAxiTransient._solution_monitors_on_interval(
                coupling_indices_el, interval_idx, solution_monitor_el)
            solution_monitor_interval_th = ElectrothermalProblemAxiTransient._solution_monitors_on_interval(
                coupling_indices_th, interval_idx, solution_monitor_th)
            # endregion

            # region Compute initial guesses for the solutions before entering the succ. subst. iteration
            # region Solve electric subproblem:
            self.subproblem_el.temperature_coupling = temperature_prev
            self.subproblem_el.time_steps = time_steps_el[coupling_indices_el[interval_idx]:
                                                          coupling_indices_el[interval_idx + 1] + 1]
            sol_interval_el = self.subproblem_el.solve(potential_prev, solution_monitor=solution_monitor_interval_el,
                                                       solver_info=solver_info.solver_info_el,
                                                       **solver_info.kwargs_el)
            sol_interval_el.linear_interpolation = solver_info.linear_interpolation_potential_coupled
            self.subproblem_th.electromagnetic_heat_source = sol_interval_el
            # endregion

            # region Solve thermal subproblem:
            self.subproblem_th.time_steps = time_steps_th[
                coupling_indices_th[interval_idx]:coupling_indices_th[interval_idx + 1] + 1]
            sol_interval_th = self.subproblem_th.solve(temperature_prev, solution_monitor=solution_monitor_interval_th,
                                                       solver_info=solver_info.solver_info_th,
                                                       **solver_info.kwargs_th)
            sol_interval_th.linear_interpolation = solver_info.linear_interpolation_temperature_coupled
            self.subproblem_el.temperature_coupling = sol_interval_th
            # endregion
            # endregion

            iter_no = 0
            while True:
                # region Update iteration variables
                iter_no += 1
                losses_el_prev_iter = sol_interval_el.joule_loss_power(index=sol_interval_el.time_steps.size - 1)
                losses_th_prev_iter = sol_interval_th.thermal_loss_power(index=sol_interval_th.time_steps.size - 1)
                # endregion

                # region Solve electric subproblem
                sol_interval_el = self.subproblem_el.solve(potential_prev,
                                                           solution_monitor=solution_monitor_interval_el,
                                                           solver_info=solver_info.solver_info_el,
                                                           **solver_info.kwargs_el)
                sol_interval_el.linear_interpolation = solver_info.linear_interpolation_potential_coupled
                self.subproblem_th.electromagnetic_heat_source = sol_interval_el
                # endregion

                # region Solve thermal subproblem
                sol_interval_th = self.subproblem_th.solve(temperature_prev,
                                                           solution_monitor=solution_monitor_interval_el,
                                                           solver_info=solver_info.solver_info_th,
                                                           **solver_info.kwargs_th)
                sol_interval_th.linear_interpolation = solver_info.linear_interpolation_temperature_coupled
                self.subproblem_el.temperature_coupling = sol_interval_th
                # endregion

                # region Compute relative errors
                idx_el = sol_interval_el.time_steps.size - 1
                losses_el_new_iter = sol_interval_el.joule_loss_power(index=idx_el)
                idx_th = sol_interval_th.time_steps.size - 1
                losses_th_new_iter = sol_interval_th.thermal_loss_power(index=idx_th)

                relative_error_el = np.abs((losses_el_new_iter - losses_el_prev_iter) / losses_el_new_iter)
                relative_error_th = np.abs((losses_th_new_iter - losses_th_prev_iter) / losses_th_new_iter)
                # endregion

                # region Check for convergence
                if relative_error_el <= solver_info.tolerance_coupled and \
                        relative_error_th <= solver_info.tolerance_coupled:
                    logger.info('%s of %s: Convergence after %d iterations. Relative error in el. losses: %f',
                                interval_idx + 1, len(coupling_indices_el) - 1,
                                iter_no, relative_error_el)
                    break
                # endregion

                # region Check if maximum number of iterations is exceeded.
                if iter_no == solver_info.max_iter_coupled:
                    logger.info(interval_idx, ' of ', len(coupling_indices_el) - 1,
                                ': Maximum number of iterations %d exceeded. Relative error in el. losses: %f',
                                iter_no, relative_error_el)
                    break
                # endregion

            # region Define initial conditions for the next interval
            potential_prev = sol_interval_el.potential(index=idx_el)
            temperature_prev = sol_interval_th.temperature(index=idx_th)
            # endregion

            # region Write interval solution to output
            sol_el = ElectrothermalProblemAxiTransient._concatenate_solutions(sol_el, sol_interval_el)
            sol_th = ElectrothermalProblemAxiTransient._concatenate_solutions(sol_th, sol_interval_th)
            # endregion

        return sol_el, sol_th

    def solve(self, initial_value_potential: Union[np.ndarray, CurrentFlowSolutionAxiStatic],
              initial_value_temperature: Union[np.ndarray, ThermalSolutionAxiStatic],
              time_steps_el: np.ndarray, time_steps_th: np.ndarray,
              solution_monitor: Tuple[Union[int, Iterable[int]], str] = (1, 1),
              solver_info: ElectrothermalSolverInfoAxiTransient = None) \
            -> Tuple[CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient]:
        # pylint: disable=arguments-differ, arguments-renamed
        """Solve the coupled transient problem.

        Parameters
        ----------
        initial_value_potential: Union[np.ndarray, CurrentFlowSolutionAxiStatic]
            Initial condition for the electric potential.
        initial_value_temperature: Union[np.ndarray, ThermalSolutionAxiStatic]
            Initial condition for the temperature.
        time_steps_el: np.ndarray
            Time discretization of the electric subproblem.
        time_steps_th: np.ndarray
            Time discretization of the thermal subproblem.
        solution_monitor : Tuple[Union[int, Iterable[int]], str]
            Tuple of solution_monitors, the first entry is passed to
            :py:func:`~pyrit.problem.CurrentFlowProblemAxiTransient.solve`, the
            other to :py:func:`~pyrit.problem.ThermalProblemAxiTransient.solve`
        solver_info: ElectrothermalSolverInfoAxiTransient
            Solver settings, regarding the coupling mechanism.

        Returns
        -------
        solution_electric: CurrentFlowSolutionAxiTransient
            The electric solution of the coupled problem.
        solution_thermal: ThermalSolutionAxiTransient
            The thermal solution of the coupled problem.
        """
        if not (np.isclose(time_steps_el[0], time_steps_th[0]) and np.isclose(time_steps_el[-1], time_steps_th[-1])):
            raise ValueError("Start and end time of thermal and electric time axes must match.")

        if solver_info is None:
            solver_info = ElectrothermalSolverInfoAxiTransient()

        # region Case that the eqs problem does not depend on the temperature
        if not self.subproblem_el.is_temperature_dependent:
            # Set time steps
            self.subproblem_el.time_steps = time_steps_el
            self.subproblem_th.time_steps = time_steps_th

            # Solve electric subproblem
            solution_el = self.subproblem_el.solve(initial_value_potential, solution_monitor=solution_monitor[0],
                                                   solver_info=solver_info.solver_info_el,
                                                   **solver_info.kwargs_el)

            # Set EM heat source
            solution_el.linear_interpolation = solver_info.linear_interpolation_potential_coupled
            self.subproblem_th.electromagnetic_heat_source = solution_el

            # Solve thermal subproblem
            solution_th = self.subproblem_th.solve(initial_value_temperature, solution_monitor=solution_monitor[1],
                                                   solver_info=solver_info.solver_info_th,
                                                   **solver_info.kwargs_th)
            return solution_el, solution_th
        # endregion

        # Weak coupling
        if solver_info.coupling_mechanism == 'weak':
            return self._weak_coupling(initial_value_potential, initial_value_temperature,
                                       time_steps_el, time_steps_th,
                                       solution_monitor, solver_info)

        # Successive substitution coupling
        if solver_info.coupling_mechanism == 'successive_substitution':
            return self._successive_substitution_coupling(initial_value_potential, initial_value_temperature,
                                                          time_steps_el, time_steps_th,
                                                          solution_monitor, solver_info)

        raise ValueError('Coupling mechanism unknown, should be either \'weak\' '
                         'or \'successive_substitution\' but was \'' + solver_info.coupling_mechanism + '\'')

    def adjoint_method(self, solution_el: CurrentFlowSolutionAxiTransient,
                       solution_th: ThermalSolutionAxiTransient,
                       qois: QuantitiesOfInterest,
                       sensitivity_potential_initial_value: Dict[str, np.ndarray],
                       sensitivity_temperature_initial_value: Dict[str, np.ndarray],
                       time_steps_adj_1: np.ndarray = None,
                       time_steps_adj_2: np.ndarray = None,
                       solver_info: ElectrothermalSolverInfoAxiTransient = None):
        """Compute the sensitivities of quantities of interest using the adjoint method.

        Parameters
        ----------
        solution_el: CurrentFlowSolutionAxiTransient
            The electric solution of the coupled problem.
        solution_th: ThermalSolutionAxiTransient
            The thermal solution of the coupled problem.
        qois: QuantitiesOfInterest
            The quantities of interest
        sensitivities_potential_initial_value: Dict[str, np.ndarray]
            The sensitivities of the electric potential at the initial time.
            Can be computed using
            :py:func:`~pyrit.problem.ElectrothermalProblemAxiStatic.direct_sensitivity_method`
        sensitivity_temperature_initial_value: Dict[str, np.ndarray]
            The sensitivities of the temperature at the initial time.
            Can be computed using
            :py:func:`~pyrit.problem.ElectrothermalProblemAxiStatic.direct_sensitivity_method`
        time_steps_adj_1: np.ndarray
            Time discretization of the first adjoint subproblem (similar to the eqs adjoint equation)
        time_steps_adj_2: np.ndarray
            Time discretization of the second adjoint subproblem (similar to the heat conduction adjoint equation)
        solver_info: ElectrothermalSolverInfoAxiStatic
            Solver settings for the successive substitution algorithm.

        Returns
        -------
        sensitivities: Dict[str: float]
            Dictionary with the sensitivities of the quantities of interests. The keys are tuples of the form
            (<name of the quantity of interest>,<name of the parameter>).
        """
        # region Solver settings
        if solver_info is None:
            solver_info = ElectrothermalSolverInfoAxiTransient()
        # Set interpolation type of solution
        solution_el.linear_interpolation = solver_info.linear_interpolation_potential_adj
        solution_th.linear_interpolation = solver_info.linear_interpolation_temperature_adj
        # endregion

        # region Define adjoint boundary conditions from boundary conditions of original problem
        bdrycond_adj_1 = solution_el.boundary_conditions.zero_dirichlet()
        bdrycond_adj_2 = solution_th.boundary_conditions.zero_dirichlet()
        # endregion

        # region Define final condition
        final_value = np.zeros((solution_el.mesh.num_node,))
        final_value_1 = {}
        final_value_2 = {}
        for qoi in qois:
            final_value_1[qoi.name] = final_value
            final_value_2[qoi.name] = final_value
        # endregion

        # region Initializations
        # region Define time axes of adjoint problems
        # If no time axes are specified, use the time axes of the original problems
        if time_steps_adj_1 is None:
            time_steps_adj_1 = solution_el.time_steps
        if time_steps_adj_2 is None:
            time_steps_adj_2 = solution_th.time_steps

        # Find coupling indices (Needed for information exchange between the subproblem)
        coupling_indices_1, coupling_indices_2 = self._find_coupling_indices(time_steps_adj_1,
                                                                             time_steps_adj_2)
        # endregion

        # region Initialize sensitivity dictionaries
        sensitivities_1 = qois.initialize_sensitivity_dictionary()
        sensitivities_boundary_terms_1 = qois.initialize_sensitivity_dictionary()
        sensitivities_2 = qois.initialize_sensitivity_dictionary()
        sensitivities_boundary_terms_2 = qois.initialize_sensitivity_dictionary()
        sensitivities = qois.initialize_sensitivity_dictionary()
        # endregion

        # Frequently used values
        num_intervals = len(coupling_indices_1) - 1
        num_node = self.subproblem_el.mesh.num_node

        # region Define static solutions used to compute the matrices
        # (instead of using the transient solution --> avoid storing/recomputing the matrices)
        static_solution_helper_el = solution_el.get_static_solution(time=time_steps_adj_1[0])
        static_solution_helper_el = CurrentFlowSolutionAxiIntermediate.extend_solution(static_solution_helper_el)
        static_solution_helper_th = solution_th.get_static_solution(time=time_steps_adj_2[0])
        static_solution_helper_th = ThermalSolutionAxiIntermediate.extend_solution(static_solution_helper_th)
        # endregion

        # region Initialize transient solution objects used to store the adjoint solutions on the subintervals
        adj_interval_1 = CurrentFlowSolutionAxiTransient("", np.zeros((1, num_node)), solution_el.mesh,
                                                         None, None, None, None, None, np.array([0]), None)
        adj_interval_1.linear_interpolation = solver_info.linear_interpolation_adj_1
        adj_interval_2 = CurrentFlowSolutionAxiTransient("", np.zeros((1, num_node)), solution_el.mesh,
                                                         None, None, None, None, None, np.array([0]), None)
        adj_interval_2.linear_interpolation = solver_info.linear_interpolation_adj_2
        # endregion
        # endregion

        # region Loop over all time intervals
        for idx in range(0, num_intervals):
            logger.info("Starting with interval %d of %d", idx + 1, num_intervals)

            # region Define time steps for time interval
            time_steps_interval_1 = time_steps_adj_1[coupling_indices_1[num_intervals - (idx + 1)]:
                                                     coupling_indices_1[num_intervals - idx] + 1]
            time_steps_interval_2 = time_steps_adj_2[coupling_indices_2[num_intervals - (idx + 1)]:
                                                     coupling_indices_2[num_intervals - idx] + 1]
            # endregion

            # region Precompute matrices needed to check convergence of successive substitution algorithm
            divgrad_sigmad = solution_el.divgrad_matrix_sigmad(time=time_steps_interval_1[0])
            divgrad_lambda = solution_th.divgrad_matrix_lambda(time=time_steps_interval_2[0])
            # endregion

            # Loop over all QoIs
            for qoi in qois:

                # region Successive substitution
                # region Initialization of iteration variables
                iter_no = 0
                integral_value_1 = 0
                integral_value_2 = 0
                relative_error_1 = 0
                relative_error_2 = 0
                # Initialize adjoint variables on subintervall using the final value of the interval.
                adj_interval_2.set_potential(np.tile(final_value_2[qoi.name],
                                                     (len(time_steps_interval_2), 1)))
                adj_interval_2.time_steps = time_steps_interval_2
                adj_interval_1.set_potential(np.tile(final_value_1[qoi.name],
                                                     (len(time_steps_interval_1), 1)))
                adj_interval_1.time_steps = time_steps_interval_1
                # endregion

                while True:
                    # region Update iteration variables
                    iter_no += 1
                    integral_value_prev_1 = integral_value_1
                    integral_value_prev_2 = integral_value_2
                    # endregion

                    # region Solve first subproblem
                    adj_prev_time_step_1 = final_value_1[qoi.name]  # Select final condition of subinterval
                    adj_interval_prev_1 = adj_interval_1.potential()
                    # Loop over the time steps of the subinterval
                    for ii in range(1, len(time_steps_interval_1)):
                        delta_t = time_steps_interval_1[len(time_steps_interval_1) - ii] - time_steps_interval_1[
                            len(time_steps_interval_1) - ii - 1]
                        time = time_steps_interval_1[len(time_steps_interval_1) - ii - 1]

                        # region Update static helper solutions to desired time step
                        static_solution_helper_el.time = time
                        static_solution_helper_el.potential = solution_el.potential(time=time)
                        static_solution_helper_el.temperature_coupling = solution_th.temperature(time=time)
                        # endregion

                        # region Compute matrices
                        # -div(sigmad grad(w1)) --> K_sigmad @ w1
                        lhs_11 = static_solution_helper_el.divgrad_matrix_sigmad

                        # div(epsd dt(grad(w2)) --> lhs: Kepsd/dt @ w1_n, rhs: K_epsd/dt @ w1_nn
                        lhs_11_dt = static_solution_helper_el.divgrad_matrix_epsd / delta_t

                        # -div(w2(sigmad @ E + J)) --> FEMDIV_(sigmad @ E + J) @ w2
                        tmp = static_solution_helper_el.e_field * \
                              static_solution_helper_el.differential_conductivity_per_element[:, :, 0] + \
                              static_solution_helper_el.e_field * \
                              static_solution_helper_el.differential_conductivity_per_element[:, :, 1] + \
                              static_solution_helper_el.current_density
                        lhs_12 = static_solution_helper_el.shape_function.fem_div_operator(tmp)

                        # dg/dphi --> q
                        q = qoi.evaluate_diff_qoi_dof('potential',
                                                      [static_solution_helper_el, static_solution_helper_th, time])
                        if q.shape[0] != num_node:
                            q = q.transpose()
                        # endregion

                        # region Shrink, solve, inflate
                        lhs_shrink, rhs_shrink = bdrycond_adj_1.shrink(
                            solution_el.mesh, solution_el.shape_function, solution_el.regions,
                            lhs_11.tocoo() + lhs_11_dt, sparse.coo_matrix(
                                q - lhs_12 @ adj_interval_2.potential(time=time)
                                + lhs_11_dt @ adj_prev_time_step_1).transpose(), 1)

                        adj_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                        rhs_shrink.todense())
                        adj_prev_time_step_1 = bdrycond_adj_1.inflate(solution_el.mesh, solution_el.shape_function,
                                                                      solution_el.regions, adj_shrink)
                        adj_interval_1.set_potential(adj_prev_time_step_1, time=time)
                        # endregion
                    # endregion

                    # region Insert relaxation
                    if solver_info.relaxation_coupled != 1:
                        adj_interval_1.set_potential(
                            solver_info.relaxation_adj * adj_interval_1.potential()
                            + (1 - solver_info.relaxation_adj) * adj_interval_prev_1)
                    # endregion

                    # region Solve second subproblem
                    adj_prev_time_step_2 = final_value_2[qoi.name]  # Select final condition of subinterval
                    # Loop over the time steps of the subinterval
                    for ii in range(1, len(time_steps_interval_2)):
                        delta_t = time_steps_interval_2[len(time_steps_interval_2) - ii] - time_steps_interval_2[
                            len(time_steps_interval_2) - ii - 1]
                        time = time_steps_interval_2[len(time_steps_interval_2) - ii - 1]

                        # region Update static helper solutions to desired time step
                        static_solution_helper_el.time = time
                        static_solution_helper_el.potential = solution_el.potential(time=time)
                        static_solution_helper_el.temperature_coupling = solution_th.temperature(time=time)
                        static_solution_helper_th.time = time
                        static_solution_helper_th.temperature = static_solution_helper_el.temperature_coupling
                        # endregion

                        # region Compute matrices
                        # -grad(w1) dsigma/dT E --> - FEMGRAD_(dsigma/dT E) @ w1
                        tmp = np.column_stack((static_solution_helper_el.diff_conductivity_temperature_per_element
                                               * static_solution_helper_el.e_field[:, 0],
                                               static_solution_helper_el.diff_conductivity_temperature_per_element
                                               * static_solution_helper_el.e_field[:, 1]))
                        lhs_21 = - static_solution_helper_el.shape_function.fem_grad_operator(tmp)

                        # d/dt(grad(w1)) deps/dT E --> FEMGRAD_(deps/dT E)@ (w1_nn - w1_n) / dt
                        tmp = np.column_stack((static_solution_helper_el.diff_permittivity_temperature_per_element
                                               * static_solution_helper_el.e_field[:, 0],
                                               static_solution_helper_el.diff_permittivity_temperature_per_element
                                               * static_solution_helper_el.e_field[:, 1]))
                        lhs_21_dt = static_solution_helper_th.shape_function.fem_grad_operator(tmp)
                        idx_time_adj1 = adj_interval_1.get_index(time, None)
                        dt_adj1 = (adj_interval_1.potential(index=idx_time_adj1 + 1)
                                   - adj_interval_1.potential(index=idx_time_adj1)) \
                                  / (adj_interval_1.time_steps[idx_time_adj1 + 1]
                                     - adj_interval_1.time_steps[idx_time_adj1])

                        # grad(w2) dlambda/dT gradT - div(lambda grad(w2)) - w2 Eabs **2 dsigma/dT
                        # --> (FEMGRAD_(dlambda/dT gradT) + K_lambda - M_(Eabs **2 dsigma/dT)) @ w2
                        # Remember that temperature gradient is defined as -gradT in the solution class
                        tmp1 = np.column_stack(
                            (static_solution_helper_th.diff_thermal_conductivity_temperature_per_element
                             * static_solution_helper_th.temperature_gradient[:, 0],
                             static_solution_helper_th.diff_thermal_conductivity_temperature_per_element
                             * static_solution_helper_th.temperature_gradient[:, 1]))
                        tmp2 = static_solution_helper_el.e_field_abs ** 2 \
                               * static_solution_helper_el.diff_conductivity_temperature_per_element
                        lhs_22 = - static_solution_helper_th.shape_function.fem_grad_operator(tmp1) \
                                 + static_solution_helper_th.divgrad_matrix_lambda \
                                 - static_solution_helper_th.shape_function.mass_matrix(tmp2)

                        # - d/dt(w2) (ds/dT * T+ s) --> - M_(ds/dT * T+ s) / dt @ (w2_nn - w2_n)
                        temperature_per_element = static_solution_helper_el.mesh.prj_nd2el(
                            static_solution_helper_th.temperature)
                        tmp = static_solution_helper_th.diff_volumetric_heat_capacity_temperature_per_element \
                              * temperature_per_element \
                              + static_solution_helper_th.volumetric_heat_capacity_per_element
                        lhs_22_dt = static_solution_helper_th.shape_function.mass_matrix(tmp) / delta_t

                        q = qoi.evaluate_diff_qoi_dof('temperature',
                                                      [static_solution_helper_el, static_solution_helper_th, time])
                        if q.shape[0] != num_node:
                            q = q.transpose()
                        # endregion

                        # region Shrink, solve, inflate
                        lhs_shrink, rhs_shrink = bdrycond_adj_2.shrink(
                            static_solution_helper_th.mesh, static_solution_helper_th.shape_function,
                            static_solution_helper_th.regions,
                            lhs_22.tocoo() + lhs_22_dt, sparse.coo_matrix(
                                q - lhs_21 @ adj_interval_1.potential(time=time)
                                - lhs_21_dt @ dt_adj1 + lhs_22_dt @ adj_prev_time_step_2).transpose(), 1)

                        adj_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                        rhs_shrink.todense())
                        adj_prev_time_step_2 = bdrycond_adj_2.inflate(static_solution_helper_th.mesh,
                                                                      static_solution_helper_th.shape_function,
                                                                      static_solution_helper_th.regions, adj_shrink)
                        adj_interval_2.set_potential(adj_prev_time_step_2, time=time)
                        # endregion
                    # endregion

                    # region Check for convergence
                    integral_value_1 = adj_interval_1.potential(time=time_steps_interval_1[0]) \
                                       @ divgrad_sigmad @ adj_interval_1.potential(time=time_steps_interval_1[0])
                    integral_value_2 = adj_interval_2.potential(time=time_steps_interval_2[0]) \
                                       @ divgrad_lambda @ adj_interval_2.potential(time=time_steps_interval_2[0])
                    if iter_no > 1:
                        if integral_value_prev_1 != 0:
                            relative_error_1 = np.abs(
                                (integral_value_1 - integral_value_prev_1) / integral_value_prev_1)
                        else:
                            relative_error_1 = 0
                        if integral_value_prev_2 != 0:
                            relative_error_2 = np.abs(
                                (integral_value_2 - integral_value_prev_2) / integral_value_prev_2)
                        else:
                            relative_error_2 = 0

                        # Check for convergence
                        if relative_error_1 <= solver_info.tolerance_adj and \
                                relative_error_2 <= solver_info.tolerance_adj:
                            break
                    # endregion

                    # region Check if maximum number of iterations is exceeded.
                    if iter_no == solver_info.max_iter_adj:
                        logger.info('Maximum number of iterations %d exceeded. Relative error: %f',
                                    iter_no, max(relative_error_1, relative_error_2))
                        break
                    # endregion
                # endregion

                # region Define final conditions for next interval
                final_value_1[qoi.name] = adj_interval_1.potential(time=time_steps_interval_1[-1])
                final_value_2[qoi.name] = adj_interval_2.potential(time=time_steps_interval_2[-1])
                # endregion

                # region Compute sensitivities
                for param in qoi.get_parameter_names():
                    # region Compute contribution attributed to w1
                    for k, time in enumerate(time_steps_interval_1):
                        time = time_steps_interval_1[k]

                        # Omit first value of each interval to avoid including it twice.
                        if k == 0 and time != time_steps_adj_1[0]:
                            continue

                        # region Update static helper solutions to desired time step
                        static_solution_helper_el.time = time
                        static_solution_helper_el.potential = solution_el.potential(time=time)
                        static_solution_helper_el.temperature_coupling = solution_th.temperature(time=time)
                        static_solution_helper_th.time = time
                        static_solution_helper_th.temperature = solution_th.temperature(time=time)
                        # endregion

                        # region Select correct parameter
                        for mat in static_solution_helper_el.materials:
                            prop: DiffConductivityParameter = mat.get_property(DiffConductivityParameter)
                            prop.parameter_key = param
                            prop: DiffPermittivityParameter = mat.get_property(DiffPermittivityParameter)
                            prop.parameter_key = param
                        for mat in static_solution_helper_th.materials:
                            prop: DiffThermalConductivityParameter = mat.get_property(DiffThermalConductivityParameter)
                            prop.parameter_key = param
                            prop: DiffVolumetricHeatCapacityParameter = mat.get_property(
                                DiffVolumetricHeatCapacityParameter)
                            prop.parameter_key = param
                        # endregion

                        # region Compute diff_qoi_param
                        dqoidparam = qoi.evaluate_diff_qoi_param(
                            param, [static_solution_helper_el, static_solution_helper_th, time])
                        # endregion

                        # region Compute dw1/dt
                        if k == 0:
                            dt_adjoint = np.zeros((num_node,))
                        elif time == time_steps_adj_1[0]:
                            dt_adjoint = (adj_interval_1.potential(time=time_steps_interval_1[k + 1])
                                          - adj_interval_1.potential(time=time)) \
                                / (time_steps_interval_1[k + 1] - time)
                        else:
                            dt_adjoint = (adj_interval_1.potential(time=time)
                                          - adj_interval_1.potential(time=time_steps_interval_1[k - 1])) \
                                / (time - time_steps_interval_1[k - 1])
                        # endregion

                        # region Compute contribution to sensitivities
                        sensitivities_1[(qoi.name, param)].append(
                            dqoidparam
                            - static_solution_helper_el.potential
                            @ static_solution_helper_el.compute_Ksigmap()
                            @ adj_interval_1.potential(time=time)
                            + static_solution_helper_el.potential
                            @ static_solution_helper_el.compute_Kepsp()
                            @ dt_adjoint)
                        # endregion

                        # region Compute boundary integrals at t=0
                        if time == time_steps_adj_1[0]:
                            sensitivities_boundary_terms_1[(qoi.name, param)] = \
                                static_solution_helper_el.potential @ static_solution_helper_el.compute_Kepsp() \
                                @ adj_interval_1.potential(time=time) + \
                                sensitivity_potential_initial_value[param] \
                                @ static_solution_helper_el.divgrad_matrix_epsd @ adj_interval_1.potential(time=time)
                        # endregion

                    sensitivities_1[(qoi.name, param)].reverse()

                    # endregion

                    # region Compute contribution attributed to w2
                    for k, time in enumerate(time_steps_interval_2):
                        time = time_steps_interval_2[k]

                        # Omit first value of each interval to avoid including it twice.
                        if k == 0 and time != time_steps_adj_2[0]:
                            continue

                        # region Update static helper solutions to desired time step
                        static_solution_helper_el.time = time
                        static_solution_helper_el.potential = solution_el.potential(time=time)
                        static_solution_helper_el.temperature_coupling = solution_th.temperature(time=time)
                        static_solution_helper_th.time = time
                        static_solution_helper_th.temperature = solution_th.temperature(time=time)
                        # endregion

                        # region Select correct parameter
                        for mat in static_solution_helper_el.materials:
                            prop: DiffConductivityParameter = mat.get_property(DiffConductivityParameter)
                            prop.parameter_key = param
                            prop: DiffPermittivityParameter = mat.get_property(DiffPermittivityParameter)
                            prop.parameter_key = param
                        for mat in static_solution_helper_th.materials:
                            prop: DiffThermalConductivityParameter = mat.get_property(DiffThermalConductivityParameter)
                            prop.parameter_key = param
                            prop: DiffVolumetricHeatCapacityParameter = mat.get_property(
                                DiffVolumetricHeatCapacityParameter)
                            prop.parameter_key = param
                        # endregion

                        # region Compute dw2/dt
                        if k == 0:
                            dt_adjoint = np.zeros((num_node,))
                        elif time == time_steps_adj_1[0]:
                            dt_adjoint = (adj_interval_2.potential(time=time_steps_interval_2[k + 1])
                                          - adj_interval_2.potential(time=time)) \
                                / (time_steps_interval_2[k + 1] - time)
                        else:
                            dt_adjoint = (adj_interval_2.potential(time=time)
                                          - adj_interval_2.potential(time=time_steps_interval_2[k - 1])) \
                                / (time - time_steps_interval_2[k - 1])
                        # endregion

                        # region Compute contribution to sensitivities
                        sensitivities_2[(qoi.name, param)].append(
                            static_solution_helper_th.temperature
                            @ static_solution_helper_th.shape_function.mass_matrix(
                                static_solution_helper_th.diff_volumetric_heat_capacity_temperature_per_element)
                            @ dt_adjoint
                            - static_solution_helper_th.temperature
                            @ static_solution_helper_th.compute_Klambdap()
                            @ adj_interval_2.potential(time=time)
                            + (adj_interval_2.potential(time=time)
                               @ static_solution_helper_th.shape_function.load_vector(
                               static_solution_helper_el.diff_conductivity_temperature_per_element
                               * static_solution_helper_el.e_field_abs ** 2))[0])
                        # endregion

                        # region Compute boundary integrals at t=0
                        if time == time_steps_adj_2[0]:
                            sensitivities_boundary_terms_2[(qoi.name, param)] = \
                                - static_solution_helper_th.temperature @ static_solution_helper_th.compute_Msp() \
                                @ adj_interval_2.potential(time=time) + \
                                sensitivity_temperature_initial_value[param] \
                                @ static_solution_helper_th.mass_matrix_s @ adj_interval_2.potential(time=time)
                        # endregion

                    sensitivities_2[(qoi.name, param)].reverse()
                    # endregion
                # endregion

        # Integrate sensitivities
        for key in sensitivities_1.keys():
            sensitivities[key] = np.trapz(sensitivities_1[key], time_steps_adj_1) + \
                np.trapz(sensitivities_2[key], time_steps_adj_2) + \
                sensitivities_boundary_terms_1[key] \
                + sensitivities_boundary_terms_2[key]

        return sensitivities
