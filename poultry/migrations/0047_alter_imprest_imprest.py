# Generated by Django 4.2.8 on 2024-01-13 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0046_alter_imprest_imprest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imprest',
            name='imprest',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
