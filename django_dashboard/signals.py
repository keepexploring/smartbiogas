from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_dashboard.models import UserDetail


#@receiver(post_save, sender=User)
#def save_profile(sender, instance, **kwargs):
#   instance.profile.save()

#@receiver(post_save, sender=UserDetail)
#def save_profile(sender, instance, **kwargs):
#   
#    instance.profile.save()


