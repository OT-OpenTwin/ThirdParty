# coding=utf-8
"""Current flow problem in two-dimensional Cartesian coordinates

.. sectionauthor:: Bergfried, Bundschuh
"""
# pylint: disable=arguments-differ
from dataclasses import dataclass
from typing import Dict, Union, Tuple, Callable, NoReturn, Any, Iterable, List

from scipy import sparse
from scipy.sparse import coo_matrix
import numpy as np

from pyrit import get_logger
from pyrit import mesh, region, material, bdrycond, excitation
from pyrit.problem.Problem import StaticProblem, HarmonicProblem, TransientProblem
from pyrit.solution.CurrentFlowSolutionCart import CurrentFlowSolutionCartStatic, CurrentFlowSolutionCartHarmonic, \
    CurrentFlowSolutionCartTransient
from pyrit.solution.CurrentFlowSolutionCart import CurrentFlowSolutionCartIntermediate
from pyrit.shapefunction import TriCartesianNodalShapeFunction

logger = get_logger(__name__)

__all__ = ['CurrentFlowProblemCartStatic', 'CurrentFlowProblemCartHarmonic', 'CurrentFlowProblemCartTransient',
           'CurrentFlowSolverInfoCartStatic', 'CurrentFlowSolverInfoCartTransient']


@dataclass()
class CurrentFlowSolverInfoCartStatic:
    """Class for passing options to the solve-method of CurrentFlowProblemCartStatic"""

    tolerance_newton: float = 1e-8  # tolerance for the newton algorithm
    max_iter_newton: int = 100  # maximum number of newton iterations
    relaxation_newton: float = 1  # relaxation for newton algorithm


@dataclass()
class CurrentFlowSolverInfoCartTransient:
    """Class for passing options to the solve-method of CurrentFlowProblemCartTransient"""

    tolerance_newton: float = 1e-8  # tolerance for the newton algorithm
    max_iter_newton: int = 100  # maximum number of newton iterations
    relaxation_newton: float = 1  # relaxation for newton algorithm


class CurrentFlowProblemCartStatic(StaticProblem):
    r"""A two-dimensional stationary current problem in Cartesian coordinates:

    The stationary current problem models resistive effects. The corresponding differential equation reads

    .. math::
        -\mathrm{div}(\sigma \, \mathrm{grad} (\phi)) = 0,

    where :math:`\sigma` is the electric conductivity (see :py:class:`Conductivity`) and :math:`\phi` denotes the \
    electric scalar potential. A possible application is, for example, the steady state simulation of a HVDC cable \
    joint.
    """

    problem_identifier: str = 'Static, current flow problem in two-dimensional Cartesian coordinates'
    associated_solution_class = CurrentFlowSolutionCartStatic

    def __init__(self, description: str, tri_mesh: mesh.TriMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond,
                 excitations: excitation.Excitations,
                 length: float = 1):
        """Constructor

        Parameters
        ----------
        description : str
            A description of the problem
        tri_mesh : TriMesh
            A mesh object. See :py:class:`pyrit.mesh.TriMesh`
        regions : Regions
            A regions object. See :py:mod:`pyrit.regions`
        materials : Materials
            A materials object. See :py:mod:`pyrit.materials`
        boundary_conditions : BdryCond
            A boundary conditions object representing the boundary conditions for the stationary current problem.
            See :py:mod:`pyrit.bdrycond`
        excitations : Excitations
            An excitations object. See :py:mod:`pyrit.excitation`
        """
        # Setup Model
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations)
        self.length = length
        # So the type is known by the IDE
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianNodalShapeFunction = TriCartesianNodalShapeFunction(tri_mesh, length)

        # Determine if problem is temperature-dependent (needed for coupled problems)
        self._is_temperature_dependent: bool = None

        self.consistency_check()

    @property
    def is_linear(self):
        """Checks if the problem is linear."""
        return self.materials.is_linear(prop_class=material.Conductivity) and \
               self.excitations.is_linear and self.boundary_conditions.is_linear

    @property
    def is_temperature_dependent(self):
        """Checks if the problem is temperature dependent."""
        if self._is_temperature_dependent is None:
            self._is_temperature_dependent = False
            for mat in self.materials:
                if 'temperature' in mat.get_property(material.Conductivity).keyword_args:
                    self._is_temperature_dependent = True
            for exci in self.excitations:
                if 'temperature' in exci.keyword_args:
                    self._is_temperature_dependent = True
            for bc in self.boundary_conditions:
                if 'temperature' in bc.keyword_args:
                    self._is_temperature_dependent = True
        return self._is_temperature_dependent

    def get_system(self, **kwargs) -> Tuple[sparse.spmatrix, sparse.spmatrix]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> CurrentFlowSolutionCartStatic:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> CurrentFlowSolutionCartStatic:
        raise NotImplementedError

    def create_solution(self, solution: np.ndarray, description: str = None, **kwargs) -> CurrentFlowSolutionCartStatic:
        raise NotImplementedError

    def _solve_system(self, matrix, rhs, **kwargs) -> np.ndarray:
        # Help routine that shrinks, solves and inflates the system "matrix * x = rhs", returns the solution x.
        matrix_shrink, rhs_shrink, _, _, support_data = self.shape_function.shrink(matrix, coo_matrix(rhs), self)
        # pylint: disable=no-member
        potential_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(),
                                                             **kwargs)

        return self.shape_function.inflate(potential_shrink, self, support_data)

    def solve(self, u0: Union[np.ndarray, CurrentFlowSolutionCartStatic] = None,
              solver_info: CurrentFlowSolverInfoCartStatic = None,
              **kwargs) -> CurrentFlowSolutionCartStatic:  # pylint: disable=arguments-differ
        """Solve the Problem using the Newton method.

        Parameters
        ----------
        u0: np.ndarray
            [V] Start guess for Newton iteration. If None is given, an all-zero vector is used.
        solver_info: CurrentFlowSolverInfoCartStatic
            Options for the Newton algorithm
        kwargs :
            Are all passed to the function :py:func:`solve_linear_system`.

        Returns
        -------
        solution : CurrentFlowSolutionCartStatic
            The solution object
        """
        # region Linear Probelm
        if self.is_linear:  # linear problem
            static_solution = CurrentFlowSolutionCartStatic.solution_from_problem(self.description,
                                                                                  self, np.zeros((self.mesh.num_node,)))
            static_solution.potential = self._solve_system(static_solution.divgrad_matrix_sigma,
                                                           static_solution.load_vector_electric, **kwargs)
            return static_solution
        # endregion

        # region Nonlinear Problem --> Newton algorithm
        # region Initializations
        iter_no = 0
        if solver_info is None:
            solver_info = CurrentFlowSolverInfoCartStatic()

        # Set initial guess for solution
        if u0 is None:
            # Initialize materials with zero solution and solve boundary value problem for this material
            # working point
            static_solution = CurrentFlowSolutionCartStatic.solution_from_problem(self.description,
                                                                                  self, np.zeros((self.mesh.num_node,)))
            self.boundary_conditions.update('solution', static_solution)
            static_solution.potential = self._solve_system(static_solution.divgrad_matrix_sigma,
                                                           static_solution.load_vector_electric, **kwargs)
        elif isinstance(u0, CurrentFlowSolutionCartStatic):
            static_solution = u0
        else:
            static_solution = CurrentFlowSolutionCartStatic.solution_from_problem(self.description, self, u0)
        self.boundary_conditions.update('solution', static_solution)
        # endregion

        # region Newton algorithm
        while True:
            iter_no += 1
            loss_power_prev = static_solution.joule_loss_power

            # region Build and solve system
            # ToDo: Split sigmad in sigma and 2 dsigma/dE^2 --> avoid loop over elements with linear materials
            rhs = coo_matrix(static_solution.load_vector_electric
                             - static_solution.divgrad_matrix_sigma @ static_solution.potential[:, None]
                             + static_solution.divgrad_matrix_sigmad @ static_solution.potential[:, None])
            lhs = static_solution.divgrad_matrix_sigmad
            potential_new = self._solve_system(lhs, rhs, **kwargs)
            # endregion

            # region Insert relaxation and write new potential vector to solution
            if solver_info.relaxation_newton != 1:
                potential_new = solver_info.relaxation_newton * potential_new + \
                    (1 - solver_info.relaxation_newton) * static_solution.potential

            # Update solution and nonlinear quantities
            static_solution.potential = potential_new
            self.boundary_conditions.update('solution', static_solution)
            # endregion

            # region Terminate algorithm
            # Compute relative error
            relative_error = (abs((loss_power_prev - static_solution.joule_loss_power) /
                                  static_solution.joule_loss_power))

            logger.info('Iteration: %d, rel. error: %e, power loss: %f', iter_no, relative_error,
                        static_solution.joule_loss_power)

            # Check for convergence
            if relative_error <= solver_info.tolerance_newton:
                logger.info('Convergence after %d iterations. Relative error: %e', iter_no, relative_error)
                return static_solution

            # Check if maximum number of iterations is exceeded.
            if iter_no == solver_info.max_iter_newton:
                logger.critical('Maximum number of iterations %d exceeded. Relative error: %f', iter_no, relative_error)
                return static_solution
            # endregion
        # endregion
        # endregion


class CurrentFlowProblemCartHarmonic(HarmonicProblem):
    r"""A two-dimensional harmonic electroquasistatic problem in Cartesian coordinates:

    The harmonic electroquasistatic problem models capacitive-resistive effects. The corresponding
    differential \
    equation reads

    .. math::
        -\mathrm{div}(j 2\pi f\varepsilon\, \mathrm{grad} (\phi)) -\mathrm{div}(\sigma\,\mathrm{grad}
         (\phi)) = 0,

    where :math:`\sigma` is the electric conductivity (see :py:class:`~pyrit.material.Conductivity`),
    :math:`\varepsilon` is the electric permittivity (see :py:class:`~pyrit.material.Permittivity`), :math:`\phi`
    denotes the electric scalar potential, and :math:`f` is the frequency. The problem can, by definition,
    only handle linear materials.
    A possible application is, e.g. the steady state simulation of the insulation system in an electrical machine.
    """

    problem_identifier = 'Harmonic, electroquasistatic problem in 2D Cartesian coordinates'

    associated_solution_class = CurrentFlowSolutionCartHarmonic

    def __init__(self, description: str, tri_mesh: mesh.TriMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond,
                 excitations: excitation.Excitations,
                 frequency: float,
                 length: float = 1):
        """Constructor

        Parameters
        ----------
        description : str
            A description of the problem
        tri_mesh : TriMesh
            A mesh object. See :py:class:`pyrit.mesh.TriMesh`
        regions : Regions
            A regions object. See :py:mod:`pyrit.regions`
        materials : Materials
            A materials object. See :py:mod:`pyrit.materials`
        boundary_conditions : BdryCond
            A boundary conditions object representing the boundary conditions for the stationary current problem.
            See :py:mod:`pyrit.bdrycond`
        excitations : Excitations
            An excitations object. See :py:mod:`pyrit.excitation`
        frequency : float
            The frequency of the problem
        length : float, optional
            The length of the problem. Default is 1
        """
        # Setup Model
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations, frequency)
        self.length = length
        # So the type is known by the IDE
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianNodalShapeFunction = TriCartesianNodalShapeFunction(tri_mesh, length)

        # Determine if problem is temperature-dependent (needed for coupled problems)
        self._is_temperature_dependent: bool = None

        self.consistency_check()

    def get_system(self, **kwargs) -> Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> CurrentFlowSolutionCartHarmonic:
        raise NotImplementedError

    def create_solution(self, solution: np.ndarray, description: str = None,
                        **kwargs) -> CurrentFlowSolutionCartHarmonic:
        raise NotImplementedError

    def solve(self, *args, **kwargs) -> CurrentFlowSolutionCartHarmonic:
        raise NotImplementedError()


class CurrentFlowProblemCartTransient(TransientProblem):
    r"""A two-dimensional transient electroquasistatic problem in Cartesian coordinates:

    The transient electroquasistatic problem models capacitive-resistive effects. The corresponding differential \
    equation reads

    .. math::
        -\mathrm{div}(\partial_t(\varepsilon\, \mathrm{grad} (\phi))) -\mathrm{div}(\sigma\,\mathrm{grad}
         (\phi)) = 0,

    where :math:`\sigma` is the electric conductivity (see :py:class:`Conductivity`), :math:`\varepsilon` is the \
    electric permittivity (see :py:class:`Permittivity`) and :math:`\phi` denotes the electric scalar potential. \
    A possible application is, for example, the simulation of transient effects in HVDC cable joints or AC surge \
    arresters.
    """

    problem_identifier = 'Transient, electroquasistatic problem in 2D Cartesian coordinates'

    available_monitors: dict = {'joule_loss_power': '_joule_loss_power'}

    def __init__(self, description: str, tri_mesh: mesh.TriMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations, time_steps: np.ndarray,
                 length: float = 1):
        """Transient EQS problem, cartesian.

        Parameters
        ----------
        description : str
            A description of the problem.
        tri_mesh : TriMesh
            A mesh object. See :py:class:`pyrit.mesh.TriMesh`.
        regions : Regions
            A regions object. See :py:mod:`pyrit.regions`.
        materials : Materials
            A materials object. See :py:mod:`pyrit.materials`.
        boundary_conditions : BdryCond
            A boundary conditions object. See :py:mod:`pyrit.bdrycond`.
        excitations : Excitations
            An excitations object. See :py:mod:`pyrit.excitation`.
        time_steps : np.ndarray
            An array with the time steps for the problem.
        """
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations, time_steps)

        self.length = length
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianNodalShapeFunction = TriCartesianNodalShapeFunction(tri_mesh, length)

        self.divgrad_eps_linear = self.materials.is_linear(material.Permittivity)
        self.divgrad_sigma_linear = self.materials.is_linear(material.Conductivity)
        self.divgrad_epsd_linear = self.materials.is_linear(material.DifferentialPermittivity)
        self.divgrad_sigmad_linear = self.materials.is_linear(material.DifferentialConductivity)
        self.load_linear = self.excitations.is_linear
        self.boundary_condition_linear = self.boundary_conditions.is_linear
        self.all_linear = all([self.divgrad_eps_linear, self.divgrad_epsd_linear, self.divgrad_sigma_linear,
                               self.divgrad_sigmad_linear, self.load_linear, self.boundary_condition_linear])
        self._is_temperature_dependent: bool = None

        self.consistency_check()

    @property
    def is_temperature_dependent(self):
        """True if one of the materials has a conductivity with the key word argument temperature."""
        if self._is_temperature_dependent is None:
            self._is_temperature_dependent = False
            for mat in self.materials:
                if 'temperature' in mat.get_property(material.Conductivity).keyword_args:
                    self._is_temperature_dependent = True
            for exci in self.excitations:
                if 'temperature' in exci.keyword_args:
                    self._is_temperature_dependent = True
            for bc in self.boundary_conditions:
                if 'temperature' in bc.keyword_args:
                    self._is_temperature_dependent = True
        return self._is_temperature_dependent

    @staticmethod
    def _joule_loss_power(solution: 'CurrentFlowSolutionCartStatic'):
        return solution.joule_loss_power

    Monitor = Union[str, Callable[['CurrentFlowSolutionCartStatic'], Any]]

    Solution_Monitor = Union[int, Iterable[int]]

    def _solve_system(self, matrix, rhs, **kwargs) -> np.ndarray:
        matrix_shrink, rhs_shrink, _, _, support_data = self.shape_function.shrink(matrix, rhs, self)
        # pylint: disable=no-member
        potential_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(),
                                                             **kwargs)

        prev_sol = self.shape_function.inflate(potential_shrink, self, support_data)
        return prev_sol

    def get_system(self, time: float, **kwargs) -> Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> CurrentFlowSolutionCartTransient:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> CurrentFlowSolutionCartTransient:
        raise NotImplementedError

    def create_solution(self, solutions, time_steps, description: str = None,
                        **kwargs) -> CurrentFlowSolutionCartTransient:
        raise NotImplementedError

    def solve(self, start_value: np.ndarray, solution_monitor: Union[int, Iterable[int]] = 1,
              monitors: Dict['str', Union[Monitor, Tuple[Solution_Monitor, Monitor]]] = None,
              callback: Callable[['CurrentFlowSolutionCartStatic'], NoReturn] = None,
              solver_info: CurrentFlowSolverInfoCartTransient = None, **kwargs) -> \
            CurrentFlowSolutionCartTransient:

        # region Initialization and Preprocessing
        if not self.all_linear:
            if solver_info is None:
                solver_info = CurrentFlowSolverInfoCartTransient()

        if not isinstance(start_value, np.ndarray):
            raise ValueError(f"The argument start_value is not of the right type. "
                             f"It is '{type(start_value)}' but should be a ndarray")

        if isinstance(solution_monitor, int):
            solution_monitor = np.arange(start=0, stop=len(self.time_steps), step=solution_monitor)
            if solution_monitor[-1] != len(self.time_steps) - 1:
                solution_monitor = np.concatenate([solution_monitor, np.array([len(self.time_steps) - 1])])

        time_steps = self.time_steps[solution_monitor]
        delta_ts = np.diff(self.time_steps)

        solution_monitor = set(solution_monitor)

        # Preprocess the monitors so that they have a fixed form
        monitors = self._monitors_preprocessing(monitors)
        monitors_results = {k: [self.time_steps[v[0]], []] for k, v in monitors.items()}

        # Add the start value to the solutions
        if 0 in solution_monitor:
            solutions = [start_value, ]
        else:
            solutions = []

        has_callback = callback is not None
        # endregion

        # Loop over all time steps
        for k in range(1, len(self.time_steps)):
            logger.info('starting with time step %d', k)
            delta_t = delta_ts[k - 1]

            # region Initialize static solution
            if k == 1:
                if isinstance(start_value, CurrentFlowSolutionCartIntermediate):
                    static_solution = start_value
                elif isinstance(start_value, CurrentFlowSolutionCartStatic):
                    static_solution = CurrentFlowSolutionCartIntermediate.extend_solution(start_value)
                else:
                    static_solution = CurrentFlowSolutionCartIntermediate(f'temporary static solution generated by '
                                                                          f'solve in ElectroquasistaticProblemCart '
                                                                          f'at time step {k}',
                                                                          start_value, self.mesh, self.shape_function,
                                                                          self.regions,
                                                                          self.materials, self.excitations)
                static_solution.time = self.time_steps[k - 1]
                self.boundary_conditions.update('solution', static_solution)
            # endregion

            # Compute part of the rhs that depends only on the previous time step
            rhs_helper = 1 / delta_t * static_solution.divgrad_matrix_eps @ static_solution.potential[:, None]

            # Update materials and matrices to current time step
            static_solution.time = self.time_steps[k]
            self.boundary_conditions.update('time', self.time_steps[k])

            # Save monitor results of first time step
            if k == 1:
                for key, monitor in monitors.items():
                    if k in monitor[0]:
                        monitors_results[key][1].append(monitor[1](static_solution))

            if self.all_linear:
                # region Solve system in case of a linear problem
                # Finish building rhs and system matrix
                rhs = rhs_helper + static_solution.load_vector_electric
                matrix = 1 / delta_t * static_solution.divgrad_matrix_eps + static_solution.divgrad_matrix_sigma
                # Solve system
                static_solution.potential = self._solve_system(matrix, coo_matrix(rhs), **kwargs)
                # endregion

            else:
                # region Perform Newton algorithm in case of a nonlinear problem
                iter_no = 0
                while True:
                    # Update iteration variables
                    iter_no += 1
                    loss_power_prev = static_solution.joule_loss_power
                    # region Build and solve system
                    # ToDo: Split differential permittivity/ conductivity into two different matrices
                    #  (sigma + tensor term) --> loop over fewer elements for Ksigmad
                    rhs = rhs_helper + \
                          static_solution.load_vector_electric - \
                          static_solution.divgrad_matrix_sigma @ static_solution.potential[:, None] + \
                          static_solution.divgrad_matrix_sigmad @ static_solution.potential[:, None] - \
                          1 / delta_t * static_solution.divgrad_matrix_eps @ static_solution.potential[:, None] + \
                          1 / delta_t * static_solution.divgrad_matrix_epsd @ static_solution.potential[:, None]
                    matrix = static_solution.divgrad_matrix_sigmad + 1 / delta_t * static_solution.divgrad_matrix_epsd
                    potential_new = self._solve_system(matrix, coo_matrix(rhs), **kwargs)
                    # endregion

                    # region Insert relaxation and write new potential vector to solution
                    if solver_info.relaxation_newton != 1:
                        potential_new = solver_info.relaxation_newton * potential_new + \
                            (1 - solver_info.relaxation_newton) * static_solution.potential

                    static_solution.potential = potential_new
                    self.boundary_conditions.update('solution', static_solution)
                    # endregion

                    # region Terminate Newton algorithm
                    relative_error = (abs((loss_power_prev - static_solution.joule_loss_power) /
                                          static_solution.joule_loss_power))

                    # Report progress
                    # logger.info('Newton iteration: %d, rel. error: %e, loss power: %f', iter_no,
                    #            relative_error, static_solution.loss_power)

                    # Check for convergence
                    if relative_error <= solver_info.tolerance_newton:
                        logger.info('Convergence after %d Newton iterations. Relative error: %f',
                                    iter_no, relative_error)
                        break

                    # Check if maximum number of iterations is exceeded.
                    if iter_no == solver_info.max_iter_newton:
                        logger.critical('Maximum number of iterations %d exceeded. Relative error: %f', iter_no,
                                        relative_error)
                        break
                    # endregion

                # endregion

            # region Post-process results of current time step
            if has_callback:
                callback(static_solution)

            for key, monitor in monitors.items():
                if k in monitor[0]:
                    monitors_results[key][1].append(monitor[1](static_solution))

            if k in solution_monitor:
                solutions.append(static_solution.potential)
            # endregion

        # region Write output
        solutions = np.stack(solutions)

        for key, monitor in monitors_results.items():
            monitors_results[key][1] = np.stack(monitors_results[key][1])
        # endregion
        return CurrentFlowSolutionCartTransient(f'solution of {self.description}', solutions, self.mesh,
                                                self.shape_function, self.regions, self.materials,
                                                self.excitations,
                                                time_steps, monitors_results)
