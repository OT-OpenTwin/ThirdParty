# coding=utf-8
"""Class ValueHandler

.. sectionauthor:: Bundschuh
"""

from typing import Any, Callable, Union
from inspect import signature
import numpy as np

from .Logger import get_logger

logger = get_logger(__name__)


# region eval functions
def eval_hom_nonlin_iso(fun: Callable[[np.ndarray], np.ndarray], elements: np.ndarray) -> np.ndarray:
    """Evaluates the function `fun` on elements.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified elements.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Callable[[int], float]
        The function to evaluate.
    elements: np.ndarray
        (E,) array. Array of elements to evaluate for.


    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of an arbitrary function is
    necessary, can be computed.
    """
    # noinspection PyArgumentList
    return fun(element=elements)


def eval_hom_nonlin_aniso(fun: Callable[[np.ndarray], np.ndarray], elements: np.ndarray) -> np.ndarray:
    """Evaluates the function `fun` on elements.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified elements.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Callable[[int], np.ndarray]
        The function to evaluate.
    elements : np.ndarray
        (E,) array. Array with the considered elements.

    Returns
    -------
    evaluations : np.ndarray
        (E,N,2,2) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.
    """
    # noinspection PyArgumentList
    return fun(element=elements)


def eval_inhom_lin_iso(fun: Union[Callable[[float, float], float],
                                  Callable[[float, float, float], float]],
                       evaluation_points: np.ndarray) -> np.ndarray:
    """Evaluates the function `fun` for numerical integration on elements.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified elements.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Union[Callable[[float, float], float], Callable[[float, float, float], float]]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) or (E,N,3) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.

    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.

    Raises
    ------
    ValueError
        If fun's signature has a wrong number of parameters.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of an arbitrary function is
    necessary, can be computed.
    """
    n_args, _ = ValueHandler.num_args(fun)
    if n_args == 2:
        try:
            return np.vectorize(fun)(evaluation_points[:, :, 0], evaluation_points[:, :, 1])
        except ValueError:
            return np.vectorize(fun, signature='(),()->(2)')(evaluation_points[:, :, 0],
                                                             evaluation_points[:, :, 1])
    if n_args == 3:
        values = np.zeros((evaluation_points.shape[0], evaluation_points.shape[1]))
        for k in range(evaluation_points.shape[0]):
            for kk in range(evaluation_points.shape[1]):
                values[k, kk] = fun(evaluation_points[k, kk, 0], evaluation_points[k, kk, 1],
                                    evaluation_points[k, kk, 2])
        return values
        # return np.vectorize(fun)(evaluation_points[:, :, 0],
        #                          evaluation_points[:, :, 1],
        #                          evaluation_points[:, :, 2])
    raise ValueError(f"The function fun has {n_args} arguments instead of 2 (2D) or 3 (3D).")


def eval_inhom_lin_aniso(fun: Union[Callable[[float, float], np.ndarray],
                                    Callable[[float, float, float], np.ndarray]],
                         evaluation_points: np.ndarray) -> np.ndarray:
    """Evaluates the function `fun` for numerical integration on elements.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified elements.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Union[Callable[[float, float], np.ndarray], Callable[[float, float, float], np.ndarray]]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) or (E,N,3) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.

    Returns
    -------
    evaluations : np.ndarray
        (E,N,2,2) or (E,N,3,3) array. For every element the N evaluations of the material function at the
        evaluation points for the numerical integration.

    Raises
    ------
    ValueError
        If fun's signature has a wrong number of parameters.
    """
    n_args, _ = ValueHandler.num_args(fun)
    if n_args == 2:
        vfun = np.vectorize(fun, signature='(),()->(i,i)')
        return vfun(evaluation_points[:, :, 0],
                    evaluation_points[:, :, 1])
    if n_args == 3:
        vfun = np.vectorize(fun, signature='(),(),()->(i,i)')
        return vfun(evaluation_points[:, :, 0],
                    evaluation_points[:, :, 1],
                    evaluation_points[:, :, 2])
    raise ValueError(f"The function fun has {n_args} arguments instead of 2 (2D) or 3 (3D).")


