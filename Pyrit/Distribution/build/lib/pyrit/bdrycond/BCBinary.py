# -*- coding: utf-8 -*-
"""Contains the class BCBinary

.. sectionauthor:: schaufelberger
"""
from typing import Callable
import numpy as np

from . import BC


def circular_map2d(x: np.ndarray, phase: float = 0) -> np.ndarray:
    """
    Simple map to transform points on a circle to the unit line

    Parameters
    ----------
    x : np.ndarray
        2D points on a circle [n_points,2]
    phase: float
        Constant float that is added before normalisation
    Returns
    -------
    res : np.ndarray
        1D points on a line [0,1] of dimension [n_points,1]
    """
    phi = np.arctan(x[:, 1] / x[:, 0])
    phi += phase

    phi /= (np.pi)

    phi -= np.min(phi)
    phi /= np.max(phi)

    return phi[:, np.newaxis]


def uniform_map2d(x: np.ndarray) -> np.ndarray:
    """
    Very simple map mapping a curve in 2D to the [0,1] line uniformly by ordering in the array

    Parameters
    ----------
    x : np.ndarray
        The point positions of a number of points [n_point,dim]

    Returns
    -------
    res : np.dnarray
        Uniformly spaced points between [0,1] for each given point

    """
    n_points, dim = x.shape

    if dim != 2:
        raise ValueError("Points are not 2D")
    return np.linspace([0], [1], n_points, axis=0)


