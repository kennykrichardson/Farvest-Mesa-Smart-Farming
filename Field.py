"""
Farvest Field

Mesa 3.5 field abstraction.
"""

from __future__ import annotations

from typing import Optional

from mesa.space import MultiGrid

from Crop import Crop


class Field:
    """
    Thin wrapper around Mesa's MultiGrid.
    """

    def __init__(
        self,
        model,
        width: int,
        height: int,
    ):

        self.model = model

        self.width = width

        self.height = height

        self.grid = MultiGrid(
            width,
            height,
            torus=False,
        )

    # =====================================================
    # Placement
    # =====================================================

    def place_agent(
        self,
        agent,
        position,
    ):

        self.grid.place_agent(
            agent,
            position,
        )

    def move_agent(
        self,
        agent,
        position,
    ):

        self.grid.move_agent(
            agent,
            position,
        )

    def remove_agent(
        self,
        agent,
    ):

        self.grid.remove_agent(agent)

    # =====================================================
    # Queries
    # =====================================================

    def random_empty_position(
        self,
        rng,
    ) -> Optional[tuple[int, int]]:

        empty = [

            pos

            for _, pos in self.grid.coord_iter()

            if self.grid.is_cell_empty(pos)

        ]

        if not empty:

            return None

        return rng.choice(empty)

    def crop_at(
        self,
        position,
    ):

        for agent in self.grid.get_cell_list_contents(
            [position]
        ):

            if isinstance(agent, Crop):

                return agent

        return None

    def neighboring_crops(
        self,
        position,
        radius=1,
    ):

        return [

            a

            for a in self.grid.get_neighbors(
                position,
                moore=True,
                radius=radius,
                include_center=False,
            )

            if isinstance(a, Crop)

        ]

    # =====================================================
    # Collections
    # =====================================================

    @property
    def crops(self):

        return [

            agent

            for agent in self.model.agents

            if isinstance(agent, Crop)

        ]

    @property
    def crop_count(self):

        return len(
            self.crops
        )

    @property
    def living_crops(self):

        return [

            crop

            for crop in self.crops

            if crop.alive

        ]

    @property
    def harvestable_crops(self):

        return [

            crop

            for crop in self.crops

            if crop.ready_for_harvest

        ]

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        crops = self.crops

        if crops:

            avg_growth = sum(
                c.growth
                for c in crops
            ) / len(crops)

            avg_health = sum(
                c.health
                for c in crops
            ) / len(crops)

            avg_water = sum(
                c.water
                for c in crops
            ) / len(crops)

        else:

            avg_growth = 0

            avg_health = 0

            avg_water = 0

        return {

            "width": self.width,

            "height": self.height,

            "tiles": self.width * self.height,

            "crop_count": self.crop_count,

            "living_crops": len(
                self.living_crops
            ),

            "harvestable_crops": len(
                self.harvestable_crops
            ),

            "average_growth": avg_growth,

            "average_health": avg_health,

            "average_water": avg_water,

        }

    def to_dict(self):

        return self.statistics()

    # =====================================================
    # Python
    # =====================================================

    def __iter__(self):

        return iter(
            self.crops
        )

    def __len__(self):

        return self.crop_count

    def __repr__(self):

        return (

            f"Field("

            f"{self.width}x{self.height}, "

            f"crops={self.crop_count})"

        )