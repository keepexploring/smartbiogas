# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-09-03 09:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_dashboard', '0006_biogasplant_volume_biogas'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Address', 'verbose_name_plural': 'Addresses'},
        ),
        migrations.RemoveField(
            model_name='address',
            name='district',
        ),
        migrations.RemoveField(
            model_name='address',
            name='village',
        ),
        migrations.RemoveField(
            model_name='address',
            name='ward',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='country',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='district',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='neighbourhood',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='other_address_details',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='region',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='srid',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='village',
        ),
        migrations.RemoveField(
            model_name='biogasplant',
            name='ward',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='continent',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='country',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='district',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='region',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='srid',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='village',
        ),
        migrations.RemoveField(
            model_name='biogasplantcontact',
            name='ward',
        ),
        migrations.RemoveField(
            model_name='company',
            name='country',
        ),
        migrations.RemoveField(
            model_name='company',
            name='district',
        ),
        migrations.RemoveField(
            model_name='company',
            name='neighbourhood',
        ),
        migrations.RemoveField(
            model_name='company',
            name='other_address_details',
        ),
        migrations.RemoveField(
            model_name='company',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='company',
            name='region',
        ),
        migrations.RemoveField(
            model_name='company',
            name='village',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ward',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='country',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='district',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='neighbourhood',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='other_address_details',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='region',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='village',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='ward',
        ),
        migrations.AddField(
            model_name='address',
            name='address_line1',
            field=models.CharField(blank=True, help_text='Address line 1', max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='address_line2',
            field=models.CharField(blank=True, help_text='Address line 2', max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='address_line3',
            field=models.CharField(blank=True, help_text='Address line 3', max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='building_name_number',
            field=models.CharField(blank=True, help_text='Name or number of building', max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, db_index=True, help_text='city', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='other',
            field=models.TextField(blank=True, help_text='Other address details', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(blank=True, help_text='zip_code/postcode', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='biogasplant',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biogasplant', to='django_dashboard.Address'),
        ),
        migrations.AddField(
            model_name='biogasplantcontact',
            name='registered_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_dashboard.UserDetail'),
        ),
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='django_dashboard.Address'),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userdetail', to='django_dashboard.Address'),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, db_index=True, help_text='Country', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='region',
            field=models.CharField(blank=True, db_index=True, help_text='region', max_length=200, null=True),
        ),
    ]
