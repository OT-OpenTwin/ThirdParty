# coding=utf-8
"""Two-dimensional, electrostatic problem.

.. sectionauthor:: Bundschuh
"""

from typing import TYPE_CHECKING, Tuple

import numpy as np
from scipy import sparse

from pyrit import get_logger
from pyrit import mesh, region, material, bdrycond, excitation

from pyrit.solution import ElectricSolutionCartStatic
from pyrit.problem.Problem import StaticProblem
from pyrit.shapefunction import TriCartesianNodalShapeFunction

if TYPE_CHECKING:
    from pyrit.mesh import TriMesh

logger = get_logger(__name__)

__all__ = ['ElectricProblemCartStatic']


class ElectricProblemCartStatic(StaticProblem):
    r"""A two-dimensional, electrostatic problem in Cartesian coordinates:

    The electrostatic problem models capacitive effects, the corresponding differential equation reads

    .. math::
        -\mathrm{div}(\varepsilon \, \mathrm{grad} (\phi)) = \varrho\,,

    where :math:`\varepsilon` is the electric permittivity (see :py:class:`~pyrit.material.Permittivity`), :math:`\phi`
    is the electric scalar potential and :math:`\varrho` is the charge density. A possible application is, for example,
    the electric field caused by a point charge in space.

    The corresponding solution class is :py:class:`~pyrit.problem.solutions.ElectricSolutionCartStatic`.
    """

    problem_identifier = 'Electrostatic problem in 2D Cartesian coordinates'
    associated_solution_class = ElectricSolutionCartStatic

    def __init__(self, description: str, tri_mesh: mesh.TriMesh,
                 regions: region.Regions, materials: material.Materials, boundary_conditions: bdrycond.BdryCond,
                 excitations: excitation.Excitations, length: float = 1):
        """An electrostatic problem in 2D Cartesian coordinates.

        Parameters
        ----------
        description : str
            A description of the problem
        tri_mesh : TriMesh
            A mesh object.
        regions : Regions
            A regions object.
        materials : Materials
            A materials object.
        boundary_conditions : BdryCond
            A boundary conditions object.
        excitations : Excitations
            An excitations object.
        length : float, optional
            The length of the problem. Default is 1
        """
        super().__init__(description, None, None, regions, materials, boundary_conditions, excitations)

        self.length = length
        self.mesh: mesh.TriMesh = tri_mesh
        self.shape_function: TriCartesianNodalShapeFunction = TriCartesianNodalShapeFunction(tri_mesh, length)

        self.consistency_check()

    def get_system(self, **kwargs) -> Tuple[sparse.spmatrix, sparse.spmatrix]:
        integration_order = kwargs.pop("integration_order", 1)
        integration_order_divgrad = kwargs.pop("integration_order_divgrad", integration_order)
        integration_order_load = kwargs.pop("integration_order_load", integration_order)

        divgrad = self.shape_function.divgrad_operator(self.regions, self.materials, material.Permittivity,
                                                       integration_order=integration_order_divgrad)
        load = self.shape_function.load_vector(self.regions, self.excitations, integration_order=integration_order_load)

        return divgrad, load

    def _solve_linear(self, **kwargs) -> ElectricSolutionCartStatic:
        integration_order = kwargs.get("integration_order", 1)
        integration_order_shrink = kwargs.get("integration_order_shrink", integration_order)

        matrix, rhs = self.get_system(**kwargs)

        matrix_shrink, rhs_shrink, _, _, support_data = \
            self.shape_function.shrink(matrix, rhs, self, integration_order=integration_order_shrink)

        a_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(), **kwargs)
        scalar_potential = self.shape_function.inflate(a_shrink, self, support_data)

        solution = self.create_solution(scalar_potential, divgrad=matrix)

        return solution

    def _solve_nonlinear(self, **kwargs) -> ElectricSolutionCartStatic:
        raise NotImplementedError

    # pylint: disable=arguments-renamed
    def create_solution(self, scalar_potential: np.ndarray, description: str = None,
                        **kwargs) -> ElectricSolutionCartStatic:
        if description is None:
            description = self.description

        solution = self.associated_solution_class(description, scalar_potential, self.mesh, self.shape_function,
                                                  self.regions, self.materials, self.excitations)

        solution.divgrad_matrix = kwargs.pop('divgrad', None)

        return solution
