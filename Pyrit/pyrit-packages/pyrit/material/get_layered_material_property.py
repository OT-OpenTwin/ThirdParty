# coding=utf-8
"""Method to get effective material properties from a layered composite material.

.. sectionauthor:: Thyssen
"""

from typing import List, Union, Callable

import numpy as np

from pyrit.material import MatProperty


Value = Union[float, Callable[[float], float], Callable[[np.ndarray], float],
              Callable[[float, np.ndarray], float]]


def direct_mixing_2d(mat_properties: List[MatProperty], ratios: List[float]) -> Value:
    r"""Mixes the property values directly using the ratios and following the mixing rule

        :math:`\epsilon_{eff} = \sum_{i=1}^n \lambda_i \epsilon_i`.

    With :math:`\epsilon_i` being the i-th material_property in the material_properties list and :math:`\lambda_i` being
    the i-th ratio in the ratio list. The function is written for 2-dimensional case.

    Parameters
    ----------
    mat_properties: List[MatProperty]
        list of mat_properties, properties of the layeres in the layered material.
    ratios: List[float]
        list of float, the i-th float indicates the ratio of the i-th material property in the mat_properties list

    Returns
    -------
    sum(weighted_values): float
        if all mat_properties are homogeneous and nonlinear, a float describing the effective property is returned.
    sum_weighted_values: Union[Callable[float], float]
        for a combination of possibly inhomogeneous and always linear material properties, the effective material
        property is a callable depending on x, y (floats) and returning float.
    sum_weighted_values: Callable[[np.ndarray], float]
        for a combination of always homogeneous and possibly nonlinear material properties, the effective material
        property is a callable depending on elements (np.ndarray) and returning a float.
    sum_weighted_values: Callable[[float, np.ndarray], float]
        for a combination of possibly inhomogeneous and possibly nonlinear material properties, the effective material
        property is a callable depending on x, y, (float), elements (np.ndarray) and returning a float.
    """
    if any(not prop.is_linear for prop in mat_properties) and any(not prop.is_homogeneous for prop in mat_properties):
        def calculate_weighted_value_nonlin_inhom(mat_properties, ratios, x, y, elements):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if elements is None:  # needed for check if isotropic
                    weighted_value = 1
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and not prop.is_homogeneous:
                    weighted_value = prop.value(x, y, elements) * ratios[i]
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value(elements) * ratios[i]
                    weighted_values.append(weighted_value)
                elif prop.is_linear and not prop.is_homogeneous:
                    weighted_value = prop.value(x, y) * ratios[i]
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value * ratios[i]
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_nonlin_inhom(x, y, element=None):
            weighted_values = calculate_weighted_value_nonlin_inhom(mat_properties, ratios, x, y, element)
            return sum(weighted_values)
        return sum_weighted_values_nonlin_inhom

    if any(not prop.is_linear for prop in mat_properties) and all(prop.is_homogeneous for prop in mat_properties):
        def calculate_weighted_value_nonlin_hom(mat_properties, ratios, elements):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if elements is None:
                    weighted_value = np.array([1])  # needed for check if isotropic
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value(elements) * ratios[i]
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value * ratios[i]
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_nonlin_hom(element=None):
            weighted_values = calculate_weighted_value_nonlin_hom(mat_properties, ratios, element)
            return sum(weighted_values)
        return sum_weighted_values_nonlin_hom

    if any(not prop.is_homogeneous for prop in mat_properties) and all(prop.is_linear for prop in mat_properties):

        def calculate_weighted_value_lin_inhom(mat_properties, ratios, x, y):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if prop.is_linear and not prop.is_homogeneous:
                    weighted_value = prop.value(x, y) * ratios[i]
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value * ratios[i]
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_lin_inhom(x, y):
            weighted_values = calculate_weighted_value_lin_inhom(mat_properties, ratios, x, y)
            return sum(weighted_values)
        return sum_weighted_values_lin_inhom

    def calculate_weighted_value_lin_hom(mat_properties, ratios):
        weighted_values = []
        for i, prop in enumerate(mat_properties):
            weighted_value = prop.value * ratios[i]
            weighted_values.append(weighted_value)
        return weighted_values

    weighted_values = calculate_weighted_value_lin_hom(mat_properties, ratios)
    return sum(weighted_values)


