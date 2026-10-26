# Phase 2 – Public MESSOTRON Data: What They Provide for the Digital Twin

_English translation of [docs/phase2/01_Webrecherche_messotron.md](../../phase2/01_Webrecherche_messotron.md). The German original remains authoritative._

Status: 26.10.2026 · belongs to [../phase1/02_data_requirements.md](../phase1/02_data_requirements.md)
and [../phase1/03_open_questions.md](../phase1/03_open_questions.md)
Data: [messotron_web_daten.json](../../phase2/messotron_web_daten.json) (23 sensor types or series, 5 signal conditioners, each with
source and reliability) · Calculation: [phase_check_results.json](../../phase2/phase_check_results.json)

---

## 0. Summary of results

The website (messotron.com / messotron.de: product pages, datasheets, operating manuals,
technical notes, knowledge base) answers some of the open questions. As expected, it does not
describe the internal construction of the sensors.

**What the website provides:**

- **Measurement chain of the MESSOTRON electronics** (open questions A.1–A.3): The carrier-frequency signal conditioners MBI 46.x
  excite with **approx. 2 V rms sine at 5 kHz** (max. 12 mA rms), have **approx. 200 kΩ
  input resistance** and demodulate **phase-sensitively with phase adjustment**. The phase
  is set so that the output is **maximum at approx. 3/4 of the rated stroke**.
- **Definitions** (A.5): Sensitivity and rated output in the datasheets are determined
  **phase-independently** (magnitude) and have **±10 %
  tolerance** for non-calibrated sensors. The linearity deviation is the largest deviation from the nominal straight line,
  **referred to the entire measuring range** (FSO).
- **Materials** (B.7, B.8): Housing made of **stainless steel**, core made of **magnetic
  stainless steel**, core extensions **non-magnetic**. Some cores are **PTFE-coated**.
- **Characteristics of 23 types**: housing Ø 5–25 mm, core Ø 2–5.6 mm, strokes from 8 mm to 1000 mm,
  standard frequency 5 kHz (option 10 kHz, individual types 3 kHz or 10 kHz standard),
  rated output of long types 80–175 mV/V, primary impedances 50 Ω to > 400 Ω.
- **Core and coil are matched pairs**: plunger cores are not freely interchangeable; each sensor
  comes with a test report.

**Most important finding for the model:** For its LVDTs, MESSOTRON states a phase between
excitation and output voltage of **typically 1–20°**. The demo LVDT from Phase 1, with the
assumed material values at 5 kHz, is at **−75°**. A recalculation (Section 5.1) shows:
the housing material alone does not explain the difference. The assumed
eddy-current losses in coil former, core and housing are together considerably too high, or the
construction of real sensors differs from the demo. The phase is therefore a strong lever for
the calibration, and the design of the coil former becomes the most important open question.

**What is missing** (as expected, internal): coil former, wall thicknesses, chamber layout,
numbers of turns, wire types, material numbers, winding programs, test station description and
the measurement database. Block A of the open questions remains open for the **test station measurements**, because
the website describes only the amplifiers, not the test station.

## 1. Approach and reliability

- Direct retrieval of www.messotron.de and www.messotron.com was blocked from the working environment
  by the network policy. The data therefore come from **excerpts of a
  web search** across these pages and PDFs. The search was restricted to the MESSOTRON domains.
- Every value in [messotron_web_daten.json](../../phase2/messotron_web_daten.json) carries source and
  reliability: **high** (identical several times or quoted verbatim), **medium** (one excerpt,
  plausible), **low** (table shifted in the excerpt or contradictory).
- Known contradictions: DTU (5 mm or 16 mm housing), DGO (core 3/5 mm in one
  variant), DPF (320 bar or < 50 bar), DFI (320 or 450 bar), DU (assignment of the
  rated outputs to the body lengths).
- **Before use in the calibration** the values must be checked against the original PDFs.
  To do so it is sufficient to allow the domains messotron.com and messotron.de in the
  network settings of the environment or to place the PDFs under `data/`.

## 2. Measurement chain and definitions according to MESSOTRON

