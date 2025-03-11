# coding=utf-8
"""Functions for time integration

.. sectionauthor:: Bundschuh
"""
from typing import Callable, Tuple, List, Dict, Any, Set, Union
from inspect import signature
from dataclasses import dataclass, field

import numpy as np
from scipy import sparse

from pyrit.toolbox.MiscellaneousToolbox import solve_linear_system
from pyrit import get_logger

logger = get_logger(__name__)

Solver = Callable[[Callable[[float], Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]],
                   float,
                   float,
                   np.ndarray,
                   Callable[[sparse.spmatrix, sparse.spmatrix], Tuple[np.ndarray, Any]]],
                  Tuple[np.ndarray, Any]]


@dataclass(frozen=True)
class ButcherTableau:
    """Class representing a butcher tableau."""

    name: str = field(compare=True)
    a_matrix: np.ndarray = field(compare=False, repr=False)
    b_vector: np.ndarray = field(compare=False, repr=False)
    c_vector: np.ndarray = field(compare=False, repr=False)
    order: int = field(compare=True)
    is_explicit: bool = field(compare=False, init=False, default=None, repr=False)
    is_implicit: bool = field(compare=False, init=False, default=None, repr=False)

    def __post_init__(self):
        object.__setattr__(self, 'is_explicit', self.__compute_is_explicit())
        object.__setattr__(self, 'is_implicit', not object.__getattribute__(self, 'is_explicit'))

    def __lt__(self, other):
        if self.order == other.order:
            return self.name < other.name
        return self.order < other.order

    def __gt__(self, other):
        if self.order == other.order:
            return self.name > other.name
        return self.order > other.order

    def get_matrices(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get the matrices of the tableau"""
        return self.a_matrix, self.b_vector, self.c_vector

    def __compute_is_explicit(self):
        for line in range(self.a_matrix.shape[0]):
            for column in range(line, self.a_matrix.shape[1]):
                if self.a_matrix[line, column] != 0:
                    return False
        return True


def _append_butcher_tableau_doc(tableaus: Set[ButcherTableau]):
    """Return the docstring text that generates a table with the butcher tableaus in the set."""
    text = "Available tableaus are listed in the following table:\n\n" \
           ".. csv-table:: Available tableaus\n" \
           "\t:header-rows: 1 \n" \
           "\t:delim: :\n\n" \
           "\tName:Order:Explicit\n"

    for bt in sorted(tableaus):
        text += f"\t{bt.name}:{bt.order}:{bt.is_explicit}\n"
    return text


class ButcherTableauDB:
    """Database of butcher tableaus"""

    tableaus = {ButcherTableau("implicit euler",
                               np.array([[1]]),
                               np.array([1]),
                               np.array([1]), 1),
                ButcherTableau("explicit euler",
                               np.array([[0]]),
                               np.array([1]),
                               np.array([0]), 1),
                ButcherTableau("heun",
                               np.array([[0, 0], [1, 0]]),
                               np.array([0.5, 0.5]),
                               np.array([0, 1]), 2),
                ButcherTableau("rk2",
                               np.array([[0, 0], [0.5, 0]]),
                               np.array([0, 1]),
                               np.array([0, 0.5]), 2),
                ButcherTableau("implicit trapezoidal",
                               np.array([[0, 0], [0.5, 0.5]]),
                               np.array([0.5, 0.5]),
                               np.array([0, 1]), 2),
                ButcherTableau("rk3",
                               np.array([[0, 0, 0], [0.5, 0, 0], [-1, 2, 0]]),
                               np.array([1 / 6, 4 / 6, 1 / 6]),
                               np.array([0, 0.5, 1]), 3),
                ButcherTableau("heun3",
                               np.array([[0, 0, 0], [1 / 3, 0, 0], [0, 2 / 3, 0]]),
                               np.array([1 / 4, 0, 3 / 4]),
                               np.array([0, 1 / 3, 2 / 3]), 3),
                ButcherTableau("rk4",
                               np.array([[0, 0, 0, 0], [0.5, 0, 0, 0], [0, 1 / 2, 0, 0], [0, 0, 1, 0]]),
                               np.array([1 / 6, 1 / 3, 1 / 3, 1 / 6]),
                               np.array([0, 0.5, 0.5, 1]), 4)}

    _append_butcher_tableau_doc = _append_butcher_tableau_doc

    __doc__ += _append_butcher_tableau_doc(tableaus)

    @classmethod
    def available_tableaus(cls) -> List[str]:
        """A list of the names of available butcher tableaus."""
        return [bt.name for bt in cls.tableaus]

    @classmethod
    def get_tableau(cls, name: str) -> ButcherTableau:
        """Get the butcher tableau of the specified name"""
        tableau_dict = {bt.name: bt for bt in cls.tableaus}
        if name not in tableau_dict:
            raise ValueError(f"The method '{name}' is not known.")
        return tableau_dict[name]

    @classmethod
    def get_matrices(cls, name: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get the matrices of the butcher tableau of the specified name"""
        return cls.get_tableau(name).get_matrices()


def rk_solver(get_system: Callable[[float], Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]],
              previous_time_step: float,
              current_time_step: float,
              previous_solution: np.ndarray,
              solve_system: Callable[[sparse.spmatrix, sparse.spmatrix], Tuple[np.ndarray, Any]],
              a_matrix: np.ndarray,
              b_vector: np.ndarray,
              c_vector: np.ndarray):
    r"""Perform a step in time integration with a rune kutta method

    The method is specified by the matrix and vectors from its butcher tableau.

    Parameters
    ----------
    get_system : Callable[[float], Tuple[List[sparse.spmatrix], List[sparse.spmatrix]]]
        Function to get the system of ODEs to solve. The following format is expected:

        .. math::

            \mathbf{A} \mathbf{u} + \mathbf{B} \partial_t\mathbf{u} = \mathbf{q}\,.

        The first entry in the return tuple is the matrix :math:`\mathbf{A}` and the second one is :math:`\mathbf{B}`.
        The second entry in the return tuple is the vector ::math:`\mathbf{q}`.
    previous_time_step : float
        Time instance of the previous time step
    current_time_step : float
        Time instance of the next time step, i.e. the time step to which a solution is computed
    previous_solution : np.ndarray
        (N,1) array. solution on the previous time step
    solve_system : Callable[[sparse.spmatrix, sparse.spmatrix], Tuple[np.ndarray, Any]]
        Function that solves a linear system of equations. Its parameters are the system matrix and the right-hand side.
        It returns the solution and some additional information, e.g. on the relative error in the case of an iterative
        solver.
    a_matrix : np.ndarray
        The matrix :math:`A` of the tableau
    b_vector : np.ndarray
        The vector :math:`b` of the tableau
    c_vector : np.ndarray
        The vector :math:`c` of the tableau

    Returns
    -------
    solution : np.ndarray
        The solution at the current time step
    solver_info : Any
        Additional information on the solution
    """
    previous_solution = sparse.csc_matrix(np.atleast_2d(previous_solution))
    step_width = current_time_step - previous_time_step
    num_steps = a_matrix.shape[0]

    # region Compute matrices and rhs
    matrices_constant, matrices_derivative, rhs = [], [], []
    for c_j in c_vector:
        matrices_tmp, rhs_tmp = get_system(previous_time_step + c_j * step_width)
        matrices_constant.append(matrices_tmp[0])
        matrices_derivative.append(matrices_tmp[1])
        rhs.append(rhs_tmp[0])
    # endregion

    size_solution = matrices_constant[0].shape[0]

    # region Build system to determine k
    # sparse.block_diag(matrices_derivative)
    b_mat_list = [[a_matrix[row, col] * matrices_constant[row] for col in range(num_steps)] for row in range(num_steps)]

    system_matrix = step_width * sparse.bmat(b_mat_list) + sparse.block_diag(matrices_derivative)

    system_rhs = sparse.vstack([rhs[k] - matrices_constant[k] @ previous_solution for k in range(num_steps)])
    # endregion

    k_vector, solver_info = solve_system(system_matrix, system_rhs.toarray())

    k_matrix = k_vector.reshape((size_solution, num_steps))
    solution = previous_solution.toarray() + step_width * np.sum(k_matrix @ np.diag(b_vector), axis=1)

    return solution.flatten(), solver_info


