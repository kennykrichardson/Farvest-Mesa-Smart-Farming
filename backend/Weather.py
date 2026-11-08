"""Seeded daily weather system."""
from __future__ import annotations
from enum import Enum, auto
from Constants import (
    RAIN_CHANCE, CLOUD_CHANCE, RAIN_GROWTH_BONUS, SUN_GROWTH_BONUS,
    SUNNY_TEMPERATURE, CLOUDY_TEMPERATURE, RAINY_TEMPERATURE,
)


class WeatherType(Enum):
    SUNNY = auto()
    CLOUDY = auto()
    RAINY = auto()


class Weather:
    def __init__(self, model):
        self.model = model
        self.current = WeatherType.SUNNY
        self.day = 0
        self.temperature = SUNNY_TEMPERATURE
        self.growth_bonus = SUN_GROWTH_BONUS
        self.sunny_days = self.cloudy_days = self.rainy_days = 0

    def generate_weather(self):
        self.day += 1
        roll = self.model.random.random()
        if roll < RAIN_CHANCE:
            self.current = WeatherType.RAINY
        elif roll < RAIN_CHANCE + CLOUD_CHANCE:
            self.current = WeatherType.CLOUDY
        else:
            self.current = WeatherType.SUNNY
        self.update_conditions()

    def update_conditions(self):
        if self.current is WeatherType.SUNNY:
            self.temperature, self.growth_bonus = SUNNY_TEMPERATURE, SUN_GROWTH_BONUS
            self.sunny_days += 1
        elif self.current is WeatherType.CLOUDY:
            self.temperature, self.growth_bonus = CLOUDY_TEMPERATURE, 0
            self.cloudy_days += 1
        else:
            self.temperature, self.growth_bonus = RAINY_TEMPERATURE, RAIN_GROWTH_BONUS
            self.rainy_days += 1

    def apply_rainfall(self):
        if self.current is WeatherType.RAINY:
            for crop in self.model.crops:
                if crop.alive:
                    crop.add_water(self.model.irrigation.water_amount)

    @property
    def weather_name(self):
        return self.current.name.title()

    @property
    def is_rainy(self):
        return self.current is WeatherType.RAINY

    def step(self):
        self.generate_weather()
        self.apply_rainfall()

    def statistics(self):
        return {
            "day": self.day, "weather": self.weather_name,
            "temperature": self.temperature, "growth_bonus": self.growth_bonus,
            "sunny_days": self.sunny_days, "cloudy_days": self.cloudy_days,
            "rainy_days": self.rainy_days,
        }
