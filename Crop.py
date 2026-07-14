"""
Farvest Crop

Mesa 3.5 compatible crop agent.
"""

from __future__ import annotations

from enum import Enum, auto

from mesa import Agent

from Constants import (
    GROWTH_PER_DAY,
    HARVEST_THRESHOLD,
    MAX_GROWTH,
    MAX_WATER,
    WATER_CONSUMPTION,
)

from Utils import clamp


class CropStage(Enum):
    SEED = auto()
    SPROUT = auto()
    YOUNG = auto()
    MATURE = auto()
    READY = auto()


class Crop(Agent):

    def __init__(self, model):
        super().__init__(model)

        self.age = 0

        self.growth = 0

        self.health = 100

        self.water = MAX_WATER

        self.harvested = False

        self.alive = True

    # -------------------------------------------------

    @property
    def stage(self):

        ratio = self.growth / MAX_GROWTH

        if ratio < .20:
            return CropStage.SEED

        if ratio < .40:
            return CropStage.SPROUT

        if ratio < .70:
            return CropStage.YOUNG

        if ratio < 1:
            return CropStage.MATURE

        return CropStage.READY

    @property
    def ready_for_harvest(self):

        return self.growth >= HARVEST_THRESHOLD

    # -------------------------------------------------

    def add_water(self, amount):

        self.water = clamp(
            self.water + amount,
            0,
            MAX_WATER,
        )

    def consume_water(self):

        self.water = clamp(
            self.water - WATER_CONSUMPTION,
            0,
            MAX_WATER,
        )

    # -------------------------------------------------

    def update_health(self):

        if self.water > 30:

            self.health = clamp(
                self.health + 1,
                0,
                100,
            )

        else:

            self.health = clamp(
                self.health - 2,
                0,
                100,
            )

        if self.health == 0:

            self.alive = False

    # -------------------------------------------------

    def grow(self):

        if not self.alive:
            return

        if self.water == 0:
            return

        growth = (
            GROWTH_PER_DAY
            + self.model.weather.growth_bonus
        )

        if self.health < 50:

            growth //= 2

        self.growth = clamp(
            self.growth + growth,
            0,
            MAX_GROWTH,
        )

    # -------------------------------------------------

    def harvest(self):

        if not self.ready_for_harvest:
            return False

        self.harvested = True

        self.age = 0

        self.growth = 0

        self.health = 100

        self.water = MAX_WATER

        self.alive = True

        return True

    # -------------------------------------------------

    def step(self):

        if not self.alive:
            return

        self.age += 1

        self.consume_water()

        self.update_health()

        self.grow()

    # -------------------------------------------------

    def statistics(self):

        return {

            "id": self.unique_id,

            "position": self.pos,

            "growth": self.growth,

            "water": self.water,

            "health": self.health,

            "alive": self.alive,

            "stage": self.stage.name,

        }

    # -------------------------------------------------

    def __repr__(self):

        return (
            f"Crop("
            f"id={self.unique_id}, "
            f"stage={self.stage.name}, "
            f"growth={self.growth})"
        )