def indirect_mixing_2d(mat_properties: List[MatProperty], ratios: List[float]) -> Callable:
    r"""Mixes the property values directly using the ratios and following the mixing rule

        :math:`\epsilon_{eff} = (\sum_{i=1}^n \lambda_i / \epsilon_i)^{-1}`

    With :math:`\epsilon_i` being the i-th material_property in the material_properties list and :math:`\lambda_i` being
    the i-th ratio in the ratio list. The function is written for 2-dimensional case.

    Parameters
    ----------
    mat_properties: List[MatProperty]
        list of mat_properties, properties of the layeres in the layered material.
    ratios: List[float]
        list of float, the i-th float indicates the ratio of the i-th material property in the mat_properties list

    Returns
    -------
    sum(weighted_values): float
        if all mat_properties are homogeneous and nonlinear, a float describing the effective property is returned.
    sum_weighted_values: Union[Callable[float], float]
        for a combination of possibly inhomogeneous and always linear material properties, the effective material
        property is a callable depending on x, y (floats) and returning float.
    sum_weighted_values: Callable[[np.ndarray], float]
        for a combination of always homogeneous and possibly nonlinear material properties, the effective material
        property is a callable depending on elements (np.ndarray) and returning a float.
    sum_weighted_values: Callable[[float, np.ndarray], float]
        for a combination of possibly inhomogeneous and possibly nonlinear material properties, the effective material
        property is a callable depending on x, y, (float), elements (np.ndarray) and returning a float.
    """
    if any(not prop.is_linear for prop in mat_properties) and any(not prop.is_homogeneous for prop in mat_properties):
        def calculate_weighted_value_nonlin_inhom(mat_properties, ratios, x, y, elements):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if elements is None:  # needed for check if isotropic
                    weighted_value = 1
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and not prop.is_homogeneous:
                    prop_value = prop.value(x, y, elements)
                    if isinstance(prop_value, np.ndarray):
                        if np.any(prop_value == 0):
                            prop_value = prop_value + 1e-10
                    elif prop_value == 0:
                        prop_value = prop_value + 1e-10
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and prop.is_homogeneous:
                    prop_value = prop.value(elements)
                    if isinstance(prop_value, np.ndarray):
                        if np.any(prop_value == 0):
                            prop_value = prop_value + 1e-10
                    elif prop_value == 0:
                        prop_value = prop_value + 1e-10
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif prop.is_linear and not prop.is_homogeneous:
                    if prop.value(x, y) == 0:
                        prop_value = prop.value(x, y) + 1e-10
                    else:
                        prop_value = prop.value(x, y)
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    if prop.value(x, y, elements) == 0:
                        prop_value = prop.value + 1e-10
                    else:
                        prop_value = prop.value
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_nonlin_inhom(x, y, element=None):
            weighted_values = calculate_weighted_value_nonlin_inhom(mat_properties, ratios, x, y, element)
            return 1 / sum(weighted_values)

        return sum_weighted_values_nonlin_inhom

    if any(not prop.is_linear for prop in mat_properties) and all(prop.is_homogeneous for prop in mat_properties):
        def calculate_weighted_value_nonlin_hom(mat_properties, ratios, elements):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if elements is None:
                    weighted_value = np.array([1])  # needed for check if isotropic
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and prop.is_homogeneous:
                    prop_value = prop.value(elements)
                    if isinstance(prop_value, np.ndarray):
                        if np.any(prop_value == 0):
                            prop_value = prop_value + 1e-10
                    elif prop_value == 0:
                        prop_value = prop_value + 1e-10
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    if prop.value == 0:
                        prop_value = prop.value + 1e-10
                    else:
                        prop_value = prop.value
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_nonlin_hom(element=None):
            weighted_values = calculate_weighted_value_nonlin_hom(mat_properties, ratios, element)
            return 1 / sum(weighted_values)

        return sum_weighted_values_nonlin_hom

    if any(not prop.is_homogeneous for prop in mat_properties) and all(prop.is_linear for prop in mat_properties):
        def calculate_weighted_value_lin_inhom(mat_properties, ratios, x, y):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if prop.is_linear and not prop.is_homogeneous:
                    if prop.value(x, y) == 0:
                        prop_value = prop.value(x, y) + 1e-10
                    else:
                        prop_value = prop.value(x, y)
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    if prop.value == 0:
                        prop_value = prop.value + 1e-10
                    else:
                        prop_value = prop.value
                    weighted_value = ratios[i] / prop.value
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_lin_inhom(x, y):
            weighted_values = calculate_weighted_value_lin_inhom(mat_properties, ratios, x, y)
            return 1 / sum(weighted_values)

        return sum_weighted_values_lin_inhom

    def calculate_weighted_value_lin_hom(mat_properties, ratios):
        weighted_values = []
        for i, prop in enumerate(mat_properties):
            if prop.value == 0:
                prop_value = prop.value + 1e-10
            else:
                prop_value = prop.value
            weighted_value = ratios[i] / prop_value
            weighted_values.append(weighted_value)
        return weighted_values

    weighted_values = calculate_weighted_value_lin_hom(mat_properties, ratios)
    return 1 / sum(weighted_values)


