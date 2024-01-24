# Generated by Django 4.2.8 on 2024-01-10 05:04

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0042_notepad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notepad',
            name='note',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notepad',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]