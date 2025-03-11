# coding=utf-8
"""Input-Output-Toolbox

.. sectionauthor:: Bundschuh
"""

from typing import Union, List, Any, Iterable, Dict, Tuple, TYPE_CHECKING
from pathlib import Path
from contextlib import contextmanager
import pickle
import datetime as dt
import io
import xml.etree.ElementTree as et
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pyrit import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from pyrit.mesh import TriMesh, TetMesh


def dumps_with_ignore(obj: Any, ignore_attributes: List[str] = None, **kwargs) -> bytes:
    """Convert an object to bytes with pickle and ignore the given attributes of the object

    Parameters
    ----------
    obj : Any
        The object to pickle
    ignore_attributes : List[str]
        A list of the attribute names on the object to ignore for pickling
    kwargs : Any
        Keyword arguments passed to the method `dumps` from the :py:mod:`pickle` module

    Returns
    -------
    dumped_obj : bytes
        Byte representation of the object from pickle module
    """
    if ignore_attributes is None:
        return pickle.dumps(obj, **kwargs)

    # Save the attributes to ignore temporarily in another dict
    tmp_dict = {}
    if ignore_attributes:
        for attribute in ignore_attributes:
            try:
                tmp_dict[attribute] = obj.__getattribute__(attribute)
                delattr(obj, attribute)
            except AttributeError:
                logger.warning("The object does not contain the attribute '%s'. It is ignored.", attribute)

    # Dump the object
    dumped_obj = pickle.dumps(obj, **kwargs)

    # Write the ignored attributes back to the object
    if ignore_attributes:
        for attribute in ignore_attributes:
            try:
                obj.__setattr__(attribute, tmp_dict[attribute])
            except KeyError:
                logger.info("The key '%s' does not exist and the object attribute cannot be set.", attribute)

    return dumped_obj


def process_path(path: Union[str, 'Path'], suffix: str = None) -> 'Path':
    """Process a given path to a valid path from the :py:mod:`pathlib` module.

    Parameters
    ----------
    path : Union[str, 'Path']
        The path to process.
    suffix : str, optional
        The suffix of the path. For example '.txt'. A valid suffix must start with a dot. Default is None.

    Returns
    -------
    path : Path
        A valid path
    """
    if suffix is None:
        path = Path(path)
    else:
        path = Path(path).with_suffix(suffix)

    if not path.parent.exists():
        logger.info("Creating path: %s.", str(path.parent))
        path.parent.mkdir()

    return path


def save(obj: Any, path: Union[str, 'Path'], ignore_attributes: List[str] = None, **kwargs) -> 'Path':
    """Saves the given object.

    Parameters
    ----------
    obj : Any
        Any object that should be saved in a file.
    path : Union[str, Path]
        The path. If a string is given, it is converted to a Path object. The file ending can but must not be given.
        In any case it will be a *.pkl* file. See `pickle doc <https://docs.python.org/3/library/pickle.html>`_ for
        more information.
        If the path contains a non-existing folder, this folder will be created.
    ignore_attributes: List[str], optional
        A list of attributes that are not included in the saved file. By default, all attributes are included.

    Returns
    -------
    path : Path
        The path that was used for opening the file.
    """
    path = process_path(path, '.pkl')

    dumped_obj = dumps_with_ignore(obj, ignore_attributes, protocol=pickle.HIGHEST_PROTOCOL, **kwargs)

    logger.info("Saving to %s.", str(path))
    with open(path, 'wb') as file:
        file.write(bytearray(dumped_obj))
    logger.info("Done saving.")

    return path


def load(path: Union[str, Path], **kwargs) -> Any:
    """Load an object from a file.

    Parameters
    ----------
    path : Union[str, Path]
        The path. If a string is given, it is converted to a Path object. The file ending can but must not be given.
        In any case it will be a *.pkl* file. See `pickle doc <https://docs.python.org/3/library/pickle.html>`_ for
        more information.

    Returns
    -------
    obj : Any
        The loaded object.
    """
    path = Path(path).with_suffix('.pkl')

    logger.info("Start reading from %s.", str(path))
    with open(path, 'rb') as file:
        obj = pickle.load(file, **kwargs)
    logger.info("Done reading problem.")

    return obj


