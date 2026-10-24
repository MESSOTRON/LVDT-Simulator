"""Phase-1 proof of concept on a generic (fictitious) LVDT.

Sections (run all, or name some on the command line):
  validation  FEM core vs. Bessel solution (eddy currents in a solid core)
  corelength  core-length study (nonlinearity / sensitivity trade-off)
  char        characteristic and nonlinearity, baseline vs. optimised core length
  field       field distribution (flux lines, |B|)
  freq        frequency response, stainless tube vs. plastic bobbin vs. housing w/o eddy currents
  material    influence of the unknown core material parameters (identifiability)
  mesh        mesh convergence check

All material values are assumptions -> results are qualitative until calibrated.

Run:  python examples/demo_generic_lvdt.py [section ...]      (all sections: ~12 minutes)
"""
from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import replace

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.tri as mtri  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tests"))

from lvdt_sim import (LIBRARY, LVDTModel, Material, MeshOptions, Region,  # noqa: E402
                      characteristic, evaluate, frequency_response, lvdt_output)
from lvdt_sim.designs import demo_design, plastic_bobbin_variant  # noqa: E402
from test_validation import cylinder_mu_eff_exact, cylinder_mu_eff_fem  # noqa: E402

OUT = os.path.join(ROOT, "docs", "phase1", "img")
RESULTS = os.path.join(ROOT, "docs", "phase1", "demo_results.json")
os.makedirs(OUT, exist_ok=True)
mm = 1e-3
F0, U0, RL = 5e3, 3.0, 100e3
X_RANGE = (-12 * mm, 12 * mm)

# reference palette (light mode), see dataviz skill
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SEQ = LinearSegmentedColormap.from_list(
    "seq", ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.spines.top": False,
    "axes.spines.right": False, "lines.linewidth": 2, "font.size": 10, "legend.frameon": False,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlecolor": INK,
    "contour.negative_linestyle": "solid",
})


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def opts(f_max=F0, **kw):
    return MeshOptions(f_max=f_max, **kw)


def marker_kw():
    return dict(ms=5, mec=SURF, mew=1.2)


def save(fig, name, dpi=150):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=dpi)
    plt.close(fig)


def l_opt(results):
    return results.get("core_length_scan", {}).get("L_opt_mm_for_+-10", 50.0) * mm


# ----------------------------------------------------------------------------
def sec_validation(results):
    core = LIBRARY["core_ferritic_stainless"]
    fs = np.geomspace(100, 50e3, 14)
    fem_v = np.array([cylinder_mu_eff_fem(3 * mm, core.mu_r, core.sigma, f) for f in fs])
    fdense = np.geomspace(100, 50e3, 200)
    ex_v = np.array([cylinder_mu_eff_exact(3 * mm, core.mu_r, core.sigma, f) for f in fdense])
    ex_at = np.array([cylinder_mu_eff_exact(3 * mm, core.mu_r, core.sigma, f) for f in fs])
    results["validation_bessel_max_err_pct"] = float(np.max(np.abs(fem_v - ex_at) / np.abs(ex_at)) * 100)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.semilogx(fdense, ex_v.real, color=C[0], label="Re(µ_eff) exakt (Bessel)")
    ax.semilogx(fdense, -ex_v.imag, color=C[1], label="−Im(µ_eff) exakt (Bessel)")
    ax.semilogx(fs, fem_v.real, "o", color=C[0], ms=6, mec=SURF, mew=1.5, label="FEM")
    ax.semilogx(fs, -fem_v.imag, "o", color=C[1], ms=6, mec=SURF, mew=1.5)
    ax.set_xlabel("Frequenz [Hz]")
    ax.set_ylabel("effektive Permeabilität")
    ax.set_title("Validierung: massiver Stahlkern Ø6 mm im Wechselfeld (µr=400, σ=1,43 MS/m)")
    ax.legend()
    save(fig, "06_validierung_bessel.png")


