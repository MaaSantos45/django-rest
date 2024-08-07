from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    print('author')
    print(sender, instance, args, kwargs)
    if created:
        profile = Profile.objects.create(author=instance)
        profile.save()
