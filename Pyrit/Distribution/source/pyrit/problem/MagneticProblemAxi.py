# coding=utf-8
"""Axisymmetric magnetic problem.

.. sectionauthor:: Bundschuh
"""

from typing import TYPE_CHECKING, Dict, Union, Callable, Any, NoReturn, Iterable, Tuple, List
import numpy as np
from scipy import sparse

from pyrit import get_logger
from pyrit import mesh, region, material, bdrycond, excitation

from pyrit.solution import MagneticSolutionAxiStatic, MagneticSolutionAxiHarmonic, MagneticSolutionAxiTransient
from pyrit.problem.Problem import StaticProblem, HarmonicProblem, TransientProblem, ProblemException
from pyrit.shapefunction import TriAxisymmetricEdgeShapeFunction
if TYPE_CHECKING:
    from pyrit.mesh import AxiMesh

logger = get_logger(__name__)


class MagneticProblemAxiStatic(StaticProblem):
    r"""A static, two-dimensional magnetic problem in axisymmetric coordinates.

    The corresponding differential equations reads:

    .. math::

        \mathrm{rot}(\nu\,\mathrm{rot}\vec{A}) = \vec{J}_{\mathrm{s}}\,,

    where :math:`\nu` is the reluctivity (see :py:class:`~pyrit.material.Reluctivity`), :math:`\vec{A}` is the magnetic
    vector potential and :math:`\vec{J}_\mathrm{s}` is the source current density. This problem can be used, whenever
    the static magnetic field that is caused by a current shall be computed. A very simple example is therefore the
    magnetic field in a coaxial cable caused by a constant current.

    The corresponding solution class is :py:class:`~pyrit.problem.solutions.MagneticSolutionAxiStatic`.
    """

    problem_identifier: str = 'Static, magnetic axisymmetric problem'
    associated_solution_class = MagneticSolutionAxiStatic

    def __init__(self, description: str, axi_mesh: mesh.AxiMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations):
        """A static, magnetic, axisymmetric problem.

        Parameters
        ----------
        description : str
            A description of the problem.
        axi_mesh : AxiMesh
            A mesh object. See :py:class:`pyrit.mesh.AxiMesh`.
        regions : Regions
            A regions object. See :py:mod:`pyrit.regions`.
        materials : Materials
            A materials object. See :py:mod:`pyrit.materials`.
        boundary_conditions : BdryCond
            A boundary conditions object. See :py:mod:`pyrit.bdrycond`.
        excitations : Excitations
            An excitations object. See :py:mod:`pyrit.excitation`.
        """
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations)

        self.mesh: mesh.AxiMesh = axi_mesh
        self.shape_function: TriAxisymmetricEdgeShapeFunction = TriAxisymmetricEdgeShapeFunction(axi_mesh)

        self.consistency_check()

    def get_system(self, **kwargs) -> Tuple[sparse.spmatrix, sparse.spmatrix]:
        integration_order = kwargs.pop("integration_order", 1)
        integration_order_curlcurl = kwargs.pop("integration_order_curlcurl", integration_order)
        integration_order_load = kwargs.pop("integration_order_load", integration_order)

        curlcurl = self.shape_function.curlcurl_operator(self.regions, self.materials, material.Reluctivity,
                                                         integration_order=integration_order_curlcurl)
        load = self.shape_function.load_vector(self.regions, self.excitations, integration_order=integration_order_load)

        return curlcurl, load

    def _solve_linear(self, **kwargs) -> MagneticSolutionAxiStatic:  # pylint: disable=arguments-differ
        """Solve the Problem.

        Parameters
        ----------
        kwargs :
            Are all passed to the function :py:func:`solve_linear_system`.

        Returns
        -------
        solution : MagneticSolutionAxiStatic
            The solution object
        """
        integration_order = kwargs.get("integration_order", 1)
        integration_order_shrink = kwargs.get("integration_order_shrink", integration_order)

        matrix, rhs = self.get_system(**kwargs)

        matrix_shrink, rhs_shrink, _, _, support_data = \
            self.shape_function.shrink(matrix, rhs, self, integration_order=integration_order_shrink)

        a_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(), **kwargs)
        vector_potential = self.shape_function.inflate(a_shrink, self, support_data)

        solution = self.create_solution(vector_potential, curlcurl=matrix)

        return solution

    def _solve_nonlinear(self, **kwargs) -> 'MagneticSolutionAxiStatic':
        raise NotImplementedError()

    # pylint: disable=arguments-renamed
    def create_solution(self, vector_potential: np.ndarray, description: str = None,
                        **kwargs) -> 'MagneticSolutionAxiStatic':
        if description is None:
            description = self.description
        solution = MagneticSolutionAxiStatic(description, vector_potential, self.mesh, self.shape_function,
                                             self.regions, self.materials, self.excitations)
        solution.curlcurl_matrix = kwargs.pop('curlcurl', None)

        return solution


