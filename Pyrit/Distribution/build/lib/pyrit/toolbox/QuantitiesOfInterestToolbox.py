# coding=utf-8
"""QuantitiesOfInterestToolbox

.. sectionauthor:: Ruppert
"""
from typing import Any, Union, Callable, Dict, TYPE_CHECKING, List, Tuple
from itertools import permutations
import numpy as np
from scipy.sparse import coo_matrix


if TYPE_CHECKING:
    from pyrit.solution import Solution, StaticSolution


class QoI():
    r"""Class that represents a specific quantity of interest (QoI).

    A QoI,

    .. math::
        G = G(\boldsymbol{u}_1(\boldsymbol{p}),...,\boldsymbol{u}_{N_{\mathrm{sol}}}(\boldsymbol{p}),\boldsymbol{p}),

    is a scalar quantity that is obtained by post-processing the solution vector(s), :math:`\boldsymbol{u}_i`, of a
    problem and that can (implicitly or explicitly) depend on a set of design parameters,
    :math:`\boldsymbol p = [p_1,p_2,...]`.

    In a transient setting, a QoI can also be written as an integral over time,

    .. math::
        G = \int_{t_{\mathrm{start}}}^{t_{\mathrm{end}}} g(\boldsymbol{u}_1(\boldsymbol{p}),...,
        \boldsymbol{u}_{N_{\mathrm{sol}}}(\boldsymbol{p}),\boldsymbol{p}, t) \mathrm{d}t,

    where :math:`t` is the time variable and :math:`g` is a functional chosen according to the QoI.

    """

    def __init__(self, name: str, definition: Callable[[Any], Union[int, float]],
                 diff_qoi_param: Dict[str, Union[float, int, Callable[[Any], Union[float, int]]]] = None,
                 diff_qoi_dof: Dict[str, Union[coo_matrix, np.ndarray,
                                               Callable[[Any], Union[coo_matrix, np.ndarray]]]] = None):
        """Constructor of QoI

        Parameters
        ----------
        name: str
            Name of the QoI.
        definition: Callable[[Solution,..], Union[int, float]]
            Function that computes the value of the QoI by post-processing one or more Solution objects.
        diff_qoi_param: Dict[str, Union[float, int, Callable[[Any], Union[float, int]]]]
            Dictionary that specifies the derivatives of the QoI to the parameters.

                key: Name of the parameter

                value: Partial derivative of :math:`G` to the specified parameter or, in a transient setting,
                the partial derivative of :math:`g` to the parameter.
        diff_qoi_dof: Dict[str, Union[coo_matrix, np.ndarray, Callable[[Any], Union[coo_matrix, np.ndarray]]]]

            Dictionary that specifies the derivative of the QoI to the degrees of freedom (DoFs).
                key: name of the solution represented by the vector of DoFs, e.g. 'temperature' or 'potential'.

                value: Vector of partial derivatives of :math:`G` or, in a transient setting, :math:`g` to the DoFs.
        """
        self.name = name
        self.definition = definition
        if diff_qoi_param is None:
            diff_qoi_param = {}
        if diff_qoi_dof is None:
            diff_qoi_dof = {}
        self._diff_qoi_param = diff_qoi_param
        self._diff_qoi_dof = diff_qoi_dof

    @property
    def diff_qoi_param(self):
        """Dictionary that specifies the derivative of the QoI to a set of parameters."""
        if self._diff_qoi_param is None:
            raise ValueError(f"Definition of diff_qoi_param in QoI \'{self.name}\' is missing.")
        return self._diff_qoi_param

    @diff_qoi_param.setter
    def diff_qoi_param(self, value):
        self._diff_qoi_param = value

    def get_parameter_names(self) -> List[str]:
        """Function that returns the names of all parameters for which the derivative of the QoI is defined."""
        if self._diff_qoi_param is None:
            return []
        return list(self._diff_qoi_param.keys())

    @property
    def diff_qoi_dof(self):
        """Dictionary that specifies the derivative of the QoI to the DoFs."""
        if self._diff_qoi_dof is None:
            raise ValueError(f"Definition of diff_qoi_dof in QoI \'{self.name}\' is missing.")
        return self._diff_qoi_dof

    @diff_qoi_dof.setter
    def diff_qoi_dof(self, value):
        self._diff_qoi_dof = value

    @staticmethod
    def call_permutations(f: Callable, *args):
        """Function that tries different input argument combinations for a given function f with unknown signature.

        Calls the function f using all permutations and subsets of a given list of arguments and returns the output.
        If no input configuration is successful, None is returned.
        """
        # pylint: disable=broad-except
        args = args[0]
        for i in range(1, len(args) + 1):
            list_permutations = permutations(args, r=i)
            for p in list_permutations:
                try:
                    return f(*p)
                # noqa: E722
                except Exception:  # noqa: E722
                    pass

        return None

    def evaluate_diff_qoi_param(self, parameter_name: str, *args: Union['StaticSolution', float, int])\
            -> Union[int, float]:
        r"""Function that returns the (evaluated) value of diff_qoi_param for a given parameter name.

        If the value is a function, evaluate_diff_qoi_param will try to call it using different combinations/subsets of
        the arguments passed in args.

        Parameters
        ----------
        parameter_name: str
            Name of the considered parameter
        args: Union['StaticSolution', float, int]
            Arguments used to evaluate the value in case it is a function. Possible arguments are the
            solution object(s) of the problem and, if appropriate, the time. In case of a transient setting,
            StaticSolution object(s) representing the solution at a specific time step are expected instead of
            TransientSolutionObjects.

        Returns
        -------
        out: Union[int, float]
            Derivative of the QoI with respect to the specified parameter.
        """
        try:
            value = self._diff_qoi_param[parameter_name]
        except Exception as e:
            raise ValueError(f"diff_qoi_param of the qoi \'{self.name}\' is not defined for the parameter "
                             f"\'{parameter_name}\'.") from e

        # Value is a number
        if isinstance(value, (float, int)):
            return value

        # Value is a function
        # Try to call it using different combinations and subsets of args
        out = QoI.call_permutations(value, *args)
        if out is not None:
            if isinstance(out, (float, int)):
                return out
            raise ValueError(f"diff_qoi_param of the QoI \'{self.name}\' for the parameter \'{parameter_name}\' "
                             f"has unexpected output format. Should be a scalar.")

        raise ValueError(f"diff_qoi_param of the qoi \'{self.name}\' for the parameter \'{parameter_name}\' "
                         f"has unexpected input format.")

    def evaluate_diff_qoi_dof(self, key: str, *args: Union['StaticSolution', float, int])\
            -> Union[np.ndarray, coo_matrix]:
        """Function that returns the (evaluated) value of diff_qoi_dof for a given key.

        If the value is a function, evaluate_diff_qoi_dof will try to evaluate it using different
        combinations/subsets of the arguments passed in args.

        Parameters
        ----------
        key: str
            Name of the solution represented by the DoF under consideration, e.g. 'potential'
        args: Union['StaticSolution', float, int]
            Arguments used to evaluate the value in case it is a function. Possible arguments are the
            solution object(s) of the problem and, if appropriate, the time. In case of transient problems,
            StaticSolution object(s) representing the solution at the current time step are passed.

        Returns
        -------
        out: Union[np.ndarray, coo_matrix]
            Derivative of the QoI with respect to the specified DoF.
        """
        try:
            value = self._diff_qoi_dof[key]
        except Exception as e:
            raise ValueError(f"diff_qoi_dof of the QoI \'{self.name}\' for is not defined for "
                             f"the solution key \'{key}\'.") from e

        # Value is a constant
        if isinstance(value, (np.ndarray, coo_matrix)):
            return value

        # Value is a function
        # Try to call it using different combinations and subsets of *args
        out = QoI.call_permutations(value, *args)
        if out is not None:
            if isinstance(out, (np.ndarray, coo_matrix)):
                return out
            raise ValueError(f"diff_qoi_dof of the QoI \'{self.name}\' for the solution key \'{key}\' "
                             "has unexpected output format. Should be np.ndarray or coo_matrix.")

        raise ValueError(f"diff_qoi_dof of the QoI \'{self.name}\' for the solution key \'{key}\' "
                         "has unexpected input format.")


