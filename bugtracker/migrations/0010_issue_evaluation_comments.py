# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker', '0009_auto_20160929_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='evaluation_comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]