"""Consistency checks of winding import, circuit and LVDT model.

Run:  python -m pytest tests -q     or     python tests/test_model.py
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lvdt_sim import LVDTModel, MeshOptions, layers_from_moves, lvdt_output  # noqa: E402
from lvdt_sim.designs import demo_design  # noqa: E402
from lvdt_sim.fem import AxiMesh  # noqa: E402

mm = 1e-3


def test_moves_to_layers_and_turn_conservation():
    # 3 traverse moves with reversal -> 3 layers; graded first layer (2 segments)
    moves = [(0, 5 * mm, 50), (5 * mm, 10 * mm, 80), (10 * mm, 0, 100), (0, 10 * mm, 100)]
    layers = layers_from_moves(moves, r_start=4 * mm, layer_pitch=0.1 * mm)
    assert len(layers) == 3
    assert [round(l.turns) for l in layers] == [130, 100, 100]
    mesh = AxiMesh(np.linspace(0, 6 * mm, 37), np.linspace(-2 * mm, 12 * mm, 71))
    t = mesh.turns_per_cell(layers)
    assert abs(t.sum() - 330) < 1e-9


def test_model_symmetry_reciprocity_and_load():
    m = LVDTModel(demo_design(), x_range=(-6 * mm, 6 * mm), opts=MeshOptions(f_max=5e3, dz=0.2 * mm))
    f = 5e3
    Z0 = m.solve(0.0, f)
    Zp = m.solve(+4 * mm, f)
    Zn = m.solve(-4 * mm, f)
    # reciprocity: complex symmetric impedance matrix
    assert np.allclose(Zp, Zp.T, rtol=1e-9, atol=1e-9)
    # null: symmetric secondaries -> output ~ 0
    o0 = lvdt_output(Z0, (0, 1, 2), 1.0)
    op = lvdt_output(Zp, (0, 1, 2), 1.0)
    on = lvdt_output(Zn, (0, 1, 2), 1.0)
    assert abs(o0["u_out"]) < 1e-9 * abs(op["u_out"])
    # mirror symmetry of the design: U(-x) = -U(x)
    assert abs(op["u_out"] + on["u_out"]) < 1e-9 * abs(op["u_out"])
    # very large load equals open circuit, finite load reduces the output
    ol = lvdt_output(Zp, (0, 1, 2), 1.0, r_load=1e12)
    assert abs(ol["u_out"] - op["u_out"]) < 1e-6 * abs(op["u_out"])
    o10k = lvdt_output(Zp, (0, 1, 2), 1.0, r_load=10e3)
    assert abs(o10k["u_out"]) < abs(op["u_out"])


if __name__ == "__main__":
    test_moves_to_layers_and_turn_conservation()
    test_model_symmetry_reciprocity_and_load()
    print("alle Modelltests bestanden")
