"""Characteristic, sensitivity, phase and linearity evaluation."""
from __future__ import annotations

import time

import numpy as np

from .circuit import lvdt_output


def characteristic(model, xs, f, u0=1.0, r_source=0.0, r_load=np.inf, coils=("P", "S1", "S2")):
    idx = tuple(model.coil_index(c) for c in coils)
    xs = model.snap(np.asarray(xs, float))
    rows = []
    t0 = time.perf_counter()
    for x in xs:
        Z = model.solve(x, f)
        rows.append(lvdt_output(Z, idx, u0, r_source, r_load))
    dt = time.perf_counter() - t0
    res = {k: np.array([r[k] for r in rows]) for k in rows[0]}
    res["x"] = xs
    res["f"] = f
    res["u0"] = u0
    res["seconds_per_point"] = dt / len(xs)
    return res


def evaluate(res, x_lo=None, x_hi=None):
    """Phase-sensitive evaluation like a synchronous demodulator.

    The complex best-fit slope b of U_out(x) defines the reference phase; the
    in-phase component is the demodulated signal, the quadrature component
    remains as residual (part of the null voltage).
    """
    x = res["x"]
    u = res["u_out"]
    sel = np.ones_like(x, bool)
    if x_lo is not None:
        sel &= x >= x_lo - 1e-12
    if x_hi is not None:
        sel &= x <= x_hi + 1e-12
    X = np.column_stack([np.ones(sel.sum()), x[sel]])
    coef, *_ = np.linalg.lstsq(X.astype(complex), u[sel], rcond=None)
    b = coef[1]
    phi = np.angle(b)
    u_inphase = (u * np.exp(-1j * phi)).real
    u_quad = (u * np.exp(-1j * phi)).imag
    # best-fit straight line on the in-phase signal
    c2, *_ = np.linalg.lstsq(X, u_inphase[sel], rcond=None)
    fit = c2[0] + c2[1] * x
    dev = u_inphase - fit
    span = u_inphase[sel].max() - u_inphase[sel].min()
    nonlin_span = np.abs(dev[sel]).max() / span * 100
    return {
        "sensitivity_mV_V_mm": abs(c2[1]) / res["u0"] * 1e3 * 1e-3,
        "phase_deg": np.degrees(phi),
        "nonlinearity_pct_span": nonlin_span,
        "nonlinearity_pct_halfspan": 2 * nonlin_span,
        "u_inphase": u_inphase,
        "u_quad": u_quad,
        "deviation": dev,
        "span": span,
        "sel": sel,
    }


def frequency_response(model, x_test, freqs, u0=1.0, r_source=0.0, r_load=np.inf,
                       coils=("P", "S1", "S2")):
    """Sensitivity and phase vs. frequency from the symmetric difference at +-x_test."""
    idx = tuple(model.coil_index(c) for c in coils)
    out = {"f": np.asarray(freqs, float), "sens": [], "phase": [], "z_in0": [], "i_p0": []}
    for f in freqs:
        up = lvdt_output(model.solve(+x_test, f), idx, u0, r_source, r_load)
        un = lvdt_output(model.solve(-x_test, f), idx, u0, r_source, r_load)
        z0 = lvdt_output(model.solve(0.0, f), idx, u0, r_source, r_load)
        slope = (up["u_out"] - un["u_out"]) / (2 * x_test)
        out["sens"].append(abs(slope) / u0 * 1e3 * 1e-3)
        out["phase"].append(np.degrees(np.angle(slope)))
        out["z_in0"].append(z0["z_in"])
        out["i_p0"].append(z0["i_p"])
    for k in ("sens", "phase", "z_in0", "i_p0"):
        out[k] = np.array(out[k])
    return out
