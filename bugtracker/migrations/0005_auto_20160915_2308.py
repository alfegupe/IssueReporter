# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-16 04:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker', '0004_auto_20160915_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bugtracker.StatusIssue'),
        ),
    ]
