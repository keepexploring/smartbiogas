
from django_dashboard.models import ( Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs, Abandoned,
                                    CardTemplate, Card, PendingAction, IndicatorsTemplate, IndicatorObjects )

from django_dashboard.enums import ContactType, UserRole, JobStatus, QPStatus, CurrentStatus, TypeBiogas, SupplierBiogas, SensorStatus,FundingSourceEnum, CardTypes, EntityTypes, AlertTypes
import uuid

class UnassignedPendingJobs():
    company = 'ALL' # Can be 'ALL', 'SELECTED' or a list of the ids of the companies. 'SELECTED' means you need to add the companies in the admin interface.
    name = 'unassigned_pending_jobs'
    title = 'Number of unassigned pending jobs'
    description = 'Number of jobs which have been rejected by technicians or abandoned'
    template_id = ''
    card_type = 'INFO' # options: INFO or ALERT
    entity_type = 'JOB' # options: BIOGASPLANT, TECHNICIAN, JOB
    image = 'test.jpg'
    created = ''
    updated = ''

    def __init__(self):
        # create cards on init of new user - could just be a function in the class
        pass

    def set_companies(self):
        if self.company == 'ALL':
            companies = Company.objects.all()
            cls.template_object.company.set(*companies)
        elif self.company == 'SELECTED': # we rely on the user updating the companies they want in the admin interface in 'Card Templates'
            pass
        elif type(self.company) is list:
            try:
                companies = Company.objects.filter(company_id__in = [uuid.UUID(hex=uid) for uid in self.company])
                cls.template_object.company.set(*companies)
            except:
                raise Exception('Invalid company_id')

    def update_companies(self, cls):
        pass

    def is_template_active(self, uob):
        self.card_object = Card.objects.filter( user=uob.userdetail, card_template = self.template_object )
        return card_object.exists()

    def __repr__(self):
        return self.name

    @classmethod
    def build_template(cls):
        # we build the template cards and add them for a user
        """Run when a user gets the templates available to them"""
        (cls.template_object, self.created) = CardTemplate.objects.get_or_create(
                                name = cls.name,
                                title = cls.title,
                                description = cls.description,
                                card_type = getattr(CardTypes(), cls.card_type),
                                entity_type = getattr(EntityTypes(), cls.entity_type),
                                image = cls.image
                                        )
        self.set_companies()
        cls.company_objects = companies
        cls.template_id = template_object.template_id
        cls.created = template_object.created
        cls.updated = template_object.updated
        cls.id = template_object.id

    def update_card(self, uob, perm, company):
        """Run everytime a user gets the cards on their dashboard"""

        if is_template_active(uob):
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

            self.card_object.value = len(pending_jobs)
            self.card_object.save()
        else:
            pass
        

        # then we have a create or get card for a user
        # then we update it
        

   # def update_total_unaccepted_pending_job_cards(self, uob, perm, company):
  #    pass

# all cards are then registered and then these are the ones that people can view and use in the app
    