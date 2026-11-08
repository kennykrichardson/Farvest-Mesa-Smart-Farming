"""Mesa portrayal styles for crops and farmers."""
from mesa.visualization.components import AgentPortrayalStyle
from Crop import Crop
from Farmer import Farmer
from Constants import CROP_COLORS, FARMER_COLOR


class Renderer:
    @staticmethod
    def crop_portrayal(crop):
        color = CROP_COLORS[crop.stage.name]
        return AgentPortrayalStyle(
            color=color, marker="s", size=78, zorder=2,
            edgecolors="#263238", linewidths=0.55,
        )

    @staticmethod
    def farmer_portrayal(farmer):
        # Bright, large, outlined marker ensures farmers cannot disappear behind crops.
        return AgentPortrayalStyle(
            color=FARMER_COLOR, marker="*", size=420, zorder=20,
            edgecolors="#FFFFFF", linewidths=1.8,
        )

    @staticmethod
    def portrayal(agent):
        if isinstance(agent, Farmer):
            return Renderer.farmer_portrayal(agent)
        if isinstance(agent, Crop):
            return Renderer.crop_portrayal(agent)
        return AgentPortrayalStyle()
