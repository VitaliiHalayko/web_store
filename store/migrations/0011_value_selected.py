# Generated by Django 4.2.11 on 2024-05-13 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_value_name_for_admin_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