class QuantitiesOfInterest():
    """Container class for QoI objects."""

    __slots__ = ['__qois']

    def __init__(self, *qois: QoI):
        """
        Constructor of QuantitiesOfInterest.

        Parameters
        ----------
        *qois : QoI
            A number of QoI, possibly empty.

        Returns
        -------
        None.

        """
        self.__qois = {}
        if len(qois) > 0:
            self.add_qoi(*qois)

    def __iter__(self):
        return self.__qois.values().__iter__()

    def add_qoi(self, *qois: QoI):
        """
        Adds a number of QoI.

        Parameters
        ----------
        *qois : QoI
            A number of QoI.

        Returns
        -------
        None.

        """
        for qoi in qois:
            self.__qois[qoi.name] = qoi

    def delete_qoi(self, *names: str):
        """
        Deletes a number of QoI specified by their name.

        Parameters
        ----------
        *names: str
            A number of names.

        Returns
        -------
        None.

        """
        for qoi_name in names:
            del self.__qois[qoi_name]

    def get_qoi(self, qoi_name: str):
        """
        Returns a number of QoI specified by their names.

        Parameters
        ----------
        id : int
            An IDs.

        Raises
        ------
        KeyError
            When the ID of the QoI is unknown.

        Returns
        -------
        QoI
            A List of the QoIs.

        """
        return self.__qois[qoi_name]

    def get_names(self):
        """
        Returns the names of all QoI saved in QuantitiesOfInterest.

        Returns
        -------
        List[int]
            A list with the names of all QoI saved in QuantitiesOfInterest.

        """
        return list(self.__qois.keys())

    def evaluate_qois(self, *sol: 'Solution') -> Dict[str, Union[float, int]]:
        """
        Evaluates all quantities of interest for given solution(s).

        Parameters
        ----------
        *sol: Solution
            Solution(s) for which the QoIs are evaluated.

        Returns
        -------
        results: Dict[str, Union[float, int]]
            Dictionary containing the results of the evaluated QoIs.
            key: Name of the QoI
            value: Value of the QoI
        """
        results = {}
        for qoi in self:
            value = QoI.call_permutations(qoi.definition, *sol)
            if value is None:
                raise ValueError(f"Definition of the QoI \'{qoi.name}\' has unexpected input format.")
            results[qoi.name] = QoI.call_permutations(qoi.definition, *sol)
        return results

    def get_parameter_names(self) -> List[str]:
        """
        Returns the names of all parameters.

        Returns
        -------
        List[str]
            A list with the names of all parameters.

        """
        all_names = []
        for qoi in self:
            all_names = all_names + qoi.get_parameter_names()
        return list(set(all_names))

    def get_qois_from_parameter_name(self, parameter_name: str) -> 'QuantitiesOfInterest':
        """
        Returns a new QuantitiesOfInterest object containing all QoI that depend on the given parameter name.

        Parameters
        ----------
        parameter_name: str
            Name of the desired parameter.

        Returns
        -------
        qois_dependent_on_parameter: QuantitiesOfInterest
            QuantitiesOfInterest object containing all QoI that depend on the given parameter name.

        """
        qois_dependent_on_parameter = QuantitiesOfInterest()
        for qoi in self:
            if parameter_name in qoi.get_parameter_names():
                qois_dependent_on_parameter.add_qoi(qoi)
        return qois_dependent_on_parameter

    def initialize_sensitivity_dictionary(self) -> Dict[Tuple[str, str], List]:
        """
        Returns an empty dictionary with the keys (<name of QoI>, <name of parameter>).

        Used to initialize the sensitivities of a QuantitiesOfInterest object.

        Returns
        -------
        out: Dict[Tuple[str, str], List]
            Dictionary containing all sensitivity keys as keys and empty lists as values.
            key: (<name of QoI>, <name of parameter>)
            value: [] (empty list)
        """
        out = {}
        for qoi in self:
            for param in qoi.get_parameter_names():
                out[(qoi.name, param)] = []
        return out
