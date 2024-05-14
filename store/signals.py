from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Product
import os


@receiver(post_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)