class ToLaTeX:
    """Export data for plotting in LaTeX using TikZ and pgfplots."""

    def __init__(self, **kwargs):
        """Constructor.

        Parameters
        ----------
        kwargs :
            Default keyword arguments for subsequent methods. If a keyword argument is not given in a method call, but
            was given in the constructor, it is used in the method. So you can set a default for multiple methods.
        """
        self.kwargs = kwargs

    def _parse_kwargs(self, **kwargs):
        """Parse the kwargs.

        If a kwarg is not given in a function, it is taken from the object (if given).
        """
        for key, val in self.kwargs.items():
            if key not in kwargs:
                kwargs[key] = val
        return kwargs

    def comment(self, msg: str, **kwargs) -> str:
        """Convert a string to a comment.

        Splits the `msh` at line breaks and starts every line with the `comment_string` of the `kwargs`.

        Parameters
        ----------
        msg : str
            The message to process.
        kwargs :
            From the keyword arguments, the key 'comment_string' is used.

        Returns
        -------
        out : str
            The formatted message.
        """
        kwargs = self._parse_kwargs(**kwargs)

        comment_string = kwargs.setdefault('comment_string', '# ')

        msg = msg.strip()
        out = ''
        for s in msg.split('\n'):
            out = out + comment_string + s + '\n'
        return out

    @staticmethod
    def check_parent(path: Path):
        """Creates the parent directory of the path, if it does not exist.

        Parameters
        ----------
        path : Path
        """
        if not path.parent.exists():
            logger.info("Creating path: %s.", str(path.parent))
            path.parent.mkdir()

    @contextmanager
    def open(self, path: Path, message: Union[str, Iterable[str]] = None, **kwargs):
        """Context manager for opening a file and adding basic information.

        Parameters
        ----------
        path : Path
            The path.
        message : Union[str, Iterable[str]], optional
            The message to add at the top of the file.
        kwargs :
            Additional keyword arguments. The key 'file_header' is used.
        """
        kwargs = self._parse_kwargs(**kwargs)

        file_header = kwargs.setdefault('file_header', True)
        logger.info("Saving to %s.", str(path))
        with open(path, 'wt') as file:  # pylint: disable=unspecified-encoding
            if isinstance(file_header, bool):
                if file_header:
                    file.write(self.comment('Created: ' + dt.datetime.now().strftime("%B %d, %Y; %H:%M:%S"), **kwargs))
            else:
                file.write(file_header)
            if message is not None:
                if isinstance(message, str):
                    message = [message, ]
                for m in message:
                    file.write(self.comment(m, **kwargs))
            yield file
        logger.info("Done saving.")

    def save_dat(self, data: Union[pd.DataFrame, Dict, Iterable[np.ndarray], np.ndarray], path: Union[str, Path],
                 message: Union[str, Iterable[str]] = None, **kwargs) -> Path:
        r"""Save data to a .dat file.

        Save data to .dat file. This file format can be used to plot the data with pgfplots in LaTeX.
        Besides the data, you can give a number of messages that are put at the top of the file as a comment.

        Parameters
        ----------
        data : Union[pd.DataFrame, Dict, Iterable[np.ndarray], np.ndarray]
            The data to save. If ``data`` is a DataFrame, nothing is changed. If not, it is converted to a DataFrame.
        path : Union[str, Path]
            The path where to save the file. If a string is given, it is converted to a Path object. The file ending can
            but must not be given.
        message : Union[str, Iterable[str]]
            A message put as a comment at the top of the file.
        kwargs : Any
            Additional arguments. With 'comment_string' you can determine the string that is used to initialize a
            commented line (used for messages).
            The remaining arguments are passed to :py:meth:`pandas.DataFrame.to_csv`

        Returns
        -------
        path : Path
            The path where the file was saved.

        Examples
        --------
        Here a small example how to use the generated .dat-file to plot in LaTeX.

        Suppose you saved following data:

        >>> time = np.arange(10)
        >>> data = {'time': time, 'func': time**2}
        >>> save_dat(data, 'data')

        Then, the most simple way to plot this data in LaTeX is by:

        .. code-block:: latex

            \begin{tikzpicture}
                \begin{axis}[xlabel={time $t$},ylabel={$f(t)$}]
                    \addplot+[] table[x=time, y=func] {data.dat};
                \end{axis}
            \end{tikzpicture}

        Note that the packages `tikzpicture` and `pgfplots` have to be loaded. This plot can then be extended as
        desired. For more information about this, see https://www.ctan.org/pkg/pgf
        """
        kwargs = self._parse_kwargs(**kwargs)

        path = Path(path).with_suffix('.dat')

        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame(data)

        sep = kwargs.pop('sep', ' ')
        lineterminator = kwargs.pop('lineterminator', '\n')
        index = kwargs.pop('index', False)

        with self.open(path, message, **kwargs) as file:
            kwargs.pop('comment_string', None)
            kwargs.pop('file_header', None)
            file.write(df.to_csv(sep=sep, lineterminator=lineterminator, index=index, **kwargs))

        return path

    def load_dat(self, path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """Load from .dat-file.

        Parameters
        ----------
        path : Union[str, Path]
            The path to load from.
        kwargs :
            Additional arguments. With `comment_string` you can determine which lines should be ignored (when they begin
            with that string). The remaining arguments are passed to :py:meth:`pandas.DataFrame.load_csv`.

        Returns
        -------
        data : pd.DataFrame
            The loaded data
        """
        kwargs = self._parse_kwargs(**kwargs)

        path = Path(path).with_suffix('.dat')

        sep = kwargs.pop('sep', ' ')
        comment_string = kwargs.pop('comment_string', '#')
        logger.info("Start reading .dat-file from %s.", str(path))
        with open(path, 'rt') as file:  # pylint: disable=unspecified-encoding
            lines = file.readlines()
            for k, line in enumerate(lines):
                if not line.startswith(comment_string):
                    break
            data_lines = lines[k:]  # pylint: disable=undefined-loop-variable
            data = pd.read_csv(io.StringIO(''.join(data_lines)), sep=sep, **kwargs)
        logger.info("Done reading.")

        return data

    def export_trimesh(self, mesh: 'TriMesh', path: Union[str, Path], message: Union[str, Iterable[str]] = None,
                       one_file: bool = False, **kwargs) -> Union[Path, Tuple[Path]]:
        r"""Save a trimesh to a dat file.

        Parameters
        ----------
        mesh : TriMesh
            The mesh.
        path : Path
            The path.
        message : Union[str, Iterable[str]], optional
            The message to add at the top of the file. If an Iterable is given. Each element is a separate line.
            Default is None
        one_file : bool, optional
            If True, one file is generated. If False, two files are generated. Two files use less memory.
        kwargs :
            Additional keyword arguments. 'sep' is the separator between two entries, 'lineterminator' is the string
            that ends a line. If `one_file` is False, 'nodes_file_appendix' is a string that is added to the file name
            of the file with node information and 'elements_file_appendix' to the file name of the file with element
            information. The rest is passed to subsequent method calls (:py:meth:`comment` and :py:meth:`open`).

        Returns
        -------
        path: Union[Path, Tuple[Path]]
            If `one_file` is True, the path of this file. If `one_file` is False, the path of the elements and the path
            of the nodes.

        Notes
        -----
        The pgfplotslibrary *patchplots* can be loaded for more options, but is not necessary.
        The LaTeX code for one file is:

        .. code-block:: latex

            \begin{tikzpicture}
                \begin{axis}[axis equal image, colormap={whitecm}{color=(white) color=(white)}]
                    \addplot[line width=0.1pt, faceted color=black] [patch] table {mesh.dat};
                \end{axis}
            \end{tikzpicture}

        and for two files:

        .. code-block:: latex

            \begin{tikzpicture}%two files
                \begin{axis}[axis equal image, colormap={whitecm}{color=(white) color=(white)}]
                    \addplot[line width=0.1pt,faceted color=black, patch table={mesh_elements.dat}] [patch] table
                    {mesh_nodes.dat};
                \end{axis}
            \end{tikzpicture}
        """
        kwargs = self._parse_kwargs(**kwargs)

        path = Path(path).with_suffix('.dat')

        sep = kwargs.pop('sep', ' ')
        lineterminator = kwargs.pop('lineterminator', '\n')

        if one_file:
            with self.open(path, message, **kwargs) as file:
                for nodes in mesh.elem2node:
                    for node in nodes:
                        n = mesh.node[node]
                        file.write(f"{n[0]}" + sep + f"{n[1]}" + lineterminator)
            return path
        # else

        nodes_file_appendix = kwargs.pop('nodes_file_appendix', '_nodes')
        elements_file_appendix = kwargs.pop('elements_file_appendix', '_elements')

        path_node = path.with_name(path.stem + nodes_file_appendix).with_suffix(path.suffix)
        path_element = path.with_name(path.stem + elements_file_appendix).with_suffix(path.suffix)

        with self.open(path_node, message, **kwargs) as file:
            file.write(self.comment(f'This is the node file. '
                                    f'The corresponding element file is \'{path_element.name}\'.', **kwargs))
            for node in mesh.node:
                file.write(f"{node[0]}" + sep + f"{node[1]}" + lineterminator)

        with self.open(path_element, message, **kwargs) as file:
            file.write(self.comment(f'This is the element file. '
                                    f'The corresponding node file is \'{path_node.name}\'.', **kwargs))
            for element in mesh.elem2node:
                file.write(f"{element[0]}" + sep + f"{element[1]}" + sep + f"{element[2]}" + lineterminator)

        return path_node, path_element

    def export_field(self, mesh: 'TriMesh', field: np.ndarray, path: Union[str, Path],
                     message: Union[str, Iterable[str]] = None, one_file: bool = False, **kwargs) \
            -> Union[Path, Tuple[Path]]:
        r"""Export a field to a .dat file.

        A field that is allocated on the elements or the nodes of the mesh is exported.

        Parameters
        ----------
        mesh : TriMesh
            The mesh
        field : np.ndarray
            The field. Must be a one dimensional array. Its size must be the number of elements or the number of nodes
            of the mesh.
        path : Union[str, Path]
            A Path or a string representing the path. The suffix will be ignored.
        message : Union[str, Iterable[str]], optional
            A message or a number of messages placed at the top of the written files. Default is None
        one_file : bool
            If True, only one file is generated. If False, two files are generated. This uses less memory.
        kwargs :
            Additional keyword arguments. 'sep' is the separator between two entries, 'lineterminator' is the string
            that ends a line. If `one_file` is False, 'nodes_file_appendix' is a string that is added to the file name
            of the file with node information and 'elements_file_appendix' to the file name of the file with element
            information. The rest is passed to subsequent method calls (:py:meth:`comment` and :py:meth:`open`).

        Returns
        -------
        path: Union[Path, Tuple[Path]]
            If `one_file` is True, the path of this file. If `one_file` is False, the path of the elements and the path
            of the nodes.

        Notes
        -----
        In the following code examples, only the field is plotted. If you also want to plot the mesh, add the options
        `line width=0.1pt,faceted color=black` in the `\addplot`-command. The pgfplotslibrary *patchplots* can be loaded
        for more options, but is not necessary.

        The LaTeX code for one file (nodal data and element wise data) is:

        .. code-block:: latex

            \begin{tikzpicture}
                \begin{axis}[axis equal image,colormap name=viridis, colorbar]
                    \addplot [patch,shader=interp]
                    table [point meta=\thisrow{v}] {file.dat};
                \end{axis}
            \end{tikzpicture}

        For nodal data and two files:

        .. code-block:: latex

            \begin{tikzpicture}
                \begin{axis}[axis equal image, colormap name=viridis, colorbar]
                    \addplot [line width=0pt,faceted color=none,patch,patch table={file_elements.dat}]
                    table [point meta=\thisrow{v}] {file_nodes.dat};
                \end{axis}
            \end{tikzpicture}

        For element wise data and two files:

        .. code-block:: latex

            \begin{tikzpicture}
                \begin{axis}[axis equal image, colormap name=viridis, colorbar]
                    \addplot [line width=0pt,faceted color=none, patch,patch table with point meta={file_elements.dat}]
                    table {file_nodes.dat};
                \end{axis}
            \end{tikzpicture}
        """
        kwargs = self._parse_kwargs(**kwargs)

        path = Path(path).with_suffix('.dat')

        flag_nodal: bool
        if field.shape[0] == mesh.num_node:
            flag_nodal = True
        elif field.shape[0] == mesh.num_elem:
            flag_nodal = False
        else:
            raise ValueError(f"field has length {field.shape[0]} but should be {mesh.num_node}, the number of nodes.")

        sep = kwargs.pop('sep', ' ')
        lineterminator = kwargs.pop('lineterminator', '\n')

        if one_file and flag_nodal:
            with self.open(path, message, **kwargs) as file:
                file.write("r" + sep + "z" + sep + "v" + lineterminator)
                for nodes in mesh.elem2node:
                    for node in nodes:
                        n = mesh.node[node]
                        file.write(f"{n[0]}" + sep + f"{n[1]}" + sep + f"{field[node]}" + lineterminator)

            return path

        if one_file and not flag_nodal:
            with self.open(path, message, **kwargs) as file:
                file.write("r" + sep + "z" + sep + "v" + lineterminator)
                for element, nodes in enumerate(mesh.elem2node):
                    for node in nodes:
                        n = mesh.node[node]
                        file.write(f"{n[0]}" + sep + f"{n[1]}" + sep + f"{field[element]}" + lineterminator)

            return path

        # one_file is False

        nodes_file_appendix = kwargs.pop('nodes_file_appendix', '_nodes')
        elements_file_appendix = kwargs.pop('elements_file_appendix', '_elements')

        path_node = path.with_name(path.stem + nodes_file_appendix).with_suffix(path.suffix)
        path_element = path.with_name(path.stem + elements_file_appendix).with_suffix(path.suffix)

        if flag_nodal:
            # file with elements to nodes
            with self.open(path_element, message, **kwargs) as file:
                file.write(self.comment(f'This is the element file. '
                                        f'The corresponding node file is \'{path_node.name}\'.', **kwargs))
                for element in mesh.elem2node:
                    file.write(f"{element[0]}" + sep + f"{element[1]}" + sep + f"{element[2]}" + lineterminator)

            # file with nodes and values
            with self.open(path_node, message, **kwargs) as file:
                file.write(
                    self.comment(f'This is the node file. '
                                 f'The corresponding element file is \'{path_element.name}\'.', **kwargs))
                file.write("r" + sep + "z" + sep + "v" + lineterminator)
                for k, node in enumerate(mesh.node):
                    file.write(f"{node[0]}" + sep + f"{node[1]}" + sep + f"{field[k]}" + lineterminator)
        else:
            # file with elements and values
            with self.open(path_element, message, **kwargs) as file:
                file.write(self.comment(f'This is the element file. '
                                        f'The corresponding node file is \'{path_node.name}\'.', **kwargs))
                for k, element in enumerate(mesh.elem2node):
                    file.write(f"{element[0]}" + sep + f"{element[1]}" + sep + f"{element[2]}" + sep +  # noqa:W504
                               f"{field[k]}" + sep + lineterminator)

            # file with nodes
            with self.open(path_node, message, **kwargs) as file:
                file.write(
                    self.comment(f'This is the node file. '
                                 f'The corresponding element file is \'{path_element.name}\'.', **kwargs))
                for node in mesh.node:
                    file.write(f"{node[0]}" + sep + f"{node[1]}" + lineterminator)

        return path_element, path_node

    def export_nodes(self, mesh: 'TriMesh', node_indices: Iterable[int], path: Union[str, Path],
                     message: Union[str, Iterable[str]] = None, **kwargs) -> Path:
        """Export nodes of the mesh to LaTeX.

        Parameters
        ----------
        mesh : TriMesh
            The mesh.
        node_indices : Iterable[int]
            Iterable ove node indices.
        path : Union[str, Path]
            A Path or a string representing the path. The suffix will be ignored.
        message : Union[str, Iterable[str]]
            A message or a number of messages placed at the top of the written files. Default is None
        kwargs :
            Additional keyword arguments. 'tikz_cs' is the coordinate system, the points are declared in, 'options'
            is a string of options that is added to the draw command, 'command' is the tikz-command for a line and
            'radius' is the radius of a node. The rest is passed to :py:meth:`open`.

        Returns
        -------
        path : Path
            The path of the saved file.
        """
        kwargs = self._parse_kwargs(**kwargs)

        path = Path(path).with_suffix('.tex')

        if 'comment_string' not in kwargs:
            kwargs['comment_string'] = '% '

        tikz_cs = kwargs.pop('tikz_cs', 'axis cs:')
        command = kwargs.pop('command', r"\fill")
        options = kwargs.pop('options', "black")
        radius = kwargs.pop('radius', '1pt')

        with self.open(path, message, **kwargs) as file:
            for index in node_indices:
                file.write(f"{command}[{options}] ({tikz_cs}{mesh.node[index][0]},{mesh.node[index][1]}) "
                           f"circle ({radius});\n")

        return path

    def export_edges(self, mesh: 'TriMesh', edge_indices: Iterable[int], path: Union[str, Path],
                     message: Union[str, Iterable[str]] = None, **kwargs) -> Path:
        """Export edges of the mesh to LaTeX

        Parameters
        ----------
        mesh : TriMesh
            The mesh.
        edge_indices : Iterable[int]
            Iterable over edge indices.
        path : Union[str, Path]
            A Path or a string representing the path. The suffix will be ignored.
        message : Union[str, Iterable[str]], optional
            A message or a number of messages placed at the top of the written files. Default is None
        kwargs :
            Additional keyword arguments. 'tikz_cs' is the coordinate system, the points are declared in, and 'options'
            is a string of options that is added to the draw command. The rest is passed to :py:meth:`open`.

        Returns
        -------
        path : Path
            The path of the saved file.
        """
        kwargs = self._parse_kwargs(**kwargs)

        path = Path(path).with_suffix('.tex')
        tikz_cs = kwargs.pop('tikz_cs', 'axis cs:')
        options = kwargs.pop('options', None)

        if 'comment_string' not in kwargs:
            kwargs['comment_string'] = '% '

        if options is not None:
            option_str = f"[{options}]"
        else:
            option_str = ''

        with self.open(path, message, **kwargs) as file:
            for index in edge_indices:
                node1, node2 = mesh.edge2node[index]
                file.write(r"\draw" + f"{option_str} ({tikz_cs}{mesh.node[node1][0]},{mesh.node[node1][1]}) -- "
                                      f"({tikz_cs}{mesh.node[node2][0]},{mesh.node[node2][1]});\n")

        return path

    def export_elements(self, mesh: 'TriMesh', element_indices: Iterable[int], path: Union[str, Path],
                        message: Union[str, Iterable[str]] = None, **kwargs) -> Path:
        """Export elements of the mesh to LaTeX

        Parameters
        ----------
        mesh : TriMesh
            The mesh.
        element_indices : Iterable[int]
            Iterable over the element indices.
        path : Path
            A Path or a string representing the path. The suffix will be ignored.
        message : Union[str, Iterable[str]], optional
            A message or a number of messages placed at the top of the written files. Default is None
        kwargs :
            Additional keyword arguments. 'tikz_cs' is the coordinate system, the points are declared in, and 'options'
            is a string of options that is added to the draw command. The rest is passed to :py:meth:`open`.

        Returns
        -------
        path : Path
            The path of the saved file.
        """
        kwargs = self._parse_kwargs(**kwargs)

        path = Path(path).with_suffix('.tex')

        if 'comment_string' not in kwargs:
            kwargs['comment_string'] = '% '

        tikz_cs = kwargs.pop('tikz_cs', 'axis cs:')
        options = kwargs.pop('options', None)

        if options is not None:
            option_str = f"[{options}]"
        else:
            option_str = ''

        with self.open(path, message, **kwargs) as file:
            for index in element_indices:
                node1, node2, node3 = mesh.elem2node[index]
                file.write(r"\draw " + f"{option_str}" +  # noqa:W504
                           f"({tikz_cs}{mesh.node[node1][0]},{mesh.node[node1][1]}) -- "
                           f"({tikz_cs}{mesh.node[node2][0]},{mesh.node[node2][1]}) -- "
                           f"({tikz_cs}{mesh.node[node3][0]},{mesh.node[node3][1]}) -- cycle;\n")

        return path

    def export_region_edges(self, mesh: 'TriMesh', path: Union[str, Path], message: Union[str, Iterable[str]] = None,
                            **kwargs) -> Path:
        """Export all edges that divide two regions or are at the outer boundary.

        Use :py:meth:`export_edges` to export the edges.

        Parameters
        ----------
        mesh : TriMesh
            The mesh.
        path : Union[str, Path]
            A Path or a string representing the path. The suffix will be ignored.
        message : Union[str, Iterable[str]], optional
            A message or a number of messages placed at the top of the written files. Default is None
        kwargs :
            Additional keyword arguments. All passed to :py:meth:`export_edges`.

        Returns
        -------
        path : Path
            The path of the saved file.
        """
        kwargs = self._parse_kwargs(**kwargs)

        if 'comment_string' not in kwargs:
            kwargs['comment_string'] = '% '

        edges = []
        for edge in range(mesh.num_edge):
            elems = mesh.edge2elem[edge]
            if mesh.elem2regi[elems[0]] != mesh.elem2regi[elems[1]] or elems[1] == -1:
                edges.append(edge)

        return self.export_edges(mesh, edges, path, message, **kwargs)

    def export_contour(self, mesh: 'TriMesh', field: np.ndarray, path: Union[str, Path],
                       message: Union[str, Iterable[str]] = None, **kwargs):
        r"""Export the contour lines of a field.

        Parameters
        ----------
        mesh : TriMesh
            A mesh object
        field : np.ndarray
            A field
        path : Union[str, Path]
            The path to save to the file to
        message : Union[str, Iterable[str]]
            A message that it put at the top of the file. If an iterable, each item is put on a separate line. Each line
            is started with the comment string.
        kwargs :
            Other options.

        Notes
        -----
        Instruction to display the result in LaTeX:

        .. code-block:: latex

            \begin{tikzpicture}
                \begin{axis}[axis equal image, unbounded coords=jump]
                    \addplot table {data.dat};
                \end{axis}
            \end{tikzpicture}

        Returns
        -------
        path : Path
            The path of the saved file.
        """
        kwargs = self._parse_kwargs(**kwargs)
        num_lines = kwargs.pop('num_Lines', 40)
        path = Path(path).with_suffix('.dat')

        fig, ax, _ = mesh.plot_equilines(field, num_lines)
        plt.close(fig)
        lines = []
        for col in ax.collections:
            try:
                segments = col.get_paths()
                for segment in segments:
                    lines.append(segment.vertices)
            except AttributeError:
                print("Attribute Error")

        # lines = [col.get_segments()[0] for col in ax.collections]

        sep = kwargs.pop('sep', ' ')
        lineterminator = kwargs.pop('lineterminator', '\n')
        with self.open(path, message, **kwargs) as file:
            # file.write("r" + sep + "z" + sep + "v" + lineterminator)
            for line in lines:
                x, y = line[:, 0], line[:, 1]
                num_points = len(x)
                for k in range(num_points):
                    file.write(str(x[k]) + sep + str(y[k]) + lineterminator)
                file.write(str(x[0]) + sep + str(y[0]) + lineterminator)
                file.write('0' + sep + 'nan' + lineterminator)

        return path


class ParaviewExportError(Exception):
    """An exception for errors during export to Paraview."""


# pylint: disable=line-too-long
@dataclass
class ToParaview:
    """Class to handle export to Paraview.

    The class can export meshes and data allocated at nodes or elements of the mesh to Paraview. It writes a xml file
    with a special file ending such that it can be imported into Paraview.

    Examples
    --------
    Suppose you have the solution object you received from a two-dimensional, electrostatic simulation. Now you want to
    export the potential to Paraview for further post-processing.
    First, import the class `ToParaview` and create an object.

    >>> from pyrit.toolbox.IOToolbox import ToParaview
    >>> to_paraview = ToParaview()

    Then, select the data you want to save. For instance, we want to save the scalar potential and the permittivity.
    The former is node-wise data, the latter is element-wise data.

    >>> solution: ElectricSolutionCart
    >>> node_wise_data = {'potential': solution.potential}
    >>> element_wise_data = {'permittivity': np.array([solution.materials.get_material(solution.regions.get_regi(r).mat).get_property(Permittivity).value for r in solution.mesh.elem2regi])}

    Next, save the mesh and data to a file:

    >>> path = to_paraview.save_tri_mesh('solution', solution.mesh, node_wise_data, element_wise_data)

    The returned path is a path to the saved file.


    Notes
    -----
    See also the website of `Paraview <https://www.paraview.org/>`_ and
    the `vtk users guide <https://vtk.org/wp-content/uploads/2021/08/VTKUsersGuide.pdf>`_
    """

    version: float = 2.2  #: Version of the vtk file format
    number_format: str = "ascii"  #: Number format in the vtk file
    int_data_type_string: str = "Int32"  #: Integer data type string for the vtk file
    float_data_type_string: str = "Float64"  #: Float data type string for the vtk file

    def save_tri_mesh(self, path: Union[str, 'Path'], mesh: 'TriMesh', node_wise_data: Dict[str, np.ndarray] = None,
                      element_wise_data: Dict[str, np.ndarray] = None, **kwargs) -> Path:
        """Save a triangular mesh along with data defined on the mesh.

        Parameters
        ----------
        path : Union[str, 'Path']
            A Path. If a string is given, it is converted to a Path object. The file ending will be set.
        mesh : TriMesh
            A :py:class:`~pyrit.mesh.TriMesh` object
        node_wise_data : Dict[str, np.ndarray]
            A dictionary with the node-wise data. The key is a string with the name of the data and the value is an
            array containing the data. With :math:`N` being the number of nodes, supported array shapes are:

                - :math:`(N,)`: Scalar data per node
                - :math:`(N,1)`: Scalar data per node
                - :math:`(N,2)`: Vector data per node (last component is zero)
                - :math:`(N,3)`: Vector data per node

        element_wise_data : Dict[str, np.ndarray]
            A dictionary with the element-wise data. The key is a string with the name of the data and the value is an
            array containing the data. With :math:`E` being the number of elements, supported array shapes are:

                - :math:`(E,)`: Scalar data per element
                - :math:`(E,1)`: Scalar data per element
                - :math:`(E,2)`: Vector data per element (last component is zero)
                - :math:`(E,3)`: Vector data per element
        kwargs : Any
            Additional keyword arguments. Available are the object attributes.

        Returns
        -------
        path : Path
            The path to the file
        """
        return self._save_mesh(path, np.hstack((mesh.node, np.zeros((mesh.num_node, 1)))), mesh.elem2node, 5,
                               node_wise_data, element_wise_data, **kwargs)

    def save_tet_mesh(self, path: Union[str, 'Path'], mesh: 'TetMesh', node_wise_data: Dict[str, np.ndarray] = None,
                      element_wise_data: Dict[str, np.ndarray] = None, **kwargs):
        """Save a tetrahedral mesh along with data defined on the mesh.

        Parameters
        ----------
        path : Union[str, 'Path']
            A Path. If a string is given, it is converted to a Path object. The file ending will be set.
        mesh : TetMesh
            A :py:class:`~pyrit.mesh.TetMesh` object
        node_wise_data : Dict[str, np.ndarray]
            A dictionary with the nodewise data. The key is a string with the name of the data and the value is an
            array containing the data. With :math:`N` being the number of nodes, supported array shapes are:

                - :math:`(N,)`: Scalar data per node
                - :math:`(N,1)`: Scalar data per node
                - :math:`(N,2)`: Vector data per node (last component is zero)
                - :math:`(N,3)`: Vector data per node

        element_wise_data : Dict[str, np.ndarray]
            A dictionary with the elementwise data. The key is a string with the name of the data and the value is an
            array containing the data. With :math:`E` being the number of elements, supported array shapes are:

                - :math:`(E,)`: Scalar data per element
                - :math:`(E,1)`: Scalar data per element
                - :math:`(E,2)`: Vector data per element (last component is zero)
                - :math:`(E,3)`: Vector data per element
        kwargs : Any
            Additional keyword arguments. Available are the object attributes.

        Returns
        -------
        path : Path
            The path to the file
        """
        return self._save_mesh(path, mesh.node, mesh.elem2node, 10, node_wise_data, element_wise_data, **kwargs)

    def _array_to_string(self, array: np.ndarray, **kwargs) -> str:
        """Generate a string of an array to save it in a xml file.

        Parameters
        ----------
        array : np.ndarray
            The array to process
        kwargs : Any
            - number_format: "binary" or "acsii"

        Returns
        -------
        array_string : str
            String representation of the array

        Raises
        ------
        ParaviewExportError : When the number format is unknown
        """
        number_format = kwargs.pop('number_format', self.number_format)
        if number_format == "binary":
            return array.tobytes()
        if number_format == "ascii":
            return " ".join(map(str, np.real(array.flatten())))
        raise ParaviewExportError("Number format unknown")

    def _format_data(self, pw_data: np.ndarray) -> Tuple[int, np.ndarray]:
        """Format data to save in a xml file

        Parameters
        ----------
        pw_data : np.ndarray
            The data to format

        Returns
        -------
        number_components : int
            The number of components per entity. 1 for scalar data and 3 for vector data
        formatted_data : np.ndarray
            The formatted data

        Raises
        ------
        ParaviewExportError : When the data format is unsupported.
        """
        if len(pw_data.shape) == 1:
            number_components, formatted_data = 1, pw_data
        elif len(pw_data.shape) == 2:
            if pw_data.shape[1] == 1:
                number_components, formatted_data = 1, pw_data.flatten()
            elif pw_data.shape[1] == 2:
                formatted_data = np.hstack((pw_data, np.zeros((pw_data.shape[0], 1)))).flatten()
                number_components = 3
            elif pw_data.shape[1] == 3:
                formatted_data = pw_data.flatten()
                number_components = 3
            else:
                raise ParaviewExportError(f"Unsupported data format. Second dimension too large: {pw_data.shape[1]}")
        else:
            raise ParaviewExportError(f"Unsupported data format. Too many dimensions: f{len(pw_data.shape)}")

        return number_components, formatted_data

    def _get_data_type_string(self, data: np.ndarray, **kwargs) -> str:
        """Return the data type string for the DataArray element in the xml file.

        Parameters
        ----------
        data : np.ndarray

        Returns
        -------
        data_type_string : str
            Data type string.

        Raises
        ------
        ParaviewExportError : If the data type of the data is unsupported.
        """
        if issubclass(data.dtype.type, np.complexfloating):
            raise ParaviewExportError("Unsupported data type: complex")
        if issubclass(data.dtype.type, np.integer):
            return kwargs.get("int_data_type_string", self.int_data_type_string)
        if issubclass(data.dtype.type, np.floating):
            return kwargs.get("float_data_type_string", self.float_data_type_string)
        raise ParaviewExportError(f"Unsupported data type: {data.dtype}")

    def _add_entity_wise_data(self, data_element: et.Element, entity_wise_data: Dict[str, np.ndarray] = None, **kwargs):
        """Add a 'DataArray' sub element to the data element for each entity-wise data.

        Parameters
        ----------
        data_element : et.Element
            An element from the python standard library xml.etree.ElementTree.Element.
        entity_wise_data : Dict[str, np.ndarray]
            A dictionary with the entity-wise data. The key is a string with the name of the data and the value is an
            array containing the data.
        kwargs : Any
            Additional keyword arguments. Available are the object attributes.
        """
        if entity_wise_data is None:
            return

        number_format = kwargs.get('number_format', self.number_format)

        for name, pw_data in entity_wise_data.items():
            pw_data: np.ndarray
            if issubclass(pw_data.dtype.type, np.complexfloating):
                self._add_entity_wise_data(data_element, {f"{name}_real": np.real(pw_data),
                                                          f"{name}_imaginary": np.imag(pw_data)}, **kwargs)
                continue
            number_components, formatted_data = self._format_data(pw_data)
            data_type_string = self._get_data_type_string(pw_data, **kwargs)

            pw_sub_element = et.SubElement(data_element, "DataArray", {"Name": name,
                                                                       "type": data_type_string,
                                                                       "format": number_format,
                                                                       "NumberOfComponents": str(number_components)})
            pw_sub_element.text = self._array_to_string(formatted_data, **kwargs)

    def _save_mesh(self, path: Union[str, 'Path'], node: np.ndarray, elem2node: np.ndarray, element_type: int,
                   node_wise_data: Dict[str, np.ndarray] = None, element_wise_data: Dict[str, np.ndarray] = None,
                   **kwargs) -> Path:
        """Save a mesh with data on the mesh to a .vtu file to be imported in Paraview.

        Parameters
        ----------
        path : Union[str, 'Path']
            A Path. If a string is given, it is converted to a Path object. The file ending will be set to .vtu
        node : np.ndarray
            A :math:`(N,3)` array with the node coordinates :math:`(x,y,z)`. (:math:`N` is the number of nodes)
        elem2node : np.ndarray
            A :math:`(E,K)` array with the element to node relations. (:math:`E` is the number of elements and :math:`K`
            is the number of nodes per element)
        element_type : int
            The vtk internal identifier of the cell type. See figure 19-20 in the vtk users guide for all cell types.
            (Triangles have `element_type=5` and tetrahedra have `element_type=10`)
        node_wise_data : Dict[str, np.ndarray]
            A dictionary with the node-wise data. The key is a string with the name of the data and the value is an
            array containing the data. With :math:`N` being the number of nodes, supported array shapes are:

                - :math:`(N,)`: Scalar data per node
                - :math:`(N,1)`: Scalar data per node
                - :math:`(N,2)`: Vector data per node (last component is zero)
                - :math:`(N,3)`: Vector data per node
        element_wise_data : Dict[str, np.ndarray]
            A dictionary with the element-wise data. The key is a string with the name of the data and the value is an
            array containing the data. With :math:`E` being the number of elements, supported array shapes are:

                - :math:`(E,)`: Scalar data per element
                - :math:`(E,1)`: Scalar data per element
                - :math:`(E,2)`: Vector data per element (last component is zero)
                - :math:`(E,3)`: Vector data per element
        kwargs : Any
            Additional keyword arguments. Available are the object attributes.

        Returns
        -------
        path : Path
            The path to the file
        """
        version = kwargs.pop('version', self.version)
        kwargs.setdefault("number_format", self.number_format)
        number_format = kwargs.get("number_format")
        path = process_path(path, '.vtu')

        if not len(node.shape) == 2 and node.shape[1] == 3:
            raise ParaviewExportError(f"Node data of unsupported shape: {node.shape}")
        if not len(elem2node.shape) == 2 and elem2node.shape[1] == 3:
            raise ParaviewExportError(f"Elem2node data of unsupported shape: {elem2node.shape}")

        num_node = node.shape[0]
        num_element = elem2node.shape[0]
        nodes_per_element = elem2node.shape[1]

        data = et.Element('VTKFile', {"type": "UnstructuredGrid", "version": str(version)})

        unstructured_grid = et.SubElement(data, 'UnstructuredGrid')

        piece = et.SubElement(unstructured_grid, "Piece", {"NumberOfPoints": str(num_node),
                                                           "NumberOfCells": str(num_element)})
        point_data = et.SubElement(piece, "PointData")
        cell_data = et.SubElement(piece, "CellData")
        points = et.SubElement(piece, "Points")
        cells = et.SubElement(piece, "Cells")

        points_data_array = et.SubElement(points, "DataArray", {"NumberOfComponents": "3",
                                                                "type": "Float64",
                                                                "Name": "Point data",
                                                                "format": number_format})
        points_data_array.text = self._array_to_string(node.flatten(), **kwargs)

        cells_data_array_connectivity = et.SubElement(cells, "DataArray", {"type": "Int32", "Name": "connectivity"})
        cells_data_array_offsets = et.SubElement(cells, "DataArray", {"type": "Int32", "Name": "offsets"})
        cells_data_array_types = et.SubElement(cells, "DataArray", {"type": "UInt8", "Name": "types"})

        cells_data_array_connectivity.text = self._array_to_string(elem2node.flatten(), **kwargs)
        cells_data_array_offsets.text = self._array_to_string(np.arange(nodes_per_element,
                                                                        nodes_per_element * num_element + 1,
                                                                        nodes_per_element), **kwargs)
        cells_data_array_types.text = self._array_to_string(element_type * np.ones(num_element, dtype=int), **kwargs)

        self._add_entity_wise_data(point_data, node_wise_data, **kwargs)
        self._add_entity_wise_data(cell_data, element_wise_data, **kwargs)
        try:
            et.indent(data)  # Available for Python version >= 3.9
        except AttributeError:
            pass
        with open(path, "wb") as f:
            f.write(et.tostring(data))

        return path
