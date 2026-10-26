# Handover: LVDT-Simulator, from cloud sessions to local work

Status as of 26 Oct 2026. This file replaces the cloud session transcripts. Details are in:
- [history/2026-10-24_cloud_sessions_rd.md](history/2026-10-24_cloud_sessions_rd.md): Phase 1
  and the follow-up review.
- [history/2026-10-26_cloud_sessions_simulator.md](history/2026-10-26_cloud_sessions_simulator.md):
  the Phase 2 web research.

## 1. What the project is

The MESSOTRON owner wants a **digital twin for LVDTs**. From geometry, wire, core material and
dimensions, the winding instructions and the CNC winding programs, it should predict:
- the characteristic curve and linearity;
- sensitivity;
- phase;
- primary impedance;
- a good excitation frequency.

The first goal is to recalculate existing MESSOTRON sensors, calibrated against the company's
measurement database, which holds tens of thousands of measurements. After that, the tool
should change parameters (core, material, frequency, winding) and design new sensors with
excellent linearity and a defined sensitivity.

## 2. What exists (all on branch `claude/relaxed-rubin-rhr4rj`)

| Item | Where | English version |
|---|---|---|
| Feasibility study (Phase 1) | `docs/phase1/01_Machbarkeitsanalyse.md` | [en/phase1/01_feasibility_analysis.md](en/phase1/01_feasibility_analysis.md) |
| Data requirements | `docs/phase1/02_Datenanforderungen.md` | [en/phase1/02_data_requirements.md](en/phase1/02_data_requirements.md) |
| 22 questions to MESSOTRON | `docs/phase1/03_Rueckfragen.md` | [en/phase1/03_open_questions.md](en/phase1/03_open_questions.md) |
| Public website data (Phase 2) | `docs/phase2/01_Webrecherche_messotron.md`, `messotron_web_daten.json` | [en/phase2/01_messotron_web_research.md](en/phase2/01_messotron_web_research.md) |
| FEM solver | `lvdt_sim/` | – |
| Validation tests | `tests/` (both pass; ~0.1 % against Bessel, 0.35–0.6 % for air-coil couplings) | – |
| Demo and phase check | `examples/` | – |

The German documents remain the originals.

**Git history:**
- `6a7f4ad`: Phase 1 (24 Oct).
- `1231a12`: Phase 2 web data (26 Oct, from branch `claude/eloquent-cray-3q6sag`).
- Later commits: this handover, the English translations and `CLAUDE.md`.

No work from the cloud sessions was lost: every session that produced files pushed them.

## 3. Key results so far

- **Feasible.** The recommended approach is a hybrid: 2D axisymmetric eddy-current FEM, then
  calibration on 3–5 reference sensors, then a small residual model.
- **Expected accuracy after calibration (estimates):** sensitivity ±3–5 %, phase ±2–3°,
  linearity shape about ±0.05–0.1 % of span.
- **Demo findings (fictitious sensor, assumed materials):**
  - The right core length cuts linearity error from 3.9 % to 0.33 % of span.
  - A stainless coil-former tube costs about 23 % sensitivity and 27° of phase.
  - The demodulation method alone changes measured linearity: 0.22 %, 0.33 % or 12.5 %.
- **Phase mismatch (Phase 2).** MESSOTRON states a typical phase of 1–20°, but the demo gives
  −75°. The assumed eddy-current losses are too high, or real sensors are built differently.
  Measured phase is therefore a strong calibration quantity, and **the coil-former
  construction is the most important open question.**
- **MESSOTRON MBI 46.x electronics (from the website):** about 2 V rms at 5 kHz, about 200 kΩ
  input, phase-sensitive demodulation, phase adjusted at 3/4 of the nominal stroke. Datasheet
  sensitivity is ±10 % for uncalibrated sensors.

## 4. Open items, in recommended order

1. **Check the Phase 2 values against the original PDFs.** This step was blocked in the cloud
   because the network proxy refused messotron.com/.de. It should work locally.
   - Download the PDFs listed in `docs/phase2/messotron_web_daten.json`.
   - Store the PDFs and text extracts under `data/messotron_web/`.
   - Correct deviating values and mark them as verified.
   - Resolve the contradictions for DTU, DGO, DPF, DFI and DU.
2. **Owner decision pending** (from the review session): should the study be updated with
   review points 2–5, and should the demo LVDT be cross-checked with an independent FEM program
   (FEMM, Elmer or GetDP)? The review called the cross-check the cheapest strong evidence
   before calibration. The update covers:
   - verified vs. validated;
   - material class = steel grade + processing;
   - local level-dependent µ;
   - linearity target unproven;
   - the §4.2 text error (mesh, not domain).
3. **Answers from MESSOTRON** to the open questions. The most important are:
   - test-bench measurement chain (A.1–A.3);
   - coil former: stainless tube or plastic, and wall thickness (B.9);
   - housing steel: ferritic or austenitic (B.8);
   - linearity reference line (A.5);
   - fields in the test report (A.4);
   - where CNC programs, drawings and the database may be stored (D.19).
4. **Data package for 3–5 reference sensors**: drawing, CNC program, winding-instruction PDF
   and database export. Candidates from public data: DM, DUH or DTL, and WLU or WLG for LVIT.
5. **Extra measurements**: σ of the core rods (4-wire), a frequency sweep, and a measurement at
   two supply voltages.
6. **Code work possible without data**:
   - evaluation like the MBI amplifier (fixed reference phase at 0.75·x_nominal);
   - a 200 kΩ standard load;
   - an LVIT half-bridge circuit;
   - a CNC parser framework once a sample program exists.

## 5. Continuing locally

```bash
git clone https://github.com/MESSOTRON/LVDT-Simulator.git
cd LVDT-Simulator
git checkout claude/relaxed-rubin-rhr4rj        # contains everything above
python -m venv .venv
source .venv/bin/activate                       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python tests/test_validation.py                 # should end with "alle Validierungen bestanden"
claude                                          # start Claude Code here; it reads CLAUDE.md
```

The other `claude/*` branches are older subsets of this branch and can be deleted once it is
merged.
