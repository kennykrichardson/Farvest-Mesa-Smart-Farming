"""Task-oriented farmer agent for Mesa 3.5."""
from __future__ import annotations
from mesa import Agent
from Constants import (
    DEFAULT_FARMER_ENERGY, FARMER_ENERGY_COST, FARMER_REST_THRESHOLD,
    FARMER_WATER_AMOUNT,
)
from Crop import Crop
from Utils import manhattan_distance


class Farmer(Agent):
    """A farmer that selects urgent crops, moves toward them, and acts."""

    def __init__(self, model):
        super().__init__(model)
        self.energy = DEFAULT_FARMER_ENERGY
        self.harvest_count = 0
        self.water_used = 0
        self.steps_taken = 0
        self.target_id = None
        self.current_task = "Idle"
        self.actions_completed = 0

    @property
    def target(self):
        if self.target_id is None:
            return None
        return next((c for c in self.model.crops if c.unique_id == self.target_id), None)

    def _task_score(self, crop):
        # Harvesting has priority; severe water stress is next.
        if crop.ready_for_harvest:
            urgency = 1000
        elif crop.water < 15:
            urgency = 800 + (15 - crop.water) * 5
        elif crop.water < 45:
            urgency = 300 + (45 - crop.water) * 2
        else:
            return None
        return urgency - manhattan_distance(self.pos, crop.pos) * 3

    def choose_target(self):
        candidates = [c for c in self.model.crops if c.alive and (c.ready_for_harvest or c.needs_water)]
        if not candidates:
            return None
        # Stable tie-breaking avoids agents oscillating between equally useful crops.
        return max(candidates, key=lambda c: (self._task_score(c), -c.unique_id))

    def _move_one_step(self, target):
        x, y = self.pos
        tx, ty = target.pos
        options = []
        if x != tx:
            options.append((x + (1 if tx > x else -1), y))
        if y != ty:
            options.append((x, y + (1 if ty > y else -1)))
        if not options:
            return False
        # Choose the option that reduces Manhattan distance; use seeded model RNG for ties.
        best_distance = min(manhattan_distance(p, target.pos) for p in options)
        best = [p for p in options if manhattan_distance(p, target.pos) == best_distance]
        destination = self.random.choice(best)
        self.model.grid.move_agent(self, destination)
        self.steps_taken += 1
        self._spend_energy()
        self.current_task = f"Travelling to crop #{target.unique_id}"
        return True

    def _spend_energy(self):
        self.energy = max(0, self.energy - FARMER_ENERGY_COST)

    def _act_on(self, crop):
        if crop.ready_for_harvest:
            if crop.harvest():
                self.harvest_count += 1
                self.actions_completed += 1
                self.current_task = f"Harvested crop #{crop.unique_id}"
                self.model.record_event("Harvest", f"Farmer #{self.unique_id} harvested crop #{crop.unique_id}.")
                self._spend_energy()
                return True
        if crop.needs_water:
            amount = self.model.irrigation.irrigate_crop(crop)
            amount = FARMER_WATER_AMOUNT if amount else 0
            if amount > 0:
                self.water_used += amount
                self.actions_completed += 1
                self.current_task = f"Watered crop #{crop.unique_id}"
                self.model.record_event("Irrigation", f"Farmer #{self.unique_id} watered crop #{crop.unique_id}.")
                self._spend_energy()
                return True
        return False

    def step(self):
        if self.energy <= FARMER_REST_THRESHOLD:
            self.energy = min(DEFAULT_FARMER_ENERGY, self.energy + 8)
            self.current_task = "Resting"
            return

        target = self.choose_target()
        if target is None:
            self.target_id = None
            self.current_task = "Monitoring field"
            self.energy = min(DEFAULT_FARMER_ENERGY, self.energy + 2)
            return

        self.target_id = target.unique_id
        if self.pos == target.pos:
            self._act_on(target)
        else:
            self._move_one_step(target)

    @property
    def efficiency(self):
        return self.actions_completed / max(1, self.steps_taken)

    def statistics(self):
        target = self.target
        return {
            "id": self.unique_id, "position": self.pos, "energy": self.energy,
            "target": target.unique_id if target else None,
            "task": self.current_task, "steps_taken": self.steps_taken,
            "harvest_count": self.harvest_count, "water_used": self.water_used,
            "efficiency": round(self.efficiency, 3),
        }

    def __repr__(self):
        return f"Farmer(id={self.unique_id}, pos={self.pos}, task={self.current_task!r})"
