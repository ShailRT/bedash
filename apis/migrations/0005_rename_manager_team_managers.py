# Generated by Django 5.1.7 on 2025-03-31 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0004_team'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='manager',
            new_name='managers',
        ),
    ]
