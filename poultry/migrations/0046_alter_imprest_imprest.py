# Generated by Django 4.2.8 on 2024-01-13 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0045_alter_coldroomin_chickens_in_freezer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imprest',
            name='imprest',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
