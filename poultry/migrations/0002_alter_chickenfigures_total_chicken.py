# Generated by Django 4.2.8 on 2023-12-24 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickenfigures',
            name='total_chicken',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
