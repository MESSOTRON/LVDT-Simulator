"""Generic example designs (fictitious, NOT a MESSOTRON product).

The demo LVDT mimics the construction described for phase 1: coils wound on a
thin austenitic stainless tube, three chambers S1 | P | S2, magnetic steel
housing with end discs as flux return, solid steel core. All material values
are assumptions (see materials.LIBRARY).
"""
from __future__ import annotations

from dataclasses import replace

from .geometry import Coil, LVDTDesign, Region, uniform_section
from .materials import LIBRARY, Material

mm = 1e-3


def demo_design(core_length=36 * mm, core_material: Material | None = None,
                tube_material: Material | None = None,
                housing_material: Material | None = None,
                core_radius=3.0 * mm) -> LVDTDesign:
    core_material = core_material or LIBRARY["core_ferritic_stainless"]
    tube_material = tube_material or LIBRARY["stainless_austenitic"]
    housing_material = housing_material or LIBRARY["housing_free_cutting_steel"]

    tube_ri, tube_ro = 3.3 * mm, 3.6 * mm
    hous_ri, hous_ro, hous_z = 5.0 * mm, 6.0 * mm, 33.0 * mm
    disc_t = 1.5 * mm

    static = [
        Region("Wickelrohr", tube_ri, tube_ro, -hous_z, hous_z, tube_material),
        Region("Gehaeuse", hous_ri, hous_ro, -hous_z, hous_z, housing_material),
        Region("Deckel links", tube_ro, hous_ri, -hous_z, -hous_z + disc_t, housing_material),
        Region("Deckel rechts", tube_ro, hous_ri, hous_z - disc_t, hous_z, housing_material),
    ]
    moving = [Region("Kern", 0.0, core_radius, -core_length / 2, core_length / 2, core_material)]

    # chambers: S1 [-31, -11], P [-10, 10], S2 [11, 31] (1 mm plastic flanges)
    prim = uniform_section(tube_ro, -10 * mm, 10 * mm, 0.17 * mm, 4)
    sec1 = uniform_section(tube_ro, -31 * mm, -11 * mm, 0.095 * mm, 10)
    sec2 = uniform_section(tube_ro, 11 * mm, 31 * mm, 0.095 * mm, 10)
    coils = {
        "P": Coil("P", prim, 0.15 * mm),
        "S1": Coil("S1", sec1, 0.08 * mm),
        "S2": Coil("S2", sec2, 0.08 * mm),
    }
    return LVDTDesign("Demo-LVDT +-10 mm (fiktiv)", static, moving, coils, stroke=10 * mm,
                      notes="Generisches Beispiel, Materialwerte angenommen")


def plastic_bobbin_variant(design: LVDTDesign) -> LVDTDesign:
    """Same design, but bobbin made of plastic / GRP instead of stainless steel."""
    static = [replace(r, material=LIBRARY["plastic"]) if r.name == "Wickelrohr" else r
              for r in design.static_regions]
    return replace(design, static_regions=static, name=design.name + " / Kunststoffkoerper")
