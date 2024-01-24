# Generated by Django 4.2.8 on 2024-01-01 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0019_profit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profit',
            name='calculate',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='profit',
            name='expenditure',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='profit',
            name='income',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]