# Generated by Django 4.2.8 on 2024-01-03 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0027_alter_chickenfigures_chicken_out_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_in',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_mortality',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_out_unit_price',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_slaughtered',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]