def eval_inhom_nonlin_iso(fun: Union[Callable[[float, float, int], float],
                                     Callable[[float, float, float, int], float]],
                          evaluation_points: np.ndarray,
                          elements: np.ndarray) -> np.ndarray:
    """Evaluates the function `fun` for numerical integration on elements.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified elements.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Union[Callable[[float, float, int], float], Callable[[float, float, float, int], float]]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) or (E,N,3) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    elements : np.ndarray
        (E,) array. Array of the considered elements.

    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.

    Raises
    ------
    ValueError
        If fun's signature has a wrong number of parameters.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of an arbitrary function is
    necessary, can be computed.
    """
    n_args, _ = ValueHandler.num_args(fun)

    indices = np.kron(np.ones((evaluation_points.shape[1], 1), dtype=int), elements).transpose()

    if n_args == 3:
        return np.vectorize(fun)(evaluation_points[:, :, 0],
                                 evaluation_points[:, :, 1],
                                 indices)
    if n_args == 4:
        return np.vectorize(fun)(evaluation_points[:, :, 0],
                                 evaluation_points[:, :, 1],
                                 evaluation_points[:, :, 2],
                                 indices)
    raise ValueError(f"The function fun has {n_args} arguments instead of 2 (2D) or 3 (3D).")


def eval_inhom_nonlin_aniso(fun: Union[Callable[[float, float, int], np.ndarray],
                                       Callable[[float, float, float, int], np.ndarray]],
                            evaluation_points: np.ndarray,
                            elements) -> np.ndarray:
    """Evaluates the function `fun` for numerical integration on elements.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified elements.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of elements in `elements`
        ======  =======

    Parameters
    ----------
    fun : Union[Callable[[float, float, int], np.ndarray], Callable[[float, float, float, int], float]]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) or (E,N,3) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
    elements : np.ndarray
        (E,) array. Array of the considered elements.

    Returns
    -------
    evaluations : np.ndarray
        (E,N,2,2) or (E,N,3,3) array. For every element the N evaluations of the material function at the
        evaluation points for the numerical integration.

    Raises
    ------
    ValueError
        If fun's signature has a wrong number of parameters.
    """
    n_args, _ = ValueHandler.num_args(fun)

    indices = np.kron(np.ones((evaluation_points.shape[1], 1), dtype=int), elements).transpose()

    if n_args == 3:
        vfun = np.vectorize(fun, signature='(),(),()->(i,i)')
        return vfun(evaluation_points[:, :, 0],
                    evaluation_points[:, :, 1],
                    indices)
    if n_args == 4:
        vfun = np.vectorize(fun, signature='(),(),(),()->(i,i)')
        return vfun(evaluation_points[:, :, 0],
                    evaluation_points[:, :, 1],
                    evaluation_points[:, :, 2],
                    indices)
    raise ValueError(f"The function fun has {n_args} arguments instead of 2 (2D) or 3 (3D).")


def evaluate_for_num_int_edge(fun: Union[Callable[[float, float], float],
                                         Callable[[float, float, float], float]],
                              evaluation_points: np.ndarray):
    """Evaluates the function `fun` for numerical integration on edges.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified edges.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of edges in `edges`
        ======  =======

    Parameters
    ----------
    fun : Union[Callable[[float, float], float], Callable[[float, float, float], float]]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,2) or (E,N,3) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_edge`.

    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of a arbitrary funtion is
    necessary, can be computed.
    """
    return eval_inhom_lin_iso(fun, evaluation_points)


def evaluate_for_num_int_face(fun: Union[Callable[[float, float, float], float]],
                              evaluation_points: np.ndarray):
    """Evaluates the function `fun` for numerical integration on faces.

    Evaluates `fun` at the evaluation points for the numerical integration for all specified edges.

    .. table:: Symbols

        ======  =======
        Symbol  Meaning
        ======  =======
        N       Number of evaluation points
        E       Number of edges in `edges`
        ======  =======

    Parameters
    ----------
    fun : Union[Callable[[float, float, float], float]]
        The function to evaluate.
    evaluation_points : np.ndarray
        (E,N,3) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_edge`.

    Returns
    -------
    evaluations : np.ndarray
        (E,N) array. For every element the N evaluations of the material function at the evaluation points for the
        numerical integration.

    Notes
    -----
    This function has to be called before matrix elements, where a numerical integration of a arbitrary funtion is
    necessary, can be computed.
    """
    return eval_inhom_lin_iso(fun, evaluation_points)
# endregion


