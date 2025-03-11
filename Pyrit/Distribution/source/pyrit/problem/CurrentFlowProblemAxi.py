# coding=utf-8
"""Current flow problem in axisymmetric coordinates

.. sectionauthor:: Ruppert
"""
# pylint: disable=arguments-differ
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Union, Tuple, Callable, NoReturn, Any, Iterable, List

from scipy import sparse
from scipy.sparse import coo_matrix
import numpy as np

from pyrit import get_logger
from pyrit import mesh, region, material, bdrycond, excitation
from pyrit.material import DiffConductivityParameter, DiffPermittivityParameter
from pyrit.problem.Problem import StaticProblem, HarmonicProblem, TransientProblem
from pyrit.solution import CurrentFlowSolutionAxiStatic, CurrentFlowSolutionAxiHarmonic, \
    CurrentFlowSolutionAxiTransient, ThermalSolutionAxiTransient, ThermalSolutionAxiStatic
from pyrit.solution.CurrentFlowSolutionAxi import CurrentFlowSolutionAxiIntermediate
from pyrit.toolbox.QuantitiesOfInterestToolbox import QuantitiesOfInterest
from pyrit.shapefunction import TriAxisymmetricNodalShapeFunction

if TYPE_CHECKING:
    from pyrit.mesh import AxiMesh

logger = get_logger(__name__)

__all__ = ['CurrentFlowProblemAxiStatic', 'CurrentFlowProblemAxiHarmonic', 'CurrentFlowProblemAxiTransient',
           'CurrentFlowSolverInfoAxiStatic', 'CurrentFlowSolverInfoAxiTransient']


@dataclass()  # todo this should be explained better/removed from the doc, as then it's for internal/expert use only.
class CurrentFlowSolverInfoAxiStatic:
    """Class for passing options to the solve-method of CurrentFlowProblemAxiStatic"""

    tolerance_newton: float = 1e-8  # tolerance for the newton algorithm
    max_iter_newton: int = 100  # maximum number of newton iterations
    relaxation_newton: float = 1  # relaxation for newton algorithm


@dataclass()
class CurrentFlowSolverInfoAxiTransient:
    """Class for passing options to the solve-method of CurrentFlowProblemAxiTransient"""

    tolerance_newton: float = 1e-8  # tolerance for the newton algorithm
    max_iter_newton: int = 100  # maximum number of newton iterations
    relaxation_newton: float = 1  # relaxation for newton algorithm


