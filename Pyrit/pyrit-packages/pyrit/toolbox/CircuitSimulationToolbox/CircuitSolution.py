# coding=utf-8
"""A circuit simulation solution

.. sectionauthor:: Bundschuh
"""

from typing import Union, TYPE_CHECKING, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np

from pyrit.toolbox.CircuitSimulationToolbox.Circuit import Circuit, Node, Edge
from pyrit.toolbox.IOToolbox import save, load
from pyrit import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from pathlib import Path


def plot_complex_entity(frequency: float, *entities: complex, **kwargs) -> Tuple[Figure, Axes]:
    """Plot complex entities

    Parameters
    ----------
    frequency : float
        The frequency o
    entities : complex
        The complex entities.
    kwargs :
        Arguments to personalize the plot:

            - fig: The figure object
            - ax: The exis object
            - labels: A list of labels to the entities
            - time: Multiples of a period to plot
            - time_steps: Explizit time steps to plot
            - plot_kwargs: Kwargs passed to every plot method
            - plt_kwargs_list: A list of kwargs passed to the plot method of the specific entity
            - x_label: The x label
            - y_label: The y label
            - title: The title of the axis
            - suptitle: The title of the figure

    Returns
    -------
    fig : Figure
        The figure the plot was added to
    ax : Axes
        The axis the plot was added to
    """
    fig = kwargs.pop('fig', None)
    ax = kwargs.pop('ax', None)
    labels = kwargs.pop('labels', ['' for _ in range(len(entities))])
    time = kwargs.pop('time', 3)
    time_steps = kwargs.pop('time_steps', 500)
    plot_kwargs = kwargs.pop('plot_kwargs', {})
    plot_kwargs_list = kwargs.pop('plot_kwargs_list', [{} for _ in range(len(entities))])
    x_label = kwargs.pop('x_label', 'time')
    y_label = kwargs.pop('y_label', '')
    title = kwargs.pop('title', '')
    suptitle = kwargs.pop('suptitle', '')

    omega = 2 * np.pi * frequency

    if fig is None:
        fig = plt.figure()

    if ax is None:
        ax = fig.add_subplot()

    if isinstance(time, (int, float)):  # Multiples of period
        time = np.linspace(0, time / frequency, time_steps)
    elif isinstance(time, (tuple, list)):
        if not len(time) == 2:
            raise ValueError("'time' has the wrong format.")
        time = np.linspace(time[0], time[1], time_steps)
    elif isinstance(time, np.ndarray):
        pass
    else:
        raise ValueError("Format of 'time' not known.")

    if len(labels) != len(entities):
        raise ValueError("The number of entities to plot dies not match the number of labels.")

    if len(plot_kwargs_list) != len(entities):
        raise ValueError("The number of elements in plot_kwargs_list and entities does not match.")

    for k, entity in enumerate(entities):
        values = np.real(entity * np.exp(1j * omega * time))
        tmp_plot_kwargs = {'label': labels[k]}
        tmp_plot_kwargs.update(plot_kwargs)
        tmp_plot_kwargs.update(plot_kwargs_list[k])
        ax.plot(time, values, **tmp_plot_kwargs)

    ax.legend()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    fig.suptitle(suptitle)

    return fig, ax


class CircuitSolution:
    """Basic class to manage the solution of a circuit."""

    def __init__(self, solution: np.ndarray, circuit: Circuit, name: str = None):
        self._solution = None
        self._circuit = None
        self.solution = solution
        self.circuit = circuit
        self.name = name

        self.consistency_check()

    @property
    def solution(self) -> np.ndarray:
        """The solution array"""
        return self._solution

    @solution.setter
    def solution(self, solution: np.ndarray):
        """The solution array"""
        if not isinstance(solution, np.ndarray):
            raise ValueError("The solution is not an array")
        self._solution = solution

    @property
    def circuit(self) -> Circuit:
        """The circuit"""
        return self._circuit

    @circuit.setter
    def circuit(self, circuit: Circuit):
        """The circuit"""
        if not isinstance(circuit, Circuit):
            raise ValueError("The circuit argument is not of the class 'Circuit'")
        self._circuit = circuit

    def set_solution_to_circuit(self):
        """Set the solution array as a solution to the circuit"""
        self.circuit.set_solution(self.solution)

    def consistency_check(self):
        """Check the consistency of the circuit solution object."""
        if self.solution.shape[0] != self.circuit.num_dof:
            raise ValueError("The solution has the wrong size")

    def save(self, path: Union[str, 'Path'], **kwargs) -> 'Path':
        """Save the object

        Parameters
        ----------
        path : Union[str, 'Path']
        kwargs :
            Keyword arguments passed to the save function (:py:func:`pyrit.toolbox.IOToolbox.save`)

        Returns
        -------
        path : 'Path'
            The path where the object is saved
        """
        return save(self, path, **kwargs)

    @classmethod
    def load(cls, path: Union[str, 'Path'], **kwargs) -> 'CircuitSolution':
        """Load a CircuitSolution

        Parameters
        ----------
        path : Union[str, 'Path']
            The path where the object is saved
        kwargs :
            Keyword arguments passed to the load function (:py:func:`pyrit.toolbox.IOToolbox.load`)

        Returns
        -------
        circuit_solution : CircuitSolution
        """
        obj = load(path, **kwargs)
        if not isinstance(obj, cls):
            raise TypeError("The loaded object has the wrong type")
        return obj


