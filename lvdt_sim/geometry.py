"""Geometry and winding description of an axisymmetric LVDT.

Coordinates: r = radius, z = axial position, both in metres. z = 0 is the
electrical null of the design; the core position x is the axial offset of the
core centre from its null position.

An LVDT cross-section in the r-z half plane consists only of rectangles
(bobbin tube, chambers, housing, end discs, core), which is what makes the
structured mesh in mesh.py possible.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .materials import Material

CU_RESISTIVITY_20C = 1.724e-8  # Ohm m (annealed copper)


@dataclass
class Region:
    """Rectangular ring region r0..r1, z0..z1 filled with one material."""
    name: str
    r0: float
    r1: float
    z0: float
    z1: float
    material: Material

    def shifted(self, dz: float) -> "Region":
        return Region(self.name, self.r0, self.r1, self.z0 + dz, self.z1 + dz, self.material)


@dataclass
class WindingLayer:
    """One winding layer: radial band r_center +- thickness/2.

    segments: list of (z_start, z_end, turns). Within a segment the turns are
    distributed uniformly, i.e. a segment corresponds to one CNC traverse move
    with constant pitch. Several segments with different pitch describe a
    progressive / graded layer.
    """
    r_center: float
    thickness: float
    segments: list[tuple[float, float, float]]

    @property
    def turns(self) -> float:
        return float(sum(t for _, _, t in self.segments))


@dataclass
class Coil:
    name: str
    layers: list[WindingLayer]
    wire_d_bare: float
    resistivity: float = CU_RESISTIVITY_20C
    r_dc_override: float | None = None  # measured DC resistance, if known

    @property
    def turns(self) -> float:
        return float(sum(layer.turns for layer in self.layers))

    @property
    def r_min(self) -> float:
        return min(l.r_center - l.thickness / 2 for l in self.layers)

    @property
    def r_max(self) -> float:
        return max(l.r_center + l.thickness / 2 for l in self.layers)

    @property
    def z_min(self) -> float:
        return min(min(s[0], s[1]) for l in self.layers for s in l.segments)

    @property
    def z_max(self) -> float:
        return max(max(s[0], s[1]) for l in self.layers for s in l.segments)

    def wire_length(self) -> float:
        return float(sum(2 * np.pi * l.r_center * l.turns for l in self.layers))

    def r_dc(self) -> float:
        if self.r_dc_override is not None:
            return self.r_dc_override
        area = np.pi * self.wire_d_bare ** 2 / 4
        return self.resistivity * self.wire_length() / area


@dataclass
class LVDTDesign:
    name: str
    static_regions: list[Region]
    moving_regions: list[Region]  # z relative to the core position x
    coils: dict[str, Coil]
    stroke: float  # nominal half stroke (+-) in m
    notes: str = ""
    meta: dict = field(default_factory=dict)


# --------------------------------------------------------------------------
# Winding helpers: these are the bridge between winding instructions / CNC
# programs and the model. A CNC program is essentially a sequence of traverse
# moves "from z_a to z_b while the spindle makes N turns"; a reversal of the
# traverse direction starts a new layer.
# --------------------------------------------------------------------------

def layers_from_moves(moves, r_start, layer_pitch, wire_d_ins=None):
    """Convert traverse moves into winding layers.

    moves: iterable of (z_from, z_to, turns) in m. Consecutive moves in the
    same traverse direction belong to the same layer; a direction reversal
    starts the next layer at radius + layer_pitch.
    """
    thickness = layer_pitch if wire_d_ins is None else wire_d_ins
    layers: list[WindingLayer] = []
    current: list[tuple[float, float, float]] = []
    direction = 0
    for z_from, z_to, turns in moves:
        d = np.sign(z_to - z_from)
        if current and d != 0 and direction != 0 and d != direction:
            layers.append(current)
            current = []
        if d != 0:
            direction = d
        current.append((min(z_from, z_to), max(z_from, z_to), float(turns)))
    if current:
        layers.append(current)
    return [WindingLayer(r_start + (k + 0.5) * layer_pitch, thickness, segs)
            for k, segs in enumerate(layers)]


def uniform_section(r_start, z0, z1, wire_d_ins, n_layers, turns_per_layer=None,
                    layer_pitch=None):
    """Classic chamber winding: n_layers layers of constant pitch between z0 and z1."""
    layer_pitch = wire_d_ins if layer_pitch is None else layer_pitch
    if turns_per_layer is None:
        turns_per_layer = np.floor((z1 - z0) / wire_d_ins)
    moves = []
    for k in range(n_layers):
        a, b = (z0, z1) if k % 2 == 0 else (z1, z0)
        moves.append((a, b, turns_per_layer))
    return layers_from_moves(moves, r_start, layer_pitch, wire_d_ins)


def progressive_section(r_start, z0, z1, wire_d_ins, n_layers, density_fn, n_seg=20,
                        layer_pitch=None):
    """Graded winding: turns per metre follow density_fn(z_rel) with z_rel in [0, 1].

    Typical use: secondaries of long-stroke LVDTs whose turn density rises
    towards the coil end ("Verlegeformel").
    """
    layer_pitch = wire_d_ins if layer_pitch is None else layer_pitch
    edges = np.linspace(z0, z1, n_seg + 1)
    mids = 0.5 * (edges[1:] + edges[:-1])
    dens = np.array([density_fn((m - z0) / (z1 - z0)) for m in mids])
    turns = dens * np.diff(edges)
    moves = []
    for k in range(n_layers):
        order = range(n_seg) if k % 2 == 0 else range(n_seg - 1, -1, -1)
        for i in order:
            a, b = (edges[i], edges[i + 1]) if k % 2 == 0 else (edges[i + 1], edges[i])
            moves.append((a, b, turns[i]))
    return layers_from_moves(moves, r_start, layer_pitch, wire_d_ins)