def rk_solver_factory(name: str) -> Solver:
    """Returns a solver that uses a runge kutta method.

    Parameters
    ----------
    name : str
        Name of the runge kutta method

    Returns
    -------
    rk_solve : Solver
    """
    a_matrix, b_vector, c_vector = ButcherTableauDB.get_matrices(name)

    def stepper(get_system, previous_time_step, current_time_step, previous_solution, solve_system):
        return rk_solver(get_system, previous_time_step, current_time_step, previous_solution, solve_system,
                         a_matrix, b_vector, c_vector)

    return stepper


def _time_integration(initial_value: np.ndarray,
                      time_steps: np.ndarray,
                      get_system: Callable[[float], Tuple[List[sparse.spmatrix], sparse.spmatrix]],
                      integration_step: Solver,
                      store_solution_time_steps: Union[np.ndarray, str],
                      events: List[Callable[[Any], None]],
                      evaluation_functions: List[Callable[[Any], Dict[str, Any]]],
                      solve_system: Callable[[sparse.spmatrix, sparse.spmatrix], Tuple[np.ndarray, Any]]) \
        -> Tuple[List[np.ndarray], Dict[str, List[Any]]]:
    r"""Time integration for an ODE

    initial_value : np.ndarray
        (N,) array with the initial value of the ODE.
    time_steps : np.ndarray
        (T,) array with the time steps.
    get_system : Callable[[float], Tuple[List[sparse.spmatrix], sparse.spmatrix]]
        Function to get the system of ODEs to solve. The following format is expected:

        .. math::

            \mathbf{A} \mathbf{u} + \mathbf{B} \partial_t\mathbf{u} = \mathbf{q}\,.

        The first entry in the return tuple is the matrix :math:`\mathbf{A}` and the second one is :math:`\mathbf{B}`.
        The second entry in the return tuple is the vector ::math:`\mathbf{q}`.
    integration_step : Union[Solver, str], optional
        The method used to compute the solution at the next time step. Default is an implicit euler
    store_solution_time_steps : Union[np.ndarray, str]
        (S,) array with the indices of the time steps to store the solution.
        Options are:

            - "every x": Store every x-th time step
            - "first x": Store the first x time steps
            - "last x": Store the last x time steps

        The initial value is per default part of this.
    events : List[Callable[[Any], None]]
        A list of functions that are called after every iteration. These functions should not return anything. The
        arguments of this function may be one of:

        - k: The current index of the time step
        - t: The current time step
        - delta_t: The time difference between this and the last time step
        - solution: The solution at the current time step
        - solution_info: The solution info at the current time step

    evaluation_functions : List[Callable[[Any], Dict[str, Any]]]
        A list of functions that are called after every iteration. These functions must return a dictionary with the
        keys being string and the value being anything. For every time step, the values of all these dictionaries are
        gathered in another dictionary and are returned as the `results`. The functions can take the same arguments as
        the events. If an evaluation should not be performed at this time instance, the function must return None.
        For the first initial time step, i.e. k=0, it must not return None.
    solve_system : Callable[[sparse.spmatrix, sparse.spmatrix], Tuple[np.ndarray, Any]]
        Function used to solve linear systems of equations.

    Returns
    -------
    solutions : List[np.ndarray]
        A list with the solutions
    results : Dict[str,Tuple[List[int], List[Any]]
        A dictionary with the results. The key ist the key from the evaluation functions. The value is a tuple with the
        indices of time instances at which the evaluations have been performed and the results of the evaluations.
    """
    time_step_dict = dict(k=0, t=time_steps[0], delta_t=None, solution=initial_value, solution_info=None)
    possible_args = time_step_dict.keys()

    # region Compute parameters for evaluation functions
    eval_function_params = []
    for eval_function in evaluation_functions:
        param_names_tmp = []
        for param_name, param in signature(eval_function).parameters.items():
            if param_name not in possible_args:
                if param.default is param.empty:
                    raise ValueError(f"The parameter {param_name} is not known and there is not default value")
            else:
                param_names_tmp.append(param_name)
        eval_function_params.append(param_names_tmp)
    # endregion

    # region Compute parameters for event functions
    event_function_params = []
    for event in events:
        param_names_tmp = []
        for param_name, param in signature(event).parameters.items():
            if param_name not in possible_args:
                if param.default is param.empty:
                    raise ValueError(f"The parameter {param_name} is not known and there is not default value")
            else:
                param_names_tmp.append(param_name)
        event_function_params.append(param_names_tmp)

    # endregion

    # region Initialize results
    results = {}
    for m, eval_function in enumerate(evaluation_functions):
        results_tmp = eval_function(**{k: v for k, v in time_step_dict.items() if k in eval_function_params[m]})
        if results_tmp is None:
            raise ValueError
        for key, value in results_tmp.items():
            if key in results:
                raise ValueError(f"The key '{key}' appears in multiple evaluation functions")
            results[key] = ([0], [value])
    # endregion

    solutions = []
    counter_solution_store = 0
    if store_solution_time_steps[0] == 0:
        solutions.append(initial_value)
        counter_solution_store += 1

    previous_solution = initial_value
    for k, time_step in enumerate(time_steps):
        if k == 0:
            continue
        previous_solution, solution_info = integration_step(get_system, time_steps[k - 1], time_step, previous_solution,
                                                            solve_system)
        previous_solution = np.atleast_1d(previous_solution)
        time_step_dict = dict(k=k, t=time_step, delta_t=time_step - time_steps[k - 1],
                              solution=previous_solution, solution_info=solution_info)

        for m, event in enumerate(events):
            event(**{key: value for key, value in time_step_dict.items() if key in event_function_params[m]})

        for m, eval_function in enumerate(evaluation_functions):
            eval_result = eval_function(
                **{key: value for key, value in time_step_dict.items() if key in eval_function_params[m]})
            if eval_result is not None:
                for key, value in eval_result.items():
                    results[key][0].append(k)
                    results[key][1].append(value)

        try:
            if store_solution_time_steps[counter_solution_store] == k:
                solutions.append(previous_solution)
                counter_solution_store += 1
        except IndexError:
            pass
    return solutions, results


