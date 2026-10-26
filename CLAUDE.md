# CLAUDE.md – LVDT-Simulator (MESSOTRON R&D)

Read [docs/HANDOVER.md](docs/HANDOVER.md) first: it holds the project history, every decision
made so far, the open questions and the next steps. Work in this repository continues
**locally** (it started in Claude Code cloud sessions).

## Project in one paragraph

A digital twin for LVDTs (linear variable differential transformers) built by MESSOTRON.
From geometry, materials, winding instructions and the CNC winding program it should predict
the characteristic curve, linearity, sensitivity, phase, primary impedance and a good
excitation frequency. It will be calibrated and validated against MESSOTRON's measurement
database, then used to compute variants and design new sensors.

## Layout

- `lvdt_sim/` – solver: 2D axisymmetric time-harmonic FEM (flux function r·A_φ) with eddy
  currents; `model.py` returns the impedance matrix P/S1/S2 per core position and frequency,
  `circuit.py` turns it into secondary output, `analysis.py` evaluates curves/linearity.
- `tests/test_validation.py` – validation against analytical solutions (must stay < 1 %).
- `examples/` – `demo_generic_lvdt.py` (Phase 1 plots, ~10 min), `phase2_phase_check.py`.
- `docs/phase1`, `docs/phase2` – German originals (authoritative).
- `docs/en/` – English translations of those documents.

## Commands

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python tests/test_validation.py        # ~2 s, prints "alle Validierungen bestanden"
python tests/test_model.py
python examples/demo_generic_lvdt.py   # regenerates docs/phase1/img
```

## Conventions

- Code identifiers and comments are mixed German/English; match the surrounding file.
  New documentation is written in English unless the owner asks for German.
- Material values in `materials.py` and `designs.py` are **assumptions**, not MESSOTRON data;
  the demo design is fictitious. Do not present results as statements about real sensors
  before calibration (Phase 3).
- Raw measurement data stays out of git (`data/raw/`, `*.sqlite`, `*.mdb`, `*.accdb`
  are ignored). Confidentiality of winding programs/drawings is still an open question (D.19).
