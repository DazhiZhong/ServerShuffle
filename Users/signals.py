from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from cards.models import CurrentDeck

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        CurrentDeck.objects.create(user=instance)
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender, instance, created, **kwargs):
    
    instance.profile.save()

