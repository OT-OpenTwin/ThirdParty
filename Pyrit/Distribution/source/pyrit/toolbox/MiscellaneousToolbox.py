# coding=utf-8
"""
Toolbox for miscellaneous functions

.. sectionauthor:: bundschuh, thyssen
"""

from inspect import signature
from typing import Union, List, Tuple, Dict, Any, Callable, Iterable
import enum
from time import time
import contextlib
import cProfile
import pstats
from abc import ABC, abstractmethod
import numpy as np
import scipy.sparse.linalg as splinalg
from scipy import sparse

from pyrit import get_logger

logger = get_logger(__name__)

_pypardiso_available = True
try:
    import pypardiso
    PyPardisoSolver = pypardiso.PyPardisoSolver
except ImportError as e:
    _pypardiso_available = False

    pypardiso = None
    PyPardisoSolver = object


def evaluate_function(fun: Callable[..., Any], dependencies: List[str] = None, **kwargs) -> Any:
    """
    Evaluates the function fun. The needed parameters are taken from kwargs.

    Parameters
    ----------
    fun : Callable[..., Any]
        The function to evaluate
    dependencies : List[str], optional
        A list of dependencies. If not given it is calculated internally.
    kwargs :
        All Attributes

    Returns
    -------
    The return value of the function fun
    """
    if dependencies is None:
        dependencies = list(signature(fun).parameters.keys())
    kw = {}
    for key in dependencies:
        if key in kwargs:
            kw[key] = kwargs[key]
        else:
            raise Exception("Key not in dependencies")

    return fun(**kw)


def timer_func(func):
    """Decorator that measures the time for a function."""

    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {((t2 - t1) * 1000):.9f} ms')
        return result

    return wrap_func


@contextlib.contextmanager
def profile(sort_key=None):
    """A profiler context manager.

    Collects the execution times of functions.

    Parameters
    ----------
    sort_key: str
        The key to sort the results. Eiter 'time', 'cumulative', 'calls', 'module' or any other `SortKey` from `pstats`
        module.
    """
    sort_keys = {'time': pstats.SortKey.TIME, 'cumulative': pstats.SortKey.CUMULATIVE, 'calls': pstats.SortKey.CALLS,
                 'module': pstats.SortKey.FILENAME}
    if sort_key is None:
        sort_key = 'time'
    sort_key = sort_keys.setdefault(sort_key, sort_key)

    with cProfile.Profile() as pr:
        yield pr
    stats = pstats.Stats(pr)
    stats.sort_stats(sort_key)
    stats.print_stats()


class SolverUnknownError(Exception):
    """Custom Error when a solver in the function `solve_linear_system` is not known."""


# pylint: disable=invalid-name
class MatrixType(enum.Enum):
    """Enum for the matrix types pardiso can handle.

    See https://pardiso-project.org/manual/manual.pdf the documentation of MTYPE

    Available types are:

    .. csv-table::
        :header-rows: 1
        :delim: :

        Name:Value
        REAL_AND_STRUCTURALLY_SYMMETRIC:1
        REAL_AND_SYMMETRIC_POSITIVE_DEFINITE:2
        REAL_AND_SYMMETRIC_INDEFINITE:-2
        COMPLEX_AND_STRUCTURALLY_SYMMETRIC:3
        COMPLEX_AND_HERMITIAN_POSITIVE_DEFINITE:4
        COMPLEX_AND_HERMITIAN_INDEFINITE:-4
        COMPLEX_AND_SYMMETRIC:6
        REAL_AND_NONSYMMETRIC:11
        COMPLEX_AND_NONSYMMETRIC:13
    """

    REAL_AND_STRUCTURALLY_SYMMETRIC = 1
    REAL_AND_SYMMETRIC_POSITIVE_DEFINITE = 2
    REAL_AND_SYMMETRIC_INDEFINITE = -2
    COMPLEX_AND_STRUCTURALLY_SYMMETRIC = 3
    COMPLEX_AND_HERMITIAN_POSITIVE_DEFINITE = 4
    COMPLEX_AND_HERMITIAN_INDEFINITE = -4
    COMPLEX_AND_SYMMETRIC = 6
    REAL_AND_NONSYMMETRIC = 11
    COMPLEX_AND_NONSYMMETRIC = 13


