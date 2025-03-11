# coding=utf-8
"""The class ModifiedLobattoShapeFunction

.. sectionauthor:: Lögl
"""

from abc import ABC

import numpy as np

from pyrit.mesh import LineMesh
from pyrit.shapefunction import SpectralShapeFunction
from pyrit.toolbox import QuadratureToolbox


def evaluate_modified_lobatto_polynomial_deriv(evaluation_nodes: np.array, max_degree: int):
    """
    Evaluates the modified Legendre polynomials of order 0,...,max_degree at the given evaluation nodes.

    Parameters
    ----------
    evaluation_nodes : np.ndarray
        nodes at which the modified Lobatto polynomial shall be evaluated (coordinates)
    max_degree : int
        maximal degree of the polynomials to be evaluated
    Returns
    -------
    out : np.ndarray
        matrix where the entry in the i-th row in the j-th column corresponds to the derivative of the modified
        Lobatto polynomial of order j evaluated at the i-th node
    """
    num_node = len(evaluation_nodes)

    modified_lobatto_shape_function_deriv = np.zeros((num_node, max_degree + 1))
    evaluation_nodes.clip(min=-1, max=1)

    # interior modes
    legendre_evaluation = QuadratureToolbox.legendre_eval(max_degree - 1, evaluation_nodes)[0][:, 1:]

    modified_lobatto_shape_function_deriv[:, 1:max_degree] = ((np.arange(start=2, stop=max_degree + 1) *
                                                               (np.arange(start=2, stop=max_degree + 1) - 1) / 4) *
                                                              legendre_evaluation)

    # boundary modes
    modified_lobatto_shape_function_deriv[:, 0] -= 1 / 2
    modified_lobatto_shape_function_deriv[:, max_degree] += 1 / 2
    return modified_lobatto_shape_function_deriv


def evaluate_modified_lobatto_polynomial(evaluation_nodes: np.ndarray, max_degree: int) -> np.ndarray:
    """
    Evaluates the modified Lobatto polynomials of order 0,...,max_degree at the given evaluation nodes.

    Parameters
    ----------
    evaluation_nodes : np.ndarray
        nodes at which the modified Lobatto polynomial shall be evaluated (coordinates)
    max_degree : int
        maximal degree of the polynomials to be evaluated
    Returns
    -------
    out : np.ndarray
        matrix where the entry in the i-th row in the j-th column corresponds to the modified Lobatto polynomial of
        order j evaluated at the i-th node
    """
    num_node = len(evaluation_nodes)

    modified_lobatto_shape_function = np.zeros((num_node, max_degree + 1))
    evaluation_nodes.clip(min=-1, max=1)
    # interior modes
    legendre_values = QuadratureToolbox.legendre_eval(max_degree - 1, evaluation_nodes)[1][:, 1:max_degree]
    modified_lobatto_shape_function[:, 1:max_degree] = (((1 - evaluation_nodes ** 2) / 4)[:, np.newaxis] *
                                                        legendre_values)

    # boundary modes
    modified_lobatto_shape_function[:, 0] = (1 - evaluation_nodes) / 2
    modified_lobatto_shape_function[:, max_degree] = (1 + evaluation_nodes) / 2
    return modified_lobatto_shape_function


class ModifiedLobattoShapeFt(SpectralShapeFunction, ABC):
    """Class representing a modified Lobatto polynomial shape function for usage in a 1D spectral element method."""

    def __init__(self, mesh: 'LineMesh', order: int):
        """
        Constructor for the modified Lobatto polynomial shape function.

        Parameters
        ----------
        mesh : LineMesh
            The 1D line mesh object.
        order : order
        """
        super().__init__(mesh)
        self._mesh = mesh
        self._order = order
        self._number_of_nodes = mesh.num_node
        self._number_of_elements = self._number_of_nodes - 1

        self.__calc_legendre_gauss_lobatto_quadrature_rule()
        self.__calc_mapping_coefficients()
        self.__calc_vandermonde_matrix()
        self.__calc_reference_shape_function()

    @property
    def mesh(self) -> 'LineMesh':
        """Returns the mesh."""
        return self._mesh

    def __calc_legendre_gauss_lobatto_quadrature_rule(self):
        """Calculates the Legendre-Gauss-Lobatto quadrature nodes and weights."""
        (lgl_nodes, lgl_weights) = QuadratureToolbox.legendre_gauss_lobatto(self._number_of_nodes)
        self._lgl_nodes = lgl_nodes
        self._lgl_weights = lgl_weights

    def __calc_mapping_coefficients(self):
        """Calculates the mapping coefficients."""
        self._coefficients_a = (self.mesh.node[0:-2] + self.mesh.node[1:-1]) / 2
        self._coefficients_b = (self.mesh.node[1:-1] - self.mesh.node[0:-2]) / 2

    def __calc_vandermonde_matrix(self):
        """Calculates the Vandermonde matrix."""
        self._vandermonde = evaluate_modified_lobatto_polynomial(self._lgl_nodes, self._order)
        self._derivative_vandermonde = evaluate_modified_lobatto_polynomial_deriv(self._lgl_nodes, self._order)

    def __calc_reference_shape_function(self):
        """Computes the reference shape function, i.e. the modified Lobatto shape function on the interval [-1,1]."""
        if self.mesh.node[0] == -1 and self.mesh.node[1] == 1:
            self._reference_shape_function = self
        else:
            self._reference_shape_function = ModifiedLobattoShapeFt(LineMesh(np.array([-1, 1]), np.array([[0, 1]])),
                                                                    self._order)
