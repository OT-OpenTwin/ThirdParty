# coding=utf-8
"""
================================
Material (:mod:`pyrit.material`)
================================

.. currentmodule:: pyrit.material

This module handles materials.

Materials and container class
-----------------------------

.. autosummary::
    :toctree: autosummary/

    Materials
    Conductivity
    MixedConductivityCart
    MixedConductivityAxi
    MixedConductivity3D
    Density
    VolumetricHeatCapacity
    Permeability
    MixedPermeabilityCart
    MixedPermeabilityAxi
    MixedPermeability3D
    Permittivity
    MixedPermittivityCart
    MixedPermittivityAxi
    MixedPermittivity3D
    Reluctivity
    MixedReluctivityCart
    MixedReluctivityAxi
    MixedReluctivity3D
    ThermalConductivity
    Resistivity
    MixedResistivityCart
    MixedResistivityAxi
    MixedResistivity3D
    DifferentialConductivity
    DifferentialPermittivity
    DifferentialReluctivity
    DiffConductivityParameter
    DiffPermittivityParameter
    DiffConductivityTemperature
    DiffPermittivityTemperature
    DiffThermalConductivityTemperature
    DiffVolumetricHeatCapacityTemperature
    DiffThermalConductivityParameter
    DiffVolumetricHeatCapacityParameter
    BrauerModel
    AnisotropicProperty
    get_layered_material_property

Abstract classes
----------------

.. autosummary::
    :toctree: autosummary/

    Mat
    MatProperty
    MixedConductivity
    MixedReluctivity
    MixedResistivity
    MixedPermittivity
    MixedPermeability

Exceptions
----------

.. autosummary::
    :toctree: autosummary/

    PropertyConversionException
"""

from .MatProperty import MatProperty
from .Conductivity import Conductivity
from .MixedConductivity import MixedConductivity, MixedConductivityCart, MixedConductivityAxi, MixedConductivity3D
from .Density import Density
from .VolumetricHeatCapacity import VolumetricHeatCapacity
from .Permeability import Permeability
from .MixedPermeability import MixedPermeability, MixedPermeabilityCart, MixedPermeabilityAxi, MixedPermeability3D
from .Permittivity import Permittivity
from .MixedPermittivity import MixedPermittivity, MixedPermittivityCart, MixedPermittivityAxi, MixedPermittivity3D
from .Reluctivity import Reluctivity
from .MixedReluctivity import MixedReluctivity, MixedReluctivityCart, MixedReluctivityAxi, MixedReluctivity3D
from .ThermalConductivity import ThermalConductivity
from .Resistivity import Resistivity
from .MixedResistivity import MixedResistivity, MixedResistivityCart, MixedResistivityAxi, MixedResistivity3D
from .DifferentialConductivity import DifferentialConductivity
from .DifferentialPermittivity import DifferentialPermittivity
from .DifferentialReluctivity import DifferentialReluctivity
from .DiffConductivityParameter import DiffConductivityParameter
from .DiffPermittivityParameter import DiffPermittivityParameter
from .DiffConductivityTemperature import DiffConductivityTemperature
from .DiffThermalConductivityParameter import DiffThermalConductivityParameter
from .DiffThermalConductivityTemperature import DiffThermalConductivityTemperature
from .DiffVolumetricHeatCapacityParameter import DiffVolumetricHeatCapacityParameter
from .DiffVolumetricHeatCapacityTemperature import DiffVolumetricHeatCapacityTemperature
from .DiffPermittivityTemperature import DiffPermittivityTemperature
from .Mat import Mat, PropertyConversionException
from .Materials import Materials
from .BrauerModel import BrauerModel
from .AnisotropicProperty import AnisotropicProperty
from .get_layered_material_property import direct_mixing_2d, indirect_mixing_2d, get_layered_property_direct_mixing,\
    get_layered_property_indirect_mixing

__all__ = ['Conductivity', 'MixedConductivity', 'MixedConductivityCart', 'MixedConductivityAxi', 'MixedConductivity3D',
           'Density', 'VolumetricHeatCapacity', 'Mat', 'MatProperty', 'Materials', 'Permeability', 'MixedPermeability',
           'MixedPermeabilityCart', 'MixedPermeabilityAxi', 'MixedPermeability3D', 'Permittivity',
           'MixedPermittivity', 'MixedPermittivityCart', 'MixedPermittivityAxi', 'MixedPermittivity3D', 'Reluctivity',
           'MixedReluctivity', 'MixedReluctivityCart', 'MixedReluctivityAxi', 'MixedReluctivity3D',
           'ThermalConductivity', 'Resistivity', 'MixedResistivity', 'MixedResistivityCart', 'MixedResistivityAxi',
           'MixedResistivity3D', 'DifferentialConductivity', 'DifferentialPermittivity', 'DifferentialReluctivity',
           'PropertyConversionException', 'DiffConductivityParameter', 'DiffPermittivityParameter',
           'DiffConductivityTemperature', 'DiffThermalConductivityParameter', 'DiffThermalConductivityTemperature',
           'DiffVolumetricHeatCapacityParameter', 'DiffVolumetricHeatCapacityTemperature',
           'DiffPermittivityTemperature', 'BrauerModel', 'AnisotropicProperty', 'get_layered_material_property']
