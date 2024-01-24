# Generated by Django 4.2.8 on 2023-12-27 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0014_necessities'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColdRoomIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chickens_in_freezer', models.IntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ColdRoomOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chickens_out_freezer', models.IntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]