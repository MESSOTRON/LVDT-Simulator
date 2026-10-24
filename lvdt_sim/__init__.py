"""lvdt_sim - proof-of-concept digital twin for LVDT design (MESSOTRON R&D, phase 1)."""
from .materials import MU0, Material, LIBRARY, AIR
from .geometry import (Region, WindingLayer, Coil, LVDTDesign, layers_from_moves,
                       uniform_section, progressive_section)
from .model import LVDTModel, MeshOptions
from .circuit import lvdt_output
from .analysis import characteristic, evaluate, frequency_response

__all__ = [
    "MU0", "Material", "LIBRARY", "AIR", "Region", "WindingLayer", "Coil", "LVDTDesign",
    "layers_from_moves", "uniform_section", "progressive_section", "LVDTModel",
    "MeshOptions", "lvdt_output", "characteristic", "evaluate", "frequency_response",
]
