# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-02 09:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_dashboard', '0009_messages_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='user',
        ),
        migrations.AddField(
            model_name='messages',
            name='user_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messages',
            name='user_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_to', to=settings.AUTH_USER_MODEL),
        ),
    ]