def direct_mixing_3d(mat_properties: List[MatProperty], ratios: List[float]) -> Value:
    r"""Mixes the property values directly using the ratios and following the mixing rule

        :math:`\epsilon_{eff} = \sum_{i=1}^n \lambda_i \epsilon_i`.

    With :math:`\epsilon_i` being the i-th material_property in the material_properties list and :math:`\lambda_i` being
    the i-th ratio in the ratio list. The function s written for 3-dimensional case.

    Parameters
    ----------
    mat_properties: List[MatProperty]
        list of mat_properties, properties of the layeres in the layered material.
    ratios: List[float]
        list of float, the i-th float indicates the ratio of the i-th material property in the mat_properties list

    Returns
    -------
    sum(weighted_values): float
        if all mat_properties are homogeneous and nonlinear, a float describing the effective property is returned.
    sum_weighted_values: Union[Callable[float], float]
        for a combination of possibly inhomogeneous and always linear material properties, the effective material
        property is a callable depending on x, y, z (floats) and returning float.
    sum_weighted_values: Callable[[np.ndarray], float]
        for a combination of always homogeneous and possibly nonlinear material properties, the effective material
        property is a callable depending on elements (np.ndarray) and returning a float.
    sum_weighted_values: Callable[[float, np.ndarray], float]
        for a combination of possibly inhomogeneous and possibly nonlinear material properties, the effective material
        property is a callable depending on x, y, z (float), elements (np.ndarray) and returning a float.
    """
    if any(not prop.is_linear for prop in mat_properties) and any(not prop.is_homogeneous for prop in mat_properties):
        def calculate_weighted_value_nonlin_inhom(mat_properties, ratios, x, y, z, elements):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if elements is None:  # needed for check if isotropic
                    weighted_value = 1
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and not prop.is_homogeneous:
                    weighted_value = prop.value(x, y, z, elements) * ratios[i]
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value(elements) * ratios[i]
                    weighted_values.append(weighted_value)
                elif prop.is_linear and not prop.is_homogeneous:
                    weighted_value = prop.value(x, y, z) * ratios[i]
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value * ratios[i]
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_nonlin_inhom(x, y, z, element=None):
            weighted_values = calculate_weighted_value_nonlin_inhom(mat_properties, ratios, x, y, z, element)
            return sum(weighted_values)
        return sum_weighted_values_nonlin_inhom

    if any(not prop.is_linear for prop in mat_properties) and all(prop.is_homogeneous for prop in mat_properties):
        def calculate_weighted_value_nonlin_hom(mat_properties, ratios, elements):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if elements is None:
                    weighted_value = np.array([1])  # needed for check if isotropic
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value(elements) * ratios[i]
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value * ratios[i]
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_nonlin_hom(element=None):
            weighted_values = calculate_weighted_value_nonlin_hom(mat_properties, ratios, element)
            return sum(weighted_values)
        return sum_weighted_values_nonlin_hom

    if any(not prop.is_homogeneous for prop in mat_properties) and all(prop.is_linear for prop in mat_properties):

        def calculate_weighted_value_lin_inhom(mat_properties, ratios, x, y, z):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if prop.is_linear and not prop.is_homogeneous:
                    weighted_value = prop.value(x, y, z) * ratios[i]
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    weighted_value = prop.value * ratios[i]
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_lin_inhom(x, y, z):
            weighted_values = calculate_weighted_value_lin_inhom(mat_properties, ratios, x, y, z)
            return sum(weighted_values)
        return sum_weighted_values_lin_inhom

    def calculate_weighted_value_lin_hom(mat_properties, ratios):
        weighted_values = []
        for i, prop in enumerate(mat_properties):
            weighted_value = prop.value * ratios[i]
            weighted_values.append(weighted_value)
        return weighted_values

    weighted_values = calculate_weighted_value_lin_hom(mat_properties, ratios)
    return sum(weighted_values)


