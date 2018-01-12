from enumfields import Enum


class PlantStatus(Enum):
    UNDER_CONSTRUCTION = 1
    COMMISSIONING = 2
    QP1_operational = 3
    QP1_fault = 4
    QP2_operational = 5
    OPERATIONAL = 6
    FAULT = 7
    DECOMMISSIONED = 8

class TypeBiogas(Enum):
    TUBULAR = 1
    FIXED_DOME = 2
    SIM_GAS = 3


# class SizeBiogas(Enum):
#     _1M3 = 1
#     _2M3 = 2
#     _3M3 
#     _4M3
#     _5M3
#     _6M3
#     _7M3
#     _8M3
#     _9M3
#     _10M3
