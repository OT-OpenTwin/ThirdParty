# coding=utf-8
"""
========================================================================
CircuitSimulationToolbox (:mod:`pyrit.toolbox.CircuitSimulationToolbox`)
========================================================================

.. currentmodule:: pyrit.toolbox.CircuitSimulationToolbox

This toolbox is for the description and simulation electrical circuits. The focus lies on simple circuits to use
with a field-circuit coupling.


Circuit description
-------------------

Circuit description classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
    :toctree: autosummary/

    Circuit
    Node
    ReferenceNode
    GroundNode
    Edge
    Resistor
    Inductor
    Capacitor
    VoltageSource
    CurrentSource
    FEElement


Abstract classes
^^^^^^^^^^^^^^^^

.. autosummary::
    :toctree: autosummary/

    Component
    ClassicalComponent
    PassiveComponent
    Source


Exceptions
^^^^^^^^^^

.. autosummary::
    :toctree: autosummary/

    CircuitException
    GetCurrentException

Default Circuits
----------------

.. autosummary::
    :toctree: autosummary/

    CurrentDrivenFE
    VoltageDrivenFE


Circuit Problems
----------------

.. autosummary::
    :toctree: autosummary/

    CircuitProblem
    CircuitProblemStatic
    CircuitProblemHarmonic
    CircuitProblemTransient

Circuit Solutions
-----------------

.. autosummary::
    :toctree: autosummary/

    CircuitSolution
    CircuitSolutionStatic
    CircuitSolutionHarmonic
    CircuitSolutionTransient
"""

from .Circuit import CircuitException, GetCurrentException, \
    Node, ReferenceNode, GroundNode, \
    Component, ClassicalComponent, PassiveComponent, Resistor, Inductor, Capacitor, \
    Source, VoltageSource, CurrentSource, \
    FEElement, Edge, Circuit

from .CircuitGenerator import CurrentDrivenFE, VoltageDrivenFE

from .CircuitProblem import CircuitProblem, CircuitProblemStatic, CircuitProblemHarmonic, CircuitProblemTransient
from .CircuitSolution import CircuitSolution, CircuitSolutionStatic, CircuitSolutionHarmonic, CircuitSolutionTransient
