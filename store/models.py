from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from categories.models import Category
import sys


# Model representing a product
class Product(models.Model):
    name = models.CharField(max_length=100, default="Product name", unique=True)  # Unique name for the product
    short_description = models.CharField(max_length=255, default='Describe the product')  # Brief description
    description = models.TextField()  # Detailed description
    # Field for product image on the all products page
    image = models.ImageField(upload_to='static/assets/images/products/')
    # Image field for product image on product page
    image_on_shop_page = models.ImageField(upload_to='static/assets/images/shop/', default=image)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)  # Foreign key to Category
    price = models.DecimalField(max_digits=7, decimal_places=2)  # Price of the product
    price_with_discount = models.DecimalField(max_digits=7, decimal_places=2)  # Discounted price
    total_orders_count = models.PositiveIntegerField(default=0)  # Total number of orders for the product
    total_count_on_warehouse = models.PositiveIntegerField(default=0)  # Stock count in the warehouse
    is_visible = models.BooleanField(default=True)  # Visibility status of the product
    updated_on = models.DateTimeField(auto_now=True)  # When product was updated last time

    def __str__(self):
        return self.name  # String representation of the product

    def save(self, *args, **kwargs):
        """
        Override the save method to resize the image before saving the product.
        """

        """mini image"""
        # Target dimensions for the resized image
        mini_image_width = 450
        mini_image_height = 300

        # Open the uploaded mini image
        mini_image = Image.open(self.image)

        # Create a BytesIO object to hold the new image data
        output = self.resize_image(mini_image, mini_image_width, mini_image_height)
        # Move to the beginning of the output buffer

        # Replace the original image with the resized image
        self.image = InMemoryUploadedFile(
            output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0],
            'image/jpeg', sys.getsizeof(output), None
        )

        """main image"""
        main_image_width = 600
        main_image_height = 400

        # Open the uploaded main image
        main_image = Image.open(self.image_on_shop_page)

        # Create a BytesIO object to hold the new image data
        output = self.resize_image(main_image, main_image_width, main_image_height)
        # Move to the beginning of the output buffer

        # Replace the original image with the resized image
        self.image = InMemoryUploadedFile(
            output, 'ImageField', "%s.jpg" % self.image_on_shop_page.name.split('.')[0],
            'image/jpeg', sys.getsizeof(output), None
        )

        # Call the save method of the superclass to save the product
        super(Product, self).save(*args, **kwargs)

    def resize_image(self, old_image, width, height):
        output = BytesIO()
        # Create a new blank image with the target dimensions
        new_img = Image.new("RGB", (width, height), "white")

        # Calculate the aspect ratios
        aspect_ratio = old_image.width / old_image.height
        target_aspect_ratio = width / height

        # Resize and paste the image to maintain aspect ratio and fit within target dimensions
        if aspect_ratio > target_aspect_ratio:
            new_height = int(width / aspect_ratio)
            y_offset = (height - new_height) // 2
            old_image = old_image.resize((width, new_height))
            new_img.paste(old_image, (0, y_offset))
        else:
            new_width = int(height * aspect_ratio)
            x_offset = (width - new_width) // 2
            old_image = old_image.resize((new_width, height))
            new_img.paste(old_image, (x_offset, 0))

        # Save the resized image to the output buffer
        new_img.save(output, format='JPEG', quality=60)

        output.seek(0)

        return output

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'


# Model representing an attribute of a product
class Attribute(models.Model):
    name = models.CharField(max_length=50)  # Name of the attribute
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to Category
    is_show = models.BooleanField(default=True)  # Visibility status of the attribute

    def __str__(self):
        return f"{self.category.name} - {self.name}"  # String representation of the attribute

    class Meta:
        verbose_name = 'Атрибут товару'  # Singular name for the Attribute model in the admin interface
        verbose_name_plural = 'Атрибути товарів'  # Plural name for the Attribute model in the admin interface


# Model representing a value for a product attribute
class Value(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)  # Foreign key to Attribute
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Foreign key to Product
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to Category
    value = models.CharField(max_length=255)  # Value of the attribute
    selected = models.BooleanField(default=False)  # Selected status of the attribute value

    def __str__(self):
        return f"{self.category.name} - {self.attribute.name} - {self.product.name} - {self.value}"  # String representation of the attribute value

    class Meta:
        verbose_name = 'Значення для атрибуту товару'  # Singular name for the Value model in the admin interface
        verbose_name_plural = 'Значення для атрибутів товарів'  # Plural name for the Value model in the admin interface