class BCBinary(BC):
    r"""

    Allow to define Binary BC of the form

    .. math::
        q_1(x)\phi(x)|_{\Gamma_1} + q_2(x)\phi(x)|_{\Gamma_2} = g(x)

    Given two boundaries and respective maps of the boundary to
    the :math:`r_i(x) : \Gamma_i \in R^n \longrightarrow [0,1]^{n-1}`

    :math:`q_1,q_2` are for now given in the BC space and defined on :math:`\Gamma`
    This might change later.
    In order to be able to work with boundaries that are not meshed identically, a
    KDTree is set up from the primary nodes, from the which the secondary nodes are
    interpolated. For that see also the ``_calc_binary_values`` in
    ``NodalShapefunction``.

    Parameters
    ----------
    value : Union[Callable[[Any], Union[ndarray, float]], ndarray, float]
        A function or value that represents the BC
    name : str, optional
        Name of the BC, by default ''
    """

    def __init__(self, value, name: str = ''):

        super().__init__(value, name=name)
        self._primary_boundary: int = None
        self._secondary_boundary: int = None

        # Defined on the Boundary, not on the mapping
        self._primary_transform: Callable[[np.ndarray], np.ndarray] = None
        self._secondary_transform: Callable[[np.ndarray], np.ndarray] = None

        self._bc_to_primary: Callable[[np.ndarray], np.ndarray] = lambda: None
        self._bc_to_secondary: Callable[[np.ndarray], np.ndarray] = lambda: None
        self._dirichlet_shift: Callable[[np.ndarray], np.ndarray] = lambda: None

    @property
    def primary_boundary(self) -> int:
        """
        The primary boundary.

        Returns
        -------
        PhysicalGroup
            The primary boundary.

        Notes
        -----
        The primary boundary is the main boundary used for mapping.
        """
        return self._primary_boundary

    @primary_boundary.setter
    def primary_boundary(self, value: int) -> None:
        """
        Set the primary boundary.

        Parameters
        ----------
        value : int
            The primary boundary as a region ID.

        Notes
        -----
        The primary boundary is the main boundary used for mapping.
        """
        self._primary_boundary = value

    @property
    def secondary_boundary(self) -> int:
        """
        The secondary boundary.

        Returns
        -------
        PhysicalGroup
            The secondary boundary.

        Notes
        -----
        The secondary boundary is the secondary boundary used for mapping.
        """
        return self._secondary_boundary

    @secondary_boundary.setter
    def secondary_boundary(self, value: int) -> None:
        """
        Set the secondary boundary.

        Parameters
        ----------
        value : Int
            The secondary boundary as a region ID.

        Notes
        -----
        The secondary boundary is the secondary boundary used for mapping.
        """
        self._secondary_boundary = value

    @property
    def primary_transform(self) -> Callable[[np.ndarray], np.ndarray]:
        """
        The primary transform.

        Returns
        -------
        callable
            The primary transform.

        Notes
        -----
        The primary transform is the transform used for the primary boundary.
        """
        return self._primary_transform

    @primary_transform.setter
    def primary_transform(self, value: Callable[[np.ndarray], np.ndarray]) -> None:
        """
        Set the primary transform.

        Parameters
        ----------
        value : callable
            The primary transform.

        Raises
        ------
        ValueError
            If the input is not a callable function.

        Notes
        -----
        The primary transform is the transform used for the primary boundary.
        """
        if not callable(value):
            raise ValueError("primary_transform must be a callable function")
        self._primary_transform = value

    @property
    def secondary_transform(self) -> Callable[[np.ndarray], np.ndarray]:
        """
        The secondary transform.

        Returns
        -------
        callable
            The secondary transform.

        Notes
        -----
        The secondary transform is the transform used for the secondary boundary.
        """
        return self._secondary_transform

    @secondary_transform.setter
    def secondary_transform(self, value: Callable[[np.ndarray], np.ndarray]) -> None:
        """
        Set the secondary transform.

        Parameters
        ----------
        value : callable
            The secondary transform.

        Raises
        ------
        ValueError
            If the input is not a callable function.

        Notes
        -----
        The secondary transform is the transform used for the secondary boundary.
        """
        if not callable(value):
            raise ValueError("secondary_transform must be a callable function")
        self._secondary_transform = value

    @property
    def bc_to_primary(self) -> Callable[[np.ndarray], np.ndarray]:
        """
        The BC to primary mapping.

        Returns
        -------
        callable
            The BC to primary mapping.

        Notes
        -----
        The BC to primary mapping is the mapping used for the primary boundary.
        """
        return self._bc_to_primary

    @bc_to_primary.setter
    def bc_to_primary(self, value: Callable[[np.ndarray], np.ndarray]) -> None:
        """
        Set the BC to primary mapping.

        Parameters
        ----------
        value : callable
            The BC to primary mapping.

        Raises
        ------
        ValueError
            If the input is not a callable function.

        Notes
        -----
        The BC to primary mapping is the mapping used for the primary boundary.
        """
        if not callable(value):
            raise ValueError("bc_to_primary must be a callable function")
        self._bc_to_primary = value

    @property
    def bc_to_secondary(self) -> Callable[[np.ndarray], np.ndarray]:
        """
        The BC to secondary mapping.

        Returns
        -------
        callable
            The BC to secondary mapping.

        Notes
        -----
        The BC to secondary mapping is the mapping used for the secondary boundary.
        """
        return self._bc_to_secondary

    @bc_to_secondary.setter
    def bc_to_secondary(self, value: Callable[[np.ndarray], np.ndarray]) -> None:
        """
        Set the BC to secondary mapping.

        Parameters
        ----------
        value : callable
            The BC to secondary mapping.

        Raises
        ------
        ValueError
            If the input is not a callable function.

        Notes
        -----
        The BC to secondary mapping is the mapping used for the secondary boundary.
        """
        if not callable(value):
            raise ValueError("bc_to_secondary must be a callable function")
        self._bc_to_secondary = value

    @property
    def dirichlet_shift(self) -> Callable[[np.ndarray], np.ndarray]:
        """
        The Dirichlet shift.

        Returns
        -------
        callable
            The Dirichlet shift.

        Notes
        -----
        The Dirichlet shift is the shift used for the Dirichlet boundary condition.
        """
        return self._dirichlet_shift

    @dirichlet_shift.setter
    def dirichlet_shift(self, value: Callable[[np.ndarray], np.ndarray]) -> None:
        """
        Set the Dirichlet shift.

        Parameters
        ----------
        value : callable
            The Dirichlet shift.

        Raises
        ------
        ValueError
            If the input is not a callable function.

        Notes
        -----
        The Dirichlet shift is the shift used for the Dirichlet boundary condition.
        """
        if not callable(value):
            raise ValueError("dirichlet_shift must be a callable function")
        self._dirichlet_shift = value
