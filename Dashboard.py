"""
Farvest Dashboard

Aggregates simulation metrics for visualization.
"""

from __future__ import annotations

from Model import FarmModel


class Dashboard:
    """
    Dashboard for the Farvest simulation.

    This class is responsible only for collecting and
    organizing simulation data.
    """

    def __init__(self, model: FarmModel):
        self.model = model

    # =====================================================
    # Core
    # =====================================================

    @property
    def day(self) -> int:
        return self.model.day

    @property
    def tick(self) -> int:
        return self.model.tick

    @property
    def running(self) -> bool:
        return self.model.running

    # =====================================================
    # Environment
    # =====================================================

    @property
    def weather(self) -> str:
        return self.model.weather.weather_name

    @property
    def temperature(self) -> int:
        return self.model.weather.temperature

    # =====================================================
    # Population
    # =====================================================

    @property
    def crops(self) -> int:
        return self.model.crop_count

    @property
    def farmers(self) -> int:
        return self.model.farmer_count

    # =====================================================
    # Farm Statistics
    # =====================================================

    @property
    def harvests(self) -> int:
        return self.model.manager.total_harvests

    @property
    def average_growth(self) -> float:
        return self.model.manager.average_growth

    @property
    def average_health(self) -> float:
        return self.model.manager.average_health

    @property
    def average_water(self) -> float:
        return self.model.manager.average_water

    @property
    def health_score(self) -> float:
        return self.model.manager.health_score

    @property
    def water_used(self) -> int:
        return self.model.irrigation.total_water_used

    # =====================================================
    # Export
    # =====================================================

    def statistics(self) -> dict:
        """
        Complete dashboard snapshot.
        """

        return {
            "day": self.day,
            "tick": self.tick,
            "running": self.running,
            "weather": self.weather,
            "temperature": self.temperature,
            "crops": self.crops,
            "farmers": self.farmers,
            "harvests": self.harvests,
            "average_growth": round(
                self.average_growth,
                2,
            ),
            "average_health": round(
                self.average_health,
                2,
            ),
            "average_water": round(
                self.average_water,
                2,
            ),
            "health_score": round(
                self.health_score,
                2,
            ),
            "water_used": self.water_used,
        }

    def to_dict(self) -> dict:
        return self.statistics()

    # =====================================================
    # Console
    # =====================================================

    def print(self) -> None:
        """
        Prints a readable dashboard.
        """

        stats = self.statistics()

        print("\n========== FARVEST ==========")

        for key, value in stats.items():
            print(f"{key:20}: {value}")

        print("=============================\n")

    # =====================================================
    # Debugging
    # =====================================================

    def __repr__(self) -> str:
        return (
            f"Dashboard("
            f"day={self.day}, "
            f"weather={self.weather}, "
            f"health={self.health_score:.2f}"
            f")"
        )