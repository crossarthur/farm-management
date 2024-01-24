# Generated by Django 4.2.8 on 2023-12-25 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0006_alter_chickenfigures_chicken_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_out_kilogram',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_out_total_cost',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_out_unit_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
