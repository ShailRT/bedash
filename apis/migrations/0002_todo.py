# Generated by Django 5.1.7 on 2025-03-24 10:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('user_assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
