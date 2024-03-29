# Generated by Django 4.2.8 on 2024-01-04 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poultry', '0031_rename_customer_customerrating_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerrating',
            old_name='client',
            new_name='customer',
        ),
        migrations.AddField(
            model_name='chickenfigures',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
