# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:19:02 2021

.. sectionauthor:: bundschuh
"""

import numpy as np

from . import MatProperty


class VolumetricHeatCapacity(MatProperty):
    r"""Class that represents the volumetric heat capacity :math:`c_v = \rho c_p` (German: Wärmespeicherzahl)"""

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
