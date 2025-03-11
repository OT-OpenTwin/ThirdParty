# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:19:25 2021

.. sectionauthor:: bundschuh
"""

import numpy as np
from . import MatProperty


class Density(MatProperty):
    """Class that represents the density"""

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
