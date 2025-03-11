# coding=utf-8
"""Two-dimensional magnetic problem.

.. sectionauthor:: Bundschuh
"""

from typing import TYPE_CHECKING, Tuple, List
import numpy as np
from scipy import sparse

from pyrit import get_logger
from pyrit import mesh, region, material, bdrycond, excitation

from pyrit.solution import MagneticSolutionCartStatic, MagneticSolutionCartHarmonic, MagneticSolutionCartTransient
from pyrit.problem.Problem import StaticProblem, HarmonicProblem, TransientProblem, ProblemException
from pyrit.shapefunction import TriCartesianEdgeShapeFunction

if TYPE_CHECKING:
    from pyrit.mesh import TriMesh

logger = get_logger(__name__)

__all__ = ['MagneticProblemCartStatic', 'MagneticProblemCartHarmonic', 'MagneticProblemCartTransient']


class MagneticProblemCartStatic(StaticProblem):
    r"""A static, two-dimensional magnetic problem in Cartesian coordinates.

    The corresponding differential equations reads:

    .. math::

        \mathrm{rot}(\nu\,\mathrm{rot}\vec{A}) = \vec{J}_{\mathrm{s}}\,,

    where :math:`\nu` is the reluctivity (see :py:class:`~pyrit.material.Reluctivity`), :math:`\vec{A}` is the magnetic
    vector potential and :math:`\vec{J}_\mathrm{s}` is the source current density. This problem can be used, whenever
    the static magnetic field that is caused by a current shall be computed. A very simple example is therefore the
    magnetic field in a coaxial cable caused by a constant current.

    The corresponding solution class is :py:class:`~pyrit.problem.solutions.MagneticSolutionCartStatic`.
    """

    problem_identifier = 'Magnetic 2D problem'
    associated_solution_class = MagneticSolutionCartStatic

    def __init__(self, description: str, tri_mesh: mesh.TriMesh, regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations, length: float = 1):
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
            A boundary conditions object. See :py:mod:`pyrit.bdrycond`
        excitations : Excitations
            An excitations object. See :py:mod:`pyrit.excitation`
        length : float, optional
            The length of the problem. Default is 1
        """
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations)

        self.length = length
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianEdgeShapeFunction = TriCartesianEdgeShapeFunction(tri_mesh, length)

        self.consistency_check()

    def get_system(self, **kwargs) -> Tuple[sparse.spmatrix, sparse.spmatrix]:
        integration_order = kwargs.pop("integration_order", 1)
        integration_order_curlcurl = kwargs.pop("integration_order_curlcurl", integration_order)
        integration_order_load = kwargs.pop("integration_order_load", integration_order)

        curlcurl = self.shape_function.curlcurl_operator(self.regions, self.materials, material.Reluctivity,
                                                         integration_order=integration_order_curlcurl)
        load = self.shape_function.load_vector(self.regions, self.excitations, integration_order=integration_order_load)

        return curlcurl, load

    def _solve_linear(self, **kwargs) -> MagneticSolutionCartStatic:
        matrix, rhs = self.get_system(**kwargs)

        matrix_shrink, rhs_shrink, _, _, support_data = self.shape_function.shrink(matrix, rhs, self, 1)

        a_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(), **kwargs)
        vector_potential = self.shape_function.inflate(a_shrink, self, support_data)

        solution = self.create_solution(vector_potential, curlcurl=matrix)

        return solution

    def _solve_nonlinear(self, **kwargs) -> MagneticSolutionCartStatic:
        raise NotImplementedError()

    # pylint: disable=arguments-renamed
    def create_solution(self, vector_potential: np.ndarray, description: str = None,
                        **kwargs) -> MagneticSolutionCartStatic:
        if description is None:
            description = self.description
        solution = MagneticSolutionCartStatic(description, vector_potential, self.mesh, self.shape_function,
                                              self.regions, self.materials, self.excitations)
        solution.curlcurl_matrix = kwargs.pop('curlcurl', None)

        return solution


class MagneticProblemCartHarmonic(HarmonicProblem):
    r"""A harmonic, magnetic problem in two-dimensional Cartesian coordinates.

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

    The corresponding solution class is :py:class:`~pyrit.problem.solutions.MagneticSolutionCartHarmonic`.
    """

    problem_identifier: str = "Harmonic, magnetic problem in two-dimensional Cartesian coordinates"
    associated_solution_class = MagneticSolutionCartHarmonic

    def __init__(self, description: str, tri_mesh: mesh.TriMesh, regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations, frequency: float,
                 length: float = 1):
        """A harmonic, magnetic, cartesian problem.

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
        frequency : float
            The frequency of the problem.
        length : float, optional
            The length of the problem. Default is 1
        """
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations, frequency)

        self.length = length
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianEdgeShapeFunction = TriCartesianEdgeShapeFunction(tri_mesh, length=length)

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

    def _solve_linear(self, **kwargs) -> 'MagneticSolutionCartHarmonic':
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
                        **kwargs) -> 'MagneticSolutionCartHarmonic':
        if description is None:
            description = self.description

        solution = self.associated_solution_class(description, vector_potential, self.mesh, self.shape_function,
                                                  self.regions, self.materials, self.excitations, self.frequency)

        solution.curlcurl_matrix = kwargs.pop('curlcurl', None)
        solution.mass = kwargs.pop('mass', None)

        return solution


class MagneticProblemCartTransient(TransientProblem):
    r"""A Transient, magnetic problem in two-dimensional Cartesian coordinates.

    This problem models magnetic fields caused by currents and takes eddy current effects into account.
    The corresponding differential equation is

    .. math::

        \mathrm{rot}(\nu\,\mathrm{rot}\vec{A}) + \sigma\frac{\partial\vec{A}}{\partial t} = \vec{J}_{\mathrm{s}}\,,

    where :math:`\nu` is the Reluctivity (see :py:class:`~pyrit.material.Reluctivity`), :math:`\sigma` is the
    conductivity (see :py:class:`~pyrit.material.Conductivity`), :math:`\vec{A}` is the magnetic vector potential,
    :math:`\vec{J}_\mathrm{s}` is the source current density, and :math:`t` is the time.

    The corresponding solution class is :py:class:`~pyrit.problem.solutions.MagneticSolutionCartTransient`.
    """

    problem_identifier: str = "Transient, magnetic problem in two-dimensional Cartesian coordinates"
    associated_solution_class = MagneticSolutionCartTransient

    def __init__(self, description: str, tri_mesh: mesh.TriMesh,
                 regions: region.Regions, materials: material.Materials,
                 boundary_conditions: bdrycond.BdryCond, excitations: excitation.Excitations, time_steps: np.ndarray,
                 length: float = 1):
        """Transient, magnetic, axisymmetric problem.

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
        """
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations, time_steps)

        self.length = length
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianEdgeShapeFunction = TriCartesianEdgeShapeFunction(tri_mesh)

        self._curlcurl_time_independent = None
        self._mass_time_independent = None
        self._load_time_independent = None

        self.consistency_check()

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

    def _solve_linear(self, **kwargs) -> MagneticSolutionCartTransient:
        raise NotImplementedError

    def _solve_nonlinear(self, **kwargs) -> MagneticSolutionCartTransient:
        raise NotImplementedError

    # pylint: disable=arguments-renamed
    def create_solution(self, vector_potentials: np.ndarray, time_steps: np.ndarray, description: str = None,
                        **kwargs):
        if description is None:
            description = self.description

        monitor_solutions = kwargs.pop("monitor_solutions", None)

        solution = MagneticSolutionCartTransient(description, vector_potentials, self.mesh, self.shape_function,
                                                 self.regions, self.materials, self.excitations, time_steps,
                                                 monitor_solutions)
        return solution
