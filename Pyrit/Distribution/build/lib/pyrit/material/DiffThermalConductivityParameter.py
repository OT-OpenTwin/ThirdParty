# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:17:45 2021

.. sectionauthor:: bundschuh
"""
from typing import Dict, Any
import numpy as np

from . import MatProperty


class DiffThermalConductivityParameter(MatProperty):
    r"""Class that represents the derivative of the thermal conductivity to a set of design parameters."""

    def __init__(self, value: Dict[str, Any], name: str = '', parameter_key: str = None, data: np.ndarray = None):
        # For internal use only
        if isinstance(value, (float, int)):
            super().__init__(value, name, data)

        else:
            if parameter_key is None:
                item = value.popitem()
                value[item[0]] = item[1]
                parameter_key = item[0]
            super().__init__(value[parameter_key], name, data)
            self._parameter_key = parameter_key
            self.dict_values = value

    @property
    def parameter_key(self):
        """Key of currently selected parameter."""
        return self._parameter_key

    @parameter_key.setter
    def parameter_key(self, key: str):
        self._parameter_key = key
        self.value = self.dict_values[key]
