# coding=utf-8
"""
===========================================
Shape function (:mod:`pyrit.shapefunction`)
===========================================

.. currentmodule:: pyrit.shapefunction

This package provides the core of the FE method, i.e. the different shape functions. There is one class per FE shape
function and dimension of the domain. For example, there is a class for nodal shape functions in axisymmetric
coordinates or a class for edge shape functions in two dimensional Cartesian coordinates. These classes implement the
routines to compute the FE matrices.

Finite element shape function classes
-------------------------------------

.. autosummary::
    :toctree: autosummary/

    TriCartesianNodalShapeFunction
    TriCartesianEdgeShapeFunction
    TriAxisymmetricNodalShapeFunction
    TriAxisymmetricEdgeShapeFunction
    TetCartesianNodalShapeFunction

Spectral shape function classes
-------------------------------------

.. autosummary::
    :toctree: autosummary/

    PolynomialShapeFunction

Abstract class
--------------

.. autosummary::
    :toctree: autosummary/

    ShapeFunction
    NodalShapeFunction
    EdgeShapeFunction
    SpectralShapeFunction

Data types
----------

.. autofunction:: Number

    .. autoattribute:: Number.__supertype__

.. autofunction:: AssemblyGenerator

    .. autoattribute:: AssemblyGenerator.__supertype__

.. autofunction:: NumericalData

    .. autoattribute:: NumericalData.__supertype__

.. autofunction:: MaterialData

    .. autoattribute:: MaterialData.__supertype__

.. autofunction:: BoundaryData

    .. autoattribute:: BoundaryData.__supertype__

.. autofunction:: ExcitationData

    .. autoattribute:: ExcitationData.__supertype__

"""

from .ShapeFunction import ShapeFunction
from .ShapeFunction import Number, AssemblyGenerator, NumericalData, MaterialData, BoundaryData, ExcitationData
from .NodalShapeFunction import NodalShapeFunction
from .EdgeShapeFunction import EdgeShapeFunction
from .TriCartesianNodalShapeFunction import TriCartesianNodalShapeFunction
from .TriAxisymmetricNodalShapeFunction import TriAxisymmetricNodalShapeFunction
from .TriAxisymmetricEdgeShapeFunction import TriAxisymmetricEdgeShapeFunction
from .TetCartesianNodalShapeFunction import TetCartesianNodalShapeFunction
from .TriCartesianEdgeShapeFunction import TriCartesianEdgeShapeFunction

from .SpectralShapeFunction import SpectralShapeFunction
from .PolynomialShapeFunction import PolynomialShapeFunction

__all__ = ['ShapeFunction', 'NodalShapeFunction', 'EdgeShapeFunction', 'TriCartesianNodalShapeFunction',
           'TriAxisymmetricNodalShapeFunction', 'TriAxisymmetricEdgeShapeFunction', 'TetCartesianNodalShapeFunction',
           'TriCartesianEdgeShapeFunction',
           'SpectralShapeFunction', 'PolynomialShapeFunction']
