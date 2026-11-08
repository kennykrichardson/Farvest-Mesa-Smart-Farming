"""Farvest Mesa model: one model step represents one simulated day."""
from __future__ import annotations
from mesa import Model
from Constants import GRID_WIDTH, GRID_HEIGHT, INITIAL_CROPS, INITIAL_FARMERS
from Crop import Crop
from Farmer import Farmer
from Field import Field
from Weather import Weather
from Irrigation import Irrigation
from FarmManager import FarmManager
from Scheduler import FarmScheduler


class FarmModel(Model):
    def __init__(self, *, width=GRID_WIDTH, height=GRID_HEIGHT,
                 crop_count=INITIAL_CROPS, farmer_count=INITIAL_FARMERS, seed=42):
        super().__init__(seed=seed)
        self.width, self.height = int(width), int(height)
        self.seed = seed
        self.tick = 0
        self.running = True
        self.events = []
        self.field = Field(self, self.width, self.height)
        self.grid = self.field.grid
        self.weather = Weather(self)
        self.irrigation = Irrigation(self)
        self.manager = FarmManager(self)
        self.schedule = FarmScheduler(self)
        self.populate(crop_count, farmer_count)

    def record_event(self, title, message):
        self.events.insert(0, {"tick": self.tick, "title": title, "message": message})
        del self.events[30:]

    def populate(self, crops, farmers):
        for _ in range(max(0, int(crops))):
            pos = self.field.random_empty_position(self.random)
            if pos is None:
                break
            crop = Crop(self)
            self.grid.place_agent(crop, pos)
        for _ in range(max(0, int(farmers))):
            pos = self.field.random_empty_position(self.random)
            if pos is None:
                break
            farmer = Farmer(self)
            self.grid.place_agent(farmer, pos)
        self.record_event("Simulation initialized", f"{self.crop_count} crops and {self.farmer_count} farmers are on the field.")

    @property
    def crops(self):
        return self.field.crops

    @property
    def farmers(self):
        return [a for a in self.agents if isinstance(a, Farmer)]

    @property
    def crop_count(self):
        return len(self.crops)

    @property
    def farmer_count(self):
        return len(self.farmers)

    @property
    def day(self):
        return self.tick

    def step(self):
        if not self.running:
            return
        self.weather.step()
        self.schedule.step()
        self.manager.step()
        self.tick += 1

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def reset(self):
        self.__init__(width=self.width, height=self.height,
                      crop_count=self.crop_count, farmer_count=self.farmer_count,
                      seed=self.seed)

    def statistics(self):
        return {
            "tick": self.tick, "day": self.day, "running": self.running,
            "crop_count": self.crop_count, "farmer_count": self.farmer_count,
            "weather": self.weather.statistics(), "field": self.field.statistics(),
            "manager": self.manager.statistics(), "irrigation": self.irrigation.statistics(),
            "farmers": [f.statistics() for f in self.farmers],
            "events": list(self.events),
        }

    def __repr__(self):
        return f"FarmModel(day={self.day}, crops={self.crop_count}, farmers={self.farmer_count})"
