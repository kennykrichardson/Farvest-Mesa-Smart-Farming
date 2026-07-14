"""
Farvest Constants
Global configuration values used throughout the simulation.
"""

# ==========================
# GRID SETTINGS
# ==========================

GRID_WIDTH = 25
GRID_HEIGHT = 25

# ==========================
# SIMULATION SETTINGS
# ==========================

INITIAL_FARMERS = 3
INITIAL_CROPS = 60

MAX_TICKS = 365

# ==========================
# CROP SETTINGS
# ==========================

MAX_GROWTH = 100

GROWTH_PER_DAY = 2

HARVEST_THRESHOLD = 100

PLANTING_COST = 1

# ==========================
# WATER SETTINGS
# ==========================

MAX_WATER = 100

WATER_CONSUMPTION = 3

IRRIGATION_AMOUNT = 8

# ==========================
# WEATHER
# ==========================

RAIN_CHANCE = 0.25

SUN_GROWTH_BONUS = 1

RAIN_GROWTH_BONUS = 2

# ==========================
# COLORS (Renderer)
# ==========================

GREEN = "#4CAF50"
YELLOW = "#FDD835"
BLUE = "#42A5F5"
BROWN = "#8D6E63"

# ==========================
# FARM SETTINGS
# ==========================

DEFAULT_CROP_HEALTH = 100
DEFAULT_CROP_WATER = MAX_WATER

DEFAULT_FARMER_ENERGY = 100

AUTO_IRRIGATION_THRESHOLD = 40

# ==========================
# WEATHER SETTINGS
# ==========================

SUNNY_TEMPERATURE = 30
CLOUDY_TEMPERATURE = 24
RAINY_TEMPERATURE = 20

CLOUD_CHANCE = 0.35

# ==========================
# RENDER SETTINGS
# ==========================

CROP_RADIUS = 0.35
FARMER_RADIUS = 0.50