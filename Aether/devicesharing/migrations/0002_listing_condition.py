# Generated by Django 5.1.6 on 2025-02-18 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devicesharing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='condition',
            field=models.CharField(choices=[('old', 'Old'), ('new', 'New')], default='new', max_length=50),
        ),
    ]
