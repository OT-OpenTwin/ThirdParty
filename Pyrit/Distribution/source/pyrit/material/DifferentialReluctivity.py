# coding=utf-8
"""Implementation of DifferentialReluctivity.

.. sectionauthor:: Bundschuh
"""
import numpy as np
from . import MatProperty


class DifferentialReluctivity(MatProperty):
    r"""Class that represents the derivative of the reluctivity to magnetic flux density.

    :math:`\frac{\mathrm{d}^2 \nu}{\mathrm{d} B^2}`.
    """

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
