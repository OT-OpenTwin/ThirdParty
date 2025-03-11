# coding=utf-8
"""File containing the implementation of DistributedSolidConductor

.. sectionauthor:: Bundschuh
"""

from typing import Tuple, TYPE_CHECKING, List, Dict
from copy import deepcopy
import numpy as np
from scipy import sparse

from pyrit.bdrycond.BCConductor import BCConductor
from pyrit.bdrycond.BCSolidConductor import BCSolidConductor
from pyrit.region import Regions
from pyrit.excitation import Excitations

from pyrit import get_logger

if TYPE_CHECKING:
    from pyrit.toolbox.CircuitSimulationToolbox import Circuit
    from pyrit.problem import Problem

logger = get_logger(__name__)


class BCDistributedSolidConductor(BCConductor):
    """Class representing a conductor that consists of many solid conductors in series connection."""

    def __init__(self, number_conductors: int, name: str, circuit: 'Circuit'):
        super().__init__(name, circuit)

        self.number_conductors = number_conductors
        self.solid_conductors: List[BCSolidConductor] = []

    @property
    def additional_dofs(self) -> int:
        return 2 * self.number_conductors + 2

    @property
    def voltage_index(self) -> int:
        return 2 * self.number_conductors

    @property
    def current_index(self) -> int:
        return 2 * self.number_conductors + 1

    def _get_region_id(self, regions):
        region_ids = regions.find_regions_of_boundary_condition(self.ID)

        if len(region_ids) != self.number_conductors:
            logger.warning("The number of regions (%d) does not match the number of conductors (%d). The number of"
                           "conductors is updated.", len(region_ids), self.number_conductors)
            self.number_conductors = len(region_ids)

        return region_ids

    def get_coupling_values(self, problem: 'Problem') -> \
            Tuple[sparse.coo_matrix, sparse.coo_matrix, sparse.coo_matrix, sparse.coo_matrix]:
        region_ids = self._get_region_id(problem.regions)

        tmp_problem = deepcopy(problem)

        bottom_matrices, right_matrices, diagonal_matrices, rhs_matrices = [], [], [], []
        self.solid_conductors = []

        line_current, line_voltage = [], []
        for k, region_id in enumerate(region_ids):
            sc = BCSolidConductor('_'.join([self.name, f"conductor_{k}"]), None)
            sc.region_id = region_id
            self.solid_conductors.append(sc)

            region = deepcopy(problem.regions.get_regi(region_id))
            region.bc = sc.ID

            excitations_tmp = Excitations(sc)
            regions_tmp = Regions(region)

            tmp_problem.regions = regions_tmp
            tmp_problem.excitations = excitations_tmp

            matrix_bot_tmp, matrix_right_tmp, matrix_diag_tmp, matrix_rhs_tmp = sc.get_coupling_values(tmp_problem)
            sc.cleanup(tmp_problem)

            bottom_matrices.append(matrix_bot_tmp)
            right_matrices.append(matrix_right_tmp)
            diagonal_matrices.append(matrix_diag_tmp)
            rhs_matrices.append(matrix_rhs_tmp)

            line_current.append(2 * k + sc.current_index)
            line_voltage.append(2 * k + sc.voltage_index)

        # Row s.t. the whole voltage is the sum of the single voltages
        voltage_condition_matrix = sparse.hstack((sparse.coo_matrix((np.ones(len(line_voltage)),
                                                                     (np.zeros(len(line_voltage)), line_voltage)),
                                                                    shape=(1, 2 * self.number_conductors)),
                                                  sparse.coo_matrix(([-1], ([0], [0])), shape=(1, 2))))

        # Rows s.t. all currents are equal to the outer current
        rows = np.concatenate((np.arange(self.number_conductors - 1), np.arange(self.number_conductors - 1)))
        columns = line_current[:-1] + line_current[1:]
        values = np.concatenate((np.ones(self.number_conductors - 1), -1 * np.ones(self.number_conductors - 1)))
        matrix_currents_equal = sparse.coo_matrix((values, (rows, columns)),
                                                  shape=(self.number_conductors - 1, self.additional_dofs))
        matrix_outer_current = sparse.coo_matrix(([1, -1], ([0, 0], [line_current[-1], self.additional_dofs - 1])))
        current_condition_matrix = sparse.vstack((matrix_currents_equal, matrix_outer_current))

        # matrices from the solid conductors
        bottom_matrix: sparse.coo_matrix = sparse.vstack(bottom_matrices, format='coo')
        right_matrix: sparse.coo_matrix = sparse.hstack(right_matrices, format='coo')
        diagonal_matrix: sparse.coo_matrix = sparse.block_diag(diagonal_matrices, format='coo')
        rhs_fcc: sparse.coo_matrix = sparse.vstack(rhs_matrices, format='coo')

        # Append matrices with the whole voltage and whole current
        bottom_matrix.resize((2 * self.number_conductors + 1, bottom_matrix.shape[1]))
        right_matrix.resize((right_matrix.shape[0], self.additional_dofs))
        diagonal_matrix.resize((diagonal_matrix.shape[0], self.additional_dofs))
        diagonal_matrix = sparse.vstack((diagonal_matrix, voltage_condition_matrix, current_condition_matrix))
        rhs_fcc.resize((self.additional_dofs, 1))

        return bottom_matrix, right_matrix, diagonal_matrix, rhs_fcc

    def set_solution(self, solution: np.ndarray):
        super().set_solution(solution)

        tmp = 0
        for sc in self.solid_conductors:
            sc.set_solution(solution[tmp:tmp + sc.additional_dofs])
            tmp += sc.additional_dofs

    def single_currents(self) -> Dict[int, complex]:
        """Return a dict with one current per solid conductor.

        Returns
        -------
        single_currents : Dict[int, complex]
            Key is the id of the region and value is the current through the solid conductor defined on this region
        """
        # noinspection PyUnresolvedReferences
        return {sc.region_id: sc.current for sc in self.solid_conductors}

    def single_voltages(self) -> Dict[int, complex]:
        """Return a dict with one voltage per solid conductor.

        Returns
        -------
        single_voltages : Dict[int, complex]
            Key is the id of the region and value is the voltage over the solid conductor defined on this region
        """
        # noinspection PyUnresolvedReferences
        return {sc.region_id: sc.voltage for sc in self.solid_conductors}

    def cleanup(self, problem: 'Problem') -> None:
        pass
