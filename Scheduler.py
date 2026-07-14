"""
Farvest Scheduler

Mesa 3.5 compatible scheduler.
"""

from __future__ import annotations

from Crop import Crop
from Farmer import Farmer


class FarmScheduler:
    """
    Lightweight scheduler compatible with Mesa 3.x.

    Mesa itself owns the AgentSet.

    This class simply provides a clean interface
    for Farvest.
    """

    def __init__(self, model):

        self.model = model

        self.steps = 0

        self.time = 0

    # =====================================================
    # Registration
    # =====================================================

    def add(self, agent):

        # Mesa 3 automatically registers agents
        # when Agent.__init__ is called.

        return

    def remove(self, agent):

        agent.remove()

    # =====================================================
    # Collections
    # =====================================================

    @property
    def agents(self):

        return list(self.model.agents)

    @property
    def crops(self):

        return [
            a
            for a in self.model.agents
            if isinstance(a, Crop)
        ]

    @property
    def farmers(self):

        return [
            a
            for a in self.model.agents
            if isinstance(a, Farmer)
        ]

    # =====================================================
    # Counts
    # =====================================================

    @property
    def crop_count(self):

        return len(self.crops)

    @property
    def farmer_count(self):

        return len(self.farmers)

    @property
    def total_agents(self):

        return len(self.agents)

    # =====================================================
    # Queries
    # =====================================================

    def living_crops(self):

        return [
            crop
            for crop in self.crops
            if crop.alive
        ]

    def harvestable_crops(self):

        return [
            crop
            for crop in self.crops
            if crop.ready_for_harvest
        ]

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {
            "steps": self.steps,
            "time": self.time,
            "agents": self.total_agents,
            "crops": self.crop_count,
            "farmers": self.farmer_count,
            "living_crops": len(self.living_crops()),
            "harvestable_crops": len(
                self.harvestable_crops()
            ),
        }

    def to_dict(self):

        return self.statistics()

    # =====================================================
    # Simulation
    # =====================================================

    def step(self):

        self.model.agents.shuffle_do("step")

        self.steps += 1

        self.time += 1

    # =====================================================
    # Debug
    # =====================================================

    def __repr__(self):

        return (
            f"FarmScheduler("
            f"agents={self.total_agents}, "
            f"steps={self.steps})"
        )