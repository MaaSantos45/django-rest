from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from recipes.models import Recipe
import os


@receiver(pre_save, sender=Recipe)
def create_recipe_img(**kwargs):
    instance = kwargs.get('instance')
    if not instance:
        return

    old = Recipe.objects.filter(pk=instance.pk).first()

    if old and old.cover and instance.cover != old.cover:
        path = old.cover.path
        try:
            os.remove(path)
        except (ValueError, FileNotFoundError):
            pass


@receiver(pre_delete, sender=Recipe)
def delete_recipe_img(**kwargs):
    instance = kwargs.get('instance')
    if instance and instance.cover:
        path = instance.cover.path
        try:
            os.remove(path)
        except (ValueError, FileNotFoundError):
            pass