def sec_corelength(results):
    lengths = np.arange(24, 57, 2) * mm
    strokes = [10 * mm, 7.5 * mm, 5 * mm]
    xs_scan = np.arange(-10, 10.01, 1.0) * mm
    nl = {s: [] for s in strokes}
    sens, t_pt = [], []
    for L in lengths:
        m = LVDTModel(demo_design(core_length=L), x_range=X_RANGE, opts=opts())
        res = characteristic(m, xs_scan, F0, U0, r_load=RL)
        t_pt.append(res["seconds_per_point"])
        for s in strokes:
            nl[s].append(evaluate(res, -s, s)["nonlinearity_pct_span"])
        sens.append(evaluate(res, -10 * mm, 10 * mm)["sensitivity_mV_V_mm"])
        log(f"  L={L / mm:.0f} mm  NL(+-10)={nl[strokes[0]][-1]:.3f} %")
    results["core_length_scan"] = {
        "lengths_mm": (lengths / mm).tolist(),
        "nl_pct_span": {f"+-{s / mm:g}mm": v for s, v in nl.items()},
        "sensitivity_mV_V_mm": sens,
        "L_opt_mm_for_+-10": float(lengths[int(np.argmin(nl[strokes[0]]))] / mm),
    }
    results["seconds_per_position"] = float(np.mean(t_pt))
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    for k, s in enumerate(strokes):
        axs[0].semilogy(lengths / mm, nl[s], "-o", color=C[k], label=f"Messbereich ±{s / mm:g} mm", **marker_kw())
    axs[0].set_xlabel("Kernlänge [mm]")
    axs[0].set_ylabel("Linearitätsabweichung [% Spanne]")
    axs[0].set_title("Linearität vs. Kernlänge")
    axs[0].legend()
    axs[1].plot(lengths / mm, sens, "-o", color=C[0], **marker_kw())
    axs[1].set_xlabel("Kernlänge [mm]")
    axs[1].set_ylabel("Empfindlichkeit [mV/V/mm]")
    axs[1].set_title("Empfindlichkeit vs. Kernlänge (±10 mm)")
    save(fig, "03_kernlaengen_studie.png")


def demodulation_variants(res, ev, stroke):
    """Nonlinearity of the same sensor as seen by different measurement chains."""
    sel = ev["sel"] & (np.abs(res["x"]) <= stroke + 1e-12)
    x, u = res["x"][sel], res["u_out"][sel]

    def nl(y):
        X = np.column_stack([np.ones_like(x), x])
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        return float(np.abs(y - X @ c).max() / (y.max() - y.min()) * 100)

    return {
        "synchron_phase_abgeglichen": nl(ev["u_inphase"][sel]),
        "gleichgerichtet_betrag": nl(np.abs(u) * np.sign(x + 1e-12)),
        "synchron_referenz_speisespannung": nl(u.real),
    }


def sec_char(results):
    L_opt = l_opt(results)
    xs = np.arange(-12, 12.01, 0.5) * mm
    char = {}
    for L in (36 * mm, L_opt):
        m = LVDTModel(demo_design(core_length=L), x_range=X_RANGE, opts=opts())
        res = characteristic(m, xs, F0, U0, r_load=RL)
        ev = evaluate(res, -10 * mm, 10 * mm)
        char[L] = (res, ev)
        i0, i10 = np.argmin(abs(xs)), np.argmin(abs(xs - 10 * mm))
        results[f"characteristic_L{L / mm:.0f}mm"] = {
            "sensitivity_mV_V_mm": ev["sensitivity_mV_V_mm"], "phase_deg": ev["phase_deg"],
            "nonlinearity_pct_span_+-10": ev["nonlinearity_pct_span"],
            "u_out_rms_at_+10mm": float(abs(res["u_out"][i10])),
            "i_p_mA_at_null": float(abs(res["i_p"][i0]) * 1e3),
            "z_primary_at_null_ohm": [float(abs(res["z_in"][i0])), float(np.degrees(np.angle(res["z_in"][i0])))],
            "r_dc_ohm": {k: float(v) for k, v in m.r_dc.items()},
            "phase_deg_at_x": {f"{x / mm:g}mm": float(np.degrees(np.angle(
                res["u_out"][np.argmin(abs(xs - x))] - res["u_out"][np.argmin(abs(xs + x))])))
                for x in (1 * mm, 5 * mm, 10 * mm)},
            "nonlinearity_by_demodulation_pct_span": demodulation_variants(res, ev, 10 * mm),
        }
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    for k, (L, (res, ev)) in enumerate(char.items()):
        lab = f"Kern {L / mm:.0f} mm"
        axs[0].plot(res["x"] / mm, ev["u_inphase"] * 1e3, color=C[k], label=lab)
        sel = ev["sel"]
        axs[1].plot(res["x"][sel] / mm, ev["deviation"][sel] / ev["span"] * 100, color=C[k],
                    label=f"{lab}: max {ev['nonlinearity_pct_span']:.2f} %")
    axs[0].set_xlabel("Kernposition x [mm]")
    axs[0].set_ylabel("Ausgang (phasenrichtig) [mV eff]")
    axs[0].set_title(f"Kennlinie bei {U0:g} V / {F0 / 1e3:g} kHz, R_L = 100 kΩ")
    axs[0].legend()
    axs[1].set_xlabel("Kernposition x [mm]")
    axs[1].set_ylabel("Abweichung von Ausgleichsgerade [% Spanne]")
    axs[1].set_title("Linearitätsabweichung im Messbereich ±10 mm")
    axs[1].legend()
    save(fig, "02_kennlinie_linearitaet.png")


