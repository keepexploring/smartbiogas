from enumfields import Enum


class JobStatus(Enum):
    UNASSIGNED = 1
    RESOLVING = 2
    ASSISTANCE = 3
    RESOLVED = 4
    FLAG = 5

