# -*- coding: utf-8 -*-
"""
Created on Tue June 15 2021

Contains the class BCAntiPeriodic
.. sectionauthor:: menzenbach
"""

import numpy as np

from . import BCBinary
from .BCBinary import uniform_map2d


class BCAntiPeriodic(BCBinary):
    """Class of BCAntiPeriodic with super class BCBinary.

    The value is set to -1. #todo: Add physical meaning and
    possible usages.
    """

    def __init__(self, name: str = ''):
        """
        Constructor of class BCAntiPeriodic.

        Parameters
        ----------
        name : str, optional
            Name of the BC, by default ''
        """
        super().__init__(1, name=name)
        self.primary_transform = lambda x: 1 * np.ones_like(x)
        self.secondary_transform = lambda x: 1 * np.ones_like(x)
        self.dirichlet_shift = lambda x: np.zeros((x.shape[0],))

        # Define simple mappings, both boundaries have same uniform value
        self.bc_to_primary = uniform_map2d
        self.bc_to_secondary = uniform_map2d
