# Generated by Django 4.2.8 on 2024-01-01 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0022_alter_profit_calculate_alter_profit_expenditure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickenfigures',
            name='customer',
            field=models.CharField(max_length=100),
        ),
    ]
