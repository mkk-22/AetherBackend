# Generated by Django 5.1.6 on 2025-02-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy', '0005_alter_intervalreading_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='energyusage',
            name='period',
            field=models.CharField(choices=[('hourly', 'Hourly'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], max_length=10),
        ),
    ]
