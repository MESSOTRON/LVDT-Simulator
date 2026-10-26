# Phase 1 – Open Questions to MESSOTRON

_English translation of [docs/phase1/03_Rueckfragen.md](../../phase1/03_Rueckfragen.md). The German original remains authoritative._

Status: 24.10.2026 · belongs to [01_feasibility_analysis.md](01_feasibility_analysis.md)

> **Update 26.10.2026:** The public MESSOTRON documentation answers some of the
> questions. Status per question: [../phase2/01_messotron_web_research.md](../phase2/01_messotron_web_research.md),
> Section 6.

The questions are sorted by importance. Block A decides whether and how well we can calibrate
with the existing measurement database. Keywords are sufficient as answers.

## A. Measurement data and measurement conditions (decisive)

1. **Measurement chain:** Is the stored output value the raw secondary voltage (rms value)
   or the output signal of a signal conditioner (demodulated, amplified)? If
   electronics: type, gain, demodulation (phase-sensitive or rectifying),
   is the reference phase adjusted, filters?
   → *Without this information neither absolute sensitivities nor linearities can be
   compared. In the demo model the same sensor yields 0.22 %, 0.33 % or
   12.5 % linearity deviation depending on the evaluation (analysis, Section 2.6).*
2. **Excitation:** Voltage (rms), frequency, constant voltage or constant current,
   internal resistance of the source. The same for all measurements of a type?
3. **Load:** Input resistance of the measuring instrument or electronics at the secondary output, cable length.
4. **Which quantities does a data record contain?** Only position and output signal, or also
   phase, primary current, individual voltages S1/S2, null voltage, temperature?
   → *Phase or primary current make the material identification unambiguous.*
5. **Linearity definition:** Least-squares best-fit line, minimax or
   end-point line? Reference: % of full-scale value (one-sided) or % of span?
6. **Database:** System (SQL Server, Access, CSV, …), approximate number of measurements and
   sensor types. Is each measurement uniquely assigned to an article, a winding program version and
   a core (material, length), or is the assignment only via article number
   and drawing?

## B. Design and materials

7. **Core materials:** Which steel grades (material numbers) do you use, in which
   condition (drawn, ground, annealed)? How is the core attached (threaded rod,
   push rod), and is this part magnetic?
8. **Housing/cage:** Material, wall thickness, end discs/covers (material, bore).
   Are there slots, additional shielding (e.g. mu-metal) or a
   non-rotationally-symmetric cable exit?
9. **Coil former:** Stainless steel tube (grade, wall thickness, cold-worked?) or plastic/GRP
   (material, chamber dividers).
10. **Rotational symmetry:** Are there designs with distinctly non-rotationally-symmetric
    elements? We would postpone these for now.

## C. Winding and CNC programs

11. **Winding machine and controller:** Manufacturer/type and program format. Please send an
    example program with the corresponding winding instruction. I will use it to build the
    import (parser).
12. **Content of the programs:** Is every layer contained with reversal points and pitch per section,
    or are layers generated via repeat loops/parameters?
13. **Arrangement:** Is the primary coil below, above or beside the secondary coils? Are there
    chamber windings, continuous layer windings, progressive or stepped
    traverse laws, counter-wound layers?
14. **Wire and winding pattern:** Wire types (bare Ø, enamel grade), winding pattern (orthocyclic,
    random, layer by layer), insulation foils between the coils?
15. Are **measured DC resistances** per coil available (test report)?

## D. Goals and boundary conditions

16. **Priorities of the output quantities** (please rank): characteristic curve/linearity,
    sensitivity, phase, optimum frequency, primary impedance/current consumption,
    temperature behaviour, null voltage.
17. **Accuracy target:** Which deviation model ↔ measurement would be "good enough" for you,
    e.g. sensitivity ±5 %, phase ±3°, linearity profile ±0.1 % of span?
18. **Users and platform:** Who will work with the tool (development, production,
    sales)? Windows desktop application, browser interface or Python tool for
    development? Are licenses for FEM software (COMSOL, Ansys Maxwell, FEMM) available?
    They would only serve for cross-checking.
19. **Data transfer and confidentiality:** May winding programs and drawings go into this
    private GitHub repository? Should the measurement database rather be provided via
    SharePoint/OneDrive?
20. **Additional measurements:** Are an LCR meter or impedance analyzer and a test station for
    frequency sweeps available? Can we specifically re-measure 3–5 reference sensors (see
    data requirements, Section 5)?
21. **Scope:** Only LVDTs (differential transformer with three coils) or also inductive
    half-bridges or LVITs? The model covers both; only the circuit is different.
22. **Reference sensors:** Which 3–5 types do you propose (profile see
    data requirements, Section 6)?
