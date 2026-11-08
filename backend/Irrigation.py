"""Central irrigation system with accurate applied-water accounting."""
from Constants import IRRIGATION_AMOUNT
from Crop import Crop


class Irrigation:
    def __init__(self, model):
        self.model = model
        self.enabled = True
        self.water_amount = IRRIGATION_AMOUNT
        self.total_water_used = 0
        self.total_irrigations = 0

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def set_water_amount(self, amount):
        self.water_amount = max(0, int(amount))

    def irrigate_crop(self, crop):
        if not self.enabled or not crop.alive:
            return False
        applied = crop.add_water(self.water_amount)
        if applied <= 0:
            return False
        self.total_water_used += applied
        self.total_irrigations += 1
        return True

    def irrigate_crops(self, crops):
        return sum(1 for crop in crops if self.irrigate_crop(crop))

    def irrigate_all(self):
        return self.irrigate_crops(self.model.crops)

    def step(self):
        return None

    def statistics(self):
        return {
            "enabled": self.enabled, "water_amount": self.water_amount,
            "total_water_used": self.total_water_used,
            "total_irrigations": self.total_irrigations,
        }
