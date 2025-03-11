# coding=utf-8
"""Implementation of Reluctivity.

.. sectionauthor:: Bundschuh
"""

import numpy as np

from . import MatProperty


class Reluctivity(MatProperty):
    r"""Class that represents the Reluctivity :math:`\nu=\mu^{-1}`"""

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
