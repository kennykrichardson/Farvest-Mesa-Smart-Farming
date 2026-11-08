"""Small deterministic helpers used throughout Farvest."""
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
