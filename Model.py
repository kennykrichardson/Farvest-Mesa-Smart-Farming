"""
Farvest Model

Mesa 3.5 native simulation model.
"""

from __future__ import annotations

from mesa import Model

from Constants import (
    GRID_WIDTH,
    GRID_HEIGHT,
    INITIAL_CROPS,
    INITIAL_FARMERS,
)

from Crop import Crop
from Farmer import Farmer

from Field import Field
from Weather import Weather
from Irrigation import Irrigation
from FarmManager import FarmManager
from Scheduler import FarmScheduler


class FarmModel(Model):
    """
    Main Farvest simulation model.
    """

    def __init__(
        self,
        *,
        width: int = GRID_WIDTH,
        height: int = GRID_HEIGHT,
        crop_count: int = INITIAL_CROPS,
        farmer_count: int = INITIAL_FARMERS,
    ):

        super().__init__()

        # -------------------------------------------------
        # Configuration
        # -------------------------------------------------

        self.width = width

        self.height = height

        self.tick = 0

        self.running = True

        # -------------------------------------------------
        # Core
        # -------------------------------------------------

        self.field = Field(
            self,
            width,
            height,
        )

        # Mesa visualization uses model.grid
        self.grid = self.field.grid

        self.weather = Weather(self)

        self.irrigation = Irrigation(self)

        self.manager = FarmManager(self)

        self.schedule = FarmScheduler(self)

        # -------------------------------------------------
        # Population
        # -------------------------------------------------

        self.populate(
            crop_count,
            farmer_count,
        )

        print(f"Crops   : {self.crop_count}")
        print(f"Farmers : {self.farmer_count}")

    # =====================================================
    # Population
    # =====================================================

    def populate(
        self,
        crops: int,
        farmers: int,
    ):

        # ----------------------------
        # Create Crops
        # ----------------------------

        for _ in range(crops):

            position = self.field.random_empty_position(
                self.random
            )

            if position is None:
                break

            crop = Crop(self)

            self.grid.place_agent(
                crop,
                position,
            )

        # ----------------------------
        # Create Farmers
        # ----------------------------

        for _ in range(farmers):

            position = self.field.random_empty_position(
                self.random
           )

            if position is None:
                break

            farmer = Farmer(self)

            self.grid.place_agent(
                farmer,
                position,
            )

        # ----------------------------
        # Debug
        # ----------------------------

        print("Total agents:", len(self.agents))

    # =====================================================
    # Agent Collections
    # =====================================================

    @property
    def crops(self):
        return self.field.crops

    @property
    def farmers(self):
        return [
            agent
            for agent in self.agents
            if isinstance(agent, Farmer)
        ]

    @property
    def crop_count(self):
        return len(self.crops)

    @property
    def farmer_count(self):
        return len(self.farmers)

    # =====================================================
    # Simulation
    # =====================================================

    def step(self):

        if not self.running:
            return

        # Environment
        self.weather.step()

        # Infrastructure
        self.irrigation.step()

        # Agents
        self.schedule.step()

        # Farm Management
        self.manager.step()

        # Advance Time
        self.tick += 1

    # =====================================================
    # Simulation Control
    # =====================================================

    def start(self):

        self.running = True

    def stop(self):

        self.running = False

    def reset(self):

        width = self.width
        height = self.height

        crops = self.crop_count
        farmers = self.farmer_count

        self.__init__(
            width=width,
            height=height,
            crop_count=crops,
            farmer_count=farmers,
        )

    # =====================================================
    # Queries
    # =====================================================

    @property
    def day(self):

        return self.manager.day

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        return {

            "tick": self.tick,

            "day": self.day,

            "running": self.running,

            "crops": self.crop_count,

            "farmers": self.farmer_count,

            "weather": self.weather.statistics(),

            "field": self.field.statistics(),

            "manager": self.manager.statistics(),

            "irrigation": self.irrigation.statistics(),

        }

    def to_dict(self):

        return self.statistics()

    # =====================================================
    # Debugging
    # =====================================================

    def __repr__(self):

        return (

            f"FarmModel("

            f"tick={self.tick}, "

            f"day={self.day}, "

            f"crops={self.crop_count}, "

            f"farmers={self.farmer_count}"

            f")"

        )