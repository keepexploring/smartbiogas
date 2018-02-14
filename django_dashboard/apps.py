# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class DjangoDashboardConfig(AppConfig):
    name = 'django_dashboard'
    verbose_name = 'Biogas Owners, Plants and Technicans'
    def ready(self):
        import django_dashboard.signals