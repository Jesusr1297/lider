# Generated by Django 4.0.6 on 2022-08-10 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_materials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materials',
            name='name',
            field=models.TextField(max_length=40, verbose_name='Nombre del Material'),
        ),
    ]