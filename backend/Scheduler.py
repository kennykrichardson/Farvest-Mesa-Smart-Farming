"""Thin Mesa 3.x AgentSet adapter retained for existing modules."""
from Crop import Crop
from Farmer import Farmer


class FarmScheduler:
    def __init__(self, model):
        self.model = model
        self.steps = 0

    @property
    def agents(self):
        return list(self.model.agents)

    @property
    def crops(self):
        return [a for a in self.model.agents if isinstance(a, Crop)]

    @property
    def farmers(self):
        return [a for a in self.model.agents if isinstance(a, Farmer)]

    @property
    def crop_count(self):
        return len(self.crops)

    @property
    def farmer_count(self):
        return len(self.farmers)

    def step(self):
        self.model.agents.shuffle_do("step")
        self.steps += 1

    def statistics(self):
        return {"steps": self.steps, "agents": len(self.agents), "crops": self.crop_count, "farmers": self.farmer_count}
