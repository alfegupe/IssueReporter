# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 16:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker', '0013_statusissue_show_in_main_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='identification',
        ),
    ]
