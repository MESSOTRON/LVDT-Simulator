"""Structured, graded tensor-product mesh of the r-z half plane.

Every LVDT region is a rectangle, so all material interfaces can be put on
grid lines. Near conductive surfaces the radial spacing is refined to a
fraction of the skin depth. Axially the region swept by the core is meshed
uniformly so that moving the core by multiples of dz does not change the mesh
(no remeshing noise in the characteristic).
"""
from __future__ import annotations

import numpy as np


def graded_interval(a, b, h_a, h_b, h_max, growth):
    """Nodes on [a, b] whose spacing grows from h_a / h_b at the ends to at most h_max."""
    if b - a <= 0:
        return np.array([a])
    xs = np.linspace(a, b, 4001)
    h = np.minimum(np.minimum(h_a + growth * (xs - a), h_b + growth * (b - xs)), h_max)
    inv = 1.0 / h
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (inv[1:] + inv[:-1]) * np.diff(xs))])
    n = max(1, int(np.ceil(cum[-1] - 1e-9)))
    nodes = np.interp(np.linspace(0.0, cum[-1], n + 1), cum, xs)
    nodes[0], nodes[-1] = a, b
    return nodes


def build_axis(breaks, h_at_breaks, h_max_intervals, growth=0.3):
    """Concatenate graded intervals between mandatory break points."""
    breaks = np.asarray(breaks, float)
    out = [np.array([breaks[0]])]
    for i in range(len(breaks) - 1):
        seg = graded_interval(breaks[i], breaks[i + 1], h_at_breaks[i], h_at_breaks[i + 1],
                              h_max_intervals[i], growth)
        out.append(seg[1:])
    return np.concatenate(out)


def unique_sorted(values, tol=1e-9):
    v = np.sort(np.asarray(values, float))
    keep = np.concatenate([[True], np.diff(v) > tol])
    return v[keep]
