# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:17:11 2021

.. sectionauthor:: bundschuh
"""

import numpy as np

from . import MatProperty


class Permeability(MatProperty):
    r"""Class that represents the permeability :math:`\mu=\mu_{\mathrm{r}} \mu_0`"""

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
