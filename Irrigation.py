"""
Farvest Irrigation

Handles irrigation across the farm.
"""

from __future__ import annotations

from Crop import Crop

from Constants import (
    IRRIGATION_AMOUNT,
)


class Irrigation:
    """
    Farm irrigation system.

    Responsibilities
    ----------------
    • Water crops
    • Track water usage
    • Provide configurable irrigation amounts
    """

    def __init__(self, model):
        self.model = model

        self.enabled = True

        self.water_amount = IRRIGATION_AMOUNT

        self.total_water_used = 0

        self.total_irrigations = 0

    # =====================================================
    # Configuration
    # =====================================================

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def set_water_amount(self, amount: int) -> None:
        """
        Sets the irrigation amount per application.
        """

        self.water_amount = max(0, amount)

    # =====================================================
    # Irrigation
    # =====================================================

    def irrigate_crop(self, crop: Crop) -> bool:
        """
        Irrigate a single crop.

        Returns
        -------
        bool
            True if water was applied.
        """

        if not self.enabled:
            return False

        if not crop.alive:
            return False

        crop.add_water(self.water_amount)

        self.total_water_used += self.water_amount

        self.total_irrigations += 1

        return True

    def irrigate_all(self) -> int:
        """
        Irrigate every crop in the farm.

        Returns
        -------
        int
            Number of crops irrigated.
        """

        if not self.enabled:
            return 0

        count = 0

        for agent in self.model.schedule.agents:

            if not isinstance(agent, Crop):
                continue

            if not agent.alive:
                continue

            agent.add_water(self.water_amount)

            self.total_water_used += self.water_amount

            self.total_irrigations += 1

            count += 1

        return count

    # =====================================================
    # Statistics
    # =====================================================

    @property
    def average_water_per_irrigation(self) -> float:

        if self.total_irrigations == 0:
            return 0.0

        return (
            self.total_water_used
            / self.total_irrigations
        )

    def statistics(self) -> dict:
        """
        Returns irrigation statistics.
        """

        return {
            "enabled": self.enabled,
            "water_amount": self.water_amount,
            "total_water_used": self.total_water_used,
            "total_irrigations": self.total_irrigations,
            "average_water_per_irrigation":
                self.average_water_per_irrigation,
        }

    def to_dict(self) -> dict:
        return self.statistics()

    # =====================================================
    # Simulation
    # =====================================================

    def step(self) -> None:
        """
        Called once per simulation tick.

        The irrigation system itself is passive.
        Farmers or managers decide when irrigation occurs.
        """

        return

    # =====================================================
    # Debugging
    # =====================================================

    def __repr__(self) -> str:
        return (
            f"Irrigation("
            f"enabled={self.enabled}, "
            f"water_amount={self.water_amount}, "
            f"water_used={self.total_water_used}, "
            f"applications={self.total_irrigations}"
            f")"
        )