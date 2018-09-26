
from django_dashboard.models import ( Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs, Abandoned,
                                    CardTemplate, Card, PendingAction, IndicatorsTemplate, IndicatorObjects )

class PendingJobs():
    company = 'ALL'
    name = 'unassigned_pending_jobs'
    title = 'View Unassigned Pending Jobs'
    description = 'Get all the jobs which have been rejected by technician or abandoned'
    template_id = ''
    card_type = 'INFO' # options: INFO or ALERT
    entity_type = 'JOB' # options: BIOGASPLANT, TECHNICIAN, JOB
    image = ''
    created = ''
    updated = ''

    def __init__(self):
        # create cards on init of new user - could just be a function in the class
        pass

    @classmethod
    def build_template(cls):
        # we build the template cards and add them for a user
        CardTemplate()

    def update_unassigned_pending_job_cards(self, uob, perm, company):
        if uob.is_superuser or perm.is_global_admin():
            try:
                pending_jobs = PendingJobs.objects.filter(technician = None)
            except:
                raise Exception("Object not found")
        elif perm.is_admin():
            try:
                pending_jobs = PendingJobs.objects.filter( technician = None, associated_with_company__in = [company] )
            except:
                raise Exception("Object not found")

        # then we have a create or get card for a user
        # then we update it
        

    def update_total_unaccepted_pending_job_cards(self, uob, perm, company):
        pass

# all cards are then registered and then these are the ones that people can view and use in the app
    