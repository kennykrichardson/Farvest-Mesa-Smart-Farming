"""Farm-wide policies and aggregate metrics."""
from Constants import AUTO_IRRIGATION_THRESHOLD
from Crop import Crop
from Farmer import Farmer


class FarmManager:
    def __init__(self, model):
        self.model = model
        self.day = 0
        self.total_harvests = 0
        self.total_dead_crops = 0

    @property
    def crops(self):
        return self.model.crops

    @property
    def farmers(self):
        return [a for a in self.model.agents if isinstance(a, Farmer)]

    @property
    def living_crops(self):
        return [c for c in self.crops if c.alive]

    @property
    def dead_crops(self):
        return [c for c in self.crops if not c.alive]

    @property
    def harvestable_crops(self):
        return [c for c in self.crops if c.ready_for_harvest]

    def _average(self, attribute):
        items = self.living_crops
        return sum(getattr(c, attribute) for c in items) / len(items) if items else 0.0

    @property
    def average_growth(self):
        return self._average("growth")

    @property
    def average_health(self):
        return self._average("health")

    @property
    def average_water(self):
        return self._average("water")

    @property
    def health_score(self):
        return 0.4 * self.average_health + 0.35 * self.average_water + 0.25 * self.average_growth

    @property
    def harvest_rate(self):
        return self.total_harvests / max(1, self.day)

    def perform_irrigation(self):
        living = self.living_crops
        if not self.model.irrigation.enabled or not living:
            return 0
        stressed = [c for c in living if c.water < AUTO_IRRIGATION_THRESHOLD]
        if len(stressed) < max(3, int(len(living) * 0.25)):
            return 0
        return self.model.irrigation.irrigate_crops(stressed)

    def step(self):
        self.day += 1
        self.perform_irrigation()
        self.total_dead_crops = len(self.dead_crops)

    def statistics(self):
        return {
            "day": self.day, "crop_count": len(self.crops),
            "living_crops": len(self.living_crops), "dead_crops": len(self.dead_crops),
            "harvestable_crops": len(self.harvestable_crops),
            "average_growth": self.average_growth, "average_health": self.average_health,
            "average_water": self.average_water, "health_score": self.health_score,
            "total_harvests": self.total_harvests, "harvest_rate": self.harvest_rate,
        }
