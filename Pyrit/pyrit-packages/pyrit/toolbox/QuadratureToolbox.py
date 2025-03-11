# coding=utf-8
"""
Quadrature Toolbox

.. sectionauthor:: bundschuh, menzenbach
"""
# pylint: disable=unspecified-encoding

import pathlib
import json
from typing import Tuple
import numpy as np
import scipy as sp

file_directory = pathlib.Path(__file__).parent


def gauss(order: int, left: float = 0, right: float = 1) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Returns weights and points for Gauss-Legendre quadrature on the interval [left,right].

    Parameters
    ----------
    order : int
        The order of the quadrature rule.
    left : float, optional
        Left border of the interval. Default is 0
    right : float, optional
        Right border of the interval. Default is 1

    Returns
    -------
    weights : np.ndarray
        (N,) array. The weights of the quadrature rule.
    points : np.ndarray
        (N,) array. The points of the quadrature rule.

    Notes
    -----
    The weights :math:`w_i` and points :math:`x_i` are used as follows:
    :math:`\int_a^b f(x) dx \approx \sum_{i=1}{N} w_i f(x_i)`
    """
    if left >= right:
        raise ValueError("The left border has to be smaller than the right border.")

    try:
        p, w = np.polynomial.legendre.leggauss(order)
    except ValueError as ve:
        raise ValueError(f"Order is {order}, but has to be a positive integer.") from ve
    except TypeError as te:
        raise TypeError(f"Order is {order}, but has to be a positive integer.") from te

    weights = (right - left) / 2 * w
    points = (right - left) / 2 * p + (left + right) / 2

    return weights, points


def gauss_triangle(p: int) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Returns weights and local coordinates in reference triangle (spanned by (0,0), (0,1), (1,0)).

    Parameters
    ----------
    p : int
        Degree of the approximation.

    Returns
    -------
    weights : np.ndarray
        (N,) array with N weights
    local_cds : np.ndarray
        (N,2) array with N points in reference triangle and 2 coordinates (x and y) for each point

    Raises
    ------
    ValueError
        If the parameter p has the wrong type or is not available.

    Notes
    -----
    With T being the reference triangle, the weights :math:`w_i` and coordinates :math:`x_i` and :math:`y_i` are used as
    follows: :math:`\int_T f(x,y) dA \approx \sum_{i=1}^{N} w_i f(x_i,y_i)`.

    Points and weights from https://www.math.unipd.it/~alvise/SETS_CUBATURE_TRIANGLE/rules_triangle.html
    """
    if not isinstance(p, int):
        raise ValueError("Order has to be an integer.")
    if not 1 <= p <= 20:
        raise ValueError(f"The order '{p}' is not available.")
    with open(file_directory.joinpath('schemes/dunavant_all.json'), 'r') as f:
        data = json.load(f)

    data = data[f'{p}']

    return np.atleast_1d(np.array(data['weights'])), np.atleast_2d(np.array(data['points']))