def sec_field(results):
    L_opt = l_opt(results)
    d = demo_design(core_length=L_opt)
    m = LVDTModel(d, x_range=X_RANGE, opts=opts())
    x_f = 5 * mm
    Z, A = m.solve(x_f, F0, return_fields=True)
    o = lvdt_output(Z, (0, 1, 2), U0, r_load=RL)
    psi = m.fem.full(A[:, 0] * o["i_p"])  # secondary currents (R_L = 100 kOhm) are negligible
    br, bz = m.fem.flux_density(psi)
    bmag = np.sqrt(np.abs(br) ** 2 + np.abs(bz) ** 2) * np.sqrt(2) * 1e3  # peak, mT
    mesh = m.mesh
    T = mtri.Triangulation(mesh.nodes[:, 1] / mm, mesh.nodes[:, 0] / mm, mesh.tri)
    fig, ax = plt.subplots(figsize=(11, 3.4))
    inside = (mesh.cell_rc[mesh.tri_cell] < 6 * mm) & (np.abs(mesh.cell_zc[mesh.tri_cell]) < 36 * mm)
    vmax = np.percentile(bmag[inside], 99)
    tpc = ax.tripcolor(T, facecolors=bmag, cmap=SEQ, shading="flat", vmin=0, vmax=vmax, rasterized=True)
    psi_r = np.real(psi * np.exp(-1j * np.angle(o["i_p"])))
    lv = np.linspace(psi_r.min(), psi_r.max(), 30)[1:-1]
    ax.tricontour(T, psi_r, levels=lv, colors=INK2, linewidths=0.6)
    for reg in d.static_regions + [r.shifted(x_f) for r in d.moving_regions]:
        ax.add_patch(plt.Rectangle((reg.z0 / mm, reg.r0 / mm), (reg.z1 - reg.z0) / mm, (reg.r1 - reg.r0) / mm,
                                   fill=False, ec=INK, lw=0.8))
    for name, coil in d.coils.items():
        ax.add_patch(plt.Rectangle((coil.z_min / mm, coil.r_min / mm), (coil.z_max - coil.z_min) / mm,
                                   (coil.r_max - coil.r_min) / mm, fill=False, ec=C[1], lw=1.4))
        ax.text((coil.z_min + coil.z_max) / 2 / mm, 6.3, name, ha="center", va="bottom", color=INK, fontsize=9)
    ax.text(x_f / mm, 1.4, "Kern", ha="center", color=INK, fontsize=9)
    ax.set_xlim(-38, 38)
    ax.set_ylim(0, 7.5)
    ax.grid(False)
    ax.set_xlabel("z [mm]")
    ax.set_ylabel("r [mm]  (überhöht)")
    ax.set_title(f"Feldlinien und |B| – Kern {L_opt / mm:.0f} mm bei x = +5 mm, {U0:g} V / {F0 / 1e3:g} kHz "
                 "(Momentanbild, Primärstrom)")
    cb = fig.colorbar(tpc, ax=ax, fraction=0.02, pad=0.01)
    cb.set_label("|B| Scheitel [mT]")
    save(fig, "01_feldbild.png", dpi=170)


