# coding=utf-8
"""This module is for the description of electrical circuits

.. sectionauthor:: Bundschuh
"""

from typing import Tuple, Union, List, Callable, Any, Type, Generator
from abc import abstractmethod, ABC
from pathlib import PurePath
import numpy as np
from scipy import sparse

from pyrit import get_logger

logger = get_logger(__name__)


class CircuitException(Exception):
    """Exception for errors in the Circuit class"""


class GetCurrentException(Exception):
    """Exception for the case when the current through an edge cannot be computed"""


# region Nodes


class Node:
    """Representing a node in an electrical circuit."""

    __slots__ = ('name', 'index', '_value')

    def __init__(self, name: str = None):
        """Constructor of node.

        Parameters
        ----------
        name : str, optional
            The name of the node. Default is None
        """
        self.name = name
        self.index = None
        self._value = None

    @property
    def has_name(self):
        """True if the nodes name is not None."""
        return self.name is not None

    @property
    def potential(self):
        """The potential at the node"""
        return self._value

    @potential.setter
    def potential(self, potential):
        """The potential of the node"""
        self._value = potential

    @property
    def time_domain(self):
        """True, if the potential is in time domain"""
        return isinstance(self.potential, np.ndarray)

    @property
    def frequency_domain(self):
        """True, if the potential is in frequency domain"""
        return isinstance(self.potential, complex)

    def __repr__(self):
        return f"Node '{self.name}' with index {self.index}"


class ReferenceNode(Node):
    """A node in an electrical circuit where a reference potential is defined on"""

    def __init__(self, value: Union[float, complex], name: str = ''):
        """Constructor

        Parameters
        ----------
        value : Union[float, complex]
            Value of the potential at this node. This cannot be a function
        name : str, optional
            The name of the node. Default is ''.
        """
        super().__init__(name)
        self._value = value


class GroundNode(ReferenceNode):
    """A special reference node with zero potential on it."""

    def __init__(self, name: str = ''):
        """Constructor of node.

        Parameters
        ----------
        name : str, optional
            The name of the node. Default is ''
        """
        super().__init__(0, name)


# endregion


# region Components


class Component(ABC):
    """A general component in an electrical circuit. Two nodes are connected by a component."""

    @abstractmethod
    def __init__(self, name: str = ''):
        """Constructor of a general component.

        Parameters
        ----------
        name : str, optional
            Name of the component, Default is ''
        """
        self.name = name

    def get_current(self, voltage: Union[float, complex, np.ndarray], omega: float) -> \
            Union[float, complex, np.ndarray]:
        """Get the current through the component

        Parameters
        ----------
        voltage : Union[float, complex, np.ndarray]
            The voltage over the component
        omega : float
            The angular frequency

        Returns
        -------
        current : Union[float, complex, np.ndarray]
            The current through the component
        """
        raise GetCurrentException

    def __repr__(self):
        return f"{type(self).__name__} with name '{self.name}'"


class ClassicalComponent(Component, ABC):
    """A classical component in an electrical circuit, i.e. a lumped element."""

    @abstractmethod
    def __init__(self, value: Union[float, complex, Callable[[float], Union[float]]], name: str = ''):
        """Constructor of component

        Parameters
        ----------
        value : Union[float, complex, Callable[[float], Union[float]]]
            The value of the component.
        name : str, optional
            The name of the component. Default is ''
        """
        super().__init__(name)
        self._value = None
        self.value = value

    @classmethod
    def _check_value(cls, value: Any):
        if not isinstance(value, (int, float, complex)) and not callable(value):
            raise ValueError(f"The value of the component of class {cls} is not as expected. It is {value}")

    @property
    def value(self):
        """The value of the component."""
        return self._value

    @value.setter
    def value(self, value):
        type(self)._check_value(value)
        self._value = value


class PassiveComponent(ClassicalComponent, ABC):
    """A passive component in an electrical circuit."""

    @abstractmethod
    def __init__(self, value: float, name: str = ''):
        """Constructor of a passive component in an electrical circuit.

        Parameters
        ----------
        value : float
            The value of the component
        name : str, optional
            The name of the component. Default is ''
        """
        super().__init__(value, name)

    @classmethod
    def _check_value(cls, value: Any):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Value has to be a real number, but is {value} of class {type(value)}.")
        if value <= 0:
            raise ValueError("Value must be a positive number")


class Resistor(PassiveComponent):
    """A resistor."""

    def __init__(self, value: float, name: str = ''):
        """Constructor of the passive component Resistor.

        Parameters
        ----------
        value : float
            The value of the component
        name : str, optional
            The name of the component. Default is ''
        """
        super().__init__(value, name)

    def get_current(self, voltage, omega):
        return voltage / self.value

    # def _set_voltage(self, voltage):
    #     self._voltage = voltage
    #     self._current = voltage / self.value