class MagneticProblemAxiHarmonic(HarmonicProblem):
    r"""A harmonic, magnetic problem in two-dimensional axisymmetric coordinates.

    This problem models magnetic fields caused by currents and takes eddy current effects into account.
    The corresponding differential equation is:

    .. math::

        \mathrm{rot}(\nu\,\mathrm{rot}\vec{A}) + j\omega\sigma\vec{A} = \vec{J}_{\mathrm{s}}\,,

    where :math:`\nu` is the Reluctivity (see :py:class:`~pyrit.material.Reluctivity`), :math:`\sigma` is the
    conductivity (see :py:class:`~pyrit.material.Conductivity`), :math:`\vec{A}` is the magnetic vector potential,
    :math:`\vec{J}_\mathrm{s}` is the source current density, and :math:`\omega=2\pi f` is the angular frequency, with
    the frequency :math:`f`.
    Both, the magnetic vector potential and the source current density are complex. The problem can, by definition,
    only handle linear materials.

    The corresponding solution class is :py:class:`~pyrit.problem.solutions.MagneticSolutionAxiHarmonic`.
    """

    problem_identifier: str = 'Harmonic, magnetic axisymmetric problem'
    associated_solution_class = MagneticSolutionAxiHarmonic

    def __init__(self, description: str, axi_mesh: mesh.AxiMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations, frequency: float):
        """A harmonic, magnetic, axisymmetric problem.

        Parameters
        ----------
        description : str
            A description of the problem.
        axi_mesh : AxiMesh
            A mesh object. See :py:class:`pyrit.mesh.AxiMesh`.
        regions : Regions
            A regions object. See :py:mod:`pyrit.regions`.
        materials : Materials
            A materials object. See :py:mod:`pyrit.materials`.
        boundary_conditions : BdryCond
            A boundary conditions object. See :py:mod:`pyrit.bdrycond`.
        excitations : Excitations
            An excitations object. See :py:mod:`pyrit.excitation`.
        frequency : float
            The frequency of the problem.
        """
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations, frequency)

        self.mesh: mesh.AxiMesh = axi_mesh
        self.shape_function: TriAxisymmetricEdgeShapeFunction = TriAxisymmetricEdgeShapeFunction(axi_mesh)

        self.consistency_check()

    def get_system(self, **kwargs) -> Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]:
        integration_order = kwargs.get("integration_order", 1)
        integration_order_curlcurl = kwargs.get("integration_order_curlcurl", integration_order)
        integration_order_mass = kwargs.get("integration_order_mass", integration_order)
        integration_order_load = kwargs.get("integration_order_load", integration_order)

        curlcurl = self.shape_function.curlcurl_operator(self.regions, self.materials, material.Reluctivity,
                                                         integration_order=integration_order_curlcurl)
        mass = self.shape_function.mass_matrix(self.regions, self.materials, material.Conductivity,
                                               integration_order=integration_order_mass)

        load = self.shape_function.load_vector(self.regions, self.excitations, integration_order=integration_order_load)

        return [curlcurl, mass], [load, ]

    def _solve_linear(self, **kwargs) -> 'MagneticSolutionAxiHarmonic':
        integration_order = kwargs.get("integration_order", 1)
        integration_order_shrink = kwargs.get("integration_order_shrink", integration_order)

        matrices, rhs = self.get_system(**kwargs)
        if len(matrices) != 2:
            raise ProblemException(f"The number of matrices is not as expected. It is {len(matrices)} but should be 2")
        if len(rhs) != 1:
            raise ProblemException(f"The number of rhs is not as expected. It is {len(rhs)} but should be 1")

        matrix = matrices[0] + 1j * self.omega * matrices[1]

        matrix_shrink, rhs_shrink, _, _, support_data = \
            self.shape_function.shrink(matrix, rhs[0], self, integration_order=integration_order_shrink)
        a_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(), **kwargs)
        vector_potential = self.shape_function.inflate(a_shrink, self, support_data)

        solution = self.create_solution(vector_potential, curlcurl=matrices[0], mass=matrices[1])
        return solution

    # pylint: disable=arguments-renamed
    def create_solution(self, vector_potential: np.ndarray, description: str = None,
                        **kwargs) -> 'MagneticSolutionAxiHarmonic':
        if description is None:
            description = self.description

        solution = self.associated_solution_class(description, vector_potential, self.mesh, self.shape_function,
                                                  self.regions, self.materials, self.excitations, self.frequency)

        solution.curlcurl_matrix = kwargs.pop('curlcurl', None)
        solution.mass = kwargs.pop('mass', None)

        return solution


