# coding=utf-8
"""This toolbox provides tools for inspecting problems in Pyrit.

.. sectionauthor:: Seif
"""

from typing import Tuple, Dict, List

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.tri import Triangulation
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

import numpy as np

from pyrit.mesh import TriMesh
from pyrit.region import Regions
from pyrit import get_logger

logger = get_logger(__name__)


def count_colors(colorcode: np.ndarray) -> int:
    """This method count the amount of different colorcodes, which are not equal to -1

    Parameters
    ----------
    colorcode: np.ndarray
        (P,) array. Each row contains an integer value, representing a single color

    Returns
    -------
    number_of_colors : int
        the total amount of different color values, excluding -1
    """
    number = len(np.unique(colorcode))
    if -1 in colorcode:
        return number - 1
    return number


def get_edge_colors(colorcode: np.ndarray) -> LinearSegmentedColormap:
    """A bijective colormap for edges is created. Length of the map = amount of distinguishing colors that are not -1

    Parameters
    ----------
    colorcode: np.ndarray
        (P,) array. Each row contains an integer value, representing a single color

    Returns
    -------
    colors : ListedColormap
        the corresponding ListedColormap
    """
    numb_of_colors = count_colors(colorcode)
    colors = mpl.colormaps['seismic'].resampled(numb_of_colors)
    return colors


def get_node_colors(colorcode: np.ndarray) -> LinearSegmentedColormap:
    """A bijective colormap for nodes is created. Length of the map = amount of distinguishing colors that are not -1

    Parameters
    ----------
    colorcode: np.ndarray
        (P,) array. Each row contains an integer value, representing a single color

    Returns
    -------
    colors : ListedColormap
        the corresponding ListedColormap
    """
    numb_of_colors = count_colors(colorcode)
    colors = mpl.colormaps['PiYG'].resampled(numb_of_colors)
    return colors


def get_colormapping(colorcode: np.ndarray, colorpalette: ListedColormap) -> Dict:
    """Pairing colorcodes with colors in a dictionary. black is paired represented as: -1 -> '#000000'

    Parameters
    ----------
    colorcode: np.ndarray
        (P,) array. Each row contains an integer value, representing a single color

    colorpalette: ListedColormap
        colormap with colors as RGBA values that are not black

    Returns
    -------
    color_distribution : Dict
        the corresponding Dictionary,
            key     ->  colorcode (int)
            value   ->  color (entry out of a Listed Colormap RGBA)
    """
    color_keys: set = set()
    for color_key in colorcode:
        if color_key != -1:
            color_keys.add(color_key)
    color_distribution = {colorkey: colorpalette(color_idx) for color_idx, colorkey in enumerate(list(color_keys))}
    color_distribution[-1] = '#000000'

    return color_distribution


