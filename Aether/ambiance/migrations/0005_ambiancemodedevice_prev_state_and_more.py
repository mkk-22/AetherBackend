# Generated by Django 5.1.5 on 2025-01-29 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambiance', '0004_remove_ambiancemodedevice_light_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambiancemodedevice',
            name='prev_state',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AddField(
            model_name='ambiancemodedevice',
            name='prev_status',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='ambiancemodedevice',
            name='state',
            field=models.CharField(default=' ', max_length=100),
        ),
    ]
