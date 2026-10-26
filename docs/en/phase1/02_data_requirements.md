# Phase 1 – Data Requirements for the Digital Twin

_English translation of [docs/phase1/02_Datenanforderungen.md](../../phase1/02_Datenanforderungen.md). The German original remains authoritative._

Status: 24.10.2026 · belongs to [01_feasibility_analysis.md](01_feasibility_analysis.md)

This list describes which data the model needs, what for, and in what form. We will not
start with all products, but with **3 to 5 reference sensors** (proposal in
Section 6). For these types the data package should be as complete as possible.

Priorities:
- **A**: mandatory for the recalculation
- **B**: makes the calibration considerably more reliable
- **C**: useful for later expansion stages

---

## 1. Geometry (per sensor type)

| Prio | Item | Purpose | Form |
|---|---|---|---|
| A | Coil former: inner/outer diameter, wall thickness of the stainless steel tube or plastic former, length | Turn radii, eddy currents in the tube | Drawing (PDF) or 3D model (STEP) |
| A | Chamber layout: position and width of the chambers and dividers (z coordinates) | Position of the coils | Drawing |
| A | Housing: inner/outer diameter, length, covers/end discs (thickness, bore), position relative to the coil former | Magnetic return path, eddy currents | Drawing / STEP |
| A | Core: diameter, length, bore/chamfer if any; core connection (push rod, threaded rod: diameter, length, material) | Flux-carrying element; a magnetic push rod changes the characteristic curve | Drawing |
| A | Definition of the zero point and the measuring range (core position ↔ housing) | Reference of the characteristic curve | Drawing / test instruction |
| B | Deviations from rotational symmetry: slots in the housing, cable exit, flats | Assessment of whether 2D is sufficient | Photo / drawing |
| C | Tolerances of the above dimensions | Tolerance analysis | Drawing |

## 2. Materials

| Prio | Item | Purpose |
|---|---|---|
| A | Material number or trade name for core, housing, cover, coil former, push rod | Starting values and assignment to material classes |
| A | Delivery condition / heat treatment (drawn, peeled, annealed, magnetically final-annealed?) | Permeability depends strongly on it |
| B | Available properties: electrical resistivity, permeability, coercivity (mill certificate, datasheet) | Starting values for the calibration |
| B | **Sample rods** of each core material (approx. 100 mm each) | Conductivity via 4-wire measurement; optionally permeability |
| C | Batch information of the core rods | Batch-to-batch variation |

## 3. Winding (per coil P, S1, S2)

| Prio | Item | Purpose | Form |
|---|---|---|---|
| A | **CNC winding program** (original file) plus designation of machine and controller | Turn-accurate distribution n(z) per layer | Text file(s) |
| A | **Winding instruction** (PDF): wire type, number of turns, layers, winding direction, start/end, insulation foils, connection | Supplement to and check of the program | PDF |
| A | Wire: nominal bare diameter, enamel grade (Grade 1/2/3), manufacturer | Layer height, DC resistance | Specification |
| A | Connection of the secondary coils (series opposition, pin assignment, 4-/5-/6-wire) | Sign, output circuit | Circuit diagram |
| B | **Measured DC resistance** per coil (nominal and actual) | Plausibility check of number of turns and layer build-up | Table |
| B | Measured outer diameter per winding | Actual layer height (winding pattern) | Table |
| C | Winding pattern (orthocyclic, random, layer by layer), wire tension | Detailed model of the turn radii | Specification |

## 4. Measurement data (measurement database)

| Prio | Item | Purpose |
|---|---|---|
| A | Characteristic curve: core position and output signal per measuring point, per serial number | Calibration and validation |
| A | Assignment of each measurement to article, winding program (version), core (material, length) and test date | Without assignment, no calibration |
| A | Measurement conditions: excitation voltage (rms), frequency, source impedance, load resistance at the output, cable | Absolute values of sensitivity and phase |
| A | Measurement chain: is the AC signal measured directly (rms value, with or without phase) or a demodulated signal from an electronics unit? Type, gain, demodulation method and phase adjustment of the electronics | Back-calculation to the secondary voltage; the evaluation also affects the measured linearity |
| A | Definition of the stated linearity (best-fit line, reference quantity) | Identical evaluation in the model |
| B | Phase output ↔ excitation, primary current, individual voltages S1 and S2, null voltage | Separates permeability from conductivity (see analysis, Section 5) |
| B | Measurements at several frequencies or excitation voltages (if available) | Frequency response, influence of excitation level |
| C | Temperature during measurement, temperature drift measurements | Temperature model |

**Format:** An export as CSV/Excel is sufficient (one row per measuring point or per measurement with
position/value columns), together with a short description of the columns. For direct
database access: schema (tables/fields) and type (SQL Server, Access, …).

## 5. Targeted additional measurements (recommendation, Prio B)

These measurements take little time but make the calibration unambiguous:

1. **Frequency response** on 3–5 reference sensors: 500 Hz … 20 kHz (approx. 10 frequencies), with the core
   in null position and at ± end of measuring range: secondary voltage with phase and primary current
   (magnitude and phase) or primary impedance.
2. **Impedances with LCR meter**: L and R of P, S1, S2, each without core and with core in
   null position, at 1, 2.5, 5 and 10 kHz.
3. **Level dependence**: characteristic curve or full-scale value at two excitation voltages (e.g. 1 V and 5 V),
   to detect non-linear material behaviour (Rayleigh region).
4. **Conductivity of the core rods** (4-wire resistance measurement, approx. 100 mm rod).
5. Optional: **self-resonance** of the secondary coils (impedance analyzer), to rule out capacitive
   effects.

## 6. Proposed reference sensors

| No. | Profile | Purpose |
|---|---|---|
| R1 | Stainless steel tube, short stroke, most common core material, many measurements | Baseline calibration |
| R2 | as R1, but different core material or different core length | Separates core influence from coil influence |
| R3 | Plastic or GRP coil former | Eddy-current influence of the tube |
| R4 | Long stroke with progressive/stepped winding | Checks the implementation of the traverse law |
| R5 | A type with available phase or frequency data | Identification permeability ↔ conductivity |

For validation we additionally need 1–2 types whose data are **not** used in the
calibration. They show whether the model truly predicts.

## 7. Data transfer

- **Small files** (winding programs, PDFs, drawings) can go into this repository under
  `data/` (private repository, please confirm) or into a SharePoint folder.
- **Measurement database**: not in Git. Better an export to a SharePoint/OneDrive folder; the
  Microsoft 365 connection of this session can read there if you grant access.
- Confidential customer data (customer names, order numbers) can be removed before the transfer.
  The model only needs article/design identifiers.
