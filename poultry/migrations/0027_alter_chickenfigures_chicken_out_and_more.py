# Generated by Django 4.2.8 on 2024-01-03 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0026_alter_drugs_drug_cost_alter_feed_feed_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_out',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='chickenfigures',
            name='chicken_out_total_cost',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='chickenfigures',
            name='total_chicken',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