def with_solution_set(func):
    """Decorator to set the solution array to the circuit."""
    def wrapper(self: CircuitSolution, *args, **kwargs):
        """Wrapper function of the decorator 'with_solution_set'."""
        self.set_solution_to_circuit()
        return func(self, *args, **kwargs)

    return wrapper


class CircuitSolutionStatic(CircuitSolution):
    """Class for managing the static solution of a circuit"""

    def __init__(self, solution: np.ndarray, circuit: Circuit, name: str = None):
        super().__init__(solution, circuit, name)

    def consistency_check(self):
        if not issubclass(self._solution.dtype.type, (np.floating, np.integer)):
            raise ValueError("Solution must be a real-valued array.")

        super().consistency_check()

    @with_solution_set
    def get_potential(self, *nodes: Union[Node, str]) -> List[float]:
        """Get a list of the potentials of the given nodes.

        Parameters
        ----------
        nodes : Union[Node, str]
            The nodes. Eiter a Node object or the node's name can be given

        Returns
        -------
        potentials : List[float]
            A list of potentials
        """
        return [node.potential for node in self.circuit.iter_nodes(*nodes)]

    def get_all_potentials(self) -> List[float]:
        """Get a list of all potentials

        Returns
        -------
        potentials : List[float]
            A list of all potentials
        """
        return self.get_potential(*self.circuit.get_nodes())

    def print_potential(self, *nodes: Union[Node, str]):
        """Print all potentials of the circuit

        Parameters
        ----------
        nodes : Union[Node, str]
            The nodes. Eiter a Node object or the node's name can be given
        """
        for node, potential in zip(self.circuit.iter_nodes(*nodes), self.get_potential(*nodes)):
            name = node.name if node.has_name else f"Index: {node.index}"
            print(f"Node: \'{name}\'\tPotential: {potential:.4f}")

    def print_all_potentials(self):
        """Print the potentials of all nodes"""
        self.print_potential(*self.circuit.get_nodes())

    @with_solution_set
    def get_voltage(self, *edges: Union[Edge, str]) -> List[float]:
        """Get a list of voltages over the given edges

        Parameters
        ----------
        edges : Union[Edge, str]
            The edges. Eiter an Edge object or the edge's name can be given

        Returns
        -------
        voltages : List[float]
            A list of voltages over the edges
        """
        return [edge.get_voltage() for edge in self.circuit.iter_edges(*edges)]

    def get_all_voltages(self) -> List[float]:
        """Get a list of all voltages in the circuit

        Returns
        -------
        voltages : List[float]
            A list of voltages over all edges
        """
        return self.get_voltage(*self.circuit.get_edges())

    def print_voltage(self, *edges: Union[Edge, str]):
        """Print voltages of the circuit

        Parameters
        ----------
        edges : Union[Edge, str]
            The edges. Eiter an Edge object or the edge's name can be given
        """
        for edge, voltage in zip(self.circuit.iter_edges(*edges), self.get_voltage(*edges)):
            name = edge.name if edge.has_name else f"Index: {edge.index}"
            print(f"Edge: \'{name}\'\tVoltage: {voltage:.4f}")

    def print_all_voltages(self):
        """Print all voltages in the circuit"""
        self.print_voltage(*self.circuit.get_edges())

    @with_solution_set
    def get_current(self, *edges: Union[Edge, str]) -> List[float]:
        """Get a list of currents through the given edges.

        Parameters
        ----------
        edges : Union[Edge, str]
            The edges. Eiter an Edge object or the edge's name can be given

        Returns
        -------
        currents : List[float]
            A list of currents through the edges.
        """
        return [edge.get_current() for edge in self.circuit.iter_edges(*edges)]

    def get_all_currents(self) -> List[float]:
        """Get a list of all currents in the circuit.

        Returns
        -------
        currents : List[float]
            A list of currents through all edges.
        """
        return self.get_current(*self.circuit.get_edges())

    def print_current(self, *edges: Union[Edge, str]):
        """Print the currents through the given edges.

        Parameters
        ----------
        edges : Union[Edge, str]
            The edges. Eiter an Edge object or the edge's name can be given
        """
        for edge, current in zip(self.circuit.iter_edges(*edges), self.get_current(*edges)):
            name = edge.name if edge.has_name else f"Index: {edge.index}"
            print(f"Edge: \'{name}\'\tCurrent: {current:.4f}")

    def print_all_currents(self):
        """Print all currents of the circuit."""
        self.print_current(*self.circuit.get_edges())


