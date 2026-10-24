"""Material definitions for the axisymmetric LVDT model.

All materials are treated as linear (small-signal) with a complex relative
permeability mu_r = mu' - j*mu'' (mu'' models hysteresis losses) and an
electrical conductivity sigma (eddy currents).

IMPORTANT: The values in LIBRARY are rough handbook *assumptions* for the
proof of concept. The steels used for LVDT cores and housings are not
specified magnetically by their suppliers, so the real values must be
identified from measurements (see docs/phase1).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

MU0 = 4e-7 * np.pi


@dataclass(frozen=True)
class Material:
    name: str
    mu_r: complex = 1.0
    sigma: float = 0.0  # S/m
    note: str = ""

    @property
    def conductive(self) -> bool:
        return self.sigma > 0.0

    def skin_depth(self, f: float) -> float:
        """Classical skin depth in m (inf for non-conductors)."""
        if self.sigma <= 0.0 or f <= 0.0:
            return np.inf
        return 1.0 / np.sqrt(np.pi * f * MU0 * abs(self.mu_r) * self.sigma)


AIR = Material("Luft / Kunststoff / GFK", 1.0, 0.0, "nicht leitend, unmagnetisch")

LIBRARY = {
    "air": AIR,
    "plastic": Material("Kunststoff-Spulenkörper", 1.0, 0.0, "Spritzguss oder GFK"),
    "stainless_austenitic": Material(
        "Edelstahlrohr austenitisch (z.B. 1.4301)", 1.05, 1.4e6,
        "Annahme: mu_r 1.0..1.3 je nach Kaltverformung, rho ~0.72 uOhm m"),
    "core_ferritic_stainless": Material(
        "Kern ferritischer Edelstahl (z.B. 1.4105)", 400.0 - 40.0j, 1.43e6,
        "Annahme: Anfangspermeabilitaet unbekannt -> kalibrieren"),
    "housing_free_cutting_steel": Material(
        "Gehaeuse Automatenstahl (z.B. 1.0718)", 300.0 - 30.0j, 5.0e6,
        "Annahme: Anfangspermeabilitaet unbekannt -> kalibrieren"),
}
