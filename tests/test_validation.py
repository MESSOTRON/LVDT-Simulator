"""Validation of the FEM core against closed-form solutions.

1. Infinitely long conducting, permeable cylinder in a uniform axial AC field
   (eddy currents / skin effect in the core): Bessel-function solution.
2. Mutual inductance of two coaxial air coils: Maxwell's formula for coaxial
   circular filaments (elliptic integrals), summed over the winding cross-sections.

Run:  python -m pytest tests -q     or     python tests/test_validation.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
from scipy.special import ellipe, ellipk, jv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lvdt_sim.fem import AxiFEM, AxiMesh  # noqa: E402
from lvdt_sim.geometry import Coil, LVDTDesign, uniform_section  # noqa: E402
from lvdt_sim.materials import MU0  # noqa: E402
from lvdt_sim.mesh import build_axis  # noqa: E402
from lvdt_sim.model import LVDTModel, MeshOptions  # noqa: E402


def cylinder_mu_eff_fem(a, mu_r, sigma, f):
    """Core flux / (mu0 H0 pi a^2) from the FEM for an infinitely long cylinder."""
    delta = 1 / np.sqrt(np.pi * f * MU0 * abs(mu_r) * sigma) if sigma > 0 else a
    rc0, rc1, R = 4.0e-3, 4.2e-3, 5.0e-3
    r = build_axis([0, a, rc0, rc1, R],
                   [a / 10, min(delta / 12, a / 20), 0.05e-3, 0.05e-3, 0.1e-3],
                   [a / 30, 0.1e-3, 0.05e-3, 0.2e-3], growth=0.1)
    z = np.linspace(0, 0.4e-3, 5)
    mesh = AxiMesh(r, z)
    fem = AxiFEM(mesh, dirichlet="axis")
    in_core = mesh.cell_rc < a
    mu = np.where(in_core, mu_r, 1.0)[mesh.tri_cell]
    sig = np.where(in_core, sigma, 0.0)[mesh.tri_cell]
    # current sheet with H0 = 1 A/m: turns per metre = 1
    in_coil = (mesh.cell_rc > rc0) & (mesh.cell_rc < rc1)
    n = np.where(in_coil, 1.0 / (rc1 - rc0), 0.0)[mesh.tri_cell]
    lu = fem.factorize(mu, sig, 2 * np.pi * f)
    A = fem.full(lu.solve(fem.load_vector(n).astype(complex)))
    i_a = np.flatnonzero(np.isclose(mesh.nodes[:, 0], a) & np.isclose(mesh.nodes[:, 1], z[2]))[0]
    phi = 2 * np.pi * A[i_a]  # A holds psi = r A_phi
    return phi / (MU0 * 1.0 * np.pi * a ** 2)


def cylinder_mu_eff_exact(a, mu_r, sigma, f):
    if sigma == 0:
        return complex(mu_r)
    k = np.sqrt(-1j * 2 * np.pi * f * MU0 * mu_r * sigma)
    return mu_r * 2 * jv(1, k * a) / (k * a * jv(0, k * a))


def test_cylinder_skin_effect():
    a = 3e-3
    cases = [(1.0, 0.0, 1e3), (400.0, 0.0, 1e3), (400.0, 1.43e6, 500.0),
             (400.0, 1.43e6, 5e3), (400.0 - 40j, 1.43e6, 20e3), (1.05, 1.4e6, 5e3)]
    for mu_r, sigma, f in cases:
        fem = cylinder_mu_eff_fem(a, mu_r, sigma, f)
        ex = cylinder_mu_eff_exact(a, mu_r, sigma, f)
        err = abs(fem - ex) / abs(ex)
        print(f"mu_r={mu_r!s:>10} sigma={sigma:9.3g} f={f:7.0f} Hz  "
              f"FEM={fem:.4g}  exakt={ex:.4g}  Abw.={err * 100:.3f} %")
        assert err < 3e-3


def mutual_filaments(c1: Coil, c2: Coil, nr=8, nz=40):
    """Mutual inductance by summing Maxwell's coaxial-loop formula over filaments."""
    def filaments(c):
        pts = []
        for layer in c.layers:
            for z0, z1, turns in layer.segments:
                zs = z0 + (np.arange(nz) + 0.5) * (z1 - z0) / nz
                rs = layer.r_center - layer.thickness / 2 + (np.arange(nr) + 0.5) * layer.thickness / nr
                R, Zm = np.meshgrid(rs, zs)
                w = np.full(R.size, turns / R.size)
                pts.append(np.column_stack([R.ravel(), Zm.ravel(), w]))
        return np.vstack(pts)

    p1, p2 = filaments(c1), filaments(c2)
    a = p1[:, None, 0]
    b = p2[None, :, 0]
    d = p1[:, None, 1] - p2[None, :, 1]
    m = 4 * a * b / ((a + b) ** 2 + d ** 2)
    k = np.sqrt(m)
    M = MU0 * np.sqrt(a * b) * ((2 / k - k) * ellipk(m) - 2 / k * ellipe(m))
    return float(np.sum(M * p1[:, None, 2] * p2[None, :, 2]))


def test_air_coils_mutual_inductance():
    wire = 0.1e-3
    c1 = Coil("P", uniform_section(4e-3, -10e-3, 0.0, wire, 4), 0.09e-3)
    c2 = Coil("S1", uniform_section(4e-3, 2e-3, 12e-3, wire, 4), 0.09e-3)
    c3 = Coil("S2", uniform_section(4.5e-3, -25e-3, -15e-3, wire, 4), 0.09e-3)
    design = LVDTDesign("air", [], [], {"P": c1, "S1": c2, "S2": c3}, stroke=1e-3)
    model = LVDTModel(design, x_range=(0, 0),
                      opts=MeshOptions(far_factor=12.0, dz=0.1e-3, h_fine=0.05e-3))
    f = 1e3
    Z = model.solve(0.0, f)
    for (i, ci), (j, cj) in [((0, c1), (1, c2)), ((0, c1), (2, c3)), ((1, c2), (2, c3))]:
        m_fem = (Z[i, j] / (2j * np.pi * f)).real
        m_ex = mutual_filaments(ci, cj)
        err = abs(m_fem - m_ex) / abs(m_ex)
        print(f"M({ci.name},{cj.name}): FEM={m_fem * 1e6:.4f} uH  Filament={m_ex * 1e6:.4f} uH  "
              f"Abw.={err * 100:.3f} %")
        assert err < 1e-2


if __name__ == "__main__":
    test_cylinder_skin_effect()
    test_air_coils_mutual_inductance()
    print("alle Validierungen bestanden")