# pylint: disable=invalid-name,consider-using-f-string,logging-too-many-args,logging-format-interpolation
class PyritPardisoSolver(PyPardisoSolver):
    """Extension of the class PyPardisoSolver from pypardiso

    For documentation on pardiso, see https://pardiso-project.org/manual/manual.pdf
    """

    MatrixType = MatrixType

    def _check_A(self, A):
        if A.shape[0] != A.shape[1]:
            raise ValueError('Matrix A needs to be square, but has shape: {}'.format(A.shape))

        if sparse.isspmatrix_csr(A):
            self._solve_transposed = False
            self.set_iparm(12, 0)
        elif sparse.isspmatrix_csc(A):
            self._solve_transposed = True
            self.set_iparm(12, 1)
        else:
            msg = 'PyPardiso requires matrix A to be in CSR or CSC format, but matrix A is: {}'.format(type(A))
            raise TypeError(msg)

        # scipy allows unsorted csr-indices, which lead to completely wrong pardiso results
        if not A.has_sorted_indices:
            A.sort_indices()

        # scipy allows csr matrices with empty rows. a square matrix with an empty row is singular. calling
        # pardiso with a matrix A that contains empty rows leads to a segfault, same applies for csc with
        # empty columns
        if not np.diff(A.indptr).all():
            row_col = 'column' if self._solve_transposed else 'row'
            raise ValueError('Matrix A is singular, because it contains empty {}(s)'.format(row_col))

    def _check_b(self, A, b):
        if sparse.isspmatrix(b):
            logger.warning('PyPardiso requires the right-hand side b to be a dense array for maximum efficiency',
                           sparse.SparseEfficiencyWarning)
            b = b.todense()

        # pardiso expects fortran (column-major) order for b
        if not b.flags.f_contiguous:
            b = np.asfortranarray(b)

        if b.shape[0] != A.shape[0]:
            raise ValueError("Dimension mismatch: Matrix A {} and array b {}".format(A.shape, b.shape))

        if b.dtype in [np.float16, np.float32, np.int16, np.int32, np.int64]:
            logger.warning("Array b's data type was converted from {} to float64".format(str(b.dtype)))
            b = b.astype(np.float64)

        return b

    def solve(self, A, b):
        """Solve a linear system Ax=b"""
        return super().solve(A, b)

    def __call__(self, A: sparse.csr_matrix, b: Union[sparse.spmatrix, np.ndarray], **kwargs):
        if not _pypardiso_available:
            raise ImportError("pypardiso is not available. Please install it to use the Pardiso solver.")

        if "print_info" in kwargs:
            self.msglvl = int(bool(kwargs.pop("print_info")))
        mtype = kwargs.pop("mtype", self.MatrixType.REAL_AND_NONSYMMETRIC)

        if not isinstance(mtype, self.MatrixType):
            raise ValueError("Wrong type of mtype")

        if np.issubdtype(A.dtype, np.complexfloating) or np.issubdtype(b.dtype, np.complexfloating):
            mtype = self.MatrixType.COMPLEX_AND_NONSYMMETRIC
        self.mtype = mtype.value

        if isinstance(b, sparse.spmatrix):
            return pypardiso.spsolve(A, b.toarray(), solver=self)
        return pypardiso.spsolve(A, b, solver=self)


pyrit_pardiso_solver = PyritPardisoSolver()


# pylint: disable=line-too-long
def solve_linear_system(matrix: sparse.spmatrix, rhs: Union[sparse.spmatrix, np.ndarray],
                        solver: Union[str, Callable[[sparse.csr_matrix, Union[sparse.spmatrix, np.ndarray]],
                                                    Tuple[np.ndarray, Dict[str, Any]]]] = None,
                        **kwargs) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Solve a system of linear equations.

    General method for solving a system of linear equations,
    defined at :py:func:`pyrit.toolbox.MiscelaneousToolbox.solve_linear_system`.
    The matrix and the right-hand-side (rhs) must be given.
    With solver, it can be determined how to solve the system. There are some predefined solvers. It can also be passed
    a function, if you want to provide your own solver. The signature has to be as defined.

    Parameters
    ----------
    matrix : sparse.spmatrix
        The system matrix.
    rhs : Union[sparse.spmatrix, np.ndarray]
        The right-hand-side vector
    solver : Union[str, Callable[[sparse.csr_matrix, Union[sparse.spmatrix, np.ndarray]], Tuple[np.ndarray, Dict[str, Any]]]], optional
        The used solver. In the case of a string, use one of the predefined solvers. In the case of a function, make
        sure that the signature is as expected. The function gets the system matrix as first argument and the
        right-hand-side as second argument. It must return the solution as first value and a dictionary with information
        as second value.  Furthermore, the kwargs are passed to the function.
    kwargs :
        kwargs passed to the solver.

    Returns
    -------
    solution : np.ndarray
        The solution of the system of linear equations.
    info : Dict[str, Any]
        A dictionary with information from the solver.
    """
    if solver is None:
        solver = "pardiso" if _pypardiso_available else "spsolve"

    if solver == "pardiso" and not _pypardiso_available:
        logger.warning("Pardiso solver is not available. Using spsolve instead.")
        solver = "spsolve"

    matrix = matrix.tocsr()
    if not isinstance(rhs, (sparse.spmatrix, np.ndarray)):
        raise ValueError("The type of the right hand side is not known.")
    if isinstance(rhs, sparse.spmatrix):
        rhs = rhs.tocsr()

    # Iterative solvers from scipy.sparse.linalg. All have the same basic signature
    iteratiev_solvers = {'bicg': splinalg.bicg, 'bicgstab': splinalg.bicgstab, 'cg': splinalg.cg, 'cgs': splinalg.cgs,
                         'gmres': splinalg.gmres, 'lgmres': splinalg.lgmres, 'minres': splinalg.minres,
                         'qmr': splinalg.qmr, 'gcrotmk': splinalg.gcrotmk, 'tfqmr': splinalg.tfqmr}
    if callable(solver):
        result, info = solver(matrix, rhs, **kwargs)
    else:
        if solver == 'spsolve':
            result = splinalg.spsolve(matrix, rhs, **kwargs)
            info = {}
        elif solver in iteratiev_solvers:
            result, conv_info = iteratiev_solvers[solver](matrix, rhs, **kwargs)
            info = {'convergence info': conv_info}
        elif solver == 'pardiso':
            result = pyrit_pardiso_solver(matrix, rhs, **kwargs)
            info = {}
        else:
            raise SolverUnknownError(f"Solver '{solver}' not known.")

    return result, info


class NonlinearSolver(ABC):
    """Constructor of Nonlinear Solver"""

    @abstractmethod
    def __init__(self, convergence_checker):
        """
        Parameters: convergence_checker

        Parameters
        ----------
        convergence_checker: ConvergenceChecker
            providing a convergence check following numpy p norm, numpy max norm or a convergence check based on energy
            considerations
        """
        self.convergence_checker = convergence_checker

    @abstractmethod
    def compute_iteration_result(self, operating_point: np.ndarray) -> np.ndarray:
        """Compute the result of one iteration following a specified method

        Returns
        -------
        iteration_result: np.ndarray
            The result of one iteration
        """

    @abstractmethod
    def update_solution(self, old_solution: np.ndarray, iteration_result: np.ndarray) -> np.ndarray:
        """Update the new old solution with the obtained iteration result following a specified method

        Returns
        -------
        new_solution: np.ndarray
            The new solution that results from the last obtained iteration result and the old_solution
        """

    def check_convergence(self, old_solution: np.ndarray, new_solution: np.ndarray) -> bool:
        """Check convergence of the new solution

        Returns
        -------
        convergence: bool
            True if converged, False if not
        """
        convergence = self.convergence_checker.check_convergence(old_solution, new_solution)
        return convergence


class ConvergenceChecker(ABC):
    """Abtract base class for realization of convergence check classes"""

    @abstractmethod
    def __init__(self, tolerance):
        """Parameters: tolerance

        Parameters
        ----------
        tolerance: float
            Convergence is reached, when the norm of the difference of old_solution and new_solution or energy
            consideration value are smaller than the tolerance value
        """
        self.tolerance = tolerance

    @abstractmethod
    def check_convergence(self, old_solution: np.ndarray, new_solution: np.ndarray) -> bool:
        """Check convergence of the result"""


class PNorm(ConvergenceChecker):
    """Convergence check based on numpy p norm"""

    def __init__(self, tolerance, order):
        """Parameters: tolerance, old_solution, new_solution, order

        Parameters
        ----------
        tolerance: float
            Convergence is reached, when the p norm of the difference of old_solution and new_solution is smaller than
            the tolerance value
        order: int
            order of the norm
        """
        self.order = order
        super().__init__(tolerance)

    def check_convergence(self, old_solution: np.ndarray, new_solution: np.ndarray) -> bool:
        """Check convergence using norm of a specified order"""
        convergence = np.linalg.norm((old_solution - new_solution), self.order)
        return convergence < self.tolerance


class MaxNorm(ConvergenceChecker):
    """Convergence check based on numpy maximum norm"""

    def __init__(self, tolerance):
        """Parameters: tolerance

        Parameters
        ----------
        tolerance: float
            Convergence is reached, when the maximum norm of the difference of old_solution and new_solution is smaller
            than the tolerance value
        """
        super().__init__(tolerance)

    def check_convergence(self, old_solution: np.ndarray, new_solution: np.ndarray) -> bool:
        """Check convergence using numpy maximum norm"""
        convergence = np.linalg.norm((old_solution - new_solution), np.inf)
        return convergence < self.tolerance


class EnergyNorm(ConvergenceChecker):
    """Convergence check based on energy considerations"""

    def __init__(self, tolerance: float, get_energy: Callable[[np.ndarray], float]):
        """Parameters: tolerance, old_solution, new_solution

        Parameters
        ----------
        tolerance: float
            Convergence is reached, when the difference of the energy for the old_solution and for the
            new_solution normed to the new solution is smaller than the tolerance value
        get_energy: Callable[[ndarray], float]
            Callable that takes the operating point and returns the energy value at this operating point
        """
        self.get_energy = get_energy
        super().__init__(tolerance)

    def check_convergence(self, old_solution: np.ndarray, new_solution: np.ndarray) -> bool:
        """Check convergence based on energy considerations"""
        new_energy = self.get_energy(new_solution)
        old_energy = self.get_energy(old_solution)
        convergence = abs((new_energy - old_energy) / new_energy)
        return bool(convergence < self.tolerance)


class NewtonSolver(NonlinearSolver):
    """Nonlinear solver based on Newton method"""

    def __init__(self, problem_function: Callable[[np.ndarray], np.ndarray], convergence_checker: ConvergenceChecker):
        """
        Parameters: problem_function, convergence_checker

        Parameters
        ----------
        problem_function: Callable[[np.ndarray], np.ndarray]
            Function describing the nonlinear problem. It takes the operating point and returns the increment
            for the next iteration.
        convergence_checker: ConvergenceChecker
            object of either PNorm, MaxNorm or EnergyNorm class providing a method to check convergence
        """
        self.problem_function = problem_function
        super().__init__(convergence_checker)

    def compute_iteration_result(self, operating_point: np.ndarray) -> np.ndarray:
        r"""Compute the result of one iteration following a Newton method

        Returns
        -------
        delta_k1: np.ndarray
            increment :math:`\delta \vec A ^{(k+1)}` from old operating point :math:`\vec A ^{(k)}` to the new
            operating point :math:`\vec A ^{(k+1)}`
        """
        if not isinstance(operating_point, np.ndarray):
            raise ValueError("Operating point must be a numpy array.")

        delta_k1 = self.problem_function(operating_point)

        return delta_k1

    def update_solution(self, old_solution: np.ndarray, iteration_result: np.ndarray) -> np.ndarray:
        r"""Update the solution with the obtained iteration result from Newton method

        Returns
        -------
        new_solution: np.ndarray
            np.ndarray containing the new solution which is the sum of the old solution :math:`\vec A ^{(k)}` and the
            increment :math:`\delta \vec A ^{(k+1)}`. So the new solution reads
            :math:`\vec A ^{(k+1)} = \vec A ^{(k)}+\delta \vec A ^{(k+1)}`.
        """
        return old_solution + iteration_result


class SuccessiveSubstitutionSolver(NonlinearSolver):
    """Nonlinear solver based on successive substitution method"""

    def __init__(self, problem_function: Callable[[np.ndarray], np.ndarray],
                 convergence_checker: ConvergenceChecker, relaxation_factor: float):
        r"""Parameters: problem_function, convergence_checker, relaxation_factor

        Parameters
        ----------
        problem_function: Union[Callable[[np.ndarray], np.ndarray]
            Function describing the nonlinear problem. It takes the operating point and returns the function matrix at
            this operating point.
        convergence_checker: ConvergenceChecker
            object of either PNorm, MaxNorm or EnergyNorm class providing a method to check convergence
        relaxation_factor: float
            Factor :math:`0< \alpha < 1` to weight old and new solution to calculate the final new solution
        """
        self.problem_function = problem_function
        self.relaxation_factor = relaxation_factor
        super().__init__(convergence_checker)

    def compute_iteration_result(self, operating_point: np.ndarray) -> np.ndarray:
        """Compute the result of one iteration following successive substitution method

        Returns
        -------
        problem_func_at_op_point: np.ndarray
            solution of the problem function at the operating point
        """
        problem_func_at_op_point = self.problem_function(operating_point)
        return problem_func_at_op_point

    def update_solution(self, old_solution: np.ndarray, iteration_result: np.ndarray) -> np.ndarray:
        r"""Update the solution with the obtained iteration result from successive substitution method

        Returns
        -------
        new_solution: np.ndarray
            np.ndarray being the weighted sum of the old operating pont and the new operating point
            :math:`\vec A^{(k+1)}= \alpha * \vec A^{(k+1)} + (1-\alpha)*\vec A^{(k)}`. :math:`\alpha` is the
            relaxation factor
        """
        new_solution = self.relaxation_factor * iteration_result + (1 - self.relaxation_factor) * \
                       old_solution
        return new_solution


def solve_nonlinear_problem(nonlinear_solver_object: Union[NewtonSolver, SuccessiveSubstitutionSolver],
                            initial_solution: np.ndarray, maximum_iterations: int,
                            callback: Callable, monitor: Dict, solution_monitor: Union[int, Iterable[int]], **kwargs) \
        -> Tuple[np.ndarray, list, Dict]:
    """Solve nonlinear problem using an object of a specified solver and monitor solutions and other results"""
    if isinstance(solution_monitor, int):
        solution_monitor = np.arange(start=0, stop=maximum_iterations - 1, step=solution_monitor)
    solutions = []
    monitor_results = {k: [[], []] for k in monitor.keys()} if monitor else None
    start_solution = initial_solution.flatten()
    for i in range(maximum_iterations):
        iteration_result = nonlinear_solver_object.compute_iteration_result(start_solution)
        new_solution = nonlinear_solver_object.update_solution(start_solution, iteration_result)
        if i in solution_monitor:
            solutions.append(new_solution.toarray() if isinstance(new_solution, sparse.spmatrix) else new_solution)
        has_callback = callback is not None
        if has_callback:
            callback(new_solution.toarray() if isinstance(new_solution, sparse.spmatrix) else new_solution)
        if monitor:
            for key, monitor_func in monitor.items():
                monitor_results[key][0].append(i)
                monitor_results[key][1].append(monitor_func(new_solution.toarray() if isinstance(new_solution,
                                                                                                 sparse.spmatrix)
                                                            else new_solution))
        if i == maximum_iterations - 1:
            print(f"Maximum number of iterations is reached. The current solution is"
                  f"{new_solution.toarray() if isinstance(new_solution, sparse.spmatrix) else new_solution}.")
        elif not nonlinear_solver_object.check_convergence(start_solution, new_solution):
            start_solution = new_solution
        elif nonlinear_solver_object.check_convergence(start_solution, new_solution):
            return (new_solution.toarray() if isinstance(new_solution,
                                                         sparse.spmatrix) else new_solution), solutions, monitor_results
    return (new_solution.toarray() if isinstance(new_solution,
                                                 sparse.spmatrix) else new_solution), solutions, monitor_results
