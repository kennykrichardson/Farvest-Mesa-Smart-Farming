"""
Farvest Farmer

Canonical Farmer implementation for Mesa 3.5.
"""

from __future__ import annotations

from typing import Optional

from mesa import Agent

from Crop import Crop
from Constants import DEFAULT_FARMER_ENERGY


class Farmer(Agent):
    """
    Intelligent farmer agent.

    Priority:

        1. Work current tile
        2. Work neighboring crops
        3. Travel to nearest crop needing work
        4. Wander
    """

    def __init__(self, model):

        super().__init__(model)

        self.energy = DEFAULT_FARMER_ENERGY

        self.harvest_count = 0

        self.water_used = 0

        self.steps_taken = 0

        self.target: Optional[Crop] = None

    # =====================================================
    # Current Tile
    # =====================================================

    @property
    def current_crops(self):

        return [

            agent

            for agent in self.model.grid.get_cell_list_contents(
                [self.pos]
            )

            if isinstance(agent, Crop)

        ]

    # =====================================================
    # Nearby Crops
    # =====================================================

    @property
    def nearby_crops(self):

        return [

            agent

            for agent in self.model.grid.get_neighbors(

                self.pos,

                moore=True,

                include_center=False,

            )

            if isinstance(agent, Crop)

        ]

    # =====================================================
    # Crops Needing Work
    # =====================================================

    @property
    def workable_crops(self):

        return [

            crop

            for crop in self.model.crops

            if (
                crop.alive
                and (
                    crop.ready_for_harvest
                    or crop.water < 50
                )
            )

        ]
    
    # =====================================================
    # Movement
    # =====================================================

    def wander(self):
        """
        Random movement when there is nothing useful to do.
        """

        neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
        )

        if not neighborhood:
            return

        destination = self.random.choice(neighborhood)

        self.model.grid.move_agent(
            self,
            destination,
        )

        self.steps_taken += 1

        self.energy = max(
            self.energy - 1,
            0,
        )

    # =====================================================
    # Target Selection
    # =====================================================

    def distance_to(self, crop: Crop) -> int:

        return (
            abs(crop.pos[0] - self.pos[0])
            +
            abs(crop.pos[1] - self.pos[1])
        )

    def choose_target(self) -> Optional[Crop]:
        """
        Select the nearest crop that actually needs work.
        """

        candidates = self.workable_crops

        if not candidates:
            return None

        return min(
            candidates,
            key=self.distance_to,
        )

    # =====================================================
    # Movement
    # =====================================================

    def move_towards(self, crop: Crop):

        if crop is None:
            return

        if crop.pos == self.pos:
            return

        x, y = self.pos

        tx, ty = crop.pos

        if tx > x:
            x += 1
        elif tx < x:
            x -= 1

        if ty > y:
            y += 1
        elif ty < y:
            y -= 1
 
        destination = (x, y)
    
        self.model.grid.move_agent(
            self,
            destination,
        )

        self.steps_taken += 1
    # =====================================================
    # Actions
    # =====================================================

    def water_crop(self, crop: Crop) -> bool:

        if crop.water >= 50:
            return False

        crop.add_water(30)

        self.water_used += 30

        return True

    def harvest_crop(self, crop: Crop) -> bool:

        if not crop.ready_for_harvest:
            return False

        if crop.harvest():

            self.harvest_count += 1

            return True

        return False

    # =====================================================
    # AI
    # =====================================================

    def perform_work(self):
        """
        Farmer AI
        """

        # -------------------------------------------------
        # Harvest current tile first
        # -------------------------------------------------

        for crop in self.current_crops:

            if not crop.alive:
                continue

            if crop.ready_for_harvest:
    
                self.harvest_crop(crop)

                self.target = None

                return

        # -------------------------------------------------
        # Water current tile
        # -------------------------------------------------

        for crop in self.current_crops:

            if not crop.alive:
                continue
    
            if crop.water < 50:

                self.water_crop(crop)

                self.target = None

                return

        # -------------------------------------------------
        # Find new target
        # -------------------------------------------------

        target = self.choose_target()

        if target is None:

            self.target = None

            self.wander()

            return

        self.target = target

        if self.pos == target.pos:

            if target.ready_for_harvest:

                self.harvest_crop(target)

            elif target.water < 50:

                self.water_crop(target)

            self.target = None

            return

        self.move_towards(target)

    # =====================================================
    # Energy
    # =====================================================

    def recover_energy(self):
        """
        Passive energy recovery.
        """

        self.energy = min(
            self.energy + 1,
            DEFAULT_FARMER_ENERGY,
        )

    # =====================================================
    # Mesa
    # =====================================================

    def step(self):
        """
        Executes one simulation tick.
        """

        if self.energy <= 0:

            self.recover_energy()

            return

        self.perform_work()

        self.recover_energy()

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def efficiency(self) -> float:
        """
        Harvests per movement step.
        """

        if self.steps_taken == 0:
            return 0.0

        return self.harvest_count / self.steps_taken

    def statistics(self):

        return {

            "id": self.unique_id,

            "position": self.pos,

            "energy": self.energy,

            "target":
                self.target.pos
                if self.target
                else None,

            "steps_taken": self.steps_taken,

            "harvest_count": self.harvest_count,

            "water_used": self.water_used,

            "efficiency": round(
                self.efficiency,
                3,
            ),

        }

    def to_dict(self):

        return self.statistics()

    # =====================================================
    # Python
    # =====================================================

    def __repr__(self):

        target = (
            self.target.pos
            if self.target
            else None
        )

        return (

            "Farmer("

            f"id={self.unique_id}, "

            f"pos={self.pos}, "

            f"energy={self.energy}, "

            f"target={target}, "

            f"harvests={self.harvest_count}, "

            f"steps={self.steps_taken}"

            ")"

        )