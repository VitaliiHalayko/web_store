# Generated by Django 4.2.11 on 2024-05-09 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0008_alter_category_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
            ],
            options={
                'verbose_name': 'Атрибут товару',
                'verbose_name_plural': 'Атрибути товарів',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Product name', max_length=50, unique=True)),
                ('short_description', models.CharField(default='Describe the product', max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='static/assets/images/products/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('price_with_discount', models.DecimalField(decimal_places=2, max_digits=4)),
                ('total_orders_count', models.PositiveIntegerField(default=0)),
                ('total_count_on_warehouse', models.PositiveIntegerField(default=0)),
                ('is_visible', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукти',
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(max_length=50)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.attribute')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'verbose_name': 'Значення для атрибуту товару',
                'verbose_name_plural': 'Значення для атрибутів товарів',
            },
        ),
        migrations.AddField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
