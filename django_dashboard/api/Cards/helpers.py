
from django_dashboard.models import ( Company, UserDetail, TechnicianDetail, BiogasPlantContact, BiogasPlant, JobHistory, Dashboard, PendingJobs, Abandoned,
                                    CardTemplate, Card, PendingAction, IndicatorsTemplate, IndicatorObjects )


def is_template_active(uob, card_template):
    return Card.objects.filter( user=uob.userdetail, card_template = card_template ).exists()

        