from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='static/assets/images/about/')
    desc = models.CharField(max_length=100, default='Describe your category')
    is_visible = models.BooleanField(default=True)
    sort_order = models.SmallIntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        width = 450
        height = 300

        img = Image.open(self.image)
        output = BytesIO()

        aspect_ratio = img.width / img.height

        target_aspect_ratio = width / height

        if aspect_ratio > target_aspect_ratio:
            new_height = int(img.width / target_aspect_ratio)
            y_offset = (img.height - new_height) / 2
            img = img.crop((0, y_offset, img.width, img.height - y_offset))
        else:
            new_width = int(img.height * target_aspect_ratio)
            x_offset = (img.width - new_width) / 2
            img = img.crop((x_offset, 0, img.width - x_offset, img.height))

        img = img.resize((width, height))

        img.save(output, format='JPEG', quality=60)

        output.seek(0)

        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