def indirect_mixing_3d(mat_properties: List[MatProperty], ratios: List[float]) -> Callable:
    r"""Mixes the property values directly using the ratios and following the mixing rule

        :math:`\epsilon_{eff} = (\sum_{i=1}^n \lambda_i / \epsilon_i)^{-1}`

    With :math:`\epsilon_i` being the i-th material_property in the material_properties list and :math:`\lambda_i` being
    the i-th ratio in the ratio list. The function is written for 3-dimensional case.

    Parameters
    ----------
    mat_properties: List[MatProperty]
        list of mat_properties, properties of the layeres in the layered material.
    ratios: List[float]
        list of float, the i-th float indicates the ratio of the i-th material property in the mat_properties list

    Returns
    -------
    sum(weighted_values): float
        if all mat_properties are homogeneous and nonlinear, a float describing the effective property is returned.
    sum_weighted_values: Union[Callable[float], float]
        for a combination of possibly inhomogeneous and always linear material properties, the effective material
        property is a callable depending on x, y, z (floats) and returning float.
    sum_weighted_values: Callable[[np.ndarray], float]
        for a combination of always homogeneous and possibly nonlinear material properties, the effective material
        property is a callable depending on elements (np.ndarray) and returning a float.
    sum_weighted_values: Callable[[float, np.ndarray], float]
        for a combination of possibly inhomogeneous and possibly nonlinear material properties, the effective material
        property is a callable depending on x, y, z (float), elements (np.ndarray) and returning a float.
    """
    if any(not prop.is_linear for prop in mat_properties) and any(not prop.is_homogeneous for prop in mat_properties):
        def calculate_weighted_value_nonlin_inhom(mat_properties, ratios, x, y, z, elements):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if elements is None:  # needed for check if isotropic
                    weighted_value = 1
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and not prop.is_homogeneous:
                    prop_value = prop.value(x, y, z, elements)
                    if isinstance(prop_value, np.ndarray):
                        if np.any(prop_value == 0):
                            prop_value = prop_value + 1e-10
                    elif prop_value == 0:
                        prop_value = prop_value + 1e-10
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and prop.is_homogeneous:
                    prop_value = prop.value(elements)
                    if isinstance(prop_value, np.ndarray):
                        if np.any(prop_value == 0):
                            prop_value = prop_value + 1e-10
                    elif prop_value == 0:
                        prop_value = prop_value + 1e-10
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif prop.is_linear and not prop.is_homogeneous:
                    if prop.value(x, y, z) == 0:
                        prop_value = prop.value(x, y, z) + 1e-10
                    else:
                        prop_value = prop.value(x, y, z)
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    if prop.value(x, y, z, elements) == 0:
                        prop_value = prop.value + 1e-10
                    else:
                        prop_value = prop.value
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_nonlin_inhom(x, y, z, element=None):
            weighted_values = calculate_weighted_value_nonlin_inhom(mat_properties, ratios, x, y, z, element)
            return 1 / sum(weighted_values)

        return sum_weighted_values_nonlin_inhom

    if any(not prop.is_linear for prop in mat_properties) and all(prop.is_homogeneous for prop in mat_properties):
        def calculate_weighted_value_nonlin_hom(mat_properties, ratios, elements):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if elements is None:
                    weighted_value = np.array([1])  # needed for check if isotropic
                    weighted_values.append(weighted_value)
                elif not prop.is_linear and prop.is_homogeneous:
                    if np.any(prop.value(elements) == 0):
                        prop_value = prop.value(elements) + 1e-10
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    if prop.value == 0:
                        prop_value = prop.value + 1e-10
                    else:
                        prop_value = prop.value
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_nonlin_hom(element=None):
            weighted_values = calculate_weighted_value_nonlin_hom(mat_properties, ratios, element)
            return 1 / sum(weighted_values)

        return sum_weighted_values_nonlin_hom

    if any(not prop.is_homogeneous for prop in mat_properties) and all(prop.is_linear for prop in mat_properties):
        def calculate_weighted_value_lin_inhom(mat_properties, ratios, x, y, z):
            weighted_values = []
            for i, prop in enumerate(mat_properties):
                if prop.is_linear and not prop.is_homogeneous:
                    if prop.value(x, y, z) == 0:
                        prop_value = prop.value(x, y, z) + 1e-10
                    else:
                        prop_value = prop.value(x, y, z)
                    weighted_value = ratios[i] / prop_value
                    weighted_values.append(weighted_value)
                elif prop.is_linear and prop.is_homogeneous:
                    if prop.value == 0:
                        prop_value = prop.value + 1e-10
                    else:
                        prop_value = prop.value
                    weighted_value = ratios[i] / prop.value
                    weighted_values.append(weighted_value)
            return weighted_values

        def sum_weighted_values_lin_inhom(x, y, z):
            weighted_values = calculate_weighted_value_lin_inhom(mat_properties, ratios, x, y, z)
            return 1 / sum(weighted_values)

        return sum_weighted_values_lin_inhom

    def calculate_weighted_value_lin_hom(mat_properties, ratios):
        weighted_values = []
        for i, prop in enumerate(mat_properties):
            if prop.value == 0:
                prop_value = prop.value + 1e-10
            else:
                prop_value = prop.value
            weighted_value = ratios[i] / prop_value
            weighted_values.append(weighted_value)
        return weighted_values

    weighted_values = calculate_weighted_value_lin_hom(mat_properties, ratios)
    return 1 / sum(weighted_values)