def time_integration(initial_value: np.ndarray,
                     time_steps: np.ndarray,
                     get_system: Callable[[float], Tuple[List[sparse.spmatrix], sparse.spmatrix]], *,
                     integration_step: Union[Solver, str] = None,
                     store_solution_time_steps: Union[np.ndarray, str] = None,
                     events: List[Callable[[Any], None]] = None,
                     evaluation_functions: List[Callable[[Any], Dict[str, Any]]] = None,
                     solve_system: Callable[[sparse.spmatrix, sparse.spmatrix], Tuple[np.ndarray, Any]] = None) \
        -> Tuple[np.ndarray, List[np.ndarray], Dict[str, Tuple[List[int], List[Any]]]]:
    r"""Time integration for an ODE

    Parameters
    ----------
    initial_value : np.ndarray
        (N,) array with the initial value of the ODE.
    time_steps : np.ndarray
        (T,) array with the time steps.
    get_system : Callable[[float], Tuple[List[sparse.spmatrix], sparse.spmatrix]]
        Function to get the system of ODEs to solve. The following format is expected:

        .. math::

            \mathbf{A} \mathbf{u} + \mathbf{B} \partial_t\mathbf{u} = \mathbf{q}\,.

        The first entry in the return tuple is the matrix :math:`\mathbf{A}` and the second one is :math:`\mathbf{B}`.
        The second entry in the return tuple is the vector ::math:`\mathbf{q}`.
    integration_step : Union[Solver, str], optional
        The method used to compute the solution at the next time step. Default is an implicit euler
    store_solution_time_steps : Union[np.ndarray, str], optional
        (S,) array with the indices of the time steps to store the solution. Default is all time steps
        Options are:

            - "every x": Store every x-th time step
            - "first x": Store the first x time steps
            - "last x": Store the last x time steps

        The initial value is per default part of this.
    events : List[Callable[[Any], None]], optional
        A list of functions that are called after every iteration. These functions should not return anything. The
        arguments of this function may be one of:

        - k: The current index of the time step
        - t: The current time step
        - delta_t: The time difference between this and the last time step
        - solution: The solution at the current time step
        - solution_info: The solution info at the current time step

        The default is an empty list.
    evaluation_functions : List[Callable[[Any], Dict[str, Any]]], optional
        A list of functions that are called after every iteration. These functions must return a dictionary with the
        keys being string and the value being anything. For every time step, the values of all these dictionaries are
        gathered in another dictionary and are returned as the `results`. The functions can take the same arguments as
        the events. If an evaluation should not be performed at this time instance, the function must return None.
        For the first initial time step, i.e. k=0, it must not return None. The default is an empty list.
    solve_system : Callable[[sparse.spmatrix, sparse.spmatrix], Tuple[np.ndarray, Any]], optional
        Function used to solve linear systems of equations.

    Returns
    -------
    solution_time_steps: np.ndarray
        An array with the time steps of the solution.
    solutions : List[np.ndarray]
        A list with the solutions
    results : Dict[str,Tuple[List[int], List[Any]]
        A dictionary with the results. The key ist the key from the evaluation functions. The value is a tuple with the
        indices of time instances at which the evaluations have been performed and the results of the evaluations.

    Examples
    --------
    A simple example is a 1-dimensional ODE. We consider

    .. math::

        u + \partial_t u = \sin(t) + \cos(t)\,.

    The solution to this ODE is :math:`u(t) = \sin(t)`. We define the function that gets the system as

    >>> def get_system(time):
    >>>     return [sparse.csr_matrix(np.array([[1.]])),
    >>>             sparse.csr_matrix(np.array([[1.]]))],
    >>>            [sparse.csr_matrix(np.cos(time)+np.sin(time))]

    Then, we can solve the problem with

    >>> time_steps = np.linspace(0, 2*np.pi, 1000)
    >>> solution_time_steps, solution, results = time_integration(np.array([0]), time_steps, get_system)

    If we only want to have the solution at every fifth time step, we can write

    >>> time_integration(np.array([0]), time_steps, get_system, store_solution_time_steps="every 5")

    If we want to print the iteration number, we first define a function:

    >>> def print_iteration_number(k):
    >>>     if k%10 == 0:
    >>>         print(f"Iteration {k}")

    Then, we write

    >>> time_integration(np.array([0]), time_steps, get_system, store_solution_time_steps="every 5",
    >>>                  events=[print_iteration_number])

    The default method for time integration is an implicit Euler method. However, an arbitrary Runge-Kutta method can be
    used. This is supported by the function :py:func:`rk_solver` that has the matrix and vectors of the Butcher tableau
    as arguments. Also, a predefined Runge-Kutta scheme can be used. For that, use the function
    :py:func:`rk_solver_factory` as in the following code cell:

    >>> time_integration(np.array([0]), time_steps, get_system, integration_step=rk_solver_factory("heun3"))

    See the class :py:class:`ButcherTableauDB` for available methods.
    """
    if not len(initial_value.shape) == 1:
        logger.warning("The initial value is not in expected format")

    if not len(time_steps.shape) == 1:
        logger.warning("The time_steps array is not in expected format.")

    if integration_step is None:
        integration_step = rk_solver_factory("implicit euler")
    elif isinstance(integration_step, str):
        integration_step = rk_solver_factory(integration_step)

    if store_solution_time_steps is None:
        store_solution_time_steps = np.arange(len(time_steps))
    elif isinstance(store_solution_time_steps, str):
        try:
            kind, number = store_solution_time_steps.split(" ")
        except ValueError as e:
            raise ValueError(f"Wrong format '{store_solution_time_steps}'") from e
        number = int(number)

        if kind == "every":
            store_solution_time_steps = np.arange(0, len(time_steps), number)
            if store_solution_time_steps[-1] != len(time_steps) - 1:
                store_solution_time_steps = np.append(store_solution_time_steps, len(time_steps) - 1)
        elif kind == "first":
            store_solution_time_steps = np.arange(number)
        elif kind == "last":
            store_solution_time_steps = np.arange(len(time_steps) - number, len(time_steps))
        else:
            raise ValueError(f"Kind '{kind}' not known. Use one of 'every', 'first', 'last'")
    elif not np.issubdtype(store_solution_time_steps.dtype, np.integer):
        raise ValueError("The dtype of 'store_solution_time_steps' must be int.")

    if events is None:
        events = []
    if evaluation_functions is None:
        evaluation_functions = []
    if solve_system is None:
        solve_system = solve_linear_system

    solution_time_steps = time_steps[store_solution_time_steps]
    solution, results = _time_integration(initial_value, time_steps, get_system, integration_step,
                                          store_solution_time_steps, events, evaluation_functions, solve_system)
    return solution_time_steps, solution, results