class ValueHandler:
    """Abstract class that manages a value.

    Values can be numbers, arrays or functions. Depending on the type of values and, if it is a function, on the
    signature, it is interpreted as homogeneous, linear or time dependent. The decision is made as follows:

        - **homogeneous**: It is inhomogeneous only if it is a function with positional arguments (no default)
        - **linear**: If is nonlinear only if it is a function with keyword arguments (has a default) except the
          keyword argument `time`
        - **time dependent**: It is time dependent only if it is a function with the keyword argument `time`.

    About the positional and keyword arguments: It is not distinguished between positional-only or keyword-only
    arguments. In ths scope of this class, an argument is positional if it has no default and a keyword argument if it
    has a default.

    If the value is nonlinear or time dependent, it is strongly recommended to implement the value as a callable object
    of a class. Only then, the method `update` can be used. Furthermore, it is recommended to have an argument named
    'time' (in case of a time dependent value) and an argument named 'solution' (in case of a nonlinear value). So, it
    can be utilized by the solve-routines.

    Examples
    --------
    An example for a value class is

    >>> class Value:
    >>>     def __init__(self, time=0, solution=None):
    >>>         self.time = time
    >>>         self.solution = solution
    >>>
    >>>     def __call__(self, x, y, time=None, solution=None):
    >>>         if time is None:
    >>>             time = self.time
    >>>         if solution is None:
    >>>             solution = self.solution
    >>>         ...

    This value is nonlinear (because of the `solution` parameter), time dependent (because of the `time` parameter) and
    inhomogeneous (because of the positional arguments `x` and `y`).
    """

    __slots__ = ('_value', 'positional_args', 'keyword_args')

    def __init__(self, value):
        self._value = None
        self.positional_args = []
        self.keyword_args = []

        self.value = value

    @staticmethod
    def compute_args(value):
        """Compute the lists of arguments for a given value."""
        positional_args = []
        keyword_args = []

        if callable(value):
            for key, val in signature(value).parameters.items():
                if val.default is val.empty:
                    positional_args.append(key)
                else:
                    keyword_args.append(key)

        if 't' in keyword_args:
            logger.warning("There is a keyword argument 't' in the value. Note that this is not interpreted as time. "
                           "If you wish to have a time dependency, you have to name this argument 'time'.")

        return positional_args, keyword_args

    @staticmethod
    def num_args(value):
        """Compute the number of args and kwargs."""
        args, kwargs = ValueHandler.compute_args(value)
        return len(args), len(kwargs)

    def _compute_value_args(self):
        """Compute the lists of arguments."""
        self.positional_args, self.keyword_args = self.compute_args(self.value)

    @property
    def value(self):
        """The value."""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._compute_value_args()

    @property
    def inverse_value(self):
        """The inverse value"""
        if callable(self.value):
            parameters = signature(self.value).parameters
            defaults = [parameters.get(kwarg) for kwarg in self.keyword_args]
            if len(self.positional_args) == 0:
                variables_head = ', '.join(f'{v}={d.default}' for v, d in zip(self.keyword_args, defaults))
                variables_body = ', '.join(f'{v}={v}' for v in self.keyword_args)
            else:
                variables_head = ', '.join([', '.join(self.positional_args),
                                            ', '.join(f'{v}={d.default}' for v, d in
                                                      zip(self.keyword_args, defaults))])
                variables_body = ', '.join([', '.join(self.positional_args),
                                            ', '.join(f'{v}={v}' for v in self.keyword_args)])
            head = f'def inverse_fun({variables_head}):'
            body = f'return 1/value({variables_body})'
            local_dict = {}
            exec(f'{head}{body}', {'value': self._value}, local_dict)  # pylint: disable=exec-used

            return local_dict['inverse_fun']
        return 1 / self.value

    @property
    def is_homogeneous(self) -> bool:
        """
        Returns True if the value is homogeneous and False if not

        Returns
        -------
        bool
            True: value is homogeneous. False: value is not homogeneous.

        """
        if not callable(self.value):
            return True
        return len(self.positional_args) == 0

    @property
    def is_linear(self) -> bool:
        """
        Returns True if the value is linear and False if not

        Returns
        -------
        bool
            True: value is linear. False: value is not linear.

        """
        if not callable(self.value):
            return True
        return len(set(self.keyword_args) - {'time'}) == 0

    @property
    def is_time_dependent(self) -> bool:
        """
        Returns True if the value is time dependent and False if not

        Returns
        -------
        bool
            True: value is time dependent. False: value is not time dependent.

        """
        return 'time' in self.keyword_args

    @property
    def is_constant(self) -> bool:
        """Returns True if the value is constant, i.e. linear, homogeneous and not time dependent

        Returns
        -------
        constant : bool
        """
        return all((self.is_homogeneous, self.is_linear, not self.is_time_dependent))

    def update(self, name: str, val: Any):
        """Updates the arguments of the value, if possible.

        Parameters
        ----------
        name : str
            The name of the argument of value to update
        val : Any
            The new value
        """
        if name not in self.keyword_args:
            return
        self._value.__setattr__(name, val)

    def evaluate(self,
                 evaluation_points: np.ndarray = None,
                 elements: np.ndarray = None,
                 on_edge: bool = False,
                 on_face: bool = False,
                 **kwargs) -> Union[np.ndarray, float]:
        """
        Evaluate the Property's value at the evaluation points or for given elements for the num. integration.

        .. table:: Symbols

            ======  =======
            Symbol  Meaning
            ======  =======
            N       Number of evaluation points
            E       Number of elements in `elements`
            ======  =======

        Parameters
        ----------
        evaluation_points : np.ndarray
            (E,N,2) array. The evaluation points for all elements. See :py:func:`calc_evaluation_points_element`.
        elements : np.ndarray
            (E,) array. Array of the considered elements.
        on_edge : bool
            If true, the property is evaluated on an edge.
        on_face : bool
            If true, the property is evaluated on a face.
        **kwargs
            Pass custom eval_functions as kwarg. Key: 'eval_<hom,inhom>_<lin,nonlin>_<iso,aniso>'.

        Returns
        -------
        evaluations : np.ndarray
            (E,N,...) array. For every element the N evaluations of the material function at the evaluation points for
            the numerical integration.
        """
        if on_edge:
            if evaluation_points is None:
                raise AttributeError("evaluation_points are needed for evaluation on a edge!")
            return kwargs.get('evaluate_for_num_int_edge', evaluate_for_num_int_edge)(self.value, evaluation_points)

        if on_face:
            if evaluation_points is None:
                raise AttributeError("evaluation_points are needed for evaluation on a face!")
            return kwargs.get('evaluate_for_num_int_face', evaluate_for_num_int_face)(self.value, evaluation_points)

        if self.is_homogeneous:
            if self.is_linear:
                if hasattr(self, "is_isotrop"):
                    if self.is_isotrop:  # homogeneous, linear, isotropic  pylint: disable=no-else-return
                        return self.value() if self.is_time_dependent else self.value  # pylint: disable=not-callable
                    else:  # homogenous, linear, anisotropic
                        return self.value
                else:
                    return self.value() if self.is_time_dependent else self.value  # pylint: disable=not-callable

            else:  # homogeneous, nonlinear:
                if isinstance(self.value, np.ndarray):
                    return self.value

                if elements is None:
                    raise AttributeError("The elements' indices are needed for homogeneous nonlinear cases.")
                if hasattr(self, "is_isotrop"):
                    if self.is_isotrop:  # homogeneous, nonlinear, isotropic  pylint: disable=no-else-return
                        return kwargs.get('eval_hom_nonlin_iso', eval_hom_nonlin_iso)(self.value, elements)
                    else:  # anisotrop:  # homogeneous, nonlinear, anisotropic
                        return kwargs.get('eval_hom_nonlin_aniso', eval_hom_nonlin_aniso)(self.value, elements)
                else:
                    return kwargs.get('eval_hom_nonlin_iso', eval_hom_nonlin_iso)(self.value, elements)

        else:  # inhomogeneous:
            if evaluation_points is None:
                raise AttributeError("evaluation_points are needed for inhomogeneous cases!")

            if self.is_linear:
                if hasattr(self, "is_isotrop"):
                    if self.is_isotrop:  # inhomogeneous, linear, isotropic  pylint: disable=no-else-return
                        return kwargs.get('eval_inhom_lin_iso', eval_inhom_lin_iso)(self.value, evaluation_points)
                    else:  # inhomogeneous, linear, anisotropic:
                        return kwargs.get('eval_inhom_lin_aniso', eval_inhom_lin_aniso)(self.value, evaluation_points)
                else:
                    return kwargs.get('eval_inhom_lin_iso', eval_inhom_lin_iso)(self.value, evaluation_points)

            else:  # inhomogeneous, nonlinear:
                if elements is None:
                    raise AttributeError("The elements' indices are needed for inhomogeneous and nonlinear cases.")
                if evaluation_points.shape[0] != elements.shape[0]:
                    raise AttributeError(f"There are {evaluation_points.shape[0]} given "
                                         f"for {elements.shape[0]} elements!")
                if hasattr(self, "is_isotrop"):
                    if self.is_isotrop:  # inhomogeneous, nonlinear, isotropic  pylint: disable=no-else-return
                        return kwargs.get('eval_inhom_nonlin_iso', eval_inhom_nonlin_iso)(self.value,
                                                                                          evaluation_points,
                                                                                          elements)
                    else:  # inhomogeneous, nonlinear, anisotrop
                        return kwargs.get('eval_inhom_nonlin_aniso', eval_inhom_nonlin_aniso)(self.value,
                                                                                              evaluation_points,
                                                                                              elements)
                else:
                    return kwargs.get('eval_inhom_nonlin_iso', eval_inhom_nonlin_iso)(self.value,
                                                                                      evaluation_points,
                                                                                      elements)
