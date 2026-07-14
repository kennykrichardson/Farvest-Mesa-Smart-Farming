"""
Farvest Farm Manager

Coordinates the entire farm simulation.
"""

from __future__ import annotations

from Crop import Crop
from Farmer import Farmer
from Constants import AUTO_IRRIGATION_THRESHOLD


class FarmManager:
    """
    Oversees farm operations.

    Responsibilities
    ----------------
    • Track farm performance
    • Coordinate irrigation
    • Monitor crop health
    • Aggregate statistics
    """

    def __init__(self, model):
        self.model = model

        self.day = 0

        self.total_harvests = 0

        self.total_water_used = 0

        self.total_dead_crops = 0

        self.total_growth = 0

    # =====================================================
    # Collections
    # =====================================================

    @property
    def crops(self):
        return self.model.field.crops

    @property
    def farmers(self):
        return [
            agent
            for agent in self.model.schedule.farmers
            if isinstance(agent, Farmer)
        ]

    # =====================================================
    # Crop Metrics
    # =====================================================

    @property
    def living_crops(self):
        return [
            crop
            for crop in self.crops
            if crop.alive
        ]

    @property
    def dead_crops(self):
        return [
            crop
            for crop in self.crops
            if not crop.alive
        ]

    @property
    def harvestable_crops(self):
        return [
            crop
            for crop in self.crops
            if crop.ready_for_harvest
        ]

    @property
    def average_growth(self):

        if not self.crops:
            return 0.0

        return (
            sum(
                crop.growth
                for crop in self.crops
            )
            / len(self.crops)
        )

    @property
    def average_health(self):

        if not self.crops:
            return 0.0

        return (
            sum(
                crop.health
                for crop in self.crops
            )
            / len(self.crops)
        )

    @property
    def average_water(self):

        if not self.crops:
            return 0.0

        return (
            sum(
                crop.water
                for crop in self.crops
            )
            / len(self.crops)
        )

    # =====================================================
    # Monitoring
    # =====================================================

    def update_statistics(self):
        """
        Updates cumulative statistics.
        """

        self.day += 1

        self.total_dead_crops = len(
            self.dead_crops
        )

        self.total_growth += sum(
            crop.growth
            for crop in self.crops
        )

        self.total_harvests = sum(
            farmer.harvest_count
            for farmer in self.farmers
        )

        self.total_water_used = (
            self.model.irrigation.total_water_used
        )

    # =====================================================
    # Farm Policies
    # =====================================================

    def needs_irrigation(self) -> bool:
        """
        Determines whether the farm should perform a
        farm-wide irrigation cycle.
        """

        if not self.living_crops:
            return False

        average = (
            sum(crop.water for crop in self.living_crops)
            / len(self.living_crops)
        )

        return average < AUTO_IRRIGATION_THRESHOLD

    def perform_irrigation(self) -> int:
        """
        Performs automatic irrigation if necessary.

        Returns
        -------
        int
            Number of crops irrigated.
        """

        if not self.needs_irrigation():
            return 0

        return self.model.irrigation.irrigate_all()

    # =====================================================
    # Farm Health
    # =====================================================

    @property
    def health_score(self) -> float:
        """
        Returns an overall farm health score.
        """

        if not self.crops:
            return 0.0

        return (
            self.average_growth * 0.4
            + self.average_health * 0.4
            + self.average_water * 0.2
        )

    @property
    def harvest_rate(self) -> float:
        """
        Average harvests per day.
        """

        if self.day == 0:
            return 0.0

        return self.total_harvests / self.day

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self) -> dict:
        """
        Returns overall farm statistics.
        """

        return {
            "day": self.day,
            "crop_count": len(self.crops),
            "living_crops": len(self.living_crops),
            "dead_crops": len(self.dead_crops),
            "harvestable_crops": len(self.harvestable_crops),
            "average_growth": self.average_growth,
            "average_health": self.average_health,
            "average_water": self.average_water,
            "health_score": self.health_score,
            "total_harvests": self.total_harvests,
            "harvest_rate": self.harvest_rate,
            "total_water_used": self.total_water_used,
        }

    def to_dict(self) -> dict:
        """
        Serializable representation.
        """

        return self.statistics()

    # =====================================================
    # Simulation
    # =====================================================

    def step(self) -> None:
        """
        Executes one farm management cycle.
        """

        self.perform_irrigation()

        self.update_statistics()

    # =====================================================
    # Debugging
    # =====================================================

    def __repr__(self) -> str:
        return (
            f"FarmManager("
            f"day={self.day}, "
            f"crops={len(self.crops)}, "
            f"harvests={self.total_harvests}, "
            f"health={self.health_score:.1f}"
            f")"
        )