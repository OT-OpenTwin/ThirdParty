# coding=utf-8
# coding=utf-8
"""LineMesh - a 1D mesh

.. sectionauthor:: Bundschuh
"""
import numpy as np
import pyvista as pv

from . import Mesh


class LineMesh(Mesh):
    """A one-dimensional mesh"""

    def __init__(self, node: np.ndarray, elem2node: np.ndarray):
        """Initialize LineMesh

        Parameters
        ----------
        node : np.ndarray
            (N,) array. Every line contains the x-coordinate of a node. N nodes
        elem2node : np.ndarray
            (T,2) array. Every line contains the indices of the nodes that define an element (line). T elements
        """
        super().__init__(node, np.sort(elem2node, axis=1))

        self.__edge_length = None
        self.__node2elem = None

    @property
    def elem_length(self):
        """Length ov every element"""
        if self.__edge_length is None:
            self.__edge_length = self._calc_elem_length()
        return self.__edge_length

    def _calc_elem_length(self):
        """Calculate the length of all elements"""
        return np.abs(self.node[self.elem2node[:, 1]] - self.node[self.elem2node[:, 0]])

    @property
    def bound2regi(self):
        return self.node2regi

    @property
    def bound2node(self):
        return self.node

    @property
    def node2elem(self):
        """Returns the node-to-element relation"""
        if self.__node2elem is None:
            self.__node2elem = self.calc_node2elem(self.elem2node, self.num_node)
        return self.__node2elem

    def find_elemidx(self, coordinates: np.ndarray) -> np.ndarray:
        elem_indices = []
        for coordinate in coordinates:
            index_nearest_node = np.argmin(np.abs(self.node - coordinate))
            indices_nearest_elements = self.node2elem[index_nearest_node]

            boundaries_first_element = self.elem2node[indices_nearest_elements[0]]
            if boundaries_first_element[0] <= coordinate <= boundaries_first_element[1]:
                elem_indices.append(indices_nearest_elements[0])
            else:
                elem_indices.append(indices_nearest_elements[1])
        return np.array(elem_indices)

    def find_nodeidx(self, coordinates: np.ndarray) -> np.ndarray:
        node_indices = []
        for coordinate in coordinates:
            node_indices.append(np.argmin(np.abs(self.node - coordinate)))

        return np.array(node_indices)

    def boundary_elements(self) -> np.ndarray:
        return np.array([0, self.num_node - 1])

    def plot(self, plotter: pv.Plotter = None, **kwargs) -> pv.Plotter:
        """Plot the line mesh

        Parameters
        ----------
        plotter : pyvista.Plotter, optional
            Plotter object. If no plotter is given, a new one is created.
        kwargs : Any
            Parameters for the plotting `plotter.add_mesh`

        Returns
        -------
        plotter : pyvista.Plotter
            The plotter object.
        """
        kwargs.setdefault("show_vertices", True)
        kwargs.setdefault("color", 'blue')

        nodes = np.vstack([self.node, np.zeros_like(self.node), np.zeros_like(self.node)]).T
        lines = np.hstack([2 * np.ones((self.num_elem, 1), dtype=int), self.elem2node])
        mesh = pv.PolyData(nodes, lines=lines)

        if plotter is None:
            plotter = pv.Plotter()
            plotter.show_grid()
            plotter.add_axes()
            plotter.view_xy()
        plotter.add_mesh(mesh, **kwargs)

        return plotter
