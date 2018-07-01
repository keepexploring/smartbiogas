from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_dashboard.models import UserDetail, RegisteredNode, UICtoDeviceID, BiogasPlant
import pdb

#@receiver(post_save, sender=User)
#def save_profile(sender, instance, **kwargs):
#   instance.profile.save()

#@receiver(post_save, sender=UserDetail)
#def save_profile(sender, instance, **kwargs):
#   
#    instance.profile.save()


@receiver([post_save], sender=BiogasPlant)
def thingsboard_data_exists_check(sender, instance, **kwargs):
    """ This function checks if thingsboard data already exists when a biogas node is registered
    if it does, it links the two up """
    UIC = instance.UIC
    thingsboard_connection = UICtoDeviceID.objects.filter( UIC = UIC )
    if thingsboard_connection.exists():
        thingsboard_connection.biogas_plant = instance
        thingsboard_connection.save()
  #instance.profile.save()