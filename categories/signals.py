from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Category
import os

@receiver(post_delete, sender=Category)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)