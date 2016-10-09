# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class SoftwareIssue(models.Model):
    software = models.CharField(max_length=200)

    def __unicode__(self):
        return self.software


class PriorityIssue(models.Model):
    priority = models.CharField(max_length=200)
    bg_color = models.CharField(max_length=30, null=True)
    fa_icon = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.priority


class StatusIssue(models.Model):
    status = models.CharField(max_length=200)
    fa_icon = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.status


class ReproducibilityIssue(models.Model):
    reproducibility = models.CharField(max_length=200)

    def __unicode__(self):
        return self.reproducibility


class Headquarter(models.Model):
    headquarter = models.CharField(max_length=200)

    def __unicode__(self):
        return self.headquarter


class BrowserIssue(models.Model):
    browser = models.CharField(max_length=200)
    fa_icon = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.browser


class OsIssue(models.Model):
    os = models.CharField(max_length=200)
    fa_icon = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.os


class TypeIssue(models.Model):
    type_issue = models.CharField(max_length=100)
    fa_icon = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.type_issue


class CategoryIssue(models.Model):
    category_issue = models.CharField(max_length=100)

    def __unicode__(self):
        return self.category_issue


class Person(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    identification = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20, blank=True)
    extension = models.CharField(max_length=10, blank=True)
    headquarter = models.ForeignKey(Headquarter, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.identification + ' - ' + self.user.first_name + ' ' + \
               self.user.last_name


class Issue(models.Model):
    issue = models.CharField(max_length=300)
    description = models.TextField()
    software = models.ForeignKey(SoftwareIssue, on_delete=models.CASCADE)
    headquarter = models.ForeignKey(Headquarter, on_delete=models.CASCADE)
    browser = models.ForeignKey(BrowserIssue, on_delete=models.CASCADE)
    os = models.ForeignKey(OsIssue, on_delete=models.CASCADE)
    priority = models.ForeignKey(PriorityIssue, on_delete=models.CASCADE)
    type_issue = models.ForeignKey(TypeIssue, on_delete=models.CASCADE)
    category_issue = models.ForeignKey(CategoryIssue, on_delete=models.CASCADE)
    reproducibility_issue = models.ForeignKey(
        ReproducibilityIssue, on_delete=models.CASCADE)
    steps_to_reproduce = models.TextField(blank=True, null=True)
    evaluation_comments = models.TextField(blank=True, null=True)
    status = models.ForeignKey(
        StatusIssue, on_delete=models.CASCADE, blank=True, null=True)
    dev = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, related_name='Developer')
    ticket = models.CharField(max_length=6, null=True, blank=True)
    reporter = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='Persons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image1 = models.ImageField(
        upload_to='uploads/', max_length=1500, blank=True)
    image2 = models.ImageField(
        upload_to='uploads/', max_length=1500, blank=True)

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.issue