def sec_freq(results):
    L_opt = l_opt(results)
    freqs = np.geomspace(100, 20e3, 16)
    base = demo_design(core_length=L_opt)
    hous = LIBRARY["housing_free_cutting_steel"]
    no_eddy_housing = replace(base, static_regions=[
        replace(r, material=Material(hous.name + " ohne Wirbelstrom", hous.mu_r, 0.0))
        if r.material is hous else r for r in base.static_regions])
    variants = [("Edelstahl-Wickelrohr (Basis)", base),
                ("Kunststoff-Spulenkörper", plastic_bobbin_variant(base)),
                ("Basis, Gehäuse ohne Wirbelströme (z. B. geschlitzt)", no_eddy_housing)]
    fr = {}
    for label, des in variants:
        mf = LVDTModel(des, x_range=X_RANGE, opts=opts(f_max=20e3))
        r = frequency_response(mf, 5 * mm, freqs, U0, r_load=RL)
        fr[label] = r
        k = int(np.argmax(r["sens"]))
        ph = r["phase"]
        zero = None
        for i in range(len(ph) - 1):
            if ph[i] >= 0 > ph[i + 1]:
                t = ph[i] / (ph[i] - ph[i + 1])
                zero = float(np.exp(np.log(freqs[i]) + t * (np.log(freqs[i + 1]) - np.log(freqs[i]))))
        results[f"freq_response_{label}"] = {
            "f_Hz": freqs.tolist(), "sens_mV_V_mm": r["sens"].tolist(), "phase_deg": ph.tolist(),
            "z_in0_abs": np.abs(r["z_in0"]).tolist(), "f_max_sensitivity_Hz": float(freqs[k]),
            "f_zero_phase_Hz": zero,
        }
        log(f"  {label}: S_max bei {freqs[k]:.0f} Hz, Phase 0 bei {zero}")
    fig, axs = plt.subplots(3, 1, figsize=(7.5, 8.5), sharex=True)
    for k, (label, r) in enumerate(fr.items()):
        axs[0].semilogx(freqs, r["sens"], "-o", color=C[k], label=label, **marker_kw())
        axs[1].semilogx(freqs, r["phase"], "-o", color=C[k], **marker_kw())
        axs[2].semilogx(freqs, np.abs(r["z_in0"]), "-o", color=C[k], **marker_kw())
    axs[0].set_ylabel("Empfindlichkeit\n[mV/V/mm]")
    axs[0].set_title("Frequenzgang (Kern optimiert, Werkstoffwerte angenommen)")
    axs[0].legend(fontsize=9)
    axs[1].set_ylabel("Phase Ausgang zu\nSpeisespannung [°]")
    axs[1].axhline(0, color=INK2, lw=0.8)
    axs[2].set_ylabel("|Z| Primär in\nNullstellung [Ω]")
    axs[2].set_xlabel("Speisefrequenz [Hz]")
    save(fig, "04_frequenzgang.png")


