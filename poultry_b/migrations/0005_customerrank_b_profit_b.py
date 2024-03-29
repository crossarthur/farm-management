# Generated by Django 4.2.8 on 2024-01-14 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poultry_b', '0004_notepad_b_offals_b_rename_imprest_imprest_b'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRank_b',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_rk', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profit_b',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.IntegerField(blank=True, null=True)),
                ('expenditure', models.IntegerField(blank=True, null=True)),
                ('calculate', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
