from enumfields import Enum


class ContactType(Enum):
    WORKER = 1
    OWNER = 2
    OTHER = 3
    PRIMARYCONTACT = 4