| Topic | MESSOTRON statement | Source | Significance for the model |
|---|---|---|---|
| Excitation | MBI 46.31 / 46.12 / 46.13 / 46.51: approx. 2 V rms, sine, 5 kHz ±5 % (option 1–20 kHz), max. 12 mA rms. Sensor datasheets: 1–5 V rms | Operating manuals MBI 46.31, 46.13; datasheet MBI 46.51 | Standard case U₀ = 2 V, f = 5 kHz. Design limit \|Z_P\| ≳ 2 V / 12 mA ≈ 170 Ω |
| Load | Secondary input resistance approx. 200 kΩ | MBI 46.12, 46.13, 46.31 | R_load = 200 kΩ instead of 100 kΩ in the demo (minor influence, Section 5.1) |
| Sensor range of the electronics | Input impedance 100–1000 Ω; rated output 20–600 mV/V (46.31) or 130–600 mV/V (46.12/46.13, option /V6 for < 130 mV/V) | ditto | Target range for designs |
| Demodulation | Oscillator excites and provides the reference, ratiometric evaluation. The phase trimmer "shifts the evaluation of the measurement voltage along the time axis" | Knowledge base carrier-frequency signal conditioners; MBI 46.13 | **Phase-sensitive (synchronous) demodulation** with adjustable reference phase |
| Phase adjustment | Core at approx. 3/4 of rated stroke (46.31: "shortly before the end of the measuring range"), set the output to maximum with P_Ph, then check the zero point. Coarse step via capacitors C1/C2 | Technical notes; MBI 46.31 | Reference phase = phase of U_out at 0.75·x_rated. This corresponds roughly to row 2 of the table in analysis 2.6 |
| Zero point | Symmetrical sensors: centre. Adjust to 0 V with the **plunger core removed**, then fix the core so that 0 V is maintained. Alternatively: position at which normal and swapped excitation leads give the same value | Technical notes | x = 0 is defined electrically (output null), not geometrically |
| Phase shift | LVDT typically **1–20°**, depending on coil type and frequency; cable capacitance contributes. LVIT (differential choke) practically no phase | Technical notes (DE/EN) | Plausibility limit for the calibration (Section 5.1) |
| Sensitivity, rated output | U_out/U_excitation per mm or at the end of the rated stroke. Determined **phase-independently**, **±10 %** for non-calibrated sensors; calibrated sensors e.g. 80 mV/V regardless of stroke. Dependent on frequency, usually 3, 5 or 10 kHz | Technical notes; knowledge base | Comparison with datasheet via \|U_out(x_rated)\|/U₀ at 5 kHz; ±10 % is only sufficient as a plausibility check |
| Linearity | Largest deviation between nominal characteristic (straight line) and real characteristic curve, referred to the entire measuring range (FSO). Optimum adjustment takes the linearity error into account via zero point and gain (example: error reduced to 0.32 %) | MBI 46.51.39, MBI 46.32 | Reference = span, as `nonlinearity_pct_span` in the model. **Open:** best-fit line or line from zero and end-point adjustment? |
| Connection | LVDT 4-wire as standard, several series optionally 5-wire (centre tap) or 6-wire (separate secondary coils); LVIT 3-wire | Technical Guidelines; MBI 46.31 | Individual voltages S1/S2 can only be measured on 5-/6-wire types |
| Pairing | Displacement transducer and plunger core are matched, not freely interchangeable. On replacement, recalibrate and issue a new **test report** | Technical notes | Every measurement needs the assignment to the specific core |
| Adjustment conditions | In the installed state, at operating temperature, with the amplifier warmed up | Technical notes | Record the measurement conditions in the database |

## 3. Designs and characteristics

Extract of the LVDT types with usable figures (complete in the JSON file):

| Type | Housing Ø | Core Ø | Stroke | f | Rated output / sensitivity | Z_P | Reliability |
|---|---|---|---|---|---|---|---|
| DM | 20 mm, installation length 35 mm | – (core 3 g) | ±8 mm (extended ±10) | 5 kHz | 40 mV/V/mm | > 400 Ω | high |
| DTU | 5 mm, length 42 mm | – | 8 mm | 5 kHz | 24 mV/V | ≈ 50 Ω | medium |
| DTL | 12 mm h9 | 3 mm | 50 / 100 / 200 mm | 5 kHz | 133 / 135 / 125 mV/V | – | high |
| DUH | 16 mm | 5.6 mm incl. PTFE | ±25 … ±250 mm | 5 kHz | 107 / 140 / 163 / 175 / 160 / 162 mV/V | – | medium |
| DUR | – | – | ±12.5 … ±500 mm | 5 kHz | 100 … 175 mV/V | – | medium |
| DU | 14 mm | 2 / 3 mm (probably core) | 15 … 1000 mm | 5 / 10 kHz | approx. 80–175 mV/V (5 kHz), approx. 100–250 mV/V (10 kHz) | – | low |
| DLH | 12 mm | 3.6 mm incl. PTFE | up to 500 mm | – | – | – | medium |
| DGO | 20 mm | – | ±12.5 … ±150 mm | 5 kHz (10) | – | – | high |
| DPL | 12 mm | – | ±25 … ±200 mm | **10 kHz** (5) | – | – | medium |

