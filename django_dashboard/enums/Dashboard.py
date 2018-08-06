from enumfields import Enum


class CardTypes(Enum):
    INFO = 1
    ALERT = 2

class EntityTypes(Enum):
    BIOGASPLANT = 1
    TECHNICIAN = 2
    JOB = 3

class AlertTypes(Enum):
    CONTACT = 1 # the user needs to contact someone
    EDIT = 2 # somesort of edit need to be made to a job, technician or biogas plant
    REASSIGN = 3 # a job or tech needs to be reassigned
    FINDSUPPORT = 4 # a job needs extra support, someone needs to find additional techs and add them to the job
    DISPUTE = 5 # a customer has made a dispute, this needs to be dealt with
    LONGOUTSTANDING = 6 # there are some jobs which have been outstanding for far too long and need admin intervention
    POORFEEDBACK = 7 # a technician has received poor feedback - you might want to deal with this
    NEEDTECHICIAN = 8
    ACCEPT = 9 # a user has made a change that needs accepting by an admin
    INFO = 10
    OTHER = 11 # another action which we have not got a catagory for


