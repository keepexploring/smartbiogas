# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-18 15:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0069_auto_20180518_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardorder',
            name='user',
        ),
        migrations.AddField(
            model_name='card',
            name='position',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_user', to='django_dashboard.UserDetail'),
        ),
        migrations.DeleteModel(
            name='CardOrder',
        ),
    ]
