"""
Farvest

Main application entry point.
"""

from __future__ import annotations

from mesa.visualization import (
    SolaraViz,
    make_space_component,
)

from Model import FarmModel
from Renderer import Renderer


# ==========================================================
# Visualization Components
# ==========================================================

space = make_space_component(
    Renderer.portrayal,
)


# ==========================================================
# Adjustable Parameters
# ==========================================================

model_params = {
    "width": 25,
    "height": 25,
    "crop_count": 60,
    "farmer_count": 3,
}


# ==========================================================
# Solara Application
# ==========================================================

page = SolaraViz(
    FarmModel(
        width=25,
        height=25,
        crop_count=60,
        farmer_count=3,
    ),
    components=[
        space,
    ],
    model_params=model_params,
    name="🌾 Farvest",
)