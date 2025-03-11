# coding=utf-8
"""Thermal problems in two-dimensional Cartesian coordinates

.. sectionauthor:: Ruppert, Bergfried
"""
# pylint: disable=arguments-differ
from typing import TYPE_CHECKING, Dict, Union, Tuple, Callable, NoReturn, Any, Iterable, List
from dataclasses import dataclass

from scipy import sparse
from scipy.sparse import coo_matrix
import numpy as np

from pyrit import get_logger
from pyrit import mesh, region, material, bdrycond, excitation
from pyrit.shapefunction import TriCartesianNodalShapeFunction
from pyrit.problem.Problem import StaticProblem, HarmonicProblem, TransientProblem  # , Solution_Monitor, Monitor

from pyrit.solution import ThermalSolutionCartStatic, ThermalSolutionCartHarmonic, ThermalSolutionCartTransient, \
    TransientSolution
from pyrit.solution import CurrentFlowSolutionCartStatic, CurrentFlowSolutionCartTransient
from pyrit.solution.ThermalSolutionCart import ThermalSolutionCartIntermediate

if TYPE_CHECKING:
    from pyrit.mesh import TriMesh


logger = get_logger(__name__)

__all__ = ['ThermalProblemCartStatic', 'ThermalProblemCartHarmonic', 'ThermalProblemCartTransient',
           'ThermalSolverInfoCartStatic', 'ThermalSolverInfoCartTransient']


@dataclass()
class ThermalSolverInfoCartStatic:
    """Class for passing options to the solve-method of ThermalProblemCartStatic"""

    tolerance_successive_substitution: float = 1e-8  # tolerance for the successive_substitution algorithm
    max_iter_successive_substitution: int = 200  # maximum number of successive_substitution iterations
    relaxation_successive_substitution: float = 0.3  # relaxation for successive_substitution algorithm


@dataclass()
class ThermalSolverInfoCartTransient:
    """Class for passing options to the solve-method of ThermalProblemCartTransient"""

    tolerance_successive_substitution: float = 1e-8  # tolerance for the successive_substitution algorithm
    max_iter_successive_substitution: int = 200  # maximum number of successive_substitution iterations
    relaxation_successive_substitution: float = 0.3  # relaxation for successive_substitution algorithm


