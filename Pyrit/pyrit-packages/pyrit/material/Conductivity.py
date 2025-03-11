# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:17:45 2021

.. sectionauthor:: bundschuh
"""

import numpy as np

from . import MatProperty


class Conductivity(MatProperty):
    r"""Class that represents the conductivity :math:`\sigma` in S/m."""

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
