# coding=utf-8
import numpy as np
from dataclasses import dataclass
from scipy.constants import mu_0
import gmsh

from pyrit.geometry import Geometry
from pyrit.bdrycond import BCDirichlet, BdryCond
from pyrit.material import Mat, Materials, Reluctivity
from pyrit.excitation import Excitations, CurrentDensity
from pyrit.problem import MagneticProblemCartStatic
from pyrit.solution import MagneticSolutionCartStatic
from pyrit.toolbox.IOToolbox import ToParaview



@dataclass
class WireProblem:
    """Class representing the wire problem.

    The geometry is a wire with radius r_1, enclosed within a cylindrical, non-conducting insulating shell with inner
    radius r_1 and outer radius r_2. The outer surface of the insulation shell is considered as a perfect electric
    conductor. The depth of the wire can be given.
    """

    r_1: float = 2e-3  #: inner radius (wire) [m]
    r_2: float = 3.5e-3  #: outer radius (shell) [m]
    depth: float = 300e-3  #: Depth of wire (lz) [m]
    model_name: str = "coaxial wire"  #: model name

    mu_shell: float = 5 * mu_0  #: permeability of shell [H/m]
    mu_wire: float = mu_0  #: permeability of wire [H/m]
    current: float = 16.  #: applied current [A]

    region_wire: int = 2  #: Region ID of the wire
    region_shell: int = 3  #: Region ID of the shell

    @property
    def current_density(self):
        """Current density in [A/m^2]"""
        return self.current / (np.pi * self.r_1 ** 2)

    def create_problem(self, mesh_size: float = 0.2, refinement_steps: int = 0, show_gui: bool = False):
        """Create the Problem instance

        Parameters
        ----------
        mesh_size : float, optional
            The global mesh size factor for gmsh. Default is 0.2
        refinement_steps : int, optional
            The number of mesh refinement steps. Default is 0
        show_gui : bool, optional
            Boolean that indicates if the gmsh gui should be opened after geometry creation or not. Default is False

        Returns
        -------
        problem : Problems.MagneticProblem2D
            A problem instance
        """
        geo = Geometry(self.model_name, show_gui=show_gui, mesh_size_factor=mesh_size)
        materials = Materials(mat_shell := Mat('shell', Reluctivity(1 / self.mu_shell)),
                              mat_wire := Mat('wire', Reluctivity(1 / self.mu_wire)))
        boundary_conditions = BdryCond(bc := BCDirichlet(0))
        excitations = Excitations(exci := CurrentDensity(self.current_density))

        outer_bound = geo.create_physical_group(1, 1, 'outer_bound')
        wire = geo.create_physical_group(self.region_wire, 2, 'wire')
        shell = geo.create_physical_group(self.region_shell, 2, 'shell')

        geo.add_material_to_physical_group(mat_shell, shell)
        geo.add_material_to_physical_group(mat_wire, wire)
        geo.add_boundary_condition_to_physical_group(bc, outer_bound)
        geo.add_excitation_to_physical_group(exci, wire)

        with geo:
            inner_disc = gmsh.model.occ.addDisk(0, 0, 0, self.r_1, self.r_1)
            outer_disc = gmsh.model.occ.addDisk(0, 0, 0, self.r_2, self.r_2)

            gmsh.model.occ.cut([[2, outer_disc]], [[2, inner_disc]], removeTool=False)

            outer_bound.add_entity(2)
            wire.add_entity(1)
            shell.add_entity(2)

            geo.create_mesh(dim=2)
            for _ in range(refinement_steps):
                geo.refine_mesh()
            mesh = geo.get_mesh(dim=2)
            regions = geo.get_regions()

        prb = MagneticProblemCartStatic(self.model_name, mesh, regions, materials,
                                        boundary_conditions, excitations, self.depth)

        return prb


def export(path, solution: MagneticSolutionCartStatic):
    exporter = ToParaview()

    reluctivity_per_element = np.zeros(solution.mesh.num_elem)
    for element in range(solution.mesh.num_elem):
        region_per_element = solution.mesh.elem2regi[element]
        material_id = solution.regions.get_regi(region_per_element).mat
        reluctivity = solution.materials.get_material(material_id).get_property(Reluctivity)
        reluctivity_per_element[element] = reluctivity.value

    node_wise_data = {"vector_potential": solution.vector_potential_field_values,}
    element_wise_data = {"flux_density": solution.b_field,
                         "magnetic_field": solution.h_field,
                         "energy_density": solution.energy_density,
                         "region IDs": solution.mesh.elem2regi,
                         "reluctivity": reluctivity_per_element}

    return exporter.save_tri_mesh(path, solution.mesh, node_wise_data, element_wise_data)

def main():
    wire_problem = WireProblem()

    problem: MagneticProblemCartStatic = wire_problem.create_problem()

    solution: MagneticSolutionCartStatic = problem.solve()

    export("result", solution)


if __name__ == '__main__':
    main()