class ThermalProblemCartStatic(StaticProblem):
    r"""A two-dimensional stationary heat conduction problem in Cartesian coordinates:

    The stationary heat conduction problem models the steady-state temperature distribution of a body with \
    constant external heat sources. The corresponding differential equation reads

    .. math::
        -\mathrm{div}(\lambda \, \mathrm{grad} (T)) = \dot q,

    where :math:`\lambda` is the thermal conductivity (see :py:class:`ThermalConductivity`), \
    :math:`\dot q` is the heat flux density and :math:`T` denotes the temperature.
    """

    problem_identifier: str = 'Stationary heat conduction problem in two-dimensional Cartesian coordinates'
    associated_solution_class = ThermalSolutionCartStatic

    def __init__(self, description: str, tri_mesh: mesh.TriMesh,
                 regions: region.Regions,
                 materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond,
                 excitations: excitation.Excitations,
                 length: float = 1,
                 electromagnetic_heat_source: CurrentFlowSolutionCartStatic = None):
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
        length : float, optional
            The length of the problem. Default is 1
        electromagnetic_heat_source: CurrentFlowSolutionCartStatic
            A current flow solution, whose joule loss density is added as a heat source to the rhs
        """
        # Setup Model
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations)

        self.length = length
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianNodalShapeFunction = TriCartesianNodalShapeFunction(tri_mesh, length)

        self.electromagnetic_heat_source = electromagnetic_heat_source

        self.consistency_check()

    @property
    def is_linear(self):
        """Checks if the problem is linear."""
        return self.materials.is_linear(prop_class=material.ThermalConductivity) and \
            self.excitations.is_linear and self.boundary_conditions.is_linear

    def _solve_system(self, matrix, rhs, **kwargs) -> np.ndarray:
        # Help routine that shrinks, solves and inflates the system matrix * x = rhs, returns the solution x.
        matrix_shrink, rhs_shrink, _, _, support_data = self.shape_function.shrink(matrix, coo_matrix(rhs), self)
        # pylint: disable=no-member
        temperature_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(),
                                                               **kwargs)

        return self.shape_function.inflate(temperature_shrink, self, support_data)

    def solve(self, temp0: Union[np.ndarray, ThermalSolutionCartStatic] = None,
              solver_info: ThermalSolverInfoCartStatic = None,
              **kwargs) -> ThermalSolutionCartStatic:
        """Solve the Problem using the successive substitution method.

        Parameters
        ----------
        temp0: np.ndarray
            [V] Start guess for Newton iteration.
        solver_info: ThermalSolverInfoCartStatic
            Options for the successive substitution algorithm
        kwargs :
            Are all passed to the function :py:func:`solve_linear_system`.

        Returns
        -------
        solution : ThermalSolutionCartStatic
            The solution object
        """
        # region Compute load vector belonging to the electromagnetic heat source
        if self.electromagnetic_heat_source is None:
            load_vector_coupling = coo_matrix((self.mesh.num_node, 1))
        else:
            load_vector_coupling = self.shape_function.load_vector(
                self.electromagnetic_heat_source.joule_loss_power_density)
        # endregion

        # region Linear problem
        if self.is_linear:
            static_solution = ThermalSolutionCartStatic.solution_from_problem(self.description,
                                                                              self,
                                                                              np.zeros((self.mesh.num_node,)))
            static_solution.temperature = self._solve_system(static_solution.divgrad_matrix_lambda,
                                                             static_solution.load_vector_thermal + load_vector_coupling,
                                                             **kwargs)
            return static_solution
        # endregion

        # region Perform successive substitution algorithm in case of nonlinear problem
        # region Initialization
        iter_no = 0
        if solver_info is None:
            solver_info = ThermalSolverInfoCartStatic()
        if temp0 is None:
            # Initialize materials with constant 293.15K solution and solve boundary value problem for this material
            # working point
            static_solution = ThermalSolutionCartStatic.solution_from_problem(self.description,
                                                                              self,
                                                                              np.ones((self.mesh.num_node,))
                                                                              * 293.15)
            self.boundary_conditions.update('solution', static_solution)
            # Set the solution of the BVP at this material working point as initial condition
            static_solution.temperature = self._solve_system(static_solution.divgrad_matrix_lambda,
                                                             static_solution.load_vector_thermal + load_vector_coupling,
                                                             **kwargs)
        elif isinstance(temp0, ThermalSolutionCartStatic):
            static_solution = temp0
        else:
            static_solution = ThermalSolutionCartStatic.solution_from_problem(self.description, self, temp0)

        self.boundary_conditions.update('solution', static_solution)
        # endregion

        while True:
            iter_no += 1
            loss_power_prev = static_solution.thermal_loss_power

            # region Build and solve system
            temperature_new = self._solve_system(static_solution.divgrad_matrix_lambda,
                                                 static_solution.load_vector_thermal + load_vector_coupling, **kwargs)
            # endregion
            # region Insert relaxation and write new temperature to solution
            if solver_info.relaxation_successive_substitution != 1:
                temperature_new = solver_info.relaxation_successive_substitution * temperature_new + \
                    (1 - solver_info.relaxation_successive_substitution) * static_solution.temperature

            static_solution.temperature = temperature_new
            self.boundary_conditions.update('solution', static_solution)
            # endregion
            # region Terminate successive substitution algorithm
            # Compute relative error
            relative_error = abs(
                (loss_power_prev - static_solution.thermal_loss_power) / static_solution.thermal_loss_power)

            logger.info('Iteration: %d, rel. error: %e, loss power: %f', iter_no, relative_error,
                        static_solution.thermal_loss_power)

            # Check for convergence
            if relative_error <= solver_info.tolerance_successive_substitution:
                logger.info('Convergence after %d iterations. Relative error: %f', iter_no, relative_error)
                return static_solution

            # Check if maximum number of iterations is exceeded.
            if iter_no == solver_info.max_iter_successive_substitution:
                logger.info('Maximum number of iterations %d exceeded. Relative error: %f', iter_no, relative_error)
                return static_solution
            # endregion
        # endregion

    def get_system(self, **kwargs) -> Tuple[sparse.spmatrix, sparse.spmatrix]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> ThermalSolutionCartStatic:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> ThermalSolutionCartStatic:
        raise NotImplementedError

    def create_solution(self, solution: np.ndarray, description: str = None, **kwargs) -> ThermalSolutionCartStatic:
        raise NotImplementedError


class ThermalProblemCartHarmonic(HarmonicProblem):
    r"""A two-dimensional harmonic heat conduction problem in Cartesian coordinates:

    The harmonic heat conduction problem models the steady-state temperature distribution of a body with \
    harmonic external heat sources. The corresponding differential equation reads

        .. math::
            j \omega s T -\mathrm{div}(\lambda\,\mathrm{grad}(T)) = \dot q,

    where :math:`\lambda` is the thermal conductivity (see :py:class:`ThermalConductivity`), \
    :math:`s` is the volumetric heat capacity (see :py:class:`VolumetricHeatCapacity`), \
    :math:`\dot q` is the heat flux density and :math:`T` denotes the temperature.
    """

    problem_identifier: str = 'Harmonic heat conduction problem in two-dimensional Cartesian coordinates'
    associated_solution_class = ThermalSolutionCartHarmonic

    def __init__(self, description: str, tri_mesh: mesh.TriMesh,
                 regions: region.Regions,
                 materials: material.Materials,
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
            The frequency of the problem.
        length : float, optional
            The length of the problem. Default is 1
        """
        # Setup Model
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations, frequency)

        self.length = length
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianNodalShapeFunction = TriCartesianNodalShapeFunction(tri_mesh, length)

        self.consistency_check()

    def get_system(self, **kwargs) -> Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]:
        raise NotImplementedError()

    def _solve_linear(self, **kwargs) -> ThermalSolutionCartHarmonic:
        raise NotImplementedError()

    def create_solution(self, solution: np.ndarray, description: str = None, **kwargs) -> ThermalSolutionCartHarmonic:
        raise NotImplementedError()


