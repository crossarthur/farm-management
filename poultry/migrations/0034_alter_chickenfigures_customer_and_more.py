# Generated by Django 4.2.8 on 2024-01-04 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0033_alter_chickenfigures_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickenfigures',
            name='customer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customerrating',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poultry.chickenfigures'),
        ),
    ]
