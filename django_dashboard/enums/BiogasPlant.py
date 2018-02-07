from enumfields import Enum


class QPStatus(Enum):
    UNDER_CONSTRUCTION = 1
    COMMISSIONING = 2
    QP1_operational = 3
    QP1_failed = 4
    QP2_operational = 5
    QP2_failed = 6
    DECOMMISSIONED = 7

class SensorStatus(Enum):
    WORKING = 1
    FAULT = 2
    UNKNOWN = 3

class TypeBiogas(Enum):
    TUBULAR = 1
    FIXED_DOME = 2
    GESISHAMBA = 3
    BIOBOLSA = 4
    OTHER = 5

class SupplierBiogas(Enum):
    CREATIVENERGIE = 1
    CAMARTEC = 2
    SIMGAS = 3
    SISTEMABIO = 4
    SNV = 5
    OTHER = 6

class FundingSourceEnum(Enum):
    PERSONAL = 1
    GRANT = 2
    GRANT_AND_PERSONAL = 3

class CurrentStatus(Enum):
    ACTIVE = 1
    FAULT = 2
    UNKNOWN = 3
    
#class VolumeBiogas(Enum):

#    > _12m3 = 20

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
