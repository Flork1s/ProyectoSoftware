from enum import Enum

class Kind(str, Enum):
    CPU = "CPU"
    GPU = "GPU"
    RAM = "RAM"
    STORAGE = "STORAGE"
    MOTHERBOARD = "MOTHERBOARD"
    POWER_SUPPLY = "POWER_SUPPLY"
    COOLER = "COOLER"
    CASE = "CASE"