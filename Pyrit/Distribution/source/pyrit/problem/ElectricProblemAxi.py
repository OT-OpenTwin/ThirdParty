# coding=utf-8
"""Electric problems in axisymmetric coordinates

.. sectionauthor:: Bundschuh
"""
from typing import Tuple

import numpy as np
from scipy import sparse

from pyrit.solution import ElectricSolutionAxiStatic
from pyrit import mesh, region, material, bdrycond, excitation

from pyrit.problem.Problem import StaticProblem
from pyrit.shapefunction import TriAxisymmetricNodalShapeFunction


class ElectricProblemAxiStatic(StaticProblem):
    r"""An electrostatic problem in axisymmetric coordinates:

    The electrostatic problem models capacitive effects, the corresponding differential equation reads

    .. math::
        -\mathrm{div}(\varepsilon \, \mathrm{grad} (\phi)) = \varrho,

    where :math:`\varepsilon` is the electric permittivity (see :py:class:`Permittivity`), :math:`\phi` is the \
    electric scalar potential and :math:`\varrho` is the charge density. A possible application is, for example, the \
    electric field caused by a point charge in space.
    """

    problem_identifier: str = 'Electrostatic problem in axisymmetric coordinates'
    associated_solution_class = ElectricSolutionAxiStatic

    def __init__(self, description: str, axi_mesh: mesh.AxiMesh, regions: region.Regions, materials: material.Materials,
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
        self.shape_function: TriAxisymmetricNodalShapeFunction = TriAxisymmetricNodalShapeFunction(axi_mesh)

        self.consistency_check()

    def get_system(self, **kwargs) -> Tuple[sparse.spmatrix, sparse.spmatrix]:
        integration_order = kwargs.pop("integration_order", 1)
        integration_order_divgrad = kwargs.pop("integration_order_divgrad", integration_order)
        integration_order_load = kwargs.pop("integration_order_load", integration_order)

        divgrad = self.shape_function.divgrad_operator(self.regions, self.materials, material.Permittivity,
                                                        integration_order=integration_order_divgrad)
        load = self.shape_function.load_vector(self.regions, self.excitations, integration_order=integration_order_load)

        return divgrad, load

    def _solve_linear(self, **kwargs) -> ElectricSolutionAxiStatic:
        integration_order = kwargs.get("integration_order", 1)
        integration_order_shrink = kwargs.get("integration_order_shrink", integration_order)

        matrix, rhs = self.get_system(**kwargs)

        matrix_shrink, rhs_shrink, _, _, support_data = \
            self.shape_function.shrink(matrix, rhs, self, integration_order=integration_order_shrink)

        a_shrink, _ = type(self).solve_linear_system(matrix_shrink.tocsr(), rhs_shrink.tocsr(), **kwargs)
        scalar_potential = self.shape_function.inflate(a_shrink, self, support_data)

        solution = self.create_solution(scalar_potential, divgrad=matrix)

        return solution

    def _solve_nonlinear(self, **kwargs) -> ElectricSolutionAxiStatic:
        raise NotImplementedError

    # pylint: disable=arguments-renamed
    def create_solution(self, scalar_potential: np.ndarray, description: str = None,
                        **kwargs) -> ElectricSolutionAxiStatic:
        if description is None:
            description = self.description

        solution = self.associated_solution_class(description, scalar_potential, self.mesh, self.shape_function,
                                                  self.regions, self.materials, self.excitations)

        solution.divgrad_matrix = kwargs.pop('divgrad', None)

        return solution
