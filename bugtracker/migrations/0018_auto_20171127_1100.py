# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-11-27 16:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker', '0017_remove_issueevaluation_observations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issueevaluation',
            old_name='satisfaction',
            new_name='satisfied',
        ),
    ]
