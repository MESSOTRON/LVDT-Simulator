"""Phase-2 plausibility check against public MESSOTRON data.

MESSOTRON's technical notes give a typical phase shift of 1...20 degrees between
excitation and output voltage. With the phase-1 material assumptions the demo LVDT
shows -75 degrees at 5 kHz. This script recomputes the demo at the measuring
conditions of the MESSOTRON amplifiers MBI 46.x (2 V rms, 5 kHz, 200 kOhm input)
for a few housing/bobbin variants. All material values remain assumptions.

Run:  python examples/phase2_phase_check.py      (~1 minute)
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from lvdt_sim import LVDTModel, MeshOptions  # noqa: E402
from lvdt_sim.analysis import frequency_response  # noqa: E402
from lvdt_sim.designs import demo_design, plastic_bobbin_variant  # noqa: E402
from lvdt_sim.materials import LIBRARY, Material  # noqa: E402

mm = 1e-3
F0, U0, RL = 5e3, 2.0, 200e3          # MBI 46.31: ~2 V rms sine, 5 kHz, ~200 kOhm input
CORE_LENGTH = 50 * mm                 # optimum core length of the phase-1 demo (+-10 mm)

# assumed housing alternatives ("rostfreier Stahl" per MESSOTRON technical notes)
HOUSING_FERRITIC = Material("Gehaeuse ferritischer Edelstahl (Annahme)", 300.0 - 30.0j, 1.6e6,
                            "Annahme: z.B. 1.4105, Permeabilitaet unbekannt")
HOUSING_AUSTENITIC = LIBRARY["stainless_austenitic"]


def no_eddy(mat: Material) -> Material:
    return Material(mat.name + " ohne Wirbelstrom", mat.mu_r, 0.0)


def variants():
    core = LIBRARY["core_ferritic_stainless"]
    base = demo_design(core_length=CORE_LENGTH)
    ferr = demo_design(core_length=CORE_LENGTH, housing_material=HOUSING_FERRITIC)
    aust = demo_design(core_length=CORE_LENGTH, housing_material=HOUSING_AUSTENITIC)
    ferr_core0 = demo_design(core_length=CORE_LENGTH, housing_material=HOUSING_FERRITIC,
                             core_material=no_eddy(core))
    ferr0 = demo_design(core_length=CORE_LENGTH, housing_material=no_eddy(HOUSING_FERRITIC))
    all0 = demo_design(core_length=CORE_LENGTH, housing_material=no_eddy(HOUSING_FERRITIC),
                       core_material=no_eddy(core))
    return [
        ("Basis Phase 1 (Automatenstahl, Edelstahlrohr)", base),
        ("Basis mit Kunststoffkoerper", plastic_bobbin_variant(base)),
        ("Gehaeuse ferritischer Edelstahl, Edelstahlrohr", ferr),
        ("Gehaeuse austenitisch (unmagnetisch), Edelstahlrohr", aust),
        ("Gehaeuse ferritischer Edelstahl, Kunststoffkoerper", plastic_bobbin_variant(ferr)),
        # decomposition: which eddy currents cause the phase lag
        ("  dito, Kern ohne Wirbelstroeme", plastic_bobbin_variant(ferr_core0)),
        ("  dito, Gehaeuse ohne Wirbelstroeme", plastic_bobbin_variant(ferr0)),
        ("  dito, Kern und Gehaeuse ohne Wirbelstroeme", plastic_bobbin_variant(all0)),
    ]


def main():
    out = {"f_Hz": F0, "u0_V": U0, "r_load_ohm": RL, "core_length_mm": CORE_LENGTH / mm,
           "variants": {}}
    print(f"{'Variante':55s} {'S [mV/V/mm]':>12s} {'Phase [deg]':>12s} {'|Z_P| [Ohm]':>12s} {'I_P [mA]':>9s}")
    for label, des in variants():
        m = LVDTModel(des, x_range=(-12 * mm, 12 * mm), opts=MeshOptions(f_max=F0))
        r = frequency_response(m, 5 * mm, [F0], U0, r_load=RL)
        sens, phase = float(r["sens"][0]), float(r["phase"][0])
        z, ip = abs(r["z_in0"][0]), abs(r["i_p0"][0]) * 1e3
        out["variants"][label] = {"sens_mV_V_mm": sens, "phase_deg": phase,
                                  "z_p0_abs_ohm": z, "i_p0_mA": ip}
        print(f"{label:55s} {sens:12.1f} {phase:12.1f} {z:12.0f} {ip:9.1f}")
    path = os.path.join(ROOT, "docs", "phase2", "phase_check_results.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