def gauss_tetrahedron(p: int) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Returns weights and local coordinates in reference tetrahedron (spanned by (0,0,0), (1,0,0), (0,1,0), (0,0,1)).

    Parameters
    ----------
    p : int
        Degree of the approximation.

    Returns
    -------
    weights : np.ndarray
        (N,) array with N weights
    points : np.ndarray
        (N,3) array with N points in reference tetrahedron and 3 coordinates (x, y and z) for each point

    Raises
    ------
    ValueError
        If the parameter p has the wrong type or is not available.

    Notes
    -----
    With T being the reference tetrahedron, the weights :math:`w_i` and coordinates :math:`x_i`, :math:`y_i` and
    :math:`z_i` are used as follows:

    .. :math:
        \int_T f(x, y, z) dV \approx \sum_{i=1}{N} w_i f(x_i, y_i, z_i)\,.

    Points and weights from https://onlinelibrary.wiley.com/doi/abs/10.1002/nme.6313
    """
    if not isinstance(p, int):
        raise ValueError("Order has to be an integer.")
    if not 1 <= p <= 20:
        raise ValueError(f"The order '{p}' is not available.")
    with open(file_directory.joinpath('schemes/jaskowiec_sukumar_all.json'), 'r') as f:
        data = json.load(f)

    data = data[f'{p}']

    return np.atleast_1d(np.array(data['weights'])), np.atleast_2d(np.array(data['points']))


def legendre_gauss_lobatto(number_nodes: int, tolerance: float = 1e-12) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Returns the Legendre-Gauss-Lobatto quadrature nodes and quadrature weights for a given number of nodes N.

    To this end, this function uses the Newton method following [1] and as initial guess an approximation given by [2].

    [1] : J. Shen, T. Tang, L. Wang: "Spectral Methods : Algorithms, Analysis and Applications." Springer-Verlag: 2011,
          p. 98-100.
    [2] : F. Lether: "On the construction of Gauss-Legendre quadrature rules." In: J. Comp. Appl. Math., vol. 42, no. 1,
         1978. p. 47-52.

    Parameters
    ----------
    number_nodes : int
        number of nodes
    tolerance : float
        tolerance for the Newton method (optional, default: 1e-12)

    Returns
    -------
    nodes : np.ndarray
        (N,) array with N quadrature nodes
    weights : np.ndarray
        (N,) array with N quadrature weights
    """
    # A: Calculate an initial guess
    k = np.arange(1, number_nodes + 1)
    theta = (4 * k - 1) * np.pi / (4 * number_nodes + 2)
    sigma = (1 - (number_nodes - 1) / (8 * number_nodes ** 3) - 1 / (384 * number_nodes ** 4)
             * (39 - 28 / np.sin(theta) ** 2)) * np.cos(theta)
    x_0 = (sigma[0:number_nodes - 1] + sigma[1:number_nodes]) / 2  # initial guess

    # B: Use Newton method to compute interior quadrature nodes
    x_diff = np.inf
    x_prev = x_0
    count = 0
    max_iterations = 100
    while (x_diff > tolerance) and (count < max_iterations):
        legendre_evaluation = legendre_eval(max_degree=number_nodes + 1, nodes=x_prev)[0][:, number_nodes - 1:]
        legendre = legendre_evaluation[:, 1]
        legendre_eval_prime = (number_nodes * (number_nodes + 1) / (2 * number_nodes + 1) *
                               (legendre_evaluation[:, 0] - legendre_evaluation[:, 2]) / (1 - x_prev ** 2))
        diff = ((1 - x_prev ** 2) * legendre_eval_prime /
                (2 * x_prev * legendre_eval_prime - number_nodes * (number_nodes + 1) * legendre))
        x_next = x_prev - diff
        x_diff = np.abs(np.linalg.norm(x_next - x_prev))
        x_prev = x_next
        count += 1
    nodes = np.sort(np.concatenate(([-1], x_prev, [1])))

    # C: Compute corresponding quadrature weights
    legendre_eval_nodes = legendre_eval(max_degree=number_nodes, nodes=nodes)[0][:, -1]
    weights = 2 / (number_nodes * (number_nodes + 1)) / legendre_eval_nodes ** 2
    return nodes, weights


def legendre_eval(max_degree: int, nodes: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Evaluates the legendre polynomials of degree 0 up to max_degree at the given nodes.

    Returns two arrays of size nodes x max_degree+1 containing the legendre polynomials
    and its derivatives.

    Parameters
    ----------
    max_degree : int
        up to max_degree the polynomial will be evaluated
    nodes : np.ndarray
        evluation nodes

    Returns
    -------
    legendre_evaluation: np.ndarray
        Values for all orders 0..maxdegree
    legendre_d_evaluation: np.ndarray
        Derivatives for all orders 0..maxdegree
    """
    legendre_evaluations, legendre_d_evaluations = [], []
    for node in nodes:
        legendre_evaluation, legendre_d_evaluation = sp.special.lpmn(m=0, n=max_degree, z=node)
        legendre_evaluations.append(legendre_evaluation)
        legendre_d_evaluations.append(legendre_d_evaluation)
    return np.vstack(legendre_evaluations), np.vstack(legendre_d_evaluations)
