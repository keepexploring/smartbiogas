# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-19 17:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0035_auto_20180219_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pendingjobs',
            options={'verbose_name': 'Pending Job', 'verbose_name_plural': 'Pending Jobs'},
        ),
        migrations.AlterField(
            model_name='pendingjobs',
            name='biogas_plant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_dashboard.BiogasPlant'),
        ),
        migrations.AlterField(
            model_name='pendingjobs',
            name='technician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_dashboard.UserDetail'),
        ),
    ]