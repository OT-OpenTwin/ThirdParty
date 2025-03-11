# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 09:44:49 2021

Contains the class MatProperty

.. sectionauthor:: Bundschuh
"""

from abc import ABC
import numpy as np

from pyrit import get_logger, ValueHandler

logger = get_logger(__name__)


class MatPropertyMeta(type):
    """Metaclass for setting the docstring is subclasses."""

    init_docstring_template = """
            Constructor of <name>

            Parameters
            ----------
            value :
                Value of the <name>. See :py:class:`~pyrit.material.MatProperty`.
            name : str, optional
                Name of the <name>. Default is ''
            data : np.ndarray, optional
                Data for a data-driven material. Default is None.

            Returns
            -------
            None.
            """

    def __new__(cls, name, bases, class_dict):
        """New method. Sets docstring of init"""
        class_obj = super().__new__(cls, name, bases, class_dict)

        class_obj.__init__.__doc__ = cls.init_docstring_template.replace('<name>', name)
        return class_obj


class MatProperty(ValueHandler, ABC):
    r"""Abstract class for material properties.

    The value of a property can be a float, an array or a callable. The following table summarizes what
    kind of value is understood as which material property. For the inhomogeneous values, two-dimensional cartesian
    coordinates are exemplary used. `kw` stands for an arbitrary keyword argument and `e` stands for an element index.

    .. table:: Interpretation of value

        ================  ===========  ===========  ======  =========
        Signature         Return type  Homogeneous  Linear  Isotropic
        ================  ===========  ===========  ======  =========
        value             float        yes          yes     yes
        value             1D array     ?            ?       ?
        value             3D array     ?            ?       ?
        value             2D array     yes          yes     no
        value(kw)         1D array     yes          no      yes
        value(kw)         3D array     yes          no      no
        value(x,y)        float        no           yes     yes
        value(x,y)        2D array     no           yes     no
        value(x,y,e, kw)  float        no           no      yes
        value(x,y,e, kw)  2D array     no           no      no
        ================  ===========  ===========  ======  =========

    For nonlinear material properties it is recommended to use for `value` an instance of a class that is callable. The
    dependencies can then be written to the object. For more information about this and about the handling of value, see
    :py:class:`~pyrit.ValueHandler`.

    If a value has positional arguments, it is considered inhomogeneous.
    If a value has keyword arguments, it is considered nonlinear.

    For homogeneous and nonlinear properties, the function needs to have a keyword argument 'element' that specifies on
    which element the property is evaluated.

    Examples
    --------
    As an example, we consider the class `Permittivity` that inherits from `MatProperty`. Its value is the permittivity.

    In this code example:

    >>> from scipy.constants import epsilon_0
    >>> permittivity = Permittivity(2*epsilon_0)

    `permittivity` is an instance of the material property `Permittivity` with an relative permittivity of 2. So it is
    :math:`\epsilon=2\epsilon_0`.

    In this code example:

    >>> from scipy.constants import epsilon_0
    >>> permittivity = Permittivity(lambda x, y: np.array([[(1+x**2)*epsilon_0,0],[0,(1+y**4)*epsilon_0]]))

    `permittivity` is again an instance of the material property `Permittivity`. This time, it is an inhomogeneous and
    isotrobic material property with

    .. math::

        \epsilon = \begin{pmatrix}(1+x^2)\epsilon_0 & 0 \\ 0 & (1+y^4)\epsilon_0\end{pmatrix}\,.

    """

    __slots__ = ('name', 'data')

    __metaclass__ = MatPropertyMeta

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        # """
        # Constructor of MatProperty
        #
        # Parameters
        # ----------
        # value :
        #     Value of the material property. See the class docstring for more information.
        # name : str, optional
        #     Name of the Property. Default is ''
        # data : np.ndarray, optional
        #     Data for a data-driven material
        #
        # Returns
        # -------
        # None.
        # """
        super().__init__(value)
        self.name = name
        self.data = data

        # Add the docstring to the subclasses
        # type(self).__init__.__doc__ = type(self).docstring_template.replace('<name>', type(self).__name__)
        # if self.is_homogeneous and not self.is_linear:
        #     assert 'element' in self.keyword_args

    @property
    def is_isotrop(self):
        """
        Returns True if the MatProperty is isotrop and False if not

        Returns
        -------
        bool
            True: MatProperty is isotrop. False: MatProperty is not isotrop.

        """
        if not callable(self.value):
            if isinstance(self.value, np.ndarray):
                return len(self.value.shape) != 2
            return True
        # It is callable
        if self.is_homogeneous:
            return len(self.value().shape) not in (2, 3)  # pylint: disable=not-callable

        variables = np.zeros(len(self.positional_args), dtype=int).tolist()
        return not isinstance(self.value(*variables), np.ndarray)  # pylint: disable=not-callable

    @property
    def is_data_driven(self) -> bool:
        """Indicates whether the MatProperty is a data-driven property or not."""
        return self.data is not None

    @property
    def is_hysteretic(self):
        """
        Returns True if the MatProperty is hysteretic and False if not

        Returns
        -------
        bool
            True: MatProperty is hysteretic. False: MatProperty is not hysteretic.

        """
        raise NotImplementedError("Not implemented yet")

    @staticmethod
    def import_from_table(path: str):
        """
        Reads the data of a material property.

        Parameters
        ----------
        path : str
            Path to the file containing the data.

        Returns
        -------
        None
        """
        raise NotImplementedError("Not implemented yet")
