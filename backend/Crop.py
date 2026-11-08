"""Crop agent and crop lifecycle for Farvest."""
from __future__ import annotations
from enum import Enum, auto
from mesa import Agent
from Constants import (
    DEFAULT_CROP_HEALTH, DEFAULT_CROP_WATER, GROWTH_PER_DAY,
    HARVEST_THRESHOLD, MAX_GROWTH, MAX_WATER, WATER_CONSUMPTION,
)
from Utils import clamp


class CropStage(Enum):
    SEED = auto()
    SPROUT = auto()
    YOUNG = auto()
    MATURE = auto()
    READY = auto()
    DEAD = auto()


class Crop(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.age = 0
        self.growth = 0
        self.health = DEFAULT_CROP_HEALTH
        self.water = DEFAULT_CROP_WATER
        self.alive = True
        self.harvest_count = 0

    @property
    def stage(self):
        if not self.alive:
            return CropStage.DEAD
        if self.growth < 15:
            return CropStage.SEED
        if self.growth < 35:
            return CropStage.SPROUT
        if self.growth < 65:
            return CropStage.YOUNG
        if self.growth < HARVEST_THRESHOLD:
            return CropStage.MATURE
        return CropStage.READY

    @property
    def ready_for_harvest(self):
        return self.alive and self.growth >= HARVEST_THRESHOLD

    @property
    def needs_water(self):
        return self.alive and self.water <= 45

    def add_water(self, amount):
        before = self.water
        self.water = clamp(self.water + max(0, amount), 0, MAX_WATER)
        return self.water - before

    def consume_water(self):
        self.water = clamp(self.water - WATER_CONSUMPTION, 0, MAX_WATER)

    def update_health(self):
        if self.water < 12:
            self.health = clamp(self.health - 4, 0, 100)
        elif self.water < 30:
            self.health = clamp(self.health - 1, 0, 100)
        else:
            self.health = clamp(self.health + 1, 0, 100)
        if self.health <= 0:
            self.alive = False
            self.model.record_event("Crop lost", f"Crop #{self.unique_id} died from water stress.")

    def grow(self):
        if not self.alive or self.water < 10 or self.health < 15:
            return
        weather_bonus = self.model.weather.growth_bonus
        health_factor = 0.5 if self.health < 45 else 1.0
        self.growth = clamp(self.growth + int((GROWTH_PER_DAY + weather_bonus) * health_factor), 0, MAX_GROWTH)

    def harvest(self):
        if not self.ready_for_harvest:
            return False
        self.harvest_count += 1
        self.model.manager.total_harvests += 1
        self.growth = 0
        self.age = 0
        self.health = DEFAULT_CROP_HEALTH
        self.water = max(65, self.water)
        self.model.record_event("Harvest completed", f"Crop #{self.unique_id} was harvested and replanted.")
        return True

    def step(self):
        if not self.alive:
            return
        self.age += 1
        self.consume_water()
        self.update_health()
        self.grow()

    def statistics(self):
        return {
            "id": self.unique_id, "position": self.pos, "growth": self.growth,
            "water": self.water, "health": self.health, "alive": self.alive,
            "stage": self.stage.name, "age": self.age,
        }

    def __repr__(self):
        return f"Crop(id={self.unique_id}, stage={self.stage.name}, growth={self.growth})"
