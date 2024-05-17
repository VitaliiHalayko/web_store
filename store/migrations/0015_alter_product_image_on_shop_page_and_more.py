# Generated by Django 4.2.11 on 2024-05-14 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_product_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_on_shop_page',
            field=models.ImageField(upload_to='static/assets/images/shop/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]