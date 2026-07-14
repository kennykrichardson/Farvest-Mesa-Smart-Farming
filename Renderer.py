"""
Farvest Renderer

Mesa 3.5.1 renderer.
"""

from __future__ import annotations

from mesa.visualization.components import AgentPortrayalStyle

from Crop import Crop, CropStage
from Farmer import Farmer


class Renderer:

    # =====================================================
    # Crop
    # =====================================================

    @staticmethod
    def crop_portrayal(crop: Crop) -> AgentPortrayalStyle:

        colors = {

            CropStage.SEED: "#8D6E63",

            CropStage.SPROUT: "#2E7D32",

            CropStage.YOUNG: "#7CB342",

            CropStage.MATURE: "#43A047",

            CropStage.READY: "#FBC02D",

        }

        return AgentPortrayalStyle(

            color=colors[crop.stage],

            marker="s",

            size=65,

            zorder=1,

            edgecolors="black",

            linewidths=0.5,

        )

    # =====================================================
    # Farmer
    # =====================================================

    @staticmethod
    def farmer_portrayal(
        farmer: Farmer,
    ) -> AgentPortrayalStyle:

        return AgentPortrayalStyle(

            color="#FF0000",

            marker="*",

            size=350,

            zorder=999,

            edgecolors="white",

            linewidths=3,

        )

    # =====================================================
    # Dispatcher
    # =====================================================

    @staticmethod
    def portrayal(agent):

        if isinstance(agent, Crop):

            return Renderer.crop_portrayal(agent)

        if isinstance(agent, Farmer):

            return Renderer.farmer_portrayal(agent)

        return AgentPortrayalStyle()

    # =====================================================
    # Legend
    # =====================================================

    @staticmethod
    def legend():

        return {

            "Farmer": "#1565C0",

            "Seed": "#8D6E63",

            "Sprout": "#2E7D32",

            "Young": "#7CB342",

            "Mature": "#43A047",

            "Ready": "#FBC02D",

        }

    # =====================================================
    # Statistics
    # =====================================================

    @staticmethod
    def statistics(model):

        return {

            "tick": model.tick,

            "day": model.day,

            "weather": model.weather.weather_name,

            "running": model.running,

        }

    # =====================================================
    # Debug
    # =====================================================

    @staticmethod
    def describe(agent):

        if isinstance(agent, Crop):

            return (
                f"Crop("
                f"{agent.stage.name}, "
                f"{agent.growth}%)"
            )

        if isinstance(agent, Farmer):

            return (
                f"Farmer("
                f"{agent.energy})"
            )

        return str(agent)