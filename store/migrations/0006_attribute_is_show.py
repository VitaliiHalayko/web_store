# Generated by Django 4.2.11 on 2024-05-09 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_attribute_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='is_show',
            field=models.BooleanField(default=True),
        ),
    ]
