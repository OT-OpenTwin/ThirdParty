# coding=utf-8
"""
File containing class the abstract class EdgeShapeFunction.

.. sectionauthor:: Bundschuh
"""

from abc import abstractmethod
from typing import Union, Callable, Tuple, Type, TYPE_CHECKING, Dict, Any, List, Set

from scipy.sparse import csr_matrix, csc_matrix, coo_matrix, lil_matrix, vstack, hstack, block_diag, bmat
from scipy.sparse import linalg as splinalg
import numpy as np
from numpy import ndarray

from pyrit.bdrycond import BdryCond, BCConductor
from pyrit import get_logger

from pyrit.excitation import CurrentDensity, SourceHField
from .ShapeFunction import ShapeFunction, NumericalData, MaterialData, ExcitationData

if TYPE_CHECKING:
    from pyrit.mesh import Mesh
    from pyrit.region import Regions
    from pyrit.excitation import FieldCircuitCoupling
    from pyrit.problem import Problem

logger = get_logger(__name__)


class EdgeShapeFunction(ShapeFunction):
    """Abstract class representing edge shape functions."""

    @abstractmethod
    def __init__(self, mesh: Type['Mesh'], dim: int, allocation_size: int):
        """
        Constructor for the abstract class EdgeShapeFunction.

        Parameters
        ----------
        mesh : Mesh
            Representing the underlying mesh on which the NodalShapeFunction is
            defined.
        dim : int
            Dimensionality of the shape function.
        allocation_size : int
            Size used for vector allocation in matrix creation.

        Returns
        -------
        None
        """
        super().__init__(mesh, dim, allocation_size)
        self._default_load_excitation_class = None
        self._default_load_curl_excitation_class = None

    @abstractmethod
    def curlcurl_operator(self, *material: Union[NumericalData, MaterialData], **kwargs) -> coo_matrix:
        """
        Compute the discrete version of the curl-curl operator as a matrix.

        Parameters
        ----------
        material : Union[NumericalData, MaterialData]
            Information of the material parameter inside the domain. See :py:mod:`pyrit.shapefunction`.
        kwargs : dict, optional
            Only for internal usage. See :py:meth:`pyrit.shapefunction.Shapefunction.ShapeFunction._process_input`.

        Returns
        -------
        coo_matrix
        """

    @abstractmethod
    def mass_matrix(self, *material: Union[NumericalData, MaterialData], **kwargs) -> coo_matrix:
        """
        Compute the mass matrix.

        Parameters
        ----------
        material : Union[NumericalData, MaterialData]
            Information of the material parameter inside the domain. See :py:mod:`pyrit.shapefunction`.
        kwargs : dict, optional
            Only for internal usage. See :py:meth:`pyrit.shapefunction.Shapefunction.ShapeFunction._process_input`.

        Returns
        -------
        coo_matrix
        """

    def load_vector(self, *load: Union[NumericalData, ExcitationData], **kwargs) -> coo_matrix:
        r"""Computes the load vector.

        The load vector is :math:`\mathbf{g} = (g_i)i` with

        .. math::

            g_i := \int_\Omega \vec{J}\cdot\vec{w}_i\;\mathrm{d}V

        Herein, :math:`\Omega` is the computational domain, :math:`\vec{J}` is the current density and :math:`\vec{w}_i`
        is the :math:`i`-th edge basis function.

        Parameters
        ----------
        load : Union[NumericalData, ExcitationData]
            Information of the load parameter inside the domain. See :py:mod:`pyrit.shapefunction`.
        kwargs : dict, optional
            Only for internal usage. See :py:meth:`pyrit.shapefunction.Shapefunction.ShapeFunction._process_input`.

        Returns
        -------
        load_vector : coo_matrix
            A (E,1) sparse matrix. E is the number of edges in the mesh.
        """
        assembly_iterator = self._process_input(*load, default_excitation_class=CurrentDensity, **kwargs)
        return self._vector_routine("load", assembly_iterator, **kwargs)

    def load_vector_curl(self, *load: Union[NumericalData, ExcitationData], **kwargs) -> coo_matrix:
        r"""Computes the load curl vector.

        The load curl vector is :math:`\mathbf{s}=(s_i)_i` with

        .. math::

            s_i := \int_\Omega \vec{H}_{\mathrm{s}} \cdot \nabla\times \vec{w}_i \;\mathrm{d}V\,.

        Herein, :math:`\Omega` is the computational domain, :math:`\vec{H}_{\mathrm{s}}` is the source H field
        and :math:`\vec{w}_j` is the :math:`j`-th edge basis function.

        Parameters
        ----------
        load : Union[NumericalData, ExcitationData]
            Information of the load parameter inside the domain. See :py:mod:`pyrit.shapefunction`.
        kwargs : dict, optional
            Only for internal usage. See :py:meth:`pyrit.shapefunction.Shapefunction.ShapeFunction._process_input`.

        Returns
        -------
        load_vector_curl : coo_matrix
            A (E,1) sparse matrix. E is the number of edges in the mesh.
        """
        assembly_iterator = self._process_input(*load, default_excitation_class=SourceHField, **kwargs)
        return self._vector_routine("load_curl", assembly_iterator, **kwargs)

    @abstractmethod
    def curl(self, val2edge: ndarray) -> ndarray:
        """
        Computes the curl or rotation of a field.

        Parameters
        ----------
        val2edge : ndarray
            (E,) array with one value per edge (E edges)

        Returns
        -------
        ndarray
            (T,2) or (T,3) array with one vector per element (T elements)
        """

    # pylint: disable=line-too-long
    @abstractmethod
    def neumann_term(self, *args: Union[Tuple['Regions', 'BdryCond'],
                                        Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[..., float]], ...],
                                                             Callable[..., Tuple[float]]]]],
                     integration_order: int = 1) -> coo_matrix:
        r"""Compute the Neumann term on a part of the boundary (see the notes).

        Parameters
        ----------
        args : Union[Tuple[Regions, BdryCond], Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[..., float]], ...], Callable[..., Tuple[float]]]]]
            The following possibilities are:

            - **Regions, BdyCond**: Will search for instances of BCNeumann in BdryCond and use the value of these.
            - **Tuple[ndarray, Union[Tuple[Union[float, ndarray, Callable[..., float]], ...], Callable[..., Tuple[float]]]]**:
              Indices of the boundary elements and the components of :math:`\vec{g}` at these elements. Each
              component can be a function, an array with one value per boundary element or a constant.
        integration_order : int, optional
            The integration order for the case that a numerical integration is necessary. Default is 1

        Returns
        -------
        q : coo_matrix
            The vector :math:`\mathbf{q}` for the Neumann term.

        Notes
        -----
        The Neumann term for edge basis functions is a vector :math:`\mathbf{q}` where the elements are defined as

        .. math::

            q_i = \int_{\partial\Omega} \vec{w}_i\cdot\vec{g}\,\mathrm{d} S\,.

        In the finite element formulation it is :math:`\vec{g} = \vec{n}\times\vec{H}`.
        """

    @abstractmethod
    def robin_terms(self, regions: 'Regions', boundary_condition: 'BdryCond', integration_order: int = 1) -> \
            Tuple[coo_matrix, coo_matrix]:
        r"""Compute the matrix :math:`\mathbf{S}` and vector :math:`\mathbf{q}` arising from Robin boundary conditions

        See the Notes section for detailed information about the matrix and vector.

        Parameters
        ----------
        regions: Regions
            An instance of Regions
        boundary_condition: BdryCond
            An instance of BdryCond
        integration_order : int, optional
            The integration order for the case that a numerical integration is necessary. Default is 1

        Returns
        -------
        S : coo_matrix
            The matrix for the left hand side. A sparse matrix of dimension (E,E), with E being the number of elements.
        q : coo_matrix
            The vector for the right hand side. A sparse vector of dimension (E,1), with E being the number of elements.

        Notes
        -----
            For edge basis functions and the Robin boundary condition given as
            :math:`\alpha \vec{n}\times\left(\vec{n}\times\vec{A}\right) + \beta\vec{n}\times\vec{H} = \vec{g}`, the
            elements of the matrix :math:`\mathbf{S}` and vector :math:`\mathbf{q}` are defined as

            .. math::

                S_{ij} &= \int_{\partial\Omega}\frac\alpha\beta\vec{w}_i\cdot\vec{w}_j\,\mathrm{d} S\,,\\
                q_i &= \int_{\partial\Omega} \frac1\beta \vec{w}_i\cdot\vec{g}\;\mathrm{d} S\,.
        """

    @abstractmethod
    def dirichlet_equations(self, regions: 'Regions', boundary_conditions: 'BdryCond') -> Tuple[coo_matrix, coo_matrix]:
        r"""Calculates a matrix and a vector to ensure dirichlet boundary conditions.

        Calculates matrix :math:`\mathbf{B}` and vector :math:`\mathbf{b}`. With :math:`\mathbf{a}` being the vector of
        unknowns, the Dirichlet boundary conditions are satisfied if :math:`\mathbf{B}\mathbf{a}=\mathbf{b}`.

        Parameters
        ----------
        regions : Regions
            Object with all regions.
        boundary_conditions : BdryCond
            Object with all boundary conditions.

        Returns
        -------
        matrix : coo_matrix
        vector : coo_matrix

        Notes
        -----
        For each edge on the Dirichlet boundary one equation has to bold. With :math:`r_m := \frac12(r_j-r_i)` and
        :math:`z_m:=\frac12(z_j-z_i)` being the averaged coordinates of the edge defined by the points :math:`i` and
        :math:`j` and :math:`\vec{n}` being the outer normal vector of this edge, the equation is

        .. math::
            \frac{1}{\pi d}\left(a_i\begin{pmatrix}\frac{-c_i}{2 r_m}\\b_i\end{pmatrix}\cdot\vec{n} + a_j
            \begin{pmatrix}\frac{-c_j}{2r_m}\\b_j\end{pmatrix}\cdot\vec{n}\right) = b(r_m,z_m)\,.
        """

    @abstractmethod
    def voltage_distribution_function(self, regions: 'Regions', fcc: 'FieldCircuitCoupling') -> coo_matrix:
        r"""Compute the voltage distribution function.

        Returns the coefficients :math:`x_i` of the voltage distribution function :math:`\vec{\zeta}` such that
        :math:`\vec{\zeta}=\sum_i x_i\vec{w}_i`.

        Parameters
        ----------
        regions : Regions
            A regions object.
        fcc : FieldCircuitCoupling
            A field circuit coupling instance.

        Returns
        -------
        x : coo_matrix
            The coefficients of the voltage distribution function.

        Notes
        -----
        With :math:`\Gamma` being a Path through the conductor from one to the other electrode, the voltage distribution
        function meets the condition

        .. math::

            \int_\Gamma\vec{\zeta}\cdot\mathrm{d}\vec{s} = 1\,.
        """

    @abstractmethod
    def current_distribution_function(self, regions: 'Regions', fcc: 'FieldCircuitCoupling') -> coo_matrix:
        r"""Compute the current distribution function.

        Returns the coefficients :math:`x_i` of the current distribution function :math:`\vec{\chi}` such that
        :math:`\vec{\chi}=\sum_i x_i\vec{w}`.

        Parameters
        ----------
        regions : Regions
            A regions object.
        fcc : FieldCircuitCoupling
            A field circuit coupling instance.

        Returns
        -------
        x : coo_matrix
            The cofficients of the current distribution function.

        Notes
        -----
        With :math:`S_c` being the area in the cross-section of the conductor, the current distribution function meets
        the condition

        .. math::

            \int_{S_c} \vec{\chi}\cdot\mathrm{d}\vec{S} = 1\,,
        """

    def shrink(self, matrix: 'coo_matrix', rhs: 'coo_matrix', problem: 'Problem',
               integration_order: int = 1) -> Tuple['coo_matrix', 'coo_matrix', ndarray, int, Dict['str', Any]]:
        bc_by_type = problem.boundary_conditions.dict_of_boundary_condition()

        ind_on_dir, ind_not_on_dir, val_on_dir = None, None, None

        if not isinstance(matrix, coo_matrix):
            if isinstance(matrix, (csc_matrix, csr_matrix, lil_matrix)):
                matrix = matrix.tocoo()
            else:
                raise ValueError("Matrix is not a coo_matrix")
        if not isinstance(rhs, coo_matrix):
            if isinstance(rhs, (csc_matrix, csr_matrix, lil_matrix)):
                rhs = rhs.tocoo()
            else:
                raise ValueError("Right-hand-side is not a coo_matrix")

        if matrix.shape[0] != rhs.shape[0]:
            raise Exception("The dimensions of matrix and right-hand-side do not match.")

        if bc_by_type['binary']:
            logger.warning("The boundary condition type 'binary' is not supported. It is going to be ignored.")

        if bc_by_type['floating']:
            logger.warning("The boundary condition type 'floating' is not supported. It is going to be ignored.")

        if bc_by_type['neumann']:
            rhs = self.shrink_neumann(rhs, problem, integration_order)

        if bc_by_type['robin']:
            matrix, rhs = self.shrink_robin(matrix, rhs, problem, integration_order)

        if bc_by_type['dirichlet']:
            matrix, rhs, ind_on_dir, ind_not_on_dir, val_on_dir = \
                self.shrink_dirichlet(matrix, rhs, problem, bc_by_type)

        support_data = {'indices_on_dirichlet': ind_on_dir,
                        'indices_not_on_dirichlet': ind_not_on_dir,
                        'values_on_dirichlet': val_on_dir}

        return matrix, rhs, ind_on_dir, 0, support_data

    def shrink_fcc(self, matrix: 'coo_matrix', rhs: 'coo_matrix', problem: 'Problem',
                   integration_order: int = 1) -> Tuple['coo_matrix', 'coo_matrix', ndarray, int, Dict['str', Any]]:
        bottom_matrices, right_matrices, diagonal_matrices, rhs_matrices = [], [], [], []

        # shrink the system with the sft
        ret = problem.shape_function.shrink(matrix, rhs, problem, integration_order=integration_order)
        matrix_shrink_sf, rhs_shrink_sf, indices_not_dof, num_new_dof, support_data = ret

        dim_matrix_shrink_sf = matrix_shrink_sf.shape[0]
        new_dof_fcc = 0  # New dofs from fcc
        try:
            for fcc in BCConductor.iter_fcc(problem.boundary_conditions):
                # get the coupling values
                # noinspection PyTupleAssignmentBalance
                matrix_bot_tmp, matrix_right_tmp, matrix_diag_tmp, matrix_rhs_tmp = fcc.get_coupling_values(problem)
                bottom_matrices.append(matrix_bot_tmp)
                right_matrices.append(matrix_right_tmp)
                diagonal_matrices.append(matrix_diag_tmp)
                rhs_matrices.append(matrix_rhs_tmp)
                fcc.first_index_in_dof_vector = dim_matrix_shrink_sf + new_dof_fcc
                new_dof_fcc += fcc.additional_dofs
        finally:  # Clean up
            for fcc in BCConductor.iter_fcc(problem.boundary_conditions):
                fcc.cleanup(problem)

        # Assembly of the matrices
        bottom_matrix: csr_matrix = vstack(bottom_matrices, format='csr')
        right_matrix: csr_matrix = hstack(right_matrices, format='csr')
        diagonal_matrix = block_diag(diagonal_matrices, format='csr')
        rhs_fcc = vstack(rhs_matrices, format='csr')

        # compose the coupling matrices and coupling values with the information from the sft.shrink
        all_indices = np.arange(rhs.shape[0])
        # num_fcc = len(bottom_matrices)
        new_lines = bottom_matrix.shape[0]

        indices_dof = np.setdiff1d(all_indices, indices_not_dof)
        bottom_matrix = bottom_matrix[np.ix_(np.arange(new_lines), indices_dof)]
        right_matrix = right_matrix[np.ix_(indices_dof)]
        bottom_matrix.resize((bottom_matrix.shape[0], dim_matrix_shrink_sf))
        right_matrix.resize((dim_matrix_shrink_sf, right_matrix.shape[1]))

        # compute the final system
        matrix_shrink = bmat([[matrix_shrink_sf, right_matrix],
                              [bottom_matrix, diagonal_matrix]], format='coo')
        rhs_shrink = vstack([rhs_shrink_sf, rhs_fcc], format='coo')

        return matrix_shrink, rhs_shrink, indices_not_dof, num_new_dof + new_dof_fcc, support_data

    def inflate(self, solution: ndarray, problem: 'Problem',
                support_data: Dict[str, Any] = None) -> ndarray:
        bc_by_type = problem.boundary_conditions.dict_of_boundary_condition()
        if support_data:  # If support data is given, use its data
            required_keys = ['indices_on_dirichlet', 'indices_not_on_dirichlet', 'values_on_dirichlet']
            for key in required_keys:
                if key not in support_data.keys():
                    logger.warning("The given support data is incomplete. The key 'num_lagrange_mul' is missing. "
                                   "It will be computed.")
                    support_data = self.compute_support_data(bc_by_type, len(solution), problem)
        else:
            support_data = self.compute_support_data(bc_by_type, len(solution), problem)

        if bc_by_type['dirichlet']:
            ind_on_dir = support_data['indices_on_dirichlet']
            ind_not_on_dir = support_data['indices_not_on_dirichlet']
            val_on_dir = support_data['values_on_dirichlet']
            solution_inflated = self.inflate_dirichlet(solution, ind_on_dir, val_on_dir, ind_not_on_dir)
            return solution_inflated

        return solution

    def inflate_fcc(self, solution: ndarray, problem: 'Problem',
                    support_data: Dict[str, Any] = None) -> ndarray:
        num_additional_dofs = sum(fcc.additional_dofs for fcc in BCConductor.iter_fcc(problem.boundary_conditions))
        solutions_fcc = solution[-num_additional_dofs:]  # Vector of the fcc solutions

        # Assign the fcc solution to the fcc
        start = 0
        for fcc in BCConductor.iter_fcc(problem.boundary_conditions):
            solution_fcc = solutions_fcc[start:start + fcc.additional_dofs]
            start += fcc.additional_dofs
            fcc.set_solution(solution_fcc)

        # Standard inflate
        solution_inflated = problem.shape_function.inflate(solution[:-num_additional_dofs], problem)

        return solution_inflated

    # region shrink methods

    def shrink_neumann(self, rhs: coo_matrix, problem: 'Problem',
                       integration_order: int = 1) -> coo_matrix:
        """Shrink with Neumann boundary conditions.

        Parameters
        ----------
        rhs : coo_matrix
            The right-hand-side of the system
        problem : Problem
            A problem object.
        integration_order : int, optional
            The integration order that is passed to the subsequent method. Default is 1

        Returns
        -------
        rhs_shrink : coo_matrix
            The shrunk right-hand-side.
        """
        rhs_shrink = rhs - self.neumann_term(problem.regions, problem.boundary_conditions,
                                             integration_order=integration_order)
        return rhs_shrink.tocoo()

    def shrink_robin(self, matrix: coo_matrix, rhs: coo_matrix, problem: 'Problem',
                     integration_order: int = 1):
        """Shrink with Robin boundary conditions.

        Parameters
        ----------
        matrix : coo_matrix
            The matrix of the system of equations.
        rhs : coo_matrix
            The right-hand-side of the system of equations.
        problem : Problem
            A problem object
        integration_order : int, optional
            The integration order that is passed to the subsequent methods.

        Returns
        -------
        matrix_shrink : coo_matrix
            The shrunk system matrix.
        rhs_shrink : coo_matrix
            The shrunk right-hand-side.
        """
        matrix_neumann, vector_neumann = self.robin_terms(problem.regions, problem.boundary_conditions,
                                                          integration_order=integration_order)
        matrix_shrink = matrix + matrix_neumann
        rhs_shrink = rhs - vector_neumann
        return matrix_shrink.tocoo(), rhs_shrink.tocoo()

    def _compute_groups_dirichlet(self, problem: 'Problem',
                                  dict_of_bc: Dict[str, List[int]]) -> List[Tuple[List[int], Set[int]]]:
        """Compute groups of connected Dirichlet boundary conditions.

        A group is a number of Dirichlet boundary conditions that are not independent of each other. Thy share at least
        one node. Thus, they have to be considered together in the shrink method.

        Parameters
        ----------
        problem : Problem
            A problem containing additional data structures. See :py:class:`ShrinkInflateProblem`.
        dict_of_bc : Dict[str, List[int]]
            Dict with the IDs of the boundary conditions, divided by type.
            See :py:meth:`.BdryCond.dict_of_boundary_condition`.

        Returns
        -------
        groups : List[Tuple[List[int], Set[int]]]
            A list of groups. Each group is a tuple with the first entry being a list of the boundary condition indices
            of this group and the second entry being a set of all node indices on this group
        """
        dirichlet_ids: List[int] = dict_of_bc['dirichlet']

        bound_inds = {}  # Indices of all edges on the boundary condition

        for dirichlet_id in dirichlet_ids:
            indices_regions = problem.regions.find_regions_of_boundary_condition(dirichlet_id)
            indices_bound = [np.where(self.mesh.bound2regi == region_id)[0] for region_id in indices_regions]
            bound_inds[dirichlet_id] = np.concatenate(indices_bound)

        # Indices of all nodes on the boundary condition
        nodes_ind = {dirichlet_id: np.unique(self.mesh.bound2node[bound]) for dirichlet_id, bound in bound_inds.items()}

        # Find groups of dirichlet boundary conditions
        groups = []
        for dirichlet_id in dirichlet_ids:
            node_indices_i: set = set(nodes_ind[dirichlet_id])
            for group in groups:
                # test if node indices i are connected to group j
                if not node_indices_i.isdisjoint(group[1]):
                    group[0].append(dirichlet_id)
                    group[1].update(node_indices_i)
                    break
            else:
                groups.append(([dirichlet_id, ], node_indices_i))

        return groups

    def _compute_data_dirichlet(self, dict_of_bc, groups, problem) -> Tuple[ndarray, ndarray]:
        """Compute the values on the dirichlet boundaries.

        Parameters
        ----------
        dict_of_bc : Dict[str, List[int]]
            Dict with the IDs of the boundary conditions, divided by type.
            See :py:meth:`.BdryCond.dict_of_boundary_condition`.
        groups : List[Tuple[List[int], Set[int]]]
            Groups of boundaries. See :py:meth:`_compute_groups_dirichlet`.
        problem : Problem
            A problem containing additional data structures. See :py:class:`ShrinkInflateProblem`.

        Returns
        -------
        indices_on_dirichlet : ndarray
            Array with indices on Dirichlet boundaries.
        values_on_dirichlet : ndarray
            Array with values to the indices on the Dirichlet boundaries.
        """
        values_all_nodes = []
        indices_all_nodes = []

        only_dirichlet = False
        if len(groups) == 1:
            # check if there are only dirichlet bcs
            for key, val in dict_of_bc.items():
                if key not in ("dirichlet", "conductor") and len(val) > 0:  # There exists a non-Dirichlet BC
                    break
            else:
                only_dirichlet = True

        if only_dirichlet:
            b_mat, b_vec = self.dirichlet_equations(problem.regions, problem.boundary_conditions)

            indices_for_a = np.unique(b_mat.col)

            b_mat: csr_matrix = b_mat.tocsr()
            b_vec: csr_matrix = b_vec.tocsr()
            b_mat = b_mat[:, b_mat.getnnz(0) > 0]
            b_mat.resize(b_mat.shape[0] - 1, b_mat.shape[1])
            b_mat = vstack([b_mat, csr_matrix(([1, ], ([0, ], [0, ])), shape=(1, b_mat.shape[1]))])
            b_vec[-1, 0] = 0
            a_on_bound = splinalg.spsolve(b_mat, b_vec)

            values_all_nodes.append(a_on_bound)
            indices_all_nodes.append(indices_for_a)
        else:
            for group in groups:
                tmp_boundary_condition = BdryCond(*[problem.boundary_conditions.get_bc(i) for i in group[0]])
                b_mat, b_vec = self.dirichlet_equations(problem.regions, tmp_boundary_condition)

                indices_for_a = np.unique(b_mat.col)

                b_mat = b_mat.tocsr()
                b_mat = b_mat[:, b_mat.getnnz(0) > 0]
                b_mat = vstack([b_mat, csr_matrix(([1, ], ([0, ], [0, ])), shape=(1, b_mat.shape[1]))])
                b_vec.resize(b_mat.shape[1], 1)
                a_on_bound = splinalg.spsolve(b_mat, b_vec)

                values_all_nodes.append(a_on_bound)
                indices_all_nodes.append(indices_for_a)

        return np.concatenate(indices_all_nodes), np.concatenate(values_all_nodes)

    def shrink_dirichlet(self, matrix: coo_matrix, rhs: coo_matrix, problem: 'Problem',
                         dict_of_bc: Dict[str, Any]) -> Tuple[coo_matrix, coo_matrix, ndarray, ndarray, ndarray]:
        """Shrink with Dirichlet boundary condition.

        Parameters
        ----------
        matrix : coo_matrix
            The matrix of the system of equations.
        rhs : coo_matrix
            The right-hand-side of the system of equations.
        problem : Problem
            A problem object.
        dict_of_bc : Dict[int, List[int]]
            A dictionary with the key being the ID of a boundary conditions and the value being a list of the IDs of
            regions having this boundary condition. See :py:meth:`.BdryCond.regions_of_bc`.

        Returns
        -------
        matrix_shrink : coo_matrix
            The shrunk matrix
        rhs_shrink : coo_matrix
            The shrunk right-hand-side.
        indices_on_dirichlet : ndarray
            An array containing the indices of nodes that are on a dirichlet boundary condition. These indices are valid
            for the input matrix.
        indices_not_on_dirichlet : ndarray
            An array containing the indices of nodes that are not on a dirichlet boundary condition. These indices are
            valid for the input matrix.
        values_on_dirichlet : ndarray
            An array with the value of every node on a dirichlet boundary condition.
        """
        groups = self._compute_groups_dirichlet(problem, dict_of_bc)

        indices_on_dirichlet, values_on_dirichlet = self._compute_data_dirichlet(dict_of_bc, groups, problem)

        indices_not_on_dirichlet = np.setdiff1d(np.arange(matrix.shape[0]), indices_on_dirichlet)

        matrix = matrix.tocsr()
        rhs = rhs.tocsr()

        # Update system matrix and right hand side vector
        rhs = rhs[indices_not_on_dirichlet] - matrix[
            np.ix_(indices_not_on_dirichlet, indices_on_dirichlet)] * csr_matrix(values_on_dirichlet).transpose()
        matrix = matrix[np.ix_(indices_not_on_dirichlet, indices_not_on_dirichlet)]

        return matrix.tocoo(), rhs.tocoo(), indices_on_dirichlet, indices_not_on_dirichlet, values_on_dirichlet.reshape(
            -1)

    # endregion

    @staticmethod
    def inflate_dirichlet(solution: ndarray, indices_on_dirichlet: ndarray, values_on_dirichlet: ndarray,
                          indices_not_on_dirichlet: ndarray) -> ndarray:
        """Inflate Dirichlet boundary conditions.

        Parameters
        ----------
        solution : ndarray
            The solution of the shrunk system of equations.
        indices_on_dirichlet : ndarray
            An array containing the indices of nodes that are on a dirichlet boundary condition. These indices are valid
            for the input matrix.
        indices_not_on_dirichlet : ndarray
            An array containing the indices of nodes that are not on a dirichlet boundary condition. These indices are
            valid for the input matrix.
        values_on_dirichlet : ndarray
            An array with the value of every node on a dirichlet boundary condition.

        Returns
        -------
        solution_inflated : ndarray
            The inflated solution.
        """
        solution_inflated = np.empty(len(indices_on_dirichlet) + len(indices_not_on_dirichlet), dtype=solution.dtype)
        solution_inflated[indices_not_on_dirichlet] = solution
        solution_inflated[indices_on_dirichlet] = values_on_dirichlet

        return solution_inflated

    # noinspection PyUnresolvedReferences
    def compute_support_data(self, dict_of_bc: Dict[str, Any], size_solution: int,
                             problem: 'Problem') -> Dict[str, Any]:
        """Compute some support data that is needed for inflating.

        Parameters
        ----------
        dict_of_bc : Dict[str, Any]
            Dict with the IDs of the boundary conditions, divided by type.
            See :py:meth:`.BdryCond.dict_of_boundary_condition`.
        size_solution : int
            Size of the solution vector.
        problem : Problem
            A problem object.

        Returns
        -------
        support_data : Dict[str, Any]
            The support data.
        """
        support_data = {}
        if dict_of_bc['dirichlet']:
            groups = self._compute_groups_dirichlet(problem, dict_of_bc)
            indices_on_dirichlet, values_on_dirichlet = self._compute_data_dirichlet(dict_of_bc, groups, problem)
            indices_not_on_dirichlet = np.setdiff1d(np.arange(size_solution + len(indices_on_dirichlet)),
                                                    indices_on_dirichlet)
            support_data.update(dict(indices_on_dirichlet=indices_on_dirichlet,
                                     indices_not_on_dirichlet=indices_not_on_dirichlet,
                                     values_on_dirichlet=values_on_dirichlet))
        return support_data