class Inductor(PassiveComponent):
    """An inductor."""

    def __init__(self, value: float, name: str = ''):
        """Constructor of the passive component Inductor.

        Parameters
        ----------
        value : float
            The value of the component
        name : str, optional
            The name of the component. Default is ''
        """
        super().__init__(value, name)

    # def _set_current(self, current):
    #     self._current = current
    #     if self.is_frequency_domain:
    #         self._voltage = 1j * self.omega * current
    #     else:
    #         raise NotImplementedError


class Capacitor(PassiveComponent):
    """A capacitor."""

    def __init__(self, value: float, name: str = ''):
        """Constructor of the passive component Capacitor.

        Parameters
        ----------
        value : float
            The value of the component
        name : str, optional
            The name of the component. Default is ''
        """
        super().__init__(value, name)

    def get_current(self, voltage, omega):
        return 1j * omega * self.value * voltage

    # def _set_voltage(self, voltage):
    #     self._voltage = voltage
    #     if self.is_frequency_domain:
    #         self._current = 1j * self.omega * voltage
    #     else:
    #         raise NotImplementedError


class Source(ClassicalComponent, ABC):
    """A source in an electrical circuit."""

    @abstractmethod
    def __init__(self, value: Union[float, complex, Callable[[float], float]], name: str = ''):
        """Constructor of a source.

        Parameters
        ----------
        value : Union[float, complex, Callable[[float], float]]
            The value of the component.
        name : str, optional
            The name of the component. Default is ''
        """
        super().__init__(value, name)

    @property
    def callable(self):
        """True if the value is callable."""
        return callable(self.value)


class VoltageSource(Source):
    """A voltage source."""

    def __init__(self, value: Union[float, complex, Callable[[float], float]], name: str = ''):
        """Constructor of a voltage source.

        Parameters
        ----------
        value : Union[float, complex, Callable[[float], float]]
            The value of the component.
        name : str, optional
            The name of the component. Default is ''
        """
        super().__init__(value, name)

    # def _set_current(self, current):
    #     self._current = current


class CurrentSource(Source):
    """A current source."""

    def __init__(self, value: Union[float, complex, Callable[[float], float]], name: str = ''):
        """Constructor of a current source.

        Parameters
        ----------
        value : Union[float, complex, Callable[[float], float]]
            The value of the component.
        name : str, optional
            The name of the component. Default is ''
        """
        super().__init__(value, name)

    def get_current(self, voltage, omega):
        return self.value
    # def _set_voltage(self, voltage):
    #     self._voltage = voltage


class FEElement(Component):
    """A component representing any finite element model"""

    def __init__(self, name: str):
        """Constructor of a finite element model component.

        Parameters
        ----------
        name : str
            The name of the component
        """
        super().__init__(name)

    # def _set_voltage(self, voltage):
    #     self._voltage = voltage
    #
    # def _set_current(self, current):
    #     self._current = current


# endregion


class Edge:
    """An edge in an electrical circuit."""

    def __init__(self, from_node: Node, to_node: Node, component: Component, name: str = None):
        """Constructor of an edge.

        Parameters
        ----------
        from_node : Node
            Node where the edge begins.
        to_node : Node
            Node where the edge ends.
        component : Component
            The component that lies on this edge.
        name : str, optional
            The name of the edge. Default is None
        """
        self._from_node = from_node
        self._to_node = to_node
        self.component = component
        self.index = None
        self.name = name

        self._current = None

    def __repr__(self):
        return f"Edge from '{self.from_node}' to '{self.to_node}' with component '{self.component}'"

    @property
    def from_node(self) -> Node:
        """The start node of the edge."""
        return self._from_node

    @property
    def to_node(self) -> Node:
        """The end node of the edge"""
        return self._to_node

    @property
    def has_name(self):
        """True if the edges name is not None"""
        return self.name is not None

    def get_voltage(self) -> Union[float, complex, np.ndarray]:
        """The voltage over the edge"""
        return self._from_node.potential - self._to_node.potential

    def get_current(self, frequency: float = None) -> Union[float, complex, np.ndarray]:
        """Get the current through the edge.

        Parameters
        ----------
        frequency : float, optional
            The frequency of the circuit.

        Returns
        -------
        current : Union[float, complex, np.ndarray]
        """
        if self._current is None:
            if frequency is None:
                omega = None
            else:
                omega = 2 * np.pi * frequency
            return self.component.get_current(self.get_voltage(), omega)
        return self._current

    def set_current(self, current: Union[float, complex, np.ndarray]):
        """Set the current to the edge

        Parameters
        ----------
        current : Union[float, complex, np.ndarra]
            The current
        """
        self._current = current


