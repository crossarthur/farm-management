# Generated by Django 4.2.8 on 2024-01-04 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0035_alter_customerrating_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerrating',
            old_name='customer',
            new_name='customer_rank',
        ),
    ]