class CircuitSolutionHarmonic(CircuitSolution):
    """Class for managing the harmonic solution of a circuit"""

    def __init__(self, solution: np.ndarray, circuit: Circuit, frequency: float, name: str = None):
        super().__init__(solution, circuit, name)
        self._frequency = None
        self.frequency = frequency

    @property
    def frequency(self) -> float:
        """The frequency"""
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: float):
        """The frequency"""
        if not frequency > 0:
            raise ValueError("The frequency must be a positive number")
        self._frequency = frequency

    @property
    def angular_frequency(self):
        """The angular frequency"""
        return 2 * np.pi * self.frequency

    omega = angular_frequency

    def consistency_check(self):
        super().consistency_check()

        if not issubclass(self._solution.dtype.type, np.complexfloating):
            raise ValueError("Solution must be a complex array.")

    def _plot(self, *entities, **kwargs):
        """Default the frequency to the function plot_complex_entity"""
        return plot_complex_entity(self.frequency, *entities, **kwargs)

    @with_solution_set
    def plot_potential(self, *nodes: Union[Node, str], **kwargs):
        """Plot the potentials of the given potentials

        Parameters
        ----------
        nodes : Union[Node, str]
        kwargs :
            Keyword arguments passed to the plot function
        """
        values, labels = [], []
        for node in self.circuit.iter_nodes(*nodes):
            labels.append(node.name if node.has_name else f"Index: {node.index}")
            values.append(node.potential)

        kwargs.setdefault('labels', labels)
        kwargs.setdefault('y_label', "Potential in V")

        return self._plot(*values, **kwargs)

    def plot_all_potentials(self, **kwargs):
        """Plot all potentials in the circuit

        Parameters
        ----------
        kwargs :
            Keyword arguments passed to the plot function
        """
        self.plot_potential(*self.circuit.get_nodes(), **kwargs)

    @with_solution_set
    def plot_voltage(self, *edges: Union[Edge, str], **kwargs):
        """Plot the voltages over the given edges

        Parameters
        ----------
        edges : Union[Edge, str]
        kwargs :
            Keyword arguments passed to the plot function
        """
        values, labels = [], []
        for edge in self.circuit.iter_edges(*edges):
            labels.append(edge.name if edge.has_name else f"Index: {edge.index}")
            values.append(edge.get_voltage())

        kwargs.setdefault('labels', labels)
        kwargs.setdefault('y_label', "Voltage in V")

        return self._plot(*values, **kwargs)

    def plot_all_voltages(self, **kwargs):
        """Plot the voltages over all edges in the circuit

        Parameters
        ----------
        kwargs :
            Keyword arguments passed to the plot function
        """
        self.plot_voltage(*self.circuit.get_edges(), **kwargs)

    @with_solution_set
    def plot_current(self, *edges, **kwargs):
        """Plot the currents through the given edges

        Parameters
        ----------
        edges : Union[Edge, str]
        kwargs :
            Keyword arguments passed to the plot function
        """
        values, labels = [], []
        for edge in self.circuit.iter_edges(*edges):
            labels.append(edge.name if edge.has_name else f"Index: {edge.index}")
            values.append(edge.get_current(self.frequency))

        kwargs.setdefault('labels', labels)
        kwargs.setdefault('y_label', "Current in A")

        return self._plot(*values, **kwargs)

    def plot_all_currents(self, **kwargs):
        """Plot the currents through all edges

        Parameters
        ----------
        edges : Union[Edge, str]
        kwargs :
            Keyword arguments passed to the plot function
        """
        self.plot_current(*self.circuit.get_edges(), **kwargs)


class CircuitSolutionTransient(CircuitSolution):
    """Class for managing the transient solution of a circuit"""

    def __init__(self, solution: np.ndarray, circuit: Circuit, name: str = None):
        super().__init__(solution, circuit, name)