class Circuit:
    """Class representing an electrical circuit.

    It consists of a list of nodes and a list of edges. Every edge connects two nodes with each other with a component
    lying in the connection. This class can compute the matrices that occur in the modified nodal analysis.
    """

    def __init__(self, nodes: List[Node] = None, edges: List[Edge] = None, name: str = None):
        """Constructor of Circuit.

        Parameters
        ----------
        nodes : List[Node], optional
            A list of nodes to be added to the circuit. Default is None.
        edges : List[Edge], optional
            A list of edges to be added to the circuit. Default is None.
        name : str, optional
            The name of the Circuit. Default is None
        """
        self._nodes = []
        self._edges = []
        self.name = name
        if nodes is not None:
            self.add_nodes(*nodes)
        if edges is not None:
            self.add_edges(*edges)
        self.__indices_written = False  #: If True, the indices of nodes and edges are not written on them

    @property
    def num_nodes(self) -> int:
        """The number of nodes in the circuit."""
        return len(self._nodes)

    @property
    def num_edges(self) -> int:
        """The number of edges in the circuit."""
        return len(self._edges)

    @property
    def num_dof(self):
        """Number of degrees of freedom of the circuit."""
        dof = 0
        for node in self._nodes:
            if isinstance(node, ReferenceNode):
                continue
            dof += 1
        for edge in self._edges:
            if isinstance(edge.component, (Inductor, VoltageSource, FEElement)):
                dof += 1

        return dof

    def add_nodes(self, *nodes: Node):
        """Add nodes to the circuit.

        Parameters
        ----------
        nodes : Tuple[Node]
            A number of nodes to be added to the circuit.
        """
        self._nodes.extend(node for node in nodes)
        self._write_index_to_nodes()

    def add_edges(self, *edges: Edge):
        """Add edges to the circuit.

        Parameters
        ----------
        edges : Tuple[Edge]
            A number of edges to be added to the circuit.
        """
        self._edges.extend(edge for edge in edges)
        self._write_index_to_edges()

    def get_edges(self, edge_component_class: Type[Edge] = None) -> List[Edge]:
        """A list of all edges of the circuit. If specified, only edges of a certain class are returned.

        Parameters
        ----------
        edge_component_class : Type[Edge], optional
            A Edge class to filter all edges

        Returns
        -------
        edges : List[Edge]
        """
        if edge_component_class is None:
            return list(self._edges)
        return [edge for edge in self._edges if isinstance(edge.component, edge_component_class)]

    def get_nodes(self) -> List[Node]:
        """A list of all nodes of the circuit

        Returns
        -------
        nodes : List[Node]
        """
        return list(self._nodes)

    def get_node_from_name(self, name: str) -> Node:
        """Get a node from its name.

        Parameters
        ----------
        name : str
            The name of the node to find.

        Returns
        -------
        node : Node
            The node with the name

        Raises
        ------
        IndexError
            When there is no node with the name or multiple nodes with the name.
        """
        nodes_with_name = [node for node in self._nodes if node.name == name]

        if len(nodes_with_name) > 1:
            raise IndexError(f"More than one node with the name '{name}'")
        if len(nodes_with_name) == 0:
            raise IndexError(f"No node exists with the name '{name}'")

        return nodes_with_name[0]

    def get_edge_from_name(self, name: str) -> Edge:
        """Get a edge from its name.

        Parameters
        ----------
        name : str
            The name of the edge to find.

        Returns
        -------
        edge : Edge
            The edge with the name

        Raises
        ------
        IndexError
            When there is no edge with the name or multiple edges with the name.
        """
        edges_with_name = [edge for edge in self._edges if edge.name == name]

        if len(edges_with_name) > 1:
            raise IndexError(f"More than one edge with the name '{name}'")
        if len(edges_with_name) == 0:
            raise IndexError(f"No edge exists with the name '{name}'")

        return edges_with_name[0]

    def iter_nodes(self, *nodes: Union[Node, str]) -> Generator[Node, None, None]:
        """Generator to iterate over nodes.

        Parameters
        ----------
        nodes : Union[Node, str]
            The nodes. Eiter a Node object or the node's name can be given. If nodes is empty, iterate over all nodes

        Yields
        ------
        node : Node
            The node

        Raises
        ------
        ValueError
            If one element in nodes is of unsupported type
        IndexError
            If a given name of a node is not unique
        """
        if len(nodes) == 0:
            nodes = self._nodes
        for node in nodes:
            if isinstance(node, str):
                node = self.get_node_from_name(node)
            elif isinstance(node, Node):
                pass
            else:
                raise ValueError("node of unsupported type")
            yield node

    def iter_edges(self, *edges: Union[Edge, str]) -> Generator[Edge, None, None]:
        """Generator to iterate over edges.

        Parameters
        ----------
        edges : Union[Edge, str]
            The edges. Eiter an Edge object or the edge's name can be given. If edges is empty, iterate over all edges

        Yields
        ------
        edge : Edge

        Raises
        ------
        ValueError
            If one element in edges is of unsupported type
        IndexError
            If a given name of an edge is not unique
        """
        if len(edges) == 0:
            edges = self._edges
        for edge in edges:
            if isinstance(edge, str):
                edge = self.get_edge_from_name(edge)
            elif isinstance(edge, Edge):
                pass
            else:
                raise ValueError("edge of unsupported type")
            yield edge

    @property
    def has_reference(self):
        """True if the circuit has a reference node."""
        return any(isinstance(node, ReferenceNode) for node in self._nodes)

    @property
    def is_time_dependent(self):
        """True if either the voltage vector or the current vector is callable, i.e. time dependent"""
        return callable(self.voltage_vector()) or callable(self.current_vector())

    @property
    def is_frequency_domain(self):
        """True if either the voltage vector or the current vector is a complex vector"""
        if self.is_time_dependent:
            return False
        return issubclass(self.voltage_vector().dtype.type, complex) or issubclass(self.current_vector().dtype.type,
                                                                                   complex)

    def consistency_check(self):
        """Check the circuit for consistency."""
        # Test of all the nodes of edges are in the circuit
        for edge in self._edges:
            if edge.from_node not in self._nodes:
                raise CircuitException(f"The from_node of '{edge}' is not in the circuit")
            if edge.to_node not in self._nodes:
                raise CircuitException(f"The to_node of '{edge}' is not in the circuit")

        if not self.has_reference:
            logger.warning("There is no reference node. The Circuit may not be solved.")

    def indices_reference(self) -> List[int]:
        """The indices of the reference nodes"""
        return [node.index for node in self._nodes if isinstance(node, ReferenceNode)]

    def values_reference(self) -> List[float]:
        """The values of the reference nodes"""
        return [node.potential for node in self._nodes if isinstance(node, ReferenceNode)]

    def _write_index_to_nodes(self):
        """Write the index of the nodes to each node."""
        for index, node in enumerate(self._nodes):
            node.index = index

    def _write_index_to_edges(self):
        """Write the index of the edges to each edge."""
        for index, edge in enumerate(self._edges):
            edge.index = index

    # region Incidence matrices

    def general_incidence_matrix(self) -> sparse.coo_matrix:
        r"""The general incidence matrix. (Alias: :py:obj:`A`)

        A :math:`N\times E` sparse matrix, where :math:`N` is the number of nodes in the circuit and :math:`E` is the
        number of edges in the graph. The matrix contains only the value -1, 0, 1 and is defined as follows:

        .. math::

            \mathbf{A} = (a_{ij}) \quad\text{with}\quad a_{ij}=
            \begin{cases}
                +1,\quad&\text{if edge $j$ leaves node $i$,}\\
                -1,\quad&\text{if edge $j$ enters node $i$,}\\
                0, \quad&\text{otherwise.}
            \end{cases}

        Notes
        -----
        Please note that in this matrix **all** nodes are considered. So also, in particular, reference nodes with the
        known a priori known potential. For the incidence matrix *without* reference nodes, see
        :py:meth:`split_incidence_matrix`.

        Returns
        -------
        matrix : sparse.coo_matrix
            The general incidence matrix
        """
        if not self.__indices_written:
            self.consistency_check()
            self._write_index_to_nodes()
            self._write_index_to_edges()

        rows = np.empty(2 * self.num_edges)
        for k, edge in enumerate(self._edges):
            rows[2 * k] = edge.from_node.index
            rows[2 * k + 1] = edge.to_node.index

        columns = np.repeat(np.arange(self.num_edges), 2)
        values = np.tile(np.array([1, -1]), self.num_edges)

        return sparse.coo_matrix((values, (rows, columns)), shape=(self.num_nodes, self.num_edges))

    def special_incidence_matrix(self, component_type: Type[Component]) -> sparse.coo_matrix:
        """A special incidence matrix that only considers edges with a component of a certain class.

        Parameters
        ----------
        component_type : Type[Component]
            The class of the component to consider.

        Returns
        -------
        matrix : sparse.coo_matrix
            The special incidence matrix.
        """
        if not self.__indices_written:
            self.consistency_check()
            self._write_index_to_nodes()
            self._write_index_to_edges()

        rows = []
        for edge in self._edges:
            if isinstance(edge.component, component_type):
                rows.append(edge.from_node.index)
                rows.append(edge.to_node.index)

        num_special_edges = int(len(rows) / 2)
        columns = np.repeat(np.arange(num_special_edges), 2)
        values = np.tile(np.array([1, -1]), num_special_edges)

        return sparse.coo_matrix((values, (rows, columns)), shape=(self.num_nodes, num_special_edges))

    def resistor_incidence_matrix(self) -> sparse.coo_matrix:
        """The resistor incidence matrix. (Alias: :py:obj:`A_R`)

        Like the general incidence matrix (:py:meth:`general_incidence_matrix`) but with only those edges where a
        :py:class:`Resistor` is defined on.

        Returns
        -------
        matrix : sparse.coo_matrix
        """
        return self.special_incidence_matrix(Resistor)

    def inductor_incidence_matrix(self) -> sparse.coo_matrix:
        """The inductor incidence matrix. (Alias: :py:obj:`A_I`)

        Like the general incidence matrix (:py:meth:`general_incidence_matrix`) but with only those edges where a
        :py:class:`Inductor` is defined on.

        Returns
        -------
        matrix : sparse.coo_matrix
        """
        return self.special_incidence_matrix(Inductor)

    def capacitor_incidence_matrix(self) -> sparse.coo_matrix:
        """The capacitor incidence matrix. (Alias: :py:obj:`A_C`)

        Like the general incidence matrix (:py:meth:`general_incidence_matrix`) but with only those edges where a
        :py:class:`Capacitor` is defined on.

        Returns
        -------
        matrix : sparse.coo_matrix
        """
        return self.special_incidence_matrix(Capacitor)

    def voltage_source_incidence_matrix(self) -> sparse.coo_matrix:
        """The voltage source incidence matrix. (Alias: :py:obj:`A_V`)

        Like the general incidence matrix (:py:meth:`general_incidence_matrix`) but with only those edges where a
        :py:class:`VoltageSource` is defined on.

        Returns
        -------
        matrix : sparse.coo_matrix
        """
        return self.special_incidence_matrix(VoltageSource)

    def current_source_incidence_matrix(self) -> sparse.coo_matrix:
        """The resistor incidence matrix. (Alias: :py:obj:`A_I`)

        Like the general incidence matrix (:py:meth:`general_incidence_matrix`) but with only those edges where a
        :py:class:`CurrentSource` is defined on.

        Returns
        -------
        matrix : sparse.coo_matrix
        """
        return self.special_incidence_matrix(CurrentSource)

    def fe_element_incidence_matrix(self) -> sparse.coo_matrix:
        """The resistor incidence matrix. (Alias: :py:obj:`A_F`)

        Like the general incidence matrix (:py:meth:`general_incidence_matrix`) but with only those edges where a
        :py:class:`FEElement` is defined on.

        Returns
        -------
        matrix : sparse.coo_matrix
        """
        return self.special_incidence_matrix(FEElement)

    # endregion

    # region Aliases for incidence matrices

    @property
    def A(self):  # pylint: disable=invalid-name
        """Alias for :py:meth:`general_incidence_matrix`"""
        return self.general_incidence_matrix()

    @property
    def A_R(self):  # pylint: disable=invalid-name
        """Alias for :py:meth:`resistor_incidence_matrix`"""
        return self.resistor_incidence_matrix()

    @property
    def A_L(self):  # pylint: disable=invalid-name
        """Alias for :py:meth:`coil_incidence_matrix`"""
        return self.inductor_incidence_matrix()

    @property
    def A_C(self):  # pylint: disable=invalid-name
        """Alias for :py:meth:`capacitor_incidence_matrix`"""
        return self.capacitor_incidence_matrix()

    @property
    def A_I(self):  # pylint: disable=invalid-name
        """Alias for :py:meth:`current_source_incidence_matrix`"""
        return self.current_source_incidence_matrix()

    @property
    def A_V(self):  # pylint: disable=invalid-name
        """Alias for :py:meth:`voltage_source_incidence_matrix`"""
        return self.voltage_source_incidence_matrix()

    @property
    def A_F(self):  # pylint: disable=invalid-name
        """Alias for :py:meth:`fe_element_incidence_matrix`"""
        return self.fe_element_incidence_matrix()

    # endregion

    def _value_matrix(self, component_class: Type[PassiveComponent]) -> sparse.dia_matrix:
        """Collect the values of passive components and write them into a diagonal matrix.

        Parameters
        ----------
        component_class : Type[PassiveComponent]
            The class of the passive components to consider.

        Returns
        -------
        value_matrix : sparse.dia_matrix
            A diagonal sparse matrix with the values of the components
        """
        values = []
        for edge in self._edges:
            if isinstance(edge.component, component_class):
                values.append(edge.component.value)
        return sparse.dia_matrix((values, [0, ]), shape=(len(values), len(values)))

    def conductance_matrix(self) -> sparse.dia_matrix:
        r"""A value matrix for conductances.

        A matrix :math:`\mathbf{G}=\operatorname{diag}(G_1,\dots,G_n)` with the conductances of all resistors in the
        circuit. Note that only resistors are considered i.e. the dimension of the matrix is the number of resistors.

        Returns
        -------
        conductance_matrix : sparse.dia_matrix
        """
        matrix = self._value_matrix(Resistor)
        matrix.data = 1 / matrix.data
        return matrix

    def inductance_matrix(self) -> sparse.dia_matrix:
        r"""A value matrix for inductances.

        A matrix :math:`\mathbf{G}=\operatorname{diag}(L_1,\dots,L_n)` with the inductances of all inductors in the
        circuit. Note that only inductors are considered, i.e. the dimension of the matrix is the number of inductors.

        Returns
        -------
        conductance_matrix : sparse.dia_matrix
        """
        return self._value_matrix(Inductor)

    def capacitance_matrix(self) -> sparse.dia_matrix:
        r"""A value matrix for capacitances.

        A matrix :math:`\mathbf{G}=\operatorname{diag}(C_1,\dots,C_n)` with the capacitances of all capacitors in the
        circuit. Note that only capacitors are considered, i.e. the dimension of the matrix is the number of capacitors.

        Returns
        -------
        conductance_matrix : sparse.dia_matrix
        """
        return self._value_matrix(Capacitor)

    def _value_vector(self, source_class: Type[Source]) \
            -> Union[sparse.coo_matrix, Callable[[float], sparse.coo_matrix]]:
        r"""A vectors with the values of the sources of the given type.

        Returns a vector :math:`\mathbf{v} = [s_1,\dots,s_n]^{T}`, where :math:`s_i` is the value of the :math:`i`-th
        source component of the given type. Each value can be a number (a constant source) or a function. If all values
        are constants, this method returns a matrix. If any value is a function, the return type is also a function that
        returns a matrix.

        Parameters
        ----------
        source_class : Type[Source]
            The source class to consider.

        Returns
        -------
        value_vector : Union[sparse.coo_matrix, Callable[[float], sparse.coo_matrix]]
        """
        values = []
        time_dependent = False
        for edge in self._edges:
            if isinstance(edge.component, source_class):
                values.append(edge.component.value)
                time_dependent |= edge.component.callable

        if time_dependent:
            def value_vector(time):
                v = []
                for val in values:
                    if callable(val):
                        v.append(val(time))
                    else:
                        v.append(val)
                return sparse.coo_matrix((v, (np.arange(len(v), dtype=int), np.zeros(len(v), dtype=int))))
        else:
            value_vector = sparse.coo_matrix(
                (values, (np.arange(len(values), dtype=int), np.zeros(len(values), dtype=int))), shape=(len(values), 1))

        return value_vector

    def current_vector(self) -> Union[sparse.coo_matrix, Callable[[float], sparse.coo_matrix]]:
        r"""A value vector for current sources.

        A vector :math:`\mathbf{i} = [i_1,\dots,i_n]^{T}` with the values of all current sources. Note that only current
        sources are considered, i.e. the dimension of the vector is equal to the number of current sources in the
        circuit.

        Returns
        -------
        current_vector : Union[sparse.coo_matrix, Callable[[float], sparse.coo_matrix]]
        """
        return self._value_vector(CurrentSource)

    def voltage_vector(self) -> Union[sparse.coo_matrix, Callable[[float], sparse.coo_matrix]]:
        r"""A value vector for voltage sources.

        A vector :math:`\mathbf{v} = [v_1,\dots,v_n]^{T}` with the values of all voltage sources. Note that only voltage
        sources are considered, i.e. the dimension of the vector is equal to the number of voltage sources in the
        circuit.

        Returns
        -------
        current_vector : Union[sparse.coo_matrix, Callable[[float], sparse.coo_matrix]]
        """
        return self._value_vector(VoltageSource)

    def split_incidence_matrix(self, matrix: sparse.spmatrix) -> Tuple[sparse.coo_matrix, sparse.coo_matrix]:
        """Split an incidence matrix in two matrices (with and without reference nodes)

        The row number of an incidence matrix is the number of nodes in the circuit. This method splits an incidence
        matrix into two matrices, where in `matrix_ref` only reference nodes are considered and in `matrix_dof` the
        remaining nodes (degrees of freedom) are considered.

        Parameters
        ----------
        matrix : sparse.spmatrix
            A sparse incidence matrix to split

        Returns
        -------
        matrix_dof : sparse.coo_matrix
            Incidence matrix without reference nodes
        matrix_ref : sparse.coo_matrix
            Incidence matrix with only reference nodes
        """
        indices_reference = np.array(self.indices_reference())
        indices_remaining = np.setdiff1d(np.arange(self.num_nodes), indices_reference)

        matrix = matrix.tocsr()

        matrix_dof = matrix[np.ix_(indices_remaining)]
        matrix_ref = matrix[np.ix_(indices_reference)]

        return matrix_dof, matrix_ref

    def mna_matrices(self) -> Tuple[sparse.coo_matrix, sparse.coo_matrix]:
        r"""Receive the MNA system matrix, split up into a time constant part and a time derivative part.

        The MNA matrix is

        .. math::

            \newcommand{\A}{\mathbf{A}}
            \mathbf{X} = \begin{pmatrix}
                \A_R\mathbf{G}\A_R^T + \partial_t\A_C\mathbf{C}\A_C^T & \A_L & \A_V\\
                -\A_L^T & \partial_t\mathbf{L} & 0\\
                -\A_V^T & 0 & 0\\
                -\A_F^T & 0 & 0
            \end{pmatrix}

        Here, the FE elements are already considered. Note that if there are no FE elements in the circuit, the last row
        is not existent and the MNA matrix is as usual.

        This matrix is split up as :math:`\mathbf{X} = \mathbf{M}\partial_t + \mathbf{K}`, with :math:`\mathbf{M}`
        being the `time_derivative_matrix` and :math:`\mathbf{K}` being the `time_constant_matrix`. Consequently, they
        are defined as

        .. math::

            \newcommand{\A}{\mathbf{A}}
            \mathbf{M} = \begin{pmatrix}
                \A_C\mathbf{C}\A_C^T & 0 & 0\\
                0 & \mathbf{L} & 0\\
                0 & 0 & 0\\
                0 & 0 & 0
            \end{pmatrix} \quad\text{and}\quad \mathbf{K} = \begin{pmatrix}
                \A_R\mathbf{G}\A_R^T & \A_L & \A_V\\
                -\A_L^T & 0 & 0\\
                -\A_V^T & 0 & 0\\
                -\A_F^T & 0 & 0
            \end{pmatrix}\,.

        Note that all the incidence matrices here are the DOF-version of the split incidence matrices
        (see :py:meth:`split_incidence_matrix`), i.e. there are no rows or columns associated with reference nodes.

        Returns
        -------
        time_constant_matrix : sparse.coo_matrix
            The matrix :math:`\mathbf{K}`
        time_derivative_matrix : sparse.coo_matrix
            The matrix :math:`\mathbf{M}`
        """
        self.consistency_check()
        self._write_index_to_nodes()
        self._write_index_to_edges()
        self.__indices_written = True

        a_r, _ = self.split_incidence_matrix(self.A_R)
        a_l, _ = self.split_incidence_matrix(self.A_L)
        a_c, _ = self.split_incidence_matrix(self.A_C)
        a_v, _ = self.split_incidence_matrix(self.A_V)
        a_f, _ = self.split_incidence_matrix(self.A_F)

        conductance_matrix = self.conductance_matrix()
        inductance_matrix = self.inductance_matrix()
        capacitance_matrix = self.capacitance_matrix()

        time_constant_matrix = sparse.bmat([[a_r @ conductance_matrix @ a_r.T, a_l, a_v],
                                            [-a_l.T, None, None],
                                            [-a_v.T, None, None],
                                            [-a_f.T, None, None]])
        time_derivative_matrix = sparse.bmat([[a_c @ capacitance_matrix @ a_c.T, None, sparse.coo_matrix(a_v.shape)],
                                              [None, inductance_matrix, None],
                                              [sparse.coo_matrix(a_v.T.shape), None, None],
                                              [sparse.coo_matrix(a_f.T.shape), None, None]])

        self.__indices_written = False

        return time_constant_matrix, time_derivative_matrix

    def mna_rhs(self) -> Union[sparse.coo_matrix, Callable[[float], sparse.coo_matrix]]:
        r"""Receive the right-hand side vector from the MNA.

        The right-hand side vector is

        .. math::

            \newcommand{\A}{\mathbf{A}}
            r = \begin{pmatrix}
                \A_I \mathbf{i}_s(t) - \A_R\mathbf{G}\A_{Rn}^T\varphi_n\\
                \A_{Ln}^T\varphi_n\\
                -\mathbf{u}_s(t) + \A_{Vn}^T\varphi_n\\
                \A_{Fn}^T\varphi_n
            \end{pmatrix}\,.

        Here, the incidence matrices with an additional :math:`n` in the subscript are the reference versions of the
        incidence matrices, i.e. only reference nodes are considered to build them (see
        :py:meth:`split_incidence_matrix`). The other incidence matrices are the DoF-Versions of the incidence matrices.

        Furthermore, :math:`\varphi_n` is a vector with known potentials at reference nodes.
        The current and voltage source vectors (:math:`\mathbf{i}_s(t)` and :math:`\mathbf{u}_s(t)`) can depend
        on time or be a constant vector. When one of them does depend on time a function is returned.

        Returns
        -------
        rhs : Union[sparse.coo_matrix, Callable[[float], sparse.coo_matrix]]
            The right-hand side vector. If any component depends on time, this is a function returning a vector.
        """
        self.consistency_check()
        self._write_index_to_nodes()
        self._write_index_to_edges()
        self.__indices_written = True

        values_reference = self.values_reference()
        values_reference = sparse.coo_matrix(
            (values_reference, (np.arange(len(values_reference)), np.zeros(len(values_reference), dtype=int))))
        a_r, a_rn = self.split_incidence_matrix(self.A_R)
        a_l, a_ln = self.split_incidence_matrix(self.A_L)
        _, a_vn = self.split_incidence_matrix(self.A_V)
        a_i, _ = self.split_incidence_matrix(self.A_I)
        a_f, a_fn = self.split_incidence_matrix(self.A_F)

        conductance_matrix = self.conductance_matrix()
        time_constant_rhs = sparse.vstack([-a_r @ conductance_matrix @ a_rn.T @ values_reference,
                                           a_ln.T @ values_reference,
                                           a_vn.T @ values_reference,
                                           a_fn.T @ values_reference])

        voltage_vector = self.voltage_vector()
        current_vector = self.current_vector()
        if callable(voltage_vector) or callable(current_vector):
            def rhs(time):
                v = []
                if callable(current_vector):
                    v.append(a_i @ current_vector(time))
                else:
                    v.append(a_i @ current_vector)
                if callable(voltage_vector):
                    v.append(-1 * voltage_vector(time))
                else:
                    v.append(-1 * voltage_vector)
                return time_constant_rhs + sparse.vstack([v[0],
                                                          sparse.coo_matrix((a_l.shape[1], 1)),
                                                          v[1],
                                                          sparse.coo_matrix((a_f.shape[1], 1))])
        else:
            rhs = time_constant_rhs + sparse.vstack([a_i @ current_vector,
                                                     sparse.coo_matrix((a_l.shape[1], 1)),
                                                     -1 * voltage_vector,
                                                     sparse.coo_matrix((a_f.shape[1], 1))])
            rhs = rhs.tocoo()
        self.__indices_written = False

        return rhs

    def set_solution(self, solution: np.ndarray):
        r"""Set the solution and save it to the nodes and edges

        Parameters
        ----------
        solution : np.ndarray
            The solution of the circuit, i.e. a vector with :math:`[\varphi,\,i_L,\,i_V,\,i_F]`.

        Raises
        ------
        ValueError
            If the shape of the solution is not correct.
        """
        idx = 0
        for node in self._nodes:
            if isinstance(node, ReferenceNode):
                continue
            node.potential = solution[idx]
            idx += 1

        for component_class in (Inductor, VoltageSource, FEElement):
            for edge in self._edges:
                if isinstance(edge.component, component_class):
                    edge.set_current(solution[idx])
                    idx += 1
        if idx != solution.shape[0]:
            raise ValueError("The shape of solution is not correct.")

    def get_solution(self) -> np.ndarray:
        """Get the solution of the circuit

        Notes
        -----
        This method does not solve the circuit. It can return the solution, if a solution was written to the circuit
        beforehand.
        """
        solution = []
        for node in self._nodes:
            if isinstance(node, ReferenceNode):
                continue
            solution.append(node.potential)

        for component_class in (Inductor, VoltageSource, FEElement):
            for edge in self._edges:
                if isinstance(edge.component, component_class):
                    solution.append(edge.get_current())

        return np.array(solution)

    def to_netlist(self) -> str:
        """Export the circuit to a netlist"""
        raise NotImplementedError

    @staticmethod
    def from_netlist(path: PurePath) -> 'Circuit':
        """Import a circuit from a netlist"""
        raise NotImplementedError