LVIT types (half-bridge): WLG (12 mm, rated output 80 mV/V, 5–10 kHz), WLH (60 … 1.4 mV/V/mm),
WLR (12 mm), **WLU** (16 mm stainless steel, coil impedance 600 ±100 Ω with core, **3 kHz**,
rated output approx. 314–340 mV/V). The **WP** series (long stroke up to 1000 mm) works with a
sleeve armature based on the eddy-current principle; the second half-bridge coil is emulated
electronically.

Notable:

- The **rated outputs of long types at 5 kHz are close together** (DTL, DUH, DUR, DU:
  roughly 100–175 mV/V). This is a first, rough check for length series in the model.
- For the DU, the datasheet states **higher rated outputs at 10 kHz than at 5 kHz** (excerpt
  uncertain). This fits a low-loss design with a resistance-dominated primary coil.
  In the demo LVDT, by contrast, the sensitivity drops above roughly 200–300 Hz
  (analysis 4.3). This also suggests that the demo losses are set too high.
- Core Ø in the datasheets partly includes the **PTFE coating** (DUH 5.6 mm,
  DLH 3.6 mm). For the model, the steel diameter is what counts.

## 4. Materials

| Part | Statement | Source |
|---|---|---|
| Housing | "high-quality stainless steel"; also aluminium for the electrical connection | Technical notes; DAA, DPF, DFI, WLU |
| Core | "magnetic stainless steel" (DM). In general: magnetizable, AC-magnetic material (mu-metal, ferrite, soft iron mentioned) | Datasheet DM; knowledge base |
| Core extension | Non-magnetic material | Datasheet DM |
| Core surface | PTFE coating (DUH, DLH) | Datasheets DUH, DLH |
| Manufacturing | Centreless cylindrical grinding, turning, CNC turning and milling in-house | Services / manufacturing |

Consequence for the model: Phase 1 assumed free-cutting steel (1.0718, σ = 5 MS/m) for the housing.
According to the website, the housing is made of stainless steel. It is still open whether it is **ferritic**
(magnetic return path, σ ≈ 1.4–1.7 MS/m) or **austenitic** (non-magnetic, no
return path). This changes sensitivity, primary impedance and phase considerably (Section 5.1).
The material library in `lvdt_sim/materials.py` remains unchanged until this is clarified.

## 5. Consequences for the model and Phase 2

### 5.1 Plausibility check of the phase

Calculation with [examples/phase2_phase_check.py](../../../examples/phase2_phase_check.py): demo LVDT
from Phase 1 (core 50 mm) under MBI conditions (2 V, 5 kHz, 200 kΩ). The material values are
still **assumptions**; the ferritic stainless steel is set to µr = 300, σ = 1.6 MS/m.

| Variant (5 kHz, ±5 mm) | Sensitivity | Phase | \|Z_P\| at null | I_P at 2 V |
|---|---|---|---|---|
| Phase 1 baseline (free-cutting steel housing, stainless steel tube) | 54.9 mV/V/mm | −75.0° | 164 Ω | 12.2 mA |
| Baseline with plastic former | 71.4 mV/V/mm | −47.0° | 210 Ω | 9.5 mA |
| Housing ferritic stainless steel, stainless steel tube | 69.5 mV/V/mm | −71.2° | 189 Ω | 10.6 mA |
| Housing austenitic (non-magnetic), stainless steel tube | 97.9 mV/V/mm | −70.1° | 113 Ω | 17.8 mA |
| Housing ferritic stainless steel, plastic former | 92.1 mV/V/mm | −40.0° | 258 Ω | 7.8 mA |
| … ditto, core without eddy currents | 145.1 mV/V/mm | −21.9° | 422 Ω | 4.7 mA |
| … ditto, housing without eddy currents | 124.1 mV/V/mm | −26.7° | 347 Ω | 5.8 mA |
| … ditto, core and housing without eddy currents | 200.0 mV/V/mm | −2.4° | 680 Ω | 2.9 mA |

Findings:

- The **housing material alone** changes the phase only from −75° to −70° to −71°. In the demo,
  the largest single contribution comes from the **stainless steel coil former tube** (around 30°), followed by core
  and housing (approx. 13–18° each).
- The demo construction only reaches the 1–20° range when the losses in tube, core **and**
  housing together are considerably smaller than assumed. Possible causes in real
  sensors: plastic or thin-walled coil former, smaller core diameters
  (2–5 mm instead of 6 mm in the demo), different material values, different proportions.
- Consequence: The absolute phase values from Phase 1 (−39° to −75°) are **not** transferable to
  MESSOTRON sensors. In return, the real phase is a **sensitive
  calibration value**, and the design of the coil former (open question B.9) becomes the most important
  open design question.

### 5.2 Measurement conditions and evaluation in the model