def get_layered_property_direct_mixing(mat_properties: List[MatProperty], ratios: List[float], dimensionality: int) \
        -> MatProperty:
    """Returns MatProperty instance with the effective property as value

    Parameters
    ----------
    mat_properties : List[MatProperty]
        The material properties of the layers.
    ratios : List[float]
        The ratios of the layer thicknesses to the total thickness.
    dimensionality : int
        2 or 3, spatial dimensionality

    Returns
    -------
    MatProperty
        The values of the MatProperty corresponds to the value perpendicular or parallel to
        the layers.
    """
    if dimensionality not in (2, 3):
        raise ValueError("Dimensionality must be 2 for 2 dimensional case or 3 for 3 dimensional case!")

    if not sum(ratios) == 1:
        raise ValueError("Ratios must add up to one!")

    if not len(mat_properties) == len(ratios):
        raise ValueError("Number of mat_properties must equal nuber of ratios!")

    if not all(isinstance(prop, type(mat_properties[0])) for prop in mat_properties):
        raise TypeError("All properties must be from the same type!")

    if dimensionality == 2:
        return type(mat_properties[0])(direct_mixing_2d(mat_properties, ratios))
    return type(mat_properties[0])(direct_mixing_3d(mat_properties, ratios))


def get_layered_property_indirect_mixing(mat_properties: List[MatProperty], ratios: List[float], dimensionality: int)\
        -> MatProperty:
    """Returns MatProperty instance with the effective property as value

    Parameters
    ----------
    mat_properties : List[MatProperty]
        The material properties of the layers.
    ratios : List[float]
        The ratios of the layer thicknesses to the total thickness.
    dimensionality : int
        2 or 3, spatial dimensionality

    Returns
    -------
    MatProperty
        The value of the MatProperty corresponds to the value perpendicular or parallel to the layers.
    """
    if dimensionality not in (2, 3):
        raise ValueError("Dimensionality must be 2 for 2 dimensional case or 3 for 3 dimensional case!")

    if not sum(ratios) == 1:
        raise ValueError("Ratios must add up to one!")

    if not len(mat_properties) == len(ratios):
        raise ValueError("Number of mat_properties must equal nuber of ratios!")

    if not all(isinstance(prop, type(mat_properties[0])) for prop in mat_properties):
        raise TypeError("All properties must be from the same type!")

    if dimensionality == 2:
        return type(mat_properties[0])(indirect_mixing_2d(mat_properties, ratios))
    return type(mat_properties[0])(indirect_mixing_3d(mat_properties, ratios))
