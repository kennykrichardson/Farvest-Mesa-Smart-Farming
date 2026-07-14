"""
Farvest Weather

Handles daily weather conditions for the farm.
"""

from __future__ import annotations

from enum import Enum, auto

from Constants import (
    RAIN_CHANCE,
    RAIN_GROWTH_BONUS,
    SUN_GROWTH_BONUS,
)
from Utils import chance


class WeatherType(Enum):
    """
    Possible weather conditions.
    """

    SUNNY = auto()
    CLOUDY = auto()
    RAINY = auto()


class Weather:
    """
    Global weather system.

    Responsibilities
    ----------------
    • Generate daily weather
    • Apply rainfall
    • Provide crop growth bonuses
    • Track weather statistics
    """

    def __init__(self, model):
        self.model = model

        self.current = WeatherType.SUNNY

        self.day = 0

        self.temperature = 25

        self.growth_bonus = SUN_GROWTH_BONUS

        self.sunny_days = 0

        self.cloudy_days = 0

        self.rainy_days = 0

    # =====================================================
    # Weather Generation
    # =====================================================

    def generate_weather(self):
        """
        Generates today's weather.
        """

        self.day += 1

        if chance(RAIN_CHANCE):
            self.current = WeatherType.RAINY

        elif chance(0.35):
            self.current = WeatherType.CLOUDY

        else:
            self.current = WeatherType.SUNNY

        self.update_conditions()

    # =====================================================
    # Weather Effects
    # =====================================================

    def update_conditions(self):
        """
        Updates temperature and growth bonus.
        """

        if self.current == WeatherType.SUNNY:

            self.temperature = 30

            self.growth_bonus = SUN_GROWTH_BONUS

            self.sunny_days += 1

            return

        if self.current == WeatherType.CLOUDY:

            self.temperature = 24

            self.growth_bonus = 0

            self.cloudy_days += 1

            return

        self.temperature = 20

        self.growth_bonus = RAIN_GROWTH_BONUS

        self.rainy_days += 1

    # =====================================================
    # Rainfall
    # =====================================================

    def apply_rainfall(self) -> None:
        """
        Automatically irrigates every living crop during rain.
        """

        if self.current != WeatherType.RAINY:
            return

        irrigation_amount = self.model.irrigation.water_amount

        for agent in self.model.schedule.agents:
            if hasattr(agent, "add_water"):
                agent.add_water(irrigation_amount)

    # =====================================================
    # Query Helpers
    # =====================================================

    @property
    def is_sunny(self) -> bool:
        return self.current == WeatherType.SUNNY

    @property
    def is_cloudy(self) -> bool:
        return self.current == WeatherType.CLOUDY

    @property
    def is_rainy(self) -> bool:
        return self.current == WeatherType.RAINY

    @property
    def weather_name(self) -> str:
        return self.current.name.title()

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self) -> dict:
        """
        Returns the current weather state.
        """

        return {
            "day": self.day,
            "weather": self.weather_name,
            "temperature": self.temperature,
            "growth_bonus": self.growth_bonus,
            "sunny_days": self.sunny_days,
            "cloudy_days": self.cloudy_days,
            "rainy_days": self.rainy_days,
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
        Advances the weather simulation by one day.
        """

        self.generate_weather()

        self.apply_rainfall()

    # =====================================================
    # Debugging
    # =====================================================

    def __repr__(self) -> str:
        return (
            f"Weather("
            f"day={self.day}, "
            f"condition={self.weather_name}, "
            f"temperature={self.temperature}°C, "
            f"growth_bonus={self.growth_bonus}"
            f")"
        )