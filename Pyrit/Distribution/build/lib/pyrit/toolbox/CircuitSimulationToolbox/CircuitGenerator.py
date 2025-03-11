# coding=utf-8
"""Generate predefined circuits

.. sectionauthor:: Bundschuh
"""

from abc import ABC, abstractmethod

from pyrit.toolbox.CircuitSimulationToolbox.Circuit import Circuit, GroundNode, Node, Edge, VoltageSource, FEElement, \
    CurrentSource


class CircuitGenerator(ABC):
    """Abstract class for a circuit generator"""

    @abstractmethod
    def generate(self) -> Circuit:
        """Generate the circuit."""


class VoltageDrivenFE(CircuitGenerator):
    """Generator for a circuit with only a voltage source and a FE element."""

    def __init__(self, voltage, name_fe: str, name_circuit: str = None):
        """Constructor of VoltageDrivenFE

        Parameters
        ----------
        voltage :
            The voltage of the source
        name_fe : str
            Name of the FEElement
        name_circuit : str, optional
            Name of the circuit. Default is None.
        """
        self.voltage = voltage
        self.name_fe = name_fe
        self.name_circuit = name_circuit

    def generate(self) -> Circuit:
        ground = GroundNode("Ground")
        top_node = Node("top node")

        nodes = [ground, top_node]
        edges = [Edge(top_node, ground, VoltageSource(self.voltage), "source"),
                 Edge(top_node, ground, FEElement(self.name_fe), "fe_element")]

        return Circuit(nodes, edges, self.name_circuit)


class CurrentDrivenFE(CircuitGenerator):
    """Generator for a circuit with only a current source and a FE element."""

    def __init__(self, current, name_fe: str, name_circuit: str = None):
        """Constructor of VoltageDrivenFE

        Parameters
        ----------
        current :
            The current of the source
        name_fe : str
            Name of the FEElement
        name_circuit : str, optional
            Name of the circuit. Default is None.
        """
        self.current = current
        self.name_fe = name_fe
        self.name_circuit = name_circuit

    def generate(self) -> Circuit:
        ground = GroundNode("Ground")
        top_node = Node("top node")

        nodes = [ground, top_node]
        edges = [Edge(top_node, ground, CurrentSource(self.current), "source"),
                 Edge(top_node, ground, FEElement(self.name_fe), "fe_element")]

        return Circuit(nodes, edges, self.name_circuit)
