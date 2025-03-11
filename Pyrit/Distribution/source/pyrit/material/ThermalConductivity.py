# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:18:22 2021

.. sectionauthor:: bundschuh
"""

import numpy as np

from . import MatProperty


class ThermalConductivity(MatProperty):
    r"""Class that represents the thermal conductivity :math:`\lambda`"""

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
