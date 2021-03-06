# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 02:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BrowserIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browser', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Headquarter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headquarter', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[(1, 'Baja'), (2, 'Normal'), (3, 'Importante'), (4, 'Urgente')], default=2, max_length=1)),
                ('ticket', models.CharField(blank=True, max_length=6, null=True)),
                ('image1', models.ImageField(height_field=1000, upload_to='media/', width_field=1000)),
                ('image2', models.ImageField(height_field=1000, upload_to='media/s', width_field=1000)),
                ('browser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.BrowserIssue')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification', models.CharField(max_length=20)),
                ('headquarter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.Headquarter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('software', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StatusIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_issue', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TypeIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_issue', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='dev',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Developer', to='bugtracker.Person'),
        ),
        migrations.AddField(
            model_name='issue',
            name='headquarter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.Headquarter'),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Persons', to='bugtracker.Person'),
        ),
        migrations.AddField(
            model_name='issue',
            name='software',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.SoftwareIssue'),
        ),
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.StatusIssue'),
        ),
        migrations.AddField(
            model_name='issue',
            name='type_issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.TypeIssue'),
        ),
    ]
