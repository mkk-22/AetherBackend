# Generated by Django 5.1.6 on 2025-02-17 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('VE', 'VE'), ('alert', 'alert')], default='general', max_length=50),
        ),
    ]
