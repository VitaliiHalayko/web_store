from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Product
import os


@receiver(post_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    """
    Signal receiver function that deletes the image file associated with a Product
    instance after the instance is deleted from the database.
    """
    # Check if the instance has an image
    if instance.image:
        # Check if the image file exists on the filesystem
        if os.path.isfile(instance.image.path):
            # Remove the image file from the filesystem
            os.remove(instance.image.path)