def sec_material(results):
    """Sensitivity and phase vs. unknown core mu_r and sigma, at two frequencies."""
    L_opt = l_opt(results)
    mus = np.geomspace(100, 1600, 7)
    sigmas = np.geomspace(0.7e6, 5.6e6, 6)
    # one model whose mesh resolves the most conductive / permeable core, core material swapped
    worst = Material("Kern", mus[-1], sigmas[-1])
    m = LVDTModel(demo_design(core_length=L_opt, core_material=worst), x_range=(-6 * mm, 6 * mm),
                  opts=opts(f_max=5e3))
    core_region = m.design.moving_regions[0]
    maps = {}
    for f in (1e3, 5e3):
        S = np.zeros((len(sigmas), len(mus)))
        P = np.zeros_like(S)
        for i, sg in enumerate(sigmas):
            for j, mu in enumerate(mus):
                m.design.moving_regions[0] = replace(core_region, material=Material("Kern", mu * (1 - 0.1j), sg))
                up = lvdt_output(m.solve(5 * mm, f), (0, 1, 2), U0, r_load=RL)["u_out"]
                un = lvdt_output(m.solve(-5 * mm, f), (0, 1, 2), U0, r_load=RL)["u_out"]
                slope = (up - un) / (10 * mm)
                S[i, j] = abs(slope) / U0
                P[i, j] = np.degrees(np.angle(slope))
        maps[f] = (S, P)
        log(f"  f={f:g} Hz fertig")
    m.design.moving_regions[0] = core_region
    results["core_material_map"] = {
        "mu_r": mus.tolist(), "sigma_S_m": sigmas.tolist(),
        **{f"sens_{f:g}Hz": maps[f][0].tolist() for f in maps},
        **{f"phase_{f:g}Hz": maps[f][1].tolist() for f in maps},
    }
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.3))
    for ax, f in zip(axs, maps):
        S, P = maps[f]
        cs1 = ax.contour(mus, sigmas / 1e6, S, levels=7, colors=C[0], linewidths=1.6)
        ax.clabel(cs1, fmt="%.0f", fontsize=8)
        cs2 = ax.contour(mus, sigmas / 1e6, P, levels=7, colors=C[1], linewidths=1.6)
        ax.clabel(cs2, fmt="%.0f°", fontsize=8)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks([100, 200, 400, 800, 1600], ["100", "200", "400", "800", "1600"])
        ax.set_yticks([0.7, 1.4, 2.8, 5.6], ["0,7", "1,4", "2,8", "5,6"])
        ax.minorticks_off()
        ax.set_xlabel("Anfangspermeabilität µr des Kerns")
        ax.set_ylabel("Leitfähigkeit σ des Kerns [MS/m]")
        ax.set_title(f"{f / 1e3:g} kHz")
    axs[0].plot([], [], color=C[0], label="Empfindlichkeit [mV/V/mm]")
    axs[0].plot([], [], color=C[1], label="Phase [°]")
    axs[0].legend(loc="upper left", fontsize=9)
    fig.suptitle("Kernwerkstoff: bei 5 kHz verlaufen die Linien fast parallel (nur µr/σ wirksam), "
                 "bei 1 kHz weichen sie voneinander ab", fontsize=11, fontweight="bold", color=INK)
    save(fig, "05_werkstoffeinfluss_kern.png")


def sec_mesh(results):
    L_opt = l_opt(results)
    conv = {}
    xs_c = np.arange(-10, 10.01, 2.0) * mm
    for label, o_ in [("Standard (dz=0.10 mm)", opts()),
                      ("fein (dz=0.05 mm, h=0.025 mm)", opts(dz=0.05 * mm, h_fine=0.025 * mm, skin_fraction=0.05))]:
        mc = LVDTModel(demo_design(core_length=L_opt), x_range=X_RANGE, opts=o_)
        res = characteristic(mc, xs_c, F0, U0, r_load=RL)
        ev = evaluate(res, -10 * mm, 10 * mm)
        conv[label] = {"unknowns": int(mc.n_unknowns), "sens": ev["sensitivity_mV_V_mm"], "phase": ev["phase_deg"],
                       "nl": ev["nonlinearity_pct_span"], "s_per_pt": res["seconds_per_point"],
                       "dev": (ev["deviation"] / ev["span"] * 100).tolist()}
        log(f"  {label}: {conv[label]['unknowns']} Unbekannte, S={ev['sensitivity_mV_V_mm']:.3f}, "
            f"phi={ev['phase_deg']:.3f}, NL={ev['nonlinearity_pct_span']:.4f} %")
    results["mesh_convergence"] = conv


SECTIONS = {"validation": sec_validation, "corelength": sec_corelength, "char": sec_char,
            "field": sec_field, "freq": sec_freq, "material": sec_material, "mesh": sec_mesh}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(SECTIONS)
    results = {}
    if os.path.exists(RESULTS):
        with open(RESULTS) as fh:
            results = json.load(fh)
    for name in wanted:
        log(name)
        SECTIONS[name](results)
        with open(RESULTS, "w") as fh:
            json.dump(results, fh, indent=1, ensure_ascii=False, default=float)
    log("fertig")