class CurrentFlowProblemAxiStatic(StaticProblem):
    r"""A stationary current problem in axisymmetric coordinates:

    The stationary current problem models resistive effects. The corresponding differential equation reads

    .. math::
        -\mathrm{div}(\sigma \, \mathrm{grad} (\phi)) = 0,

    where :math:`\sigma` is the electric conductivity (see :py:class:`~pyrit.material.Conductivity`) and :math:`\phi`
    denotes the electric scalar potential. A possible application is, for example, the steady state simulation of a HVDC
    cable joint.

    In case of nonlinear problems, the solve routine performs a Newton algorithm. The algorithm requires the definition
    of a :py:class:`~pyrit.material.DifferentialConductivity` for all materials with a nonlinear conductivity.

    The corresponding solution class is :py:class:`~pyrit.solution.CurrentFlowSolutionAxiStatic`.
    """

    problem_identifier: str = 'Stationary current problem in axisymmetric coordinates'
    associated_solution_class = CurrentFlowSolutionAxiStatic

    def __init__(self, description: str, axi_mesh: mesh.AxiMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond,
                 excitations: excitation.Excitations,
                 temperature_coupling: Union[np.ndarray, ThermalSolutionAxiStatic] = None):
        """Constructor of CurrentFlowProblemAxiStatic.

        Parameters
        ----------
        description : str
            A description of the problem
        axi_mesh : AxiMesh
            A mesh object. See :py:class:`pyrit.mesh.AxiMesh`
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
        # So the type is known by the IDE
        self.mesh: mesh.AxiMesh = axi_mesh
        self.shape_function: TriAxisymmetricNodalShapeFunction = TriAxisymmetricNodalShapeFunction(axi_mesh)

        # Determine if problem is temperature-dependent (needed for coupled problems)
        self._is_temperature_dependent: bool = None
        self._temperature_coupling: Union[np.ndarray, ThermalSolutionAxiStatic] = temperature_coupling

        self.consistency_check()

    @property
    def is_linear(self):
        solution_in_conductivity = True
        for mat in self.materials:
            if 'solution' in mat.get_property(material.Conductivity).keyword_args:
                solution_in_conductivity = False
                break
        return solution_in_conductivity and self.boundary_conditions.is_linear and self.excitations.is_linear

    @property
    def temperature_coupling(self):
        """The temperature present in the computational domain.

        Important in the case of temperature-dependent materials.
        """
        return self._temperature_coupling

    @temperature_coupling.setter
    def temperature_coupling(self, temperature_coupling: Union[np.ndarray, ThermalSolutionAxiStatic]):
        self._temperature_coupling = temperature_coupling

    @property
    def is_temperature_dependent(self):
        """Property that indicates if the problem is temperature-dependent."""
        if self._is_temperature_dependent is None:
            self._is_temperature_dependent = False
            for mat in self.materials:
                if 'temperature' in mat.get_property(material.Conductivity).keyword_args:
                    self._is_temperature_dependent = True
                if 'temperature' in mat.get_property(material.DifferentialConductivity).keyword_args:
                    self._is_temperature_dependent = True
            for exci in self.excitations:
                if 'temperature' in exci.keyword_args:
                    self._is_temperature_dependent = True
            for bc in self.boundary_conditions:
                if 'temperature' in bc.keyword_args:
                    self._is_temperature_dependent = True
        return self._is_temperature_dependent

    def _check_differential_conductivity(self) -> bool:
        """Make sure all materials with a nonlinear conductivity also have a differential conductivity"""
        success = True
        if not self.is_linear:
            for mat_id in self.materials.get_ids():
                mat = self.materials.get_material(mat_id)
                cond = mat.get_property(material.Conductivity)
                if cond is not None:
                    if not cond.is_linear:
                        if mat.get_property(material.DifferentialConductivity) is None:
                            success = False
                            logger.warning("All nonlinear materials must have a DifferentialConductivity. "
                                           "The DifferentialConductivity of %s is missing.", mat.name)
        return success

    def _consistency_check(self) -> bool:
        success = super()._consistency_check()

        success &= self._check_differential_conductivity()

        return success

    def _solve_system(self, matrix, rhs, **kwargs) -> np.ndarray:
        # Help routine that shrinks, solves and inflates the system "matrix * x = rhs", returns the solution x.

        matrix_shrink, rhs_shrink, _, _, support_data = self.shape_function.shrink(matrix.tocoo(), coo_matrix(rhs),
                                                                                   self, 1)
        # pylint: disable=no-member
        potential_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(),
                                                             **kwargs)
        return self.shape_function.inflate(potential_shrink, self, support_data)

    def get_system(self, **kwargs) -> Tuple[sparse.spmatrix, sparse.spmatrix]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> CurrentFlowSolutionAxiStatic:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> CurrentFlowSolutionAxiStatic:
        raise NotImplementedError

    def create_solution(self, solution: np.ndarray, description: str = None, **kwargs) -> CurrentFlowSolutionAxiStatic:
        raise NotImplementedError

    def solve(self, initial_guess_potential: Union[np.ndarray, CurrentFlowSolutionAxiStatic] = None,
              solver_info: CurrentFlowSolverInfoAxiStatic = None,
              **kwargs) -> CurrentFlowSolutionAxiStatic:  # pylint: disable=arguments-differ
        """Solve the Problem using the Newton method.

        Parameters
        ----------
        initial_guess_potential: np.ndarray
            [V] Start guess for Newton iteration. If None is given, the solution of the problem that is obtained when
            evaluating the materials for an all-zero solution is used as an initial guess.
        solver_info: CurrentFlowSolverInfoAxiStatic
            Options for the Newton algorithm.
        kwargs :
            Are all passed to the function :py:func:`solve_linear_system`.

        Returns
        -------
        solution : CurrentFlowSolutionAxiStatic
            The solution object
        """
        # region Linear Probelm
        if self.is_linear:
            static_solution = CurrentFlowSolutionAxiStatic.solution_from_problem(self.description,
                                                                                 self, np.zeros((self.mesh.num_node,)))
            static_solution.temperature_coupling = self._temperature_coupling
            static_solution.potential = self._solve_system(static_solution.divgrad_matrix_sigma,
                                                           static_solution.load_vector_electric, **kwargs)
            return static_solution
        # endregion

        # region Nonlinear Problem --> Newton algorithm
        # region Initializations
        iter_no = 0
        if solver_info is None:
            solver_info = CurrentFlowSolverInfoAxiStatic()

        # Set initial guess for solution
        if initial_guess_potential is None:
            # Initialize materials with zero solution and solve boundary value problem for this
            # material working point
            static_solution = CurrentFlowSolutionAxiStatic.solution_from_problem(self.description,
                                                                                 self, np.zeros((self.mesh.num_node,)))
            static_solution.temperature_coupling = self._temperature_coupling
            static_solution.potential = self._solve_system(static_solution.divgrad_matrix_sigma,
                                                           static_solution.load_vector_electric, **kwargs)
        elif isinstance(initial_guess_potential, CurrentFlowSolutionAxiStatic):
            static_solution = initial_guess_potential
            static_solution.temperature_coupling = self._temperature_coupling
        else:
            static_solution = CurrentFlowSolutionAxiStatic.solution_from_problem(self.description, self,
                                                                                 initial_guess_potential)
            static_solution.temperature_coupling = self._temperature_coupling
        # endregion

        # region Newton algorithm
        while True:
            iter_no += 1
            loss_power_prev = static_solution.joule_loss_power

            # region Build and solve system
            # ToDo: Split sigmad in sigma and 2 dsigma/dE^2 --> avoid loop over elements with linear materials
            #  (not urgent, since most mesh points located at nonlinear regions anyways)
            rhs = coo_matrix(static_solution.load_vector_electric
                             - static_solution.divgrad_matrix_sigma @ static_solution.potential[:, None]
                             + static_solution.divgrad_matrix_sigmad @ static_solution.potential[:, None])
            lhs = static_solution.divgrad_matrix_sigmad
            potential_new = self._solve_system(lhs, rhs, **kwargs)
            # endregion

            # region Insert relaxation
            if solver_info.relaxation_newton != 1:
                potential_new = solver_info.relaxation_newton * potential_new \
                    + (1 - solver_info.relaxation_newton) * static_solution.potential
            static_solution.potential = potential_new
            # endregion

            # region Terminate algorithm
            # Compute relative error
            relative_error = (abs((loss_power_prev - static_solution.joule_loss_power)
                                  / static_solution.joule_loss_power))

            logger.info('Iteration: %d, rel. error: %e, power loss: %f', iter_no, relative_error,
                        static_solution.joule_loss_power)

            # Check for convergence
            if relative_error <= solver_info.tolerance_newton:
                logger.info('Convergence after %d iterations. Relative error: %e', iter_no, relative_error)
                return static_solution

            # Check if maximum number of iterations is exceeded.
            if iter_no == solver_info.max_iter_newton:
                logger.critical('Maximum number of iterations %d exceeded. Relative error: %e', iter_no, relative_error)
                return static_solution
            # endregion
        # endregion
        # endregion

    @classmethod
    def adjoint_method(cls, solution: CurrentFlowSolutionAxiStatic, qois: QuantitiesOfInterest, save_adj: bool = False,
                       **kwargs):
        """Compute the sensitivities of quantities of interest using the adjoint method.

        Parameters
        ----------
        solution: CurrentFlowProblemAxiStatic
            The solution of the problem.
        qois: QuantitiesOfInterest
            The quantities of interest
        save_adj: bool
            Boolean that indicates whether the adjoint variables should be saved. If not, an empty dictionary is
            returned.
        kwargs:
            Are all passed to the function :py:func:`solve_linear_system`.

        Returns
        -------
        sensitivities: Dict[Tuple[str,str]: float]
            Dictionary with the sensitivities of the quantities of interests. The keys are tuples of the form
            (<name of the quantity of interest>,<name of the parameter>).
        adj_variables: Dict[str, np.ndarray]
            Dictionary containing the adjoint variables. The keys are the names of the quantities of interest. If
            save_adj is false, an empty dictionary is returned.

        """
        if not isinstance(solution, cls.associated_solution_class):
            raise ValueError(f"The solution is of the wrong type. Expected {cls.associated_solution_class} "
                             f"but got {type(solution)}")
        # region Initialization and pre-processing
        solution = CurrentFlowSolutionAxiIntermediate.extend_solution(solution)
        adj_variables = {}
        sensitivities = {}
        lhs = solution.divgrad_matrix_sigmad
        # endregion

        # Generate adjoint boundary conditions from boundary conditions of original problem
        bdrycond_adj = solution.boundary_conditions.zero_dirichlet()

        for qoi in qois:
            # region Compute rhs
            rhs = qoi.evaluate_diff_qoi_dof('potential', [solution])
            rhs = coo_matrix(rhs)
            if rhs.shape[0] != lhs.shape[0]:
                rhs = rhs.transpose()
            # endregion

            # region Shrink, solve, inflate
            lhs_shrink, rhs_shrink = bdrycond_adj.shrink(solution.mesh, solution.shape_function, solution.regions,
                                                         lhs.tocoo(), rhs, 1)

            adj_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                            rhs_shrink.tocsr(),
                                                                            **kwargs)
            adj = bdrycond_adj.inflate(solution.mesh, solution.shape_function, solution.regions, adj_shrink)
            # endregion

            if save_adj:
                adj_variables[qoi.name] = adj

            # region Post-processing/Sensitivity computation
            for param in qoi.get_parameter_names():
                # Select correct parameter in materials
                for mat in solution.materials:
                    prop: DiffConductivityParameter = mat.get_property(DiffConductivityParameter)
                    prop.parameter_key = param

                sensitivities[(qoi.name, param)] = qoi.evaluate_diff_qoi_param(param, [solution]) \
                                                   - solution.potential @ solution.compute_Ksigmap() @ adj
            # endregion

        return sensitivities, adj_variables

    @classmethod
    def direct_sensitivity_method(cls, solution: CurrentFlowSolutionAxiStatic,
                                  qois: QuantitiesOfInterest,
                                  save_sensitivities_potential: bool = False,
                                  **kwargs):
        """Compute the sensitivities of quantities of interest using the direct sensitivity method.

        Parameters
        ----------
        solution: CurrentFlowProblemAxiStatic
            The solution of the problem.
        qois: QuantitiesOfInterest
            The quantities of interest
        save_sensitivities_potential: bool
            Boolean that indicates whether the save the sensitivities of the electric potential. If not, an empty
            dictionary is returned.
        kwargs:
            Are all passed to the function :py:func:`solve_linear_system`.

        Returns
        -------
        sensitivities: Dict[Tuple[str, str]: float]
            Dictionary with the sensitivities of the quantities of interests. The keys are tuples of the form
            (<name of the quantity of interest>,<name of the parameter>).
        sensitivities_potential: Dict[str, np.ndarray]
            Dictionary containing the sensitivities of the electric potential. The keys are the names of the parameters.
            If save_sensitivities_potential is false, an empty dictionary is returned.

        """
        if not isinstance(solution, cls.associated_solution_class):
            raise ValueError(f"The solution is of the wrong type. Expected {cls.associated_solution_class} "
                             f"but got {type(solution)}")

        # region Initialization and pre-processing
        solution = CurrentFlowSolutionAxiIntermediate.extend_solution(solution)
        sensitivities_potential = {}
        sensitivities = {}
        # endregion

        # Compute left-hand side
        lhs = solution.divgrad_matrix_sigmad

        # Generate sensitivity boundary conditions from boundary conditions of original problem
        bdrycond_dsm = solution.boundary_conditions.zero_dirichlet()

        for param_name in qois.get_parameter_names():  # Loop over all parameters
            # region Select parameter in DiffConductivityParameter
            for mat in solution.materials:
                prop: DiffConductivityParameter = mat.get_property(DiffConductivityParameter)
                prop.parameter_key = param_name
            # endregion

            # region Compute right-hand side
            rhs = coo_matrix(np.expand_dims(- solution.compute_Ksigmap() @ solution.potential, axis=1))
            # endregion

            # region Shrink, solve, inflate
            lhs_shrink, rhs_shrink = bdrycond_dsm.shrink(solution.mesh, solution.shape_function, solution.regions,
                                                         lhs.tocoo(), rhs, 1)

            sens_pot_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                 rhs_shrink.tocsr(),
                                                                                 **kwargs)
            sens_pot = bdrycond_dsm.inflate(solution.mesh, solution.shape_function, solution.regions, sens_pot_shrink)
            # endregion

            if save_sensitivities_potential:
                sensitivities_potential[param_name] = sens_pot

            # region Post-processing/Sensitivity computation
            for qoi in qois.get_qois_from_parameter_name(param_name):
                dqoidparam = qoi.evaluate_diff_qoi_param(param_name, [solution])
                q = qoi.evaluate_diff_qoi_dof('potential', [solution])
                sensitivities[(qoi.name, param_name)] = dqoidparam + q @ sens_pot
            # endregion

        return sensitivities, sensitivities_potential


class CurrentFlowProblemAxiHarmonic(HarmonicProblem):
    r"""A harmonic electroquasistatic problem in axisymmetric coordinates:

    The harmonic electroquasistatic problem models capacitive-resistive effects. The corresponding differential \
    equation reads

    .. math::
        -\mathrm{div}(j 2\pi f\varepsilon\, \mathrm{grad} (\phi)) -\mathrm{div}(\sigma\,\mathrm{grad}
         (\phi)) = 0,

    where :math:`\sigma` is the electric conductivity (see :py:class:`~pyrit.material.Conductivity`),
    :math:`\varepsilon` is the electric permittivity (see :py:class:`~pyrit.material.Permittivity`), :math:`\phi`
    denotes the electric scalar potential, and :math:`f` is the frequency. The problem can, by definition, only handle
    linear materials. A possible application is, for example, the steady state simulation of the insulation system in
    an electrical machine.

    The corresponding solution class is :py:class:`~pyrit.solution.CurrentFlowSolutionAxiHarmonic`.
    """

    problem_identifier: str = 'Harmonic electroquasistatic problem in axisymmetric coordinates'
    associated_solution_class = CurrentFlowSolutionAxiHarmonic

    def __init__(self, description: str, axi_mesh: mesh.AxiMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond,
                 excitations: excitation.Excitations,
                 frequency: float):
        """Constructor of CurrentFlowProblemAxiStatic.

        Parameters
        ----------
        description : str
            A description of the problem
        axi_mesh : AxiMesh
            A mesh object. See :py:class:`pyrit.mesh.AxiMesh`
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
        """
        # Setup Model
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations, frequency)
        # So the type is known by the IDE
        self.mesh: mesh.AxiMesh = axi_mesh
        self.shape_function: TriAxisymmetricNodalShapeFunction = TriAxisymmetricNodalShapeFunction(axi_mesh)

        self.consistency_check()

    def get_system(self, **kwargs) -> Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> CurrentFlowSolutionAxiHarmonic:
        raise NotImplementedError

    def create_solution(self, solution: np.ndarray, description: str = None,
                        **kwargs) -> CurrentFlowSolutionAxiHarmonic:
        raise NotImplementedError

    def solve(self, *args, **kwargs) -> CurrentFlowSolutionAxiHarmonic:
        raise NotImplementedError()


class CurrentFlowProblemAxiTransient(TransientProblem):
    r"""A transient electroquasistatic problem in axisymmetric coordinates:

    The transient electroquasistatic problem models capacitive-resistive effects. The corresponding differential \
    equation reads

    .. math::
        -\mathrm{div}(\partial_t(\varepsilon\, \mathrm{grad} (\phi))) -\mathrm{div}(\sigma\,\mathrm{grad}
         (\phi)) = 0,

    where :math:`\sigma` is the electric conductivity (see :py:class:`Conductivity`), :math:`\varepsilon` is the \
    electric permittivity (see :py:class:`Permittivity`) and :math:`\phi` denotes the electric scalar potential. \
    A possible application is, for example, the simulation of transient effects in HVDC cable joints or AC surge \
    arresters.

    In case of nonlinear problems, the solve routine performs a Newton algorithm. The algorithm requires the definition
    of a :py:class:`~pyrit.material.DifferentialConductiviy` and :py:class:`~pyrit.material.DifferentialPermittivity`
    for materials with a nonlinear conductivity or nonlinear permittivity, respectively.

    The corresponding solution class is :py:class:`~pyrit.solution.CurrentFlowSolutionAxiTransient`.
    """

    problem_identifier: str = 'Transient electroquasistatic problem in axisymmetric coordinates'
    available_monitors: dict = {'joule_loss_power': '_joule_loss_power'}
    associated_solution_class = CurrentFlowSolutionAxiTransient

    def __init__(self, description: str, axi_mesh: mesh.AxiMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations, time_steps: np.ndarray,
                 temperature_coupling: Union[ThermalSolutionAxiTransient, np.ndarray] = None):
        """Transient EQS problem, axisymmetric.

        Parameters
        ----------
        description : str
            A description of the problem.
        axi_mesh : AxiMesh
            A mesh object. See :py:class:`pyrit.mesh.AxiMesh`.
        tri_axi_nodal_shape_function : TriAxisymmetricNodalShapeFunction
            A shape function object. See :py:class:`pyrit.shapefunction.TriAxisymmetricNodalShapeFunction`
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

        self.mesh: mesh.AxiMesh = axi_mesh
        self.shape_function: TriAxisymmetricNodalShapeFunction = TriAxisymmetricNodalShapeFunction(axi_mesh)

        # Determine if the problem is linear (avoid Newton algorithm)
        self.divgrad_eps_linear = self._properties_linear(material.Permittivity)
        self.divgrad_sigma_linear = self._properties_linear(material.Conductivity)
        self.all_linear = all([self.divgrad_eps_linear, self.divgrad_sigma_linear,
                               self.excitations.is_linear, self.boundary_conditions.is_linear])
        self._is_temperature_dependent: bool = None
        self._temperature_coupling: Union[ThermalSolutionAxiTransient, np.ndarray] = temperature_coupling

        self.consistency_check()

    def _properties_linear(self, propclass):
        """Checks if propclass of materials is linear by checking for 'solution' as a keyword_argument."""
        for mat in self.materials:
            if 'solution' in mat.get_property(propclass).keyword_args:
                return False
        return True

    @property
    def temperature_coupling(self):
        """The temperature present in the computational domain.

        Important in the case of temperature-dependent materials.
        """
        return self._temperature_coupling

    @temperature_coupling.setter
    def temperature_coupling(self, temperature_coupling):
        self._temperature_coupling = temperature_coupling

    @property
    def is_temperature_dependent(self):
        """True if the problem is temperature-dependent."""
        if self._is_temperature_dependent is None:
            self._is_temperature_dependent = False
            for mat in self.materials:
                if 'temperature' in mat.get_property(material.DifferentialConductivity).keyword_args:
                    self._is_temperature_dependent = True
            for mat in self.materials:
                if 'temperature' in mat.get_property(material.DifferentialPermittivity).keyword_args:
                    self._is_temperature_dependent = True
            for exci in self.excitations:
                if 'temperature' in exci.keyword_args:
                    self._is_temperature_dependent = True
            for bc in self.boundary_conditions:
                if 'temperature' in bc.keyword_args:
                    self._is_temperature_dependent = True
        return self._is_temperature_dependent

    def _check_differential_conductivity(self):
        """Make sure all materials with a nonlinear conductivity also have a differential conductivity"""
        success = True
        if not self.divgrad_sigma_linear:
            for mat_id in self.materials.get_ids():
                mat = self.materials.get_material(mat_id)
                cond = mat.get_property(material.Conductivity)
                if cond is not None:
                    if not cond.is_linear:
                        if mat.get_property(material.DifferentialConductivity) is None:
                            success = False
                            logger.warning("All materials with a nonlinear conductivity must have a "
                                           "DifferentialConductivity. The DifferentialConductivity of %s is missing.",
                                           mat.name)
        return success

    def _check_differential_permittivity(self):
        """Make sure all materials with a nonlinear conductivity also have a differential permittivity"""
        success = True
        if not self.divgrad_eps_linear:
            for mat_id in self.materials.get_ids():
                mat = self.materials.get_material(mat_id)
                eps = mat.get_property(material.Permittivity)
                if eps is not None:
                    if not eps.is_linear:
                        if mat.get_property(material.DifferentialPermittivity) is None:
                            success = False
                            logger.warning("All materials with a nonlinear Permittivity must have a "
                                           "DifferentialPermittivity. The DifferentialPermittivity of %s is missing.",
                                           mat.name)
        return success

    def _consistency_check(self) -> bool:
        success = super()._consistency_check()

        success &= self._check_differential_conductivity()
        success &= self._check_differential_permittivity()

        return success

    @staticmethod
    def _joule_loss_power(solution: 'CurrentFlowSolutionAxiStatic'):
        return solution.joule_loss_power

    Monitor = Union[str, Callable[['CurrentFlowSolutionAxiStatic'], Any]]
    Solution_Monitor = Union[int, Iterable[int]]

    def _solve_system(self, matrix, rhs, **kwargs) -> np.ndarray:
        matrix_shrink, rhs_shrink, _, _, support_data = self.shape_function.shrink(matrix, rhs, self, 1)
        # pylint: disable=no-member
        potential_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(),
                                                             **kwargs)

        prev_sol = self.shape_function.inflate(potential_shrink, self, support_data)
        return prev_sol

    def get_system(self, time: float, **kwargs) -> Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]:
        raise NotImplementedError

    def _solve_linear(self, **kwargs) -> CurrentFlowSolutionAxiTransient:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> CurrentFlowSolutionAxiTransient:
        raise NotImplementedError

    def create_solution(self, solutions, time_steps, description: str = None,
                        **kwargs) -> CurrentFlowSolutionAxiTransient:
        raise NotImplementedError

    def solve(self, start_value: Union[np.ndarray, CurrentFlowSolutionAxiStatic],
              solution_monitor: Union[int, Iterable[int]] = 1,
              monitors: Dict['str', Union[Monitor, Tuple[Solution_Monitor, Monitor]]] = None,
              callback: Callable[['CurrentFlowSolutionAxiStatic'], NoReturn] = None,
              solver_info: CurrentFlowSolverInfoAxiTransient = None, **kwargs) -> \
            CurrentFlowSolutionAxiTransient:
        """Solve the problem. In case of nonlinear materials, a Newton algorithm is performed.

        The problem is defined in the object. A start value has to be given. Furthermore, you can determine at which
        time steps the solution should be stored in the solution object (`solution_monitor`). With `monitors` you can
        determine what entities over time should be calculated during the simulation. Therefore, the solution in each
        time step is used. This can save memory.

        For more information on how to use the monitors, see :py:func:`~pyrit.problem.Problem.solve`.

        Parameters
        ----------
        start_value : np.ndarray
            The start value.
        solution_monitor : Union[int, np.ndarray]
            Determines at which time steps the solution should be stored in the solution object. If it is an integer
            :math:`n`, the solution is stored at every :math:`n`-th time step (including the first and the last one).
            If it is an array, store at the indicated time steps.
        monitors : Dict['str', Union[Monitor, Tuple[Solution_Monitor, Monitor]]]
            A number of monitors. Each monitor, i.e. each entry in the dict, has a name (the key). The value is either a
            'Monitor' or a tuple (or a list) with the first entry containing the time steps when the monitor is
            evaluated and the second entry being th 'Monitor'. Here, a 'Monitor' is eiter the name of a predefined
            monitor or a function that returns the information. The predefined monitors are saved in the attribute
            `available_monitors`.
        callback : Callable[['Solution'], NoReturn]
            If given, this function is executed after every iteration. This can be used to update information in e.g.
            material data.
        solver_info : CurrentFlowSolverInfoAxiTransient
            Settings for the nonlinear Newton algorithm.
        kwargs :
            Additional keyword arguments passed to the py:func:`solve_lgs` function.

        Returns
        -------
        solution : CurrentFlowSolutionAxiTransient
            The solution of the problem.

        """
        # region Initialization and Preprocessing
        if not self.all_linear:
            if solver_info is None:
                solver_info = CurrentFlowSolverInfoAxiTransient()

        if isinstance(start_value, CurrentFlowSolutionAxiStatic):
            start_value = start_value.potential
        elif not isinstance(start_value, np.ndarray):
            raise ValueError(f"The argument start_value is not of the right type. "
                             f"It is '{type(start_value)}' but should be a ndarray or CurrentFlowSolutionAxiStatic")

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
                if isinstance(start_value, CurrentFlowSolutionAxiIntermediate):
                    static_solution = start_value
                elif isinstance(start_value, CurrentFlowSolutionAxiStatic):
                    static_solution = CurrentFlowSolutionAxiIntermediate.extend_solution(start_value)
                else:
                    static_solution = CurrentFlowSolutionAxiIntermediate(f'temporary static solution generated by '
                                                                         f'solve in ElectroquasistaticProblemAxi '
                                                                         f'at time step {k}',
                                                                         start_value, self.mesh, self.shape_function,
                                                                         self.regions, self.materials,
                                                                         self.boundary_conditions, self.excitations)
                static_solution.temperature_coupling = self._temperature_coupling
                static_solution.time = self.time_steps[k - 1]
            # endregion

            # Compute part of the rhs that depends only on the previous time step
            rhs_helper = 1 / delta_t * static_solution.divgrad_matrix_eps @ static_solution.potential[:, None]

            # Update materials and matrices to current time step
            static_solution.time = self.time_steps[k]

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
                        potential_new = solver_info.relaxation_newton * potential_new \
                            + (1 - solver_info.relaxation_newton) * static_solution.potential
                    static_solution.potential = potential_new
                    # endregion

                    # region Terminate Newton algorithm
                    relative_error = (abs((loss_power_prev - static_solution.joule_loss_power)
                                          / static_solution.joule_loss_power))

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
        return CurrentFlowSolutionAxiTransient(f'solution of {self.description}', solutions, self.mesh,
                                               self.shape_function, self.regions, self.materials,
                                               self.boundary_conditions,
                                               self.excitations,
                                               time_steps, monitors_results)

    @classmethod
    def adjoint_method(cls, solution: CurrentFlowSolutionAxiTransient,
                       qois: QuantitiesOfInterest,
                       sensitivities_potential_initial_value: Dict[str, np.ndarray],
                       time_steps_adj: np.ndarray = None,
                       save_adj: bool = False,
                       solution_monitor: Union[int, Iterable[int]] = 1,
                       linear_interpolation_of_solution=True,
                       **kwargs):
        """Compute sensitivities of quantities of interest using the adjoint method.

        Parameters
        ----------
        solution : CurrentFlowSolutionAxiTransient
            The solution of the problem.
        qois : QuantitiesOfInterest
            The quantities of interest.
        sensitivities_potential_initial_value: Dict[str, np.ndarray]
            The sensitivities of the electric potential at the initial time.
            Can be computed using
            :py:func:`~pyrit.problem.CurrentFlowProblemAxiStatic.direct_sensitivity_method`
        time_steps_adj: np.ndarray
            Time steps of the adjoint problem.
        save_adj: bool
            If true, the adjoint variables are saved at the times specified by solution_monitor.
        solution_monitor : Union[int, np.ndarray]
            Determines at which time steps the adjoint variables should be stored. If it is an integer
            :math:`n`, the solution is stored at every :math:`n`-th time step (including the first and the last one). If
            it is an array, store at the indicated time steps.
        linear_interpolation_of_solution: bool
            If true, the solution is interpolated linearly otherwise nearest-neighbor interpolation is used.
            Important if the time axes of the adjoint problem and the solution differ.
        kwargs :
            Additional keyword arguments passed to the py:func:`solve_lgs` function.

        Returns
        -------
        sensitivities: Dict[Tuple[str, str]: float]
            Dictionary with the sensitivities of the quantities of interests. The keys are tuples of the form
            (<name of the quantity of interest>,<name of the parameter>).
        adj_variables: Dict[str: np.ndarray]
            Dictionary containing the adjoint variables. The keys are the names of the quantities of interest. If
            save_adj is false, an empty dictionary is returned.
        """
        if not isinstance(solution, cls.associated_solution_class):
            raise ValueError(f"The solution is of the wrong type. Expected {cls.associated_solution_class} "
                             f"but got {type(solution)}")

        # Define adjoint boundary conditions from boundary conditions of original problem
        bdrycond_adj = solution.boundary_conditions.zero_dirichlet()

        # region Define final condition
        final_value = np.zeros((solution.mesh.num_node,))
        adj_prev = {}  # adjoint variables of previous (=later) time step
        for qoi_name in qois.get_names():
            adj_prev[qoi_name] = final_value
        # endregion

        # region Define time axes of adjoint problem
        if time_steps_adj is None:
            time_steps_adj = solution.time_steps
        delta_ts = np.diff(time_steps_adj)
        # endregion

        # region Preprocess solution_monitor
        if save_adj:
            if isinstance(solution_monitor, int):
                solution_monitor = np.arange(start=0, stop=len(time_steps_adj), step=solution_monitor)
                if solution_monitor[-1] != len(time_steps_adj) - 1:
                    solution_monitor = np.concatenate([solution_monitor, np.array([len(time_steps_adj) - 1])])
            time_steps_solution_monitor = time_steps_adj[solution_monitor]
            solution_monitor = set(solution_monitor)
        # endregion

        # region Initializations
        adj_solutions = {}
        sensitivities = {}
        sensitivities_boundary_terms = {}

        solution.linear_interpolation = linear_interpolation_of_solution

        if save_adj:
            # Add the final value to adj_solutions
            if len(time_steps_adj) - 1 in solution_monitor:
                for name in qois.get_names():
                    adj_solutions[name] = [final_value, ]
            else:
                for name in qois.get_names():
                    adj_solutions[name] = []
        # endregion

        # region Define static solution used to compute the matrices (instead of using the transient solution)
        # This is done to avoid storing/recomputing the matrices for different time steps
        static_solution_helper = solution.get_static_solution(time=time_steps_adj[0])
        static_solution_helper = CurrentFlowSolutionAxiIntermediate.extend_solution(static_solution_helper)
        # endregion

        # Loop over all time steps
        for k in range(1, len(time_steps_adj)):
            logger.info('starting with time step %d', k)

            # region Update time steps
            delta_t = delta_ts[-k]
            static_solution_helper.time = time_steps_adj[-(k + 1)]
            static_solution_helper.potential = solution.potential(time=time_steps_adj[-(k + 1)])
            # endregion

            # region Build lhs
            lhs = static_solution_helper.divgrad_matrix_sigmad + static_solution_helper.divgrad_matrix_epsd / delta_t
            # endregion

            for qoi in qois:  # Loop over all QoIs
                # region Build rhs
                q = qoi.evaluate_diff_qoi_dof('potential', [static_solution_helper, static_solution_helper.time])
                rhs = q + static_solution_helper.divgrad_matrix_epsd @ adj_prev[qoi.name] / delta_t
                rhs = coo_matrix(rhs)
                if rhs.shape[0] != lhs.shape[0]:
                    rhs = rhs.transpose()
                # endregion

                # region Shrink, solve, inflate
                lhs_shrink, rhs_shrink = bdrycond_adj.shrink(solution.mesh, solution.shape_function, solution.regions,
                                                             lhs.tocoo(), rhs, 1)

                adj_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                rhs_shrink.tocsr(),
                                                                                **kwargs)
                adj = bdrycond_adj.inflate(solution.mesh, solution.shape_function, solution.regions, adj_shrink)
                # endregion

                # region Compute sensitivities
                for param in qoi.get_parameter_names():
                    # region Select correct parameter in materials
                    for mat in solution.materials:
                        prop: DiffConductivityParameter = mat.get_property(DiffConductivityParameter)
                        prop.parameter_key = param
                        prop: DiffPermittivityParameter = mat.get_property(DiffPermittivityParameter)
                        prop.parameter_key = param
                    # endregion

                    # region Include contribution at t = t_end
                    if k == 1:
                        static_solution_helper.time = time_steps_adj[-k]
                        static_solution_helper.potential = solution.potential(time=time_steps_adj[-k])

                        dgdp = qoi.evaluate_diff_qoi_param(param, [static_solution_helper, static_solution_helper.time])
                        sensitivities[(qoi.name, param)] = [dgdp + static_solution_helper.potential @
                                                            static_solution_helper.compute_Kepsp()
                                                            @ (final_value - adj) / delta_t, ]
                        static_solution_helper.time = time_steps_adj[-(k + 1)]
                        static_solution_helper.potential = solution.potential(time=time_steps_adj[-(k + 1)])
                    # endregion

                    # region Compute boundary terms at t = 0
                    if k == len(time_steps_adj) - 1:
                        sensitivities_boundary_terms[(qoi.name, param)] = \
                            static_solution_helper.potential @ static_solution_helper.compute_Kepsp() @ adj \
                            + sensitivities_potential_initial_value[param] \
                            @ static_solution_helper.divgrad_matrix_epsd @ adj
                    # endregion

                    dgdp = qoi.evaluate_diff_qoi_param(param, [static_solution_helper, static_solution_helper.time])
                    sensitivities[(qoi.name, param)].append(
                        dgdp
                        - static_solution_helper.potential @ static_solution_helper.compute_Ksigmap() @ adj
                        + static_solution_helper.potential @ static_solution_helper.compute_Kepsp()
                        @ (adj_prev[qoi.name] - adj) / delta_t)
                # endregion

                adj_prev[qoi.name] = adj

                # region Save adjoint solution
                if save_adj:
                    if k in solution_monitor:
                        adj_solutions[qoi.name].append(adj)
                # endregion

        # region Post-process adjoint solution
        if save_adj:
            for name in qois.get_names():
                adj_solutions[name].reverse()
                adj_solutions[name] = np.stack(adj_solutions[name])
            adj_solutions['time'] = time_steps_solution_monitor
        # endregion

        # region Integrate sensitivities
        for key, sensitivities_non_integrated in sensitivities.items():
            sensitivities_non_integrated.reverse()
            sensitivities[key] = np.trapz(sensitivities_non_integrated, time_steps_adj) \
                                 + sensitivities_boundary_terms[key]
        # endregion

        return sensitivities, adj_solutions

    @classmethod
    def direct_sensitivity_method(cls, solution: CurrentFlowSolutionAxiTransient,
                                  qois: QuantitiesOfInterest,
                                  sensitivity_initial_value: Dict[str, np.ndarray],
                                  time_steps_sens: np.ndarray = None,
                                  save_sensitivities_potential: bool = False,
                                  solution_monitor: Union[int, Iterable[int]] = 1,
                                  linear_interpolation_of_solution=True,
                                  **kwargs):
        """Compute sensitivities of quantities of interest using the direct sensitivity method.

        Parameters
        ----------
        solution : CurrentFlowSolutionAxiTransient
            The solution of the problem.
        qois : QuantitiesOfInterest
            The quantities of interest.
        sensitivities_potential_initial_value: Dict[str, np.ndarray]
            The sensitivities of the electric potential at the initial time.
            Can be computed using
            :py:func:`~pyrit.problem.CurrentFlowProblemAxiStatic.direct_sensitivity_method`
        time_steps_sens: np.ndarray
            Time steps of the sensitivity formulation.
        save_sensitivities_potential: bool
            If true, the sensitivities of the potential are saved at the times specified by solution_monitor.
        solution_monitor : Union[int, np.ndarray]
            Determines at which time steps the adjoint variables should be stored. If it is an integer
            :math:`n`, the solution is stored at every :math:`n`-th time step (including the first and the last one). If
            it is an array, store at the indicated time steps.
        linear_interpolation_of_solution: bool
            If true, the solution is interpolated linearly otherwise nearest-neighbor interpolation is used.
            Important if the time axes of the sensitivity problem and the solution differ.
        kwargs :
            Additional keyword arguments passed to the py:func:`solve_lgs` function.

        Returns
        -------
        sensitivities: Dict[Tuple[str, str]: float]
            Dictionary with the sensitivities of the quantities of interests. The keys are tuples of the form
            (<name of the quantity of interest>,<name of the parameter>).
        sensitivities_potential: Dict[str: np.ndarray]
            Dictionary containing the sensitivities of the potential. The keys are the names of the parameters. If
            save_sensitivities_potential is False, an empty dictionary is returned.

        """
        if not isinstance(solution, cls.associated_solution_class):
            raise ValueError(f"The solution is of the wrong type. Expected {cls.associated_solution_class} "
                             f"but got {type(solution)}")

        solution.linear_interpolation = linear_interpolation_of_solution
        parameters = qois.get_parameter_names()

        # region Define boundary conditions of the sensitivity formulation from boundary conditions of original problem
        bdrycond_dsm = solution.boundary_conditions.zero_dirichlet()
        # endregion

        # region Define time axes of sensitivity problem
        if time_steps_sens is None:
            time_steps_sens = solution.time_steps
        delta_ts = np.diff(time_steps_sens)
        # endregion

        # region Preprocess solution_monitor
        if save_sensitivities_potential:
            if isinstance(solution_monitor, int):
                solution_monitor = np.arange(start=0, stop=len(time_steps_sens), step=solution_monitor)
                if solution_monitor[-1] != len(time_steps_sens) - 1:
                    solution_monitor = np.concatenate([solution_monitor, np.array([len(time_steps_sens) - 1])])
            time_steps_solution_monitor = time_steps_sens[solution_monitor]
            solution_monitor = set(solution_monitor)
        # endregion

        # region Initializations
        sensitivities_potential = {}
        sensitivities = {}
        sens_potential_prev = sensitivity_initial_value  # sensitivities of the potential at the previous time step

        # region Add the final value to sensitivities_potential
        if save_sensitivities_potential:
            if 0 in solution_monitor:
                for name in qois.get_parameter_names():
                    sensitivities_potential[name] = [sensitivity_initial_value[name], ]
            else:
                for name in qois.get_parameter_names():
                    sensitivities_potential[name] = []
        # endregion
        # endregion

        # region Define static solution used to compute the matrices (instead of using the transient solution)
        # This is done to avoid storing/recomputing the matrices for different time steps
        static_solution_helper = solution.get_static_solution(time=time_steps_sens[0])
        static_solution_helper = CurrentFlowSolutionAxiIntermediate.extend_solution(static_solution_helper)
        # endregion

        number_of_time_steps = len(time_steps_sens)
        for k in range(0, number_of_time_steps):  # Loop over all time steps
            if k > 0:
                logger.info('starting with time step %d', k)

                # region Update time steps
                delta_t = delta_ts[k - 1]
                static_solution_helper.time = time_steps_sens[k]
                static_solution_helper.potential = solution.potential(time=time_steps_sens[k])
                # endregion

                # region Build lhs
                lhs = static_solution_helper.divgrad_matrix_sigmad + \
                      static_solution_helper.divgrad_matrix_epsd / delta_t
                # endregion

            for param in parameters:  # Loop over all parameters
                # region Select parameter in material properties
                for mat in static_solution_helper.materials:
                    prop: DiffConductivityParameter = mat.get_property(DiffConductivityParameter)
                    prop.parameter_key = param
                    prop: DiffPermittivityParameter = mat.get_property(DiffPermittivityParameter)
                    prop.parameter_key = param
                # endregion

                if k > 0:
                    # region Compute rhs
                    # Compute part of rhs that depends on the current time step
                    rhs = - static_solution_helper.compute_Ksigmap() @ static_solution_helper.potential \
                          - static_solution_helper.compute_Kepsp() @ static_solution_helper.potential / delta_t

                    # Compute part of the rhs that depends on the previous time step
                    static_solution_helper.time = time_steps_sens[k - 1]
                    static_solution_helper.potential = solution.potential(time=time_steps_sens[k - 1])
                    rhs = rhs + \
                          (static_solution_helper.divgrad_matrix_epsd @ sens_potential_prev[param]
                           + static_solution_helper.compute_Kepsp() @ static_solution_helper.potential) \
                          / delta_t
                    rhs = coo_matrix(rhs)
                    if rhs.shape[0] != lhs.shape[0]:
                        rhs = rhs.transpose()

                    # Select current time step again
                    static_solution_helper.time = time_steps_sens[k]
                    static_solution_helper.potential = solution.potential(time=time_steps_sens[k])
                    # endregion

                    # region Shrink, solve, inflate
                    lhs_shrink, rhs_shrink = bdrycond_dsm.shrink(
                        solution.mesh, solution.shape_function, solution.regions, lhs.tocoo(), rhs, 1)

                    sens_pot_shrink, _ = CurrentFlowProblemAxiStatic.solve_linear_system(lhs_shrink.tocsr(),
                                                                                         rhs_shrink.tocsr(),
                                                                                         **kwargs)
                    sens_pot = bdrycond_dsm.inflate(solution.mesh, solution.shape_function,
                                                    solution.regions, sens_pot_shrink)
                    # endregion

                # region Compute sensitivities
                for qoi in qois.get_qois_from_parameter_name(param):
                    q = qoi.evaluate_diff_qoi_dof('potential', [static_solution_helper, time_steps_sens[k]])
                    dgdp = qoi.evaluate_diff_qoi_param(param, [static_solution_helper, time_steps_sens[k]])

                    if k == 0:
                        sensitivities[(qoi.name, param)] = [dgdp + q @ sensitivity_initial_value[param], ]
                    else:
                        sensitivities[(qoi.name, param)].append(dgdp + q @ sens_pot)
                # endregion

                # region Save sensitivity of potential
                if k > 0 and save_sensitivities_potential:
                    if k in solution_monitor:
                        sensitivities_potential[param].append(sens_pot)
                # endregion

                if k > 0:
                    sens_potential_prev[param] = sens_pot

        # region Post-process sensitivities of potential
        if save_sensitivities_potential:
            for name in qois.get_parameter_names():
                sensitivities_potential[name] = np.stack(sensitivities_potential[name])
            sensitivities_potential['time'] = time_steps_solution_monitor
        # endregion

        # Integrate sensitivities
        for key in sensitivities:
            sensitivities[key] = np.trapz(sensitivities[key], time_steps_sens)

        return sensitivities, sensitivities_potential