class MagneticProblemAxiTransient(TransientProblem):
    r"""A Transient, magnetic problem in two-dimensional axisymmetric coordinates.

    This problem models magnetic fields caused by currents and takes eddy current effects into account.
    The corresponding differential equation is

    .. math::

        \mathrm{rot}(\nu\,\mathrm{rot}\vec{A}) + \sigma\frac{\partial\vec{A}}{\partial t} = \vec{J}_{\mathrm{s}}\,,

    where :math:`\nu` is the Reluctivity (see :py:class:`~pyrit.material.Reluctivity`), :math:`\sigma` is the
    conductivity (see :py:class:`~pyrit.material.Conductivity`), :math:`\vec{A}` is the magnetic vector potential,
    :math:`\vec{J}_\mathrm{s}` is the source current density, and :math:`t` is the time.

    The corresponding solution class is :py:class:`~pyrit.problem.solutions.MagneticSolutionAxiTransient`.
    """

    problem_identifier: str = 'Transient, magnetic axisymmetric problem'
    associated_solution_class = MagneticSolutionAxiHarmonic
    available_monitors: dict = {'energy': '_energy'}

    def __init__(self, description: str, axi_mesh: mesh.AxiMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations, time_steps: np.ndarray):
        """Transient, magnetic, axisymmetric problem.

        Parameters
        ----------
        description : str
            A description of the problem.
        axi_mesh : AxiMesh
            A mesh object. See :py:class:`pyrit.mesh.AxiMesh`.
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
        self.shape_function: TriAxisymmetricEdgeShapeFunction = TriAxisymmetricEdgeShapeFunction(axi_mesh)

        self._curlcurl_time_independent = None
        self._mass_time_independent = None
        self._load_time_independent = None

        self.consistency_check()

    @staticmethod
    def _energy(solution: 'MagneticSolutionAxiStatic'):
        return solution.energy

    Monitor = Union[str, Callable[['MagneticSolutionAxiStatic'], Any]]
    Solution_Monitor = Union[int, Iterable[int]]

    def get_system(self, time, **kwargs) -> Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]:
        integration_order = kwargs.get("integration_order", 1)
        integration_order_curlcurl = kwargs.get("integration_order_curlcurl", integration_order)
        integration_order_mass = kwargs.get("integration_order_mass", integration_order)
        integration_order_load = kwargs.get("integration_order_load", integration_order)

        if self.materials.is_time_dependent(material.Reluctivity):
            self.materials.update('time', time)
            curlcurl = self.shape_function.curlcurl_operator(self.regions, self.materials, material.Reluctivity,
                                                             integration_order=integration_order_curlcurl)
        else:
            if self._curlcurl_time_independent is None:
                self._curlcurl_time_independent = \
                    self.shape_function.curlcurl_operator(self.regions, self.materials, material.Reluctivity,
                                                          integration_order=integration_order_curlcurl)
            curlcurl = self._curlcurl_time_independent

        if self.materials.is_time_dependent(material.Conductivity):
            self.materials.update('time', time)
            mass = self.shape_function.mass_matrix(self.regions, self.materials, material.Conductivity,
                                                   integration_order=integration_order_mass)
        else:
            if self._mass_time_independent is None:
                self._mass_time_independent = self.shape_function.mass_matrix(self.regions, self.materials,
                                                                              material.Conductivity,
                                                                              integration_order=integration_order_mass)
            mass = self._mass_time_independent

        if self.excitations.is_time_dependent:
            self.excitations.update('time', time)
            load = self.shape_function.load_vector(self.regions, self.excitations,
                                                   integration_order=integration_order_load)
        else:
            if self._load_time_independent is None:
                self._load_time_independent = self.shape_function.load_vector(self.regions, self.excitations,
                                                                              integration_order=integration_order_load)
            load = self._load_time_independent

        return [curlcurl, mass], [load, ]

    def _solve_linear(self, **kwargs) -> MagneticSolutionAxiHarmonic:
        pass

    def _solve_nonlinear(self, **kwargs) -> MagneticSolutionAxiHarmonic:
        pass

    def solve(self, start_value: np.ndarray, solution_monitor: Union[int, Iterable[int]] = 1,
              monitors: Dict['str', Union[Monitor, Tuple[Solution_Monitor, Monitor]]] = None,
              callback: Callable[['MagneticSolutionAxiStatic'], NoReturn] = None, **kwargs) -> \
            MagneticSolutionAxiTransient:
        if not isinstance(start_value, np.ndarray):
            raise ValueError(f"The argument start_value is not of the right type. "
                             f"It is '{type(start_value)}' but should be a ndarray")

        if isinstance(solution_monitor, int):
            solution_monitor = np.arange(start=0, stop=len(self.time_steps), step=solution_monitor)
            # solution_monitor = {n for n in range(0, len(self.time_steps), solution_monitor)}
            # if len(self.time_steps)-1 not in solution_monitor:
            #     solution_monitor.add(len(self.time_steps)-1)
            if solution_monitor[-1] != len(self.time_steps) - 1:
                solution_monitor = np.concatenate([solution_monitor, np.array([len(self.time_steps) - 1])])

        time_steps = self.time_steps[solution_monitor]
        delta_ts = np.diff(self.time_steps)

        solution_monitor = set(solution_monitor)

        # Preprocess the monitors so that they have a fixed form
        monitors = self._monitors_preprocessing(monitors)
        monitors_results = {k: [self.time_steps[v[0]], []] for k, v in monitors.items()}

        mass_time_dependent = self.materials.is_time_dependent(material.Conductivity)
        curlcurl_time_dependent = self.materials.is_time_dependent(material.Reluctivity)
        load_time_dependent = self.excitations.is_time_dependent
        boundary_condition_time_dependent = self.boundary_conditions.is_time_dependent

        mass_linear = self.materials.is_linear(material.Conductivity)
        curlcurl_linear = self.materials.is_linear(material.Reluctivity)
        load_linear = self.excitations.is_linear
        boundary_condition_linear = self.boundary_conditions.is_linear

        all_linear = all([mass_linear, curlcurl_linear, load_linear, boundary_condition_linear])

        # Add the start value to the solutions
        if 0 in solution_monitor:
            solutions = [start_value, ]
        else:
            solutions = []

        prev_sol = start_value

        has_callback = callback is not None

        # bool variable that indicates if a static solution is needed or not
        need_static_solution = (not all_linear) or has_callback or len(monitors)

        for k in range(1, len(self.time_steps)):
            logger.info('starting with step %d', k)

            # region Setup time dependence and nonlinearities

            if need_static_solution and k == 1:  # (not all_linear) and (not has_callback or k == 1):
                static_solution = MagneticSolutionAxiStatic(f'temporary static solution generated by solve in '
                                                            f'MagneticProblemAxiTransient at time step {k}',
                                                            prev_sol, self.mesh, self.shape_function, self.regions,
                                                            self.materials, self.excitations)
                static_solution.time = self.time_steps[k - 1]
            else:
                static_solution = None

            if mass_time_dependent:
                self.materials.update('time', self.time_steps[k - 1])
            if not mass_linear:
                self.materials.update('solution', static_solution)
            if (mass_time_dependent or not mass_linear) or k == 1:
                mass = self.shape_function.mass_matrix(self.regions, self.materials, material.Conductivity)

            if curlcurl_time_dependent:
                self.materials.update('time', self.time_steps[k - 1])
            if not curlcurl_linear:
                self.materials.update('solution', static_solution)
            if (curlcurl_time_dependent or not curlcurl_linear) or k == 1:
                curlcurl = self.shape_function.curlcurl_operator(self.regions, self.materials, material.Reluctivity)

            if load_time_dependent:
                self.excitations.update('time', self.time_steps[k - 1])
            if not load_linear:
                self.excitations.update('solution', static_solution)
            if (load_time_dependent or not load_linear) or k == 1:
                load = self.shape_function.load_vector(self.regions, self.excitations)

            if boundary_condition_time_dependent:
                self.boundary_conditions.update('time', self.time_steps[k - 1])
            if not boundary_condition_linear:
                self.boundary_conditions.update('solution', static_solution)

            # endregion

            if k == 1:
                for key, monitor in monitors.items():
                    if k in monitor[0]:
                        monitors_results[key][1].append(monitor[1](static_solution))

            delta_t = delta_ts[k - 1]
            prev_sol = sparse.coo_matrix(prev_sol).transpose()

            # noinspection PyUnboundLocalVariable
            matrix = curlcurl + 1 / delta_t * mass
            # noinspection PyUnboundLocalVariable
            rhs = load + 1 / delta_t * mass @ prev_sol

            matrix_shrink, rhs_shrink, _, _, support_data = self.shape_function.shrink(matrix, rhs, self, 1)
            a_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(), **kwargs)

            prev_sol = self.shape_function.inflate(a_shrink, self, support_data)

            if need_static_solution:
                static_solution = MagneticSolutionAxiStatic(f'temporary static solution generated by solve in '
                                                            f'MagneticProblemAxiTransient at time step {k}',
                                                            prev_sol, self.mesh, self.shape_function, self.regions,
                                                            self.materials, self.excitations)
                static_solution.time = self.time_steps[k]

            if has_callback:
                callback(static_solution)

            for key, monitor in monitors.items():
                if k in monitor[0]:
                    monitors_results[key][1].append(monitor[1](static_solution))

            if k in solution_monitor:
                solutions.append(prev_sol)

        solutions = np.stack(solutions)

        for key, monitor in monitors_results.items():
            monitors_results[key][1] = np.stack(monitors_results[key][1])

        solution = self.create_solution(solutions, time_steps, monitor_solutions=monitors_results)
        return solution

    # pylint: disable=arguments-renamed
    def create_solution(self, vector_potentials: np.ndarray, time_steps: np.ndarray, description: str = None, **kwargs):
        if description is None:
            description = self.description

        monitor_solutions = kwargs.pop("monitor_solutions", None)

        solution = MagneticSolutionAxiTransient(description, vector_potentials, self.mesh, self.shape_function,
                                                self.regions, self.materials, self.excitations, time_steps,
                                                monitor_solutions)
        return solution

    def cleanup(self):
        self._curlcurl_time_independent = None
        self._mass_time_independent = None
        self._load_time_independent = None
