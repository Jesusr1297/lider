# Generated by Django 4.1.3 on 2022-11-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_rename_price_materials_unit_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materials',
            name='quantity_ordered',
            field=models.FloatField(verbose_name='Cantidad'),
        ),
    ]
