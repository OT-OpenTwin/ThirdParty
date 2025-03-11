# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:17:45 2021

.. sectionauthor:: bundschuh
"""

import numpy as np

from . import MatProperty


class DiffConductivityTemperature(MatProperty):
    r"""Class that represents the derivative of the electric conductivity to the temperature.

    :math:`\frac{\mathrm{d} \sigma}{\mathrm{d} T}`.
    """

    def __init__(self, value, name: str = '', data: np.ndarray = None):
        super().__init__(value, name, data)
