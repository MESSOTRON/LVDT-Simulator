"""Digital twin of an LVDT: mesh + materials + coils + circuit."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .fem import AxiFEM, AxiMesh
from .geometry import LVDTDesign
from .materials import AIR
from .mesh import build_axis, unique_sorted


@dataclass
class MeshOptions:
    f_max: float = 20e3        # highest frequency the radial grading must resolve
    dz: float = 0.1e-3         # uniform axial spacing in the core travel zone
    h_fine: float = 0.05e-3    # spacing at material interfaces (radial)
    h_max_device: float = 0.25e-3
    growth: float = 0.15
    far_factor: float = 2.0    # distance of the outer boundary relative to device size
    skin_fraction: float = 0.1  # radial spacing at conductive surfaces / skin depth


class LVDTModel:
    def __init__(self, design: LVDTDesign, x_range=None, opts: MeshOptions | None = None):
        self.design = design
        self.opts = opts or MeshOptions()
        if x_range is None:
            x_range = (-1.3 * design.stroke, 1.3 * design.stroke)
        self.x_range = x_range
        self.mesh = self._build_mesh()
        self.fem = AxiFEM(self.mesh, dirichlet="all")
        m = self.mesh
        self._mu_static = np.ones(m.ncell, complex)
        self._sig_static = np.zeros(m.ncell)
        for reg in design.static_regions:
            sel = m.cells_in_rect(reg.r0, reg.r1, reg.z0, reg.z1)
            self._mu_static[sel] = reg.material.mu_r
            self._sig_static[sel] = reg.material.sigma
        self.coil_names = list(design.coils)
        self.loads = {}
        self.turn_density = {}
        for name, coil in design.coils.items():
            t_cell = m.turns_per_cell(coil.layers)
            n_cell = t_cell / m.cell_area
            self.turn_density[name] = n_cell
            self.loads[name] = self.fem.load_vector(n_cell[m.tri_cell])
        self.r_dc = {name: coil.r_dc() for name, coil in design.coils.items()}

    # ------------------------------------------------------------------
    def _build_mesh(self):
        d, o = self.design, self.opts
        regions = list(d.static_regions)
        x0, x1 = self.x_range
        mov = [r.shifted(x0) for r in d.moving_regions] + [r.shifted(x1) for r in d.moving_regions]
        all_regions = regions + mov
        r_dev = max([r.r1 for r in all_regions] + [c.r_max for c in d.coils.values()])
        z_lo = min([r.z0 for r in all_regions] + [c.z_min for c in d.coils.values()])
        z_hi = max([r.z1 for r in all_regions] + [c.z_max for c in d.coils.values()])

        # radial axis --------------------------------------------------
        r_breaks = [0.0]
        for reg in all_regions:
            r_breaks += [reg.r0, reg.r1]
        for c in d.coils.values():
            r_breaks += [c.r_min, c.r_max]
        r_far = r_dev + o.far_factor * max(r_dev, 0.5 * (z_hi - z_lo))
        r_breaks.append(r_far)
        r_breaks = unique_sorted(r_breaks)

        def h_at_r(rb):
            h = o.h_fine
            for reg in all_regions:
                if reg.material.conductive and (np.isclose(rb, reg.r0) or np.isclose(rb, reg.r1)):
                    h = min(h, o.skin_fraction * reg.material.skin_depth(o.f_max))
                    h = min(h, (reg.r1 - reg.r0) / 4)
            return h

        h_b = np.array([h_at_r(rb) for rb in r_breaks])
        h_b[0] = max(h_b[0], 0.3e-3)
        h_b[-1] = r_far / 5
        h_int = []
        for a, b in zip(r_breaks[:-1], r_breaks[1:]):
            h_int.append(o.h_max_device if b <= r_dev + 1e-12 else r_far / 5)
        r = build_axis(r_breaks, h_b, h_int, o.growth)

        # axial axis: uniform zone + graded far field -------------------
        dz = o.dz
        zu0 = np.floor(z_lo / dz) * dz - 2 * dz
        zu1 = np.ceil(z_hi / dz) * dz + 2 * dz
        n_u = int(round((zu1 - zu0) / dz))
        z_uniform = zu0 + dz * np.arange(n_u + 1)
        z_far = o.far_factor * max(z_hi - z_lo, r_dev)
        z_left = build_axis([zu0 - z_far, zu0], [z_far / 5, dz], [z_far / 5], o.growth)
        z_right = build_axis([zu1, zu1 + z_far], [dz, z_far / 5], [z_far / 5], o.growth)
        z = np.concatenate([z_left[:-1], z_uniform, z_right[1:]])
        return AxiMesh(r, z)

    def snap(self, x):
        return np.round(np.asarray(x) / self.opts.dz) * self.opts.dz

    def materials_at(self, x):
        m = self.mesh
        mu = self._mu_static.copy()
        sig = self._sig_static.copy()
        for reg in self.design.moving_regions:
            sel = m.cells_in_rect(reg.r0, reg.r1, reg.z0 + x, reg.z1 + x)
            mu[sel] = reg.material.mu_r
            sig[sel] = reg.material.sigma
        return mu[m.tri_cell], sig[m.tri_cell]

    # ------------------------------------------------------------------
    def solve(self, x, f, return_fields=False):
        """Impedance matrix Z (coil order self.coil_names) at core position x and frequency f."""
        x = float(self.snap(x))
        w = 2 * np.pi * f
        mu, sig = self.materials_at(x)
        lu = self.fem.factorize(mu, sig, w)
        F = np.column_stack([self.loads[n] for n in self.coil_names]).astype(complex)
        A = lu.solve(F)
        lam = F.T @ A  # lam[k, l]: flux linkage of coil k for 1 A in coil l
        Z = 1j * w * lam + np.diag([self.r_dc[n] for n in self.coil_names])
        if return_fields:
            return Z, A
        return Z

    def coil_index(self, name):
        return self.coil_names.index(name)

    @property
    def n_unknowns(self):
        return self.fem.nf
