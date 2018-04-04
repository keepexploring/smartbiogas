from enumfields import Enum


class ContactType(Enum):
    WORKER = 1
    PRIMARYCONTACT = 2
    OTHER = 3
    UNKNOWN = 4