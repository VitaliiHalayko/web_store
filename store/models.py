from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from categories.models import Category
import sys

class Product(models.Model):
    name = models.CharField(max_length=100, default="Product name", unique=True)
    short_description = models.CharField(max_length=255, default='Describe the product')
    description = models.TextField()
    image = models.ImageField(upload_to='static/assets/images/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    price_with_discount = models.DecimalField(max_digits=7, decimal_places=2)
    total_orders_count = models.PositiveIntegerField(default=0)
    total_count_on_warehouse = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        width = 450
        height = 300

        img = Image.open(self.image)
        output = BytesIO()

        new_img = Image.new("RGB", (width, height), "white")

        aspect_ratio = img.width / img.height
        target_aspect_ratio = width / height

        if aspect_ratio > target_aspect_ratio:
            new_height = int(width / aspect_ratio)
            y_offset = (height - new_height) // 2
            img = img.resize((width, new_height))
            new_img.paste(img, (0, y_offset))
        else:
            new_width = int(height * aspect_ratio)
            x_offset = (width - new_width) // 2
            img = img.resize((new_width, height))
            new_img.paste(img, (x_offset, 0))

        new_img.save(output, format='JPEG', quality=60)

        output.seek(0)

        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    name_for_admin_page = models.CharField(max_length=50, default='attribute name at admin page')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return self.name_for_admin_page

    def save(self, *args, **kwargs):
        self.name_for_admin_page = f"{self.name} - {self.category.name}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Атрибут товару'
        verbose_name_plural = 'Атрибути товарів'


class Value(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    name_for_admin_page = models.CharField(max_length=150, default='product value at admin page')

    def __str__(self):
        return self.name_for_admin_page

    def save(self, *args, **kwargs):
        self.name_for_admin_page = f"{self.product.name} - {self.category.name} - {self.value}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Значення для атрибуту товару'
        verbose_name_plural = 'Значення для атрибутів товарів'