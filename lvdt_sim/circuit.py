"""External circuit of an LVDT: voltage-driven primary, secondaries in series opposition.

Passive sign convention: V_k = sum_l Z_kl I_l. The output is
U_out = V_S2 - V_S1 (a core displacement towards S2, x > 0, gives a positive,
in-phase output) and is loaded with R_load.
"""
from __future__ import annotations

import numpy as np


def lvdt_output(Z, idx, u0=1.0, r_source=0.0, r_load=np.inf):
    """Return dict with output voltage, primary current and individual secondary voltages.

    Z: impedance matrix, idx: (iP, iS1, iS2) indices into Z.
    """
    p, s1, s2 = idx
    zpp = Z[p, p] + r_source
    zd = Z[s2, p] - Z[s1, p]
    zloop = Z[s1, s1] + Z[s2, s2] - 2 * Z[s1, s2]
    if np.isinf(r_load):
        ip, il = u0 / zpp, 0.0
    else:
        # unknowns: primary current, load current (out of the S2 terminal)
        M = np.array([[zpp, -zd], [zd, -(zloop + r_load)]], dtype=complex)
        ip, il = np.linalg.solve(M, np.array([u0, 0.0], dtype=complex))
    i_s2, i_s1 = -il, il
    v_s1 = Z[s1, p] * ip + Z[s1, s1] * i_s1 + Z[s1, s2] * i_s2
    v_s2 = Z[s2, p] * ip + Z[s2, s1] * i_s1 + Z[s2, s2] * i_s2
    return {"u_out": v_s2 - v_s1, "i_p": ip, "v_s1": v_s1, "v_s2": v_s2,
            "z_in": u0 / ip - r_source}