1. **Standard conditions** for recalculations: U₀ = 2 V rms, f = 5 kHz, R_load = 200 kΩ,
   as long as the test station data do not say otherwise.
2. **Design limit**: \|Z_P\| at the excitation frequency at least ≈ 170 Ω (2 V / 12 mA), target
   100–1000 Ω and rated output 20–600 mV/V (range of the MBI amplifiers). The demo LVDT is
   just below this at 164 Ω.
3. **Excitation level**: At 2 V instead of 3 V the field strength in the core drops to about 2/3, i.e. to
   around 75–80 A/m rms (analysis 2.5). This is still within the Rayleigh region; measuring at
   two excitation voltages remains worthwhile.
4. **Evaluation like the MBI amplifiers** (not yet implemented): reference phase = phase of U_out
   at 0.75·x_rated, zero point from the output null. `lvdt_sim.analysis.evaluate` currently determines the
   reference phase from the complex best-fit line. A variant with a fixed
   reference phase is a small extension.
5. **Datasheet comparison** via the magnitude \|U_out(x_rated)\|/U₀ (phase-independent, ±10 %).
6. **Add the LVIT half-bridge**: The W series is a large part of the product range.
   `lvdt_sim/circuit.py` so far only knows the LVDT circuit. The field calculation remains
   the same. We postpone the WP series (sleeve armature, electronic half-bridge).

### 5.3 Consequences for the data transfer

- **Core-coil pairing**: The database must assign each measurement to the specific core
  (material, length, diameter without coating).
- **Test report**: One exists for each sensor. Its content (points, phase,
  conditions) is the most likely route to Block A of the open questions.
- **Two frequencies**: Several types are available for 5 and 10 kHz. Measurements of the same design
  at both frequencies help somewhat in separating µr and σ. Both, however, lie in the
  region of strong skin effect; direct σ measurement on the core rod remains the robust route.

## 6. Status of the open questions after the web research

Legend: ✔ answered · ◐ partially · ○ open (internal)

| No. | Topic | Status | What the website says / what remains open |
|---|---|---|---|
| A.1 | Measurement chain | ◐ | MBI amplifiers: phase-sensitive, phase set to maximum at 3/4 stroke; datasheet values = magnitude. **Open:** What does the test station use to measure for the database? |
| A.2 | Excitation | ◐ | Electronics 2 V rms / 5 kHz sine; sensors 1–5 V rms, 5 kHz standard, 10 kHz option. **Open:** test station values, source impedance |
| A.3 | Load | ◐ | MBI ≈ 200 kΩ. **Open:** test station, cable |
| A.4 | Content of a data record | ◐ | Test report per sensor; 4-wire standard (S1/S2 individually only with 5/6-wire). **Open:** fields of the report |
| A.5 | Linearity definition | ◐ | Reference = entire measuring range. **Open:** best-fit line or zero/end-point line |
| A.6 | Database | ○ | – |
| B.7 | Core materials | ◐ | Magnetic stainless steel, extension non-magnetic, PTFE coating, core Ø 2–5.6 mm. **Open:** material numbers, condition |
| B.8 | Housing | ◐ | Stainless steel, Ø 5–25 mm. **Open:** ferritic or austenitic, wall thickness, end discs |
| B.9 | Coil former | ○ | Nothing public; according to 5.1 the most important open question |
| B.10 | Rotational symmetry | ○ | – |
| C.11–15 | Winding, CNC programs | ○ | Nothing public (expected) |
| D.16 | Priorities | ○ | – |
| D.17 | Accuracy target | ◐ | Reference: datasheet ±10 % sensitivity, linearity classes 0.5 / 0.25 / 0.1 % FSO. The model target of ±3–5 % is considerably tighter |
| D.18–20 | Users, data transfer, additional measurements | ○ | – |
| D.21 | Scope LVDT / LVIT | ◐ | Product range includes LVDT (D series), LVIT half-bridges (W series) and WP long-stroke. **Open:** desired scope |
| D.22 | Reference sensors | ◐ | Candidates based on public data: **DM** (many characteristics, compact), **DUH** or **DTL** (length series with rated outputs), **WLU** or **WLG** for LVIT. The final decision depends on the internal data situation |

## 7. Next steps

1. Check values against the original PDFs: allow the domains messotron.com/.de in the environment
   or place the PDFs under `data/`. Priority goes to the values marked "low"
   and to the types that could become reference sensors.
2. Answer the remaining questions, above all: **test station measurement chain** (A.1–A.3), **coil former**
   (B.9), **housing steel ferritic or austenitic** (B.8), **linearity line** (A.5),
   **content of the test report** (A.4).
3. Optionally already now in the code: evaluation with fixed reference phase (MBI method) and
   standard load 200 kΩ; circuit for LVIT half-bridges.
