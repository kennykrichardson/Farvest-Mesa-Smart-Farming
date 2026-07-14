"""
Farvest Simulation

High-level simulation controller.
"""

from __future__ import annotations

from Constants import MAX_TICKS
from Model import FarmModel


class MesaSimulation:
    """
    Controls execution of a FarmModel.

    Responsibilities
    ----------------
    • Advance simulation ticks
    • Execute complete runs
    • Reset simulations
    • Expose simulation state
    """

    def __init__(
        self,
        model: FarmModel,
        max_ticks: int = MAX_TICKS,
    ):
        self.model = model

        self.max_ticks = max_ticks

    # =====================================================
    # State
    # =====================================================

    @property
    def tick(self) -> int:
        return self.model.tick

    @property
    def running(self) -> bool:
        return self.model.running

    @property
    def finished(self) -> bool:
        return self.tick >= self.max_ticks

    # =====================================================
    # Simulation
    # =====================================================

    def step(self) -> bool:
        """
        Executes one simulation tick.

        Returns
        -------
        bool
            False when the simulation has finished.
        """

        if self.finished:

            self.model.stop()

            return False

        self.model.step()

        return True

    def run(self) -> None:
        """
        Execute the simulation until completion.
        """

        while self.step():
            pass

    # =====================================================
    # Control
    # =====================================================

    def reset(self) -> None:
        """
        Reset the simulation.
        """

        self.model.reset()

    def start(self) -> None:
        self.model.start()

    def stop(self) -> None:
        self.model.stop()

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self) -> dict:
        """
        Returns simulation statistics.
        """

        stats = self.model.statistics()

        stats.update(
            {
                "finished": self.finished,
                "max_ticks": self.max_ticks,
            }
        )

        return stats

    def to_dict(self) -> dict:
        return self.statistics()

    # =====================================================
    # Debugging
    # =====================================================

    def __repr__(self) -> str:
        return (
            f"Simulation("
            f"tick={self.tick}, "
            f"max_ticks={self.max_ticks}, "
            f"running={self.running}"
            f")"
        )