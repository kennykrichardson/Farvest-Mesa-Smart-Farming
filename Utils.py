"""
Utility functions used across Farvest.
"""

import random


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def chance(probability):
    """
    Returns True with the given probability.

    Example:
        chance(0.25)
    """
    return random.random() < probability


def random_position(model):
    """
    Returns a random position using Mesa's seeded RNG.
    """

    return (
        model.random.randrange(model.grid.width),
        model.random.randrange(model.grid.height),
    )

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])