class ThermalProblemCartTransient(TransientProblem):
    r"""A two-dimensional transient heat conduction problem in Cartesian coordinates:

    This problem models the transient conductive heat transfer inside a body. The corresponding differential \
    equation reads

        .. math::
            \partial_t (s T) -\mathrm{div}(\lambda\,\mathrm{grad}(T)) = \dot q,

    where :math:`\lambda` is the thermal conductivity (see :py:class:`ThermalConductivity`), \
    :math:`s` is the volumetric heat capacity (see :py:class:`VolumetricHeatCapacity`), \
    :math:`\dot q` is the heat flux density and :math:`T` denotes the temperature.
    """

    problem_identifier: str = 'Transient heat conduction problem in two-dimensional Cartesian coordinates'
    available_monitors: dict = {'thermal_loss_power': '_thermal_loss_power'}
    associated_solution_class = ThermalSolutionCartTransient

    def __init__(self, description: str, tri_mesh: mesh.TriMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations, time_steps: np.ndarray,
                 length: float = 1, electromagnetic_heat_source: CurrentFlowSolutionCartTransient = None):
        """Transient heat conduction problem, cartesian.

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
        length : float, optional
            The length of the problem. Default is 1
        electromagnetic_heat_source: CurrentFlowSolutionCartTransient
            A current flow solution, whose joule loss density is added as a heat source to the rhs
        """
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations, time_steps)

        self.length = length
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianNodalShapeFunction = TriCartesianNodalShapeFunction(tri_mesh)

        self._mass_linear = None  # self.materials.is_linear(material.VolumetricHeatCapacity)
        self._divgrad_linear = None  # self.materials.is_linear(material.ThermalConductivity)
        self._load_linear = None  # self.excitations.is_linear
        self._boundary_condition_linear = None  # self.boundary_conditions.is_linear
        self._all_linear = None
        # all([self.mass_linear, self.divgrad_linear, self.load_linear, self.boundary_condition_linear])
        self._excitations_time_dependent = None  # self.excitations.is_time_dependent

        self.electromagnetic_heat_source = electromagnetic_heat_source

        self.consistency_check()

    @property
    def mass_linear(self):
        """Checks if the mass matrix is linear"""
        if self._mass_linear is None:
            self._mass_linear = self.materials.is_linear(material.VolumetricHeatCapacity)

        return self._mass_linear

    @property
    def divgrad_linear(self):
        """Checks if the divgrad matrix is linear"""
        if self._divgrad_linear is None:
            self._divgrad_linear = self.materials.is_linear(material.ThermalConductivity)

        return self._divgrad_linear

    @property
    def load_linear(self):
        """Checks if the load vector is linear"""
        if self._load_linear is None:
            self._load_linear = self.excitations.is_linear

        return self._load_linear

    @property
    def boundary_condition_linear(self):
        """Checks if the boundary condition is linear"""
        if self._boundary_condition_linear is None:
            self._boundary_condition_linear = self.boundary_conditions.is_linear

        return self._boundary_condition_linear

    @property
    def all_linear(self):
        """Checks if everything is linear"""
        if self._all_linear is None:
            self._all_linear = all([self.mass_linear, self.divgrad_linear, self.load_linear,
                                    self.boundary_condition_linear])

        return self._all_linear

    @property
    def excitations_time_dependent(self):
        """Checks if the excitations are time dependent"""
        if self._excitations_time_dependent is None:
            self._excitations_time_dependent = self.excitations.is_time_dependent

        return self._excitations_time_dependent

    @staticmethod
    def _thermal_loss_power(solution: 'ThermalSolutionCartStatic'):
        return solution.thermal_loss_power

    Monitor = Union[str, Callable[['ThermalSolutionCartStatic'], Any]]
    Solution_Monitor = Union[int, Iterable[int]]

    def _solve_system(self, matrix, rhs, **kwargs) -> np.ndarray:
        matrix_shrink, rhs_shrink, _, _, support_data = self.shape_function.shrink(matrix, coo_matrix(rhs), self)
        # pylint: disable=no-member
        temperature_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(),
                                                               **kwargs)

        temperature = self.shape_function.inflate(temperature_shrink, self, support_data)
        return temperature

    def solve(self, start_value: Union[np.ndarray, ThermalSolutionCartStatic],
              solution_monitor: Union[int, Iterable[int]] = 1,
              monitors: Dict['str', Union[Monitor, Tuple[Solution_Monitor, Monitor]]] = None,
              callback: Callable[['ThermalSolutionCartStatic'], NoReturn] = None,
              solver_info: ThermalSolverInfoCartTransient = None, **kwargs) -> \
            ThermalSolutionCartTransient:

        # region Initialization and Pre-processing
        if not self.all_linear:
            if solver_info is None:
                solver_info = ThermalSolverInfoCartTransient()

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
                if isinstance(start_value, ThermalSolutionCartIntermediate):
                    static_solution = start_value
                elif isinstance(start_value, ThermalSolutionCartStatic):
                    static_solution = ThermalSolutionCartIntermediate.extend_solution(start_value)
                else:
                    static_solution = ThermalSolutionCartIntermediate(
                        f'temporary static solution generated by solve in'
                        f'ThermalProblemCartTransient at time step {k}',
                        start_value, self.mesh, self.shape_function, self.regions,
                        self.materials, self.excitations)
                static_solution.time = self.time_steps[k - 1]
                self.boundary_conditions.update('solution', static_solution)
            # endregion

            # Compute part of the rhs that depends only on the previous time step
            rhs_helper = 1 / delta_t * static_solution.mass_matrix_s @ static_solution.temperature[:, None]

            # region Update materials and matrices to current time step
            static_solution.time = self.time_steps[k]
            self.boundary_conditions.update('time', self.time_steps[k])

            if k == 1 or self.excitations_time_dependent:
                load_excitations = self.shape_function.load_vector(self.regions, self.excitations)

            if self.electromagnetic_heat_source is not None:
                load_electromagnetic_heat_source = self.shape_function.load_vector(
                    self.electromagnetic_heat_source.joule_loss_power_density(time=self.time_steps[k]))
            # endregion

            # Save monitor results of first time step
            if k == 1:
                for key, monitor in monitors.items():
                    if k in monitor[0]:
                        monitors_results[key][1].append(monitor[1](static_solution))

            if self.all_linear:
                # region Solve system in case a linear problem
                # Finish building rhs and system matrix
                rhs = load_excitations + rhs_helper + static_solution.load_vector_thermal
                if self.electromagnetic_heat_source is not None:
                    rhs = rhs + load_electromagnetic_heat_source
                matrix = 1 / delta_t * static_solution.mass_matrix_s + static_solution.divgrad_matrix_lambda
                # Solve system
                static_solution.temperature = self._solve_system(matrix, rhs, **kwargs)
                # endregion

            else:
                # region Perform successive substitution algorithm if a quantity is nonlinear
                iter_no = 0
                while True:
                    # Update iteration variables
                    iter_no += 1
                    thermal_loss_power_prev = static_solution.thermal_loss_power

                    # region Build and solve system
                    rhs = load_excitations + rhs_helper + static_solution.load_vector_thermal
                    if self.electromagnetic_heat_source is not None:
                        rhs = rhs + load_electromagnetic_heat_source
                    matrix = 1 / delta_t * static_solution.mass_matrix_s + static_solution.divgrad_matrix_lambda
                    temperature_new = self._solve_system(matrix, rhs)
                    # endregion

                    # region Insert relaxation and write new temperature vector to static solution
                    if solver_info.relaxation_successive_substitution != 1:
                        temperature_new = solver_info.relaxation_successive_substitution * temperature_new + \
                            (1 - solver_info.relaxation_successive_substitution) * static_solution.temperature

                    static_solution.temperature = temperature_new
                    self.boundary_conditions.update('solution', static_solution)
                    # endregion

                    # region Terminate successive subsitution
                    relative_error = abs((thermal_loss_power_prev - static_solution.thermal_loss_power) /
                                         static_solution.thermal_loss_power)

                    # Report progress
                    # logger.info('Successive substitution iteration: %d, rel. error: %e, loss power: %f', iter_no,
                    #             relative_error, solution_new.thermal_loss_power)

                    # Check for convergence
                    if relative_error <= solver_info.tolerance_successive_substitution:
                        logger.info('Convergence after %d successive substitution iterations. Relative error: %f',
                                    iter_no, relative_error)
                        break

                    # Check if maximum number of iterations is exceeded.
                    if iter_no == solver_info.max_iter_successive_substitution:
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
                solutions.append(static_solution.temperature)
            # endregion

        # region Write output
        solutions = np.stack(solutions)

        for key, monitor in monitors_results.items():
            monitors_results[key][1] = np.stack(monitors_results[key][1])
        # endregion
        return ThermalSolutionCartTransient(f'solution of {self.description}', solutions, self.mesh,
                                            self.shape_function, self.regions, self.materials, self.excitations,
                                            time_steps, monitors_results)

    def get_system(self, time: float, **kwargs) -> Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> TransientSolution:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> TransientSolution:
        raise NotImplementedError

    def create_solution(self, solutions, time_steps, description: str = None, **kwargs) -> TransientSolution:
        raise NotImplementedError
