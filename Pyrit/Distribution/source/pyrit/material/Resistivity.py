# coding=utf-8
"""Implementation of Resistivity

.. sectionauthor:: Bundschuh
"""

import numpy as np

from pyrit.material.MatProperty import MatProperty


class Resistivity(MatProperty):
    r"""Class representing the resistivity :math:`\rho=\sigma^{-1}`"""

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
