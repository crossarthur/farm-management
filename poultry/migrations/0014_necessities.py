# Generated by Django 4.2.8 on 2023-12-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0013_drugs_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Necessities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('necessities_description', models.CharField(max_length=100)),
                ('necessities_cost', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
