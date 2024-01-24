# Generated by Django 4.2.8 on 2024-01-10 04:49

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry', '0041_remove_imprest_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotePad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', ckeditor.fields.RichTextField(blank=True, max_length=50, null=True)),
                ('note', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]