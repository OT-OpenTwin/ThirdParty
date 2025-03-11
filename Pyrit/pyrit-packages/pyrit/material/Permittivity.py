# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:02:36 2021

.. sectionauthor:: bundschuh
"""

import numpy as np

from . import MatProperty


class Permittivity(MatProperty):
    r"""Class that represents the Permittivity :math:`\varepsilon=\varepsilon_{\mathrm{r}} \varepsilon_0`"""

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