def get_mesh_components(grid: Triangulation, colorcode: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Based on a given color indication for a mesh, two arrays (one for colored, one for black elems) are created

    Parameters
    ----------
    grid: Triangulation
        the mesh, whose elements shall be analysed and sorted into one list.
    colorcode: np.ndarray
        (E,) array. Each row contains an integer value, determining the color of the corresponding element
        -> since there are E elements, colorcode must have E entries
        -> if the entry is '-1', the corresponding element must become black

    Returns
    -------
    blackelems : np.ndarray
        (B,3) array. Contains all elements of the given mesh, that shall be black: B + C = E

    coloredelems : np.ndarray
        (C,3) array. Contains all elements of the given mesh, that shall be colored: B + C = E
    """
    blackmeshlist: List = []
    colormeshlist: List = []
    elems = grid.triangles
    for idx, code in enumerate(colorcode):
        if code == -1:
            blackmeshlist.append(elems[idx])
        else:
            colormeshlist.append(elems[idx])

    blackelems: np.ndarray = np.asarray(blackmeshlist)
    coloredelems: np.ndarray = np.asarray(colormeshlist)

    return blackelems, coloredelems


def colorfilter(colorcode: np.ndarray) -> np.ndarray:
    """Elimination of all vector entries equal to -1

    Parameters
    ----------
    colorcode: np.ndarray
        (E,) array. Each row contains an integer value, determining the color of the corresponding element
        -> since there are E elements, colorcode must have E entries

    Returns
    -------
    colors : np.ndarray
        array which contains only those input entries, not equal to -1. Further, copies of the other values do not exist
    """
    filterlist: List = []
    for color_id in colorcode:
        if color_id != -1:
            filterlist.append(color_id)
    colors: np.ndarray = np.asarray(filterlist)
    return colors


def create_submesh(elems: np.ndarray, nodes: np.ndarray) -> Triangulation:
    """Based on a given subset of elem2node indications, a new TriMesh (submesh of existing Mesh) is created

    Parameters
    ----------
    nodes: np.ndarray
        (P,2) array. Each row contains the x- and y-coordinate of the corresponding node. P nodes
    elems: np.ndarray
        (E,3) array. Each row contains the node indices of the corresponding element. E elements

    Returns
    -------
    trimesh : Triangulation
        the submesh
    """
    gridnodes_x: List = []
    gridnodes_y: List = []
    addednodes: set = set()
    subgridelems: np.ndarray = np.empty_like(elems)

    new_node_id: int = 0
    old2new_node_id: Dict = {}
    for idx, node_ids in enumerate(elems):
        col_idx = 0
        for node_id in node_ids:
            if not addednodes.__contains__(node_id):
                old2new_node_id[node_id] = new_node_id
                new_node_id += 1
                gridnodes_x.append(nodes[node_id][0])
                gridnodes_y.append(nodes[node_id][1])
                addednodes.add(node_id)
            subgridelems[idx, col_idx] = old2new_node_id[node_id]
            col_idx += 1
    x_new_grid: np.ndarray = np.asarray(gridnodes_x)
    y_new_grid: np.ndarray = np.asarray(gridnodes_y)
    trimesh: Triangulation = Triangulation(x_new_grid, y_new_grid, subgridelems)

    return trimesh


def plot_nodes(nodes: np.ndarray, colorcode: np.ndarray, ax: Axes, fig: Figure) -> Tuple[Figure, Axes]:
    """This method creates a plot of distinct colored single nodes, as long as their colorcode is not '-1'

    Parameters
    ----------
    nodes: np.ndarray
        (P,2) array. Each row contains the x- and y-coordinate of the corresponding node. P nodes
    colorcode: np.ndarray
        (P,) array. Each row contains an integer value, determining the color of the corresponding edge
        -> since there are P nodes, colorcode must have P entries
    ax: Axes
        an axes object, the edges shall be plotted on
    fig: Figure
        the Figure object, holding the plot elements

    Returns
    -------
    ax : Axes
        the changed Axes object
    fig: Figure
        the changed figure object

    Raises
    ------
    ValueError: If an input parameter has not the right format
    """
    if nodes.ndim != 2:
        raise ValueError(f'nodes has dimension {str(nodes.ndim)} but should be 2')
    if colorcode.ndim != 1:
        raise ValueError(f'colorcode has dimension {str(colorcode.ndim)}but should be 1')
    if len(nodes) != len(colorcode):
        raise ValueError(
            f'number of nodes = {str(len(nodes))} but not the same as number of colors {str(len(colorcode))}')
    colorpalette: ListedColormap = get_node_colors(colorcode)

    colormapping: dict = get_colormapping(colorcode, colorpalette)
    if list(colormapping.keys()) != [-1]:
        x_colorful: List = []
        y_colorful: List = []
        legend_color_list: List = []

        for node_idx, node in enumerate(nodes):
            color_id = colorcode[node_idx]
            if color_id != -1:
                x_colorful.append(node[0])
                y_colorful.append(node[1])
                legend_color_list.append(color_id)

        nodeplotting = ax.scatter(x_colorful, y_colorful, c=legend_color_list, cmap=colorpalette, zorder=2.5)

        cb = fig.colorbar(nodeplotting, ax=ax, orientation='vertical', aspect=50, pad=0.075,
                          location='right', fraction=0.05, format='%1i')
        cb.ax.set(xlabel='n2r')
        modify_cb_label(int(min(legend_color_list)), int(max(legend_color_list)), cb)

    return fig, ax


def modify_cb_label(minimum: int, maximum: int, cb: Figure.colorbar) -> Figure.colorbar:
    """This method modifies the ticks of a colorbar

    Parameters
    ----------
    minimum: int
        minimal value of the colorbar
    maximum: int
        maximal value of the colorbar
    cb: Figure.colorbar
        the colorbar, that is modified

    Returns
    -------
    cb: Figure.colorbar
        the modified colorbar
    """
    tick_steps = get_tick_steps(maximum, minimum)
    labels = np.linspace(minimum, maximum, tick_steps, dtype=int, endpoint=True)
    loc = np.linspace(minimum, maximum, tick_steps, dtype=int, endpoint=True)
    cb.set_ticks(loc)
    cb.set_ticklabels(labels)
    return cb


def plot_edges(edge2node: np.ndarray, nodes: np.ndarray, colorcode: np.ndarray,
               ax: Axes, fig: Figure) -> Tuple[Figure, Axes]:
    """This method creates a plot of distinct colored edges

    Parameters
    ----------
    edge2node : np.ndarray
        (K,2) array. Each row contains the node indices of the corresponding edge. K edges
    nodes: np.ndarray
        (P,2) array. Each row contains the x- and y-coordinate of the corresponding node. P nodes
    colorcode: np.ndarray
        (K,) array. Each row contains an integer value, determining the color of the corresponding edge
        -> since there are K edges, colorcode must have K entries
    ax: Axes
        an axes object, the edges shall be plotted on
    fig: Figure
        the Figure object, holding the plot elements

    Returns
    -------
    ax : Axes
        the changed Axes object
    fig: Figure
        the changed figure object

    Raises
    ------
    ValueError: If an input parameter has not the right format
    """
    if edge2node.ndim != 2:
        raise ValueError(f'edge2node has dimension {str(edge2node.ndim)}but should be 2')
    if nodes.ndim != 2:
        raise ValueError(f'nodes has dimension {str(nodes.ndim)}but should be 2')
    if colorcode.ndim != 1:
        raise ValueError(f'colorcode has dimension {str(colorcode.ndim)}but should be 1')
    if len(edge2node) != len(colorcode):
        raise ValueError(f'number of edges = {str(len(edge2node))}but not the same as number of '
                         f'colors = {str(len(colorcode))}')

    colorpalette: ListedColormap = get_edge_colors(colorcode)

    colormapping: dict = get_colormapping(colorcode, colorpalette)

    id_set: set = set()
    color_set: set = set()
    for edge_idx, edge in enumerate(edge2node):
        startnode = nodes[edge[0]]
        endnode = nodes[edge[1]]
        x_pos = np.asarray([startnode[0], endnode[0]])
        y_pos = np.asarray([startnode[1], endnode[1]])
        color_id = colorcode[edge_idx]
        color = colormapping[color_id]
        if colorcode[edge_idx] != -1:
            ax.plot(x_pos, y_pos, color=color)
            if not id_set.__contains__(colorcode[edge_idx]):
                id_set.add(int(colorcode[edge_idx]))
                if not color_set.__contains__(color):
                    color_set.add(color)

    cb = fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(min(id_set), max(id_set)), cmap=colorpalette),
                      ax=ax, orientation='vertical', aspect=50, pad=0.075, fraction=0.05, format='%1i')
    cb.ax.set(xlabel='ed2r')
    modify_cb_label(int(min(id_set)), int(max(id_set)), cb)

    return fig, ax


def get_tick_steps(maximum: int, minimum: int, ticks: int = 11) -> int:
    """Determine the maximal amount of ticks indicating colorbar items.

    The ticks are chosen so that natural numbers are used as ticks

    Parameters
    ----------
    maximum : int
        the maximum id that could be used as a tick
    minimum : int
        the minimum id that could be used as a tick
    ticks: int
        the upper limit of ticks

    Returns
    -------
    ticks: int
        the final amount of ticks
    """
    potential_ticks: int = maximum - minimum + 1

    if 0 < potential_ticks < ticks:
        ticks = potential_ticks
    return ticks


def plot_triangles(elem2node: np.ndarray, nodes: np.ndarray, colorcode: np.ndarray,
                   ax: Axes, fig: Figure) -> Tuple[Figure, Axes]:
    """This method creates a plot of distinct colored elements

    Parameters
    ----------
    elem2node: np.ndarray
        (E,3) array. Each row contains the node indices of the corresponding element. E elements
    nodes: np.ndarray
        (P,2) array. Each row contains the x- and y-coordinate of the corresponding node. P nodes
    colorcode: np.ndarray
        (E,) array. Each row contains an integer value, determining the color of the corresponding element
        -> since there are E elements, colorcode must have E entries
    ax: Axes
        an axes object, the edges shall be plotted on
    fig: Figure
        the Figure object, holding the plot elements

    Returns
    -------
    ax : Axes
        the changed Axes object
    fig: Figure
        the changed figure object

    Raises
    ------
        ValueError: If an input parameter has not the right format
    """
    if nodes.ndim != 2:
        raise ValueError(f"nodes is of dimension {nodes.ndim} but should be of dimension 2")
    if elem2node.ndim != 2:
        raise ValueError(f"nodes is of dimension {elem2node.ndim} but should be of dimension 2")
    if elem2node.shape[1] != 3:
        raise ValueError(f"elem2node only refers to {elem2node.shape[1]} nodes but should refer to 3")
    if colorcode.ndim != 1:
        raise ValueError(f"colorcode has dimension {colorcode.ndim} but should be 1")
    if elem2node.shape[0] != len(colorcode):
        raise ValueError(f"number of elems = {elem2node.shape[0]} but not the same as number of colors = "
                         f"{len(colorcode)}")

    grid: Triangulation = Triangulation(nodes[:, 0], nodes[:, 1], elem2node)
    blackelems, coloredelems = get_mesh_components(grid, colorcode)

    if len(blackelems) != 0:
        blackgrid: Triangulation = create_submesh(blackelems, nodes)
        blackmap: ListedColormap = ListedColormap([0, 0, 0, 1])
        blackcolors: np.ndarray = np.ones(blackelems.shape[0])
        ax.tripcolor(blackgrid, facecolors=blackcolors, cmap=blackmap)

    if len(coloredelems) != 0:
        colorgrid: Triangulation = create_submesh(coloredelems, nodes)
        colors: np.ndarray = colorfilter(colorcode)
        cmap = mpl.colormaps['PuOr']
        elem = ax.tripcolor(colorgrid, facecolors=colors, cmap=cmap)
        cb = fig.colorbar(elem, drawedges=False, spacing='proportional', extendrect=False, orientation='vertical',
                          aspect=50, pad=0.05, fraction=0.05, format='%1i')
        cb.ax.set(xlabel='el2r')
        modify_cb_label(int(min(colors)), int(max(colors)), cb)

    return fig, ax


def get_entity_colorcode(entity2regi: np.ndarray, r2color: set) -> np.ndarray:
    """check, if specific regions are a region of an entity that belongs to the mesh

    Parameters
    ----------
    entity2regi : np.ndarray
        (P,) array. the entity2regi indication. An entity is either a node, an edge or an element. P entities
    r2color : set
        The regi_ids of the regions to visualize.

    Returns
    -------
    entities2color : np.ndarray
        a specific entity2regi indication. If the entry is -1, the regi is not part of those that shall be colored.
        else, the entry has the same idx as one of the regions, that shall be colored
    """
    entities2color: np.ndarray = -1 * np.ones_like(entity2regi)
    for idx, regi_id in enumerate(entity2regi):
        if regi_id in r2color:
            entities2color[idx] = regi_id
    return entities2color


def visualize_regions(mesh: TriMesh, regions: Regions, **kwargs) -> Tuple[Figure, Axes]:
    """Visualize the regions in a mesh.

    This function plots the regions in a mesh. The regions are visualized by coloring the entities in the mesh according
    to the region they belong to.

    Parameters
    ----------
    mesh : TriMesh
        The mesh that the regions are defined on.
    regions : Regions
        The regions to visualize.
    kwargs : dict
        Additional keyword arguments to pass to the plotting function:
            - ``fig``: The figure to plot on.
            - ``ax``: The axes to plot on.

    Returns
    -------
    fig : Figure
        The figure that was plotted on.
    ax : Axes
        The axes that was plotted on.
    """
    fig: Figure = kwargs.pop('fig', None)
    ax: Axes = kwargs.pop('ax', None)
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot()

    regions2color_ids: set = set(regions.get_keys())
    edges2color: np.ndarray = get_entity_colorcode(mesh.edge2regi, regions2color_ids)
    nodes2color: np.ndarray = get_entity_colorcode(mesh.node2regi, regions2color_ids)
    elems2color: np.ndarray = get_entity_colorcode(mesh.elem2regi, regions2color_ids)
    fig, ax = plot_triangles(mesh.elem2node, mesh.node, elems2color, ax, fig)
    fig, ax = plot_edges(mesh.edge2node, mesh.node, edges2color, ax, fig)
    fig, ax = plot_nodes(mesh.node, nodes2color, ax, fig)

    return fig, ax
