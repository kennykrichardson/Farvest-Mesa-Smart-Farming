"""Farm grid and spatial queries."""
from __future__ import annotations
from mesa.space import MultiGrid
from Crop import Crop


class Field:
    def __init__(self, model, width, height):
        self.model = model
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, torus=False)

    def random_empty_position(self, rng):
        empty = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if self.grid.is_cell_empty((x, y))
        ]
        return rng.choice(empty) if empty else None

    @property
    def crops(self):
        return [agent for agent in self.model.agents if isinstance(agent, Crop)]

    @property
    def living_crops(self):
        return [crop for crop in self.crops if crop.alive]

    @property
    def harvestable_crops(self):
        return [crop for crop in self.crops if crop.ready_for_harvest]

    def statistics(self):
        crops = self.crops
        count = len(crops) or 1
        return {
            "width": self.width, "height": self.height, "tiles": self.width * self.height,
            "crop_count": len(crops), "living_crops": len(self.living_crops),
            "dead_crops": len(crops) - len(self.living_crops),
            "harvestable_crops": len(self.harvestable_crops),
            "average_growth": sum(c.growth for c in crops) / count,
            "average_health": sum(c.health for c in crops) / count,
            "average_water": sum(c.water for c in crops) / count,
        }
