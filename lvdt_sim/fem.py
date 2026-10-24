"""Time-harmonic axisymmetric magnetoquasistatic finite elements.

Unknown: flux function psi(r, z) = r * A_phi(r, z) (complex phasor, e^{jwt});
2 pi psi is the magnetic flux through the circle of radius r at height z.

    curl( nu curl A ) + j w sigma A = J_s

Weak form with linear triangles on the r-z half plane (volume element 2 pi r):

    K_ij = 2pi Int nu grad(Li) . grad(Lj) / r dr dz
    M_ij = 2pi Int sigma Li Lj / r dr dz
    f_i  = 2pi Int J Li dr dz

with B_r = -(1/r) dpsi/dz and B_z = (1/r) dpsi/dr. The psi form represents the
field outside a strongly flux-carrying core (psi ~ const) exactly, which the
A_phi form with linear elements does not (A ~ 1/r).

For a coil k with turn density n_k (turns per m^2 of r-z cross-section) the
load vector for 1 A is f_k and the flux linkage of coil k due to a current in
coil l is lambda_kl = f_k^T psi_l, so the impedance matrix is
Z_kl = R_k delta_kl + j w f_k^T (K + j w M)^-1 f_l. It contains all
eddy-current losses (core, bobbin tube, housing) and is complex symmetric
(reciprocity).
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu

from .materials import MU0

# 3-point interior Gauss rule on triangles: barycentric coordinates (rows = points)
_QP = np.array([[2 / 3, 1 / 6, 1 / 6], [1 / 6, 2 / 3, 1 / 6], [1 / 6, 1 / 6, 2 / 3]])
_QW = np.array([1 / 3, 1 / 3, 1 / 3])


class AxiMesh:
    """Tensor grid r x z, each cell split into two linear triangles."""

    def __init__(self, r, z):
        self.r = np.asarray(r, float)
        self.z = np.asarray(z, float)
        nr, nz = len(self.r), len(self.z)
        self.nr, self.nz = nr, nz
        R, Z = np.meshgrid(self.r, self.z, indexing="ij")
        self.nodes = np.column_stack([R.ravel(), Z.ravel()])
        idx = np.arange(nr * nz).reshape(nr, nz)
        n00 = idx[:-1, :-1].ravel()
        n10 = idx[1:, :-1].ravel()
        n11 = idx[1:, 1:].ravel()
        n01 = idx[:-1, 1:].ravel()
        # diagonals mirrored at z = 0, so a symmetric design gives an exactly symmetric mesh
        zc_cell = (0.5 * (self.z[1:] + self.z[:-1]))[None, :].repeat(nr - 1, 0).ravel()
        up = zc_cell >= 0
        t1 = np.where(up[:, None], np.column_stack([n00, n10, n11]), np.column_stack([n00, n10, n01]))
        t2 = np.where(up[:, None], np.column_stack([n00, n11, n01]), np.column_stack([n10, n11, n01]))
        self.tri = np.vstack([t1, t2])
        ncell = (nr - 1) * (nz - 1)
        self.ncell = ncell
        self.tri_cell = np.concatenate([np.arange(ncell), np.arange(ncell)])
        rc = 0.5 * (self.r[1:] + self.r[:-1])
        zc = 0.5 * (self.z[1:] + self.z[:-1])
        RC, ZC = np.meshgrid(rc, zc, indexing="ij")
        self.cell_rc = RC.ravel()
        self.cell_zc = ZC.ravel()
        DR, DZ = np.meshgrid(np.diff(self.r), np.diff(self.z), indexing="ij")
        self.cell_area = (DR * DZ).ravel()

        on_axis = self.nodes[:, 0] <= 1e-15
        outer = ((np.isclose(self.nodes[:, 0], self.r[-1])) |
                 (np.isclose(self.nodes[:, 1], self.z[0])) |
                 (np.isclose(self.nodes[:, 1], self.z[-1])))
        self.on_axis = on_axis
        self.on_outer = outer & ~on_axis

    @property
    def n_nodes(self):
        return self.nodes.shape[0]

    def cells_in_rect(self, r0, r1, z0, z1):
        return ((self.cell_rc > r0) & (self.cell_rc < r1) &
                (self.cell_zc > z0) & (self.cell_zc < z1))

    def turns_per_cell(self, layers):
        """Distribute winding layers onto cells (area-overlap, conserves turns)."""
        dr_lo, dr_hi = self.r[:-1], self.r[1:]
        dz_lo, dz_hi = self.z[:-1], self.z[1:]
        T = np.zeros((self.nr - 1, self.nz - 1))
        for layer in layers:
            a = layer.r_center - layer.thickness / 2
            b = layer.r_center + layer.thickness / 2
            fr = np.clip(np.minimum(dr_hi, b) - np.maximum(dr_lo, a), 0, None) / (b - a)
            tz = np.zeros(self.nz - 1)
            for z0, z1, turns in layer.segments:
                if z1 <= z0:
                    continue
                ov = np.clip(np.minimum(dz_hi, z1) - np.maximum(dz_lo, z0), 0, None)
                tz += ov * turns / (z1 - z0)
            T += np.outer(fr, tz)
        return T.ravel()


class AxiFEM:
    """Assembly and solution on an AxiMesh.

    dirichlet: 'all'  -> A = 0 on axis and on the outer boundary (open problem,
                          boundary far away)
               'axis' -> A = 0 on the axis only; natural boundary (H_tangential = 0)
                          elsewhere. Used for the infinite-length validation case.
    """

    def __init__(self, mesh: AxiMesh, dirichlet="all"):
        self.mesh = mesh
        tri = mesh.tri
        P = mesh.nodes[tri]
        r_, z_ = P[:, :, 0], P[:, :, 1]
        b = np.stack([z_[:, 1] - z_[:, 2], z_[:, 2] - z_[:, 0], z_[:, 0] - z_[:, 1]], axis=1)
        c = np.stack([r_[:, 2] - r_[:, 1], r_[:, 0] - r_[:, 2], r_[:, 1] - r_[:, 0]], axis=1)
        area2 = np.einsum("ei,ei->e", r_, b)
        self.dLdr = b / area2[:, None]
        self.dLdz = c / area2[:, None]
        area = 0.5 * np.abs(area2)
        rq = r_ @ _QP.T  # (ne, nq), always > 0 (interior points)
        w_over_r = _QW[None, :] / rq
        two_pi_a = 2 * np.pi * area
        grad = (self.dLdr[:, :, None] * self.dLdr[:, None, :] +
                self.dLdz[:, :, None] * self.dLdz[:, None, :])
        self.Kg = (two_pi_a * w_over_r.sum(1))[:, None, None] * grad
        self.Mg = two_pi_a[:, None, None] * np.einsum("eq,qi,qj->eij", w_over_r, _QP, _QP)
        self.Fg = two_pi_a[:, None] * (_QW @ _QP)[None, :]
        self.tri_rc = r_.mean(1)

        if dirichlet == "all":
            fixed = mesh.on_axis | mesh.on_outer
        elif dirichlet == "axis":
            fixed = mesh.on_axis
        else:
            raise ValueError(dirichlet)
        self.free = np.flatnonzero(~fixed)
        n = mesh.n_nodes
        gmap = -np.ones(n, dtype=np.int64)
        gmap[self.free] = np.arange(len(self.free))
        self.gmap = gmap
        rows = np.broadcast_to(gmap[tri][:, :, None], self.Kg.shape).ravel()
        cols = np.broadcast_to(gmap[tri][:, None, :], self.Kg.shape).ravel()
        mask = (rows >= 0) & (cols >= 0)
        self._mask = mask
        nf = len(self.free)
        keys = rows[mask] * nf + cols[mask]
        ukeys, inv = np.unique(keys, return_inverse=True)
        self._inv = inv
        self._nnz = len(ukeys)
        urow = ukeys // nf
        ucol = ukeys % nf
        self._indptr = np.concatenate([[0], np.cumsum(np.bincount(urow, minlength=nf))])
        self._indices = ucol.astype(np.int32)
        self.nf = nf

    # ------------------------------------------------------------------
    def assemble(self, nu_tri, sigma_tri, omega):
        data = (nu_tri[:, None, None] * self.Kg +
                1j * omega * sigma_tri[:, None, None] * self.Mg).ravel()[self._mask]
        re = np.bincount(self._inv, weights=data.real, minlength=self._nnz)
        im = np.bincount(self._inv, weights=data.imag, minlength=self._nnz)
        return sp.csr_matrix((re + 1j * im, self._indices, self._indptr), shape=(self.nf, self.nf))

    def load_vector(self, j_tri):
        f = np.zeros(self.mesh.n_nodes)
        np.add.at(f, self.mesh.tri, j_tri[:, None] * self.Fg)
        return f[self.free]

    def factorize(self, mu_r_tri, sigma_tri, omega):
        nu = 1.0 / (MU0 * np.asarray(mu_r_tri, complex))
        S = self.assemble(nu, np.asarray(sigma_tri, float), omega)
        return splu(S.tocsc(), permc_spec="MMD_AT_PLUS_A")

    def full(self, a_free):
        a = np.zeros(self.mesh.n_nodes, dtype=complex)
        a[self.free] = a_free
        return a

    def flux_density(self, psi_full):
        """B_r, B_z per triangle (evaluated at the centroid)."""
        pt = psi_full[self.mesh.tri]
        br = -np.einsum("ei,ei->e", self.dLdz, pt) / self.tri_rc
        bz = np.einsum("ei,ei->e", self.dLdr, pt) / self.tri_rc
        return br, bz
