# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class SoftwareIssue(models.Model):
    software = models.CharField(max_length=200)

    def __str__(self):
        return self.software


class Headquarter(models.Model):
    headquarter = models.CharField(max_length=200)

    def __str__(self):
        return self.headquarter


class BrowserIssue(models.Model):
    browser = models.CharField(max_length=200)

    def __str__(self):
        return self.browser


class TypeIssue(models.Model):
    type_issue = models.CharField(max_length=100)

    def __str__(self):
        return self.type_issue


class Person(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    identification = models.CharField(max_length=20)
    headquarter = models.ForeignKey(Headquarter, on_delete=models.CASCADE)


    def __str__(self):
        return self.identification + ' - ' + self.user.first_name + ' ' + \
               self.user.last_name


class Issue(models.Model):
    PRIORITY_CHOICES = (
        ('1', 'Baja'),
        ('2', 'Normal'),
        ('3', 'Importante'),
        ('4', 'Urgente'),
    )
    STATUS_CHOICES = (
        ('n', 'Nueva'),
        ('a', 'Solucionada'),
        ('d', 'Desarrollo'),
        ('r', 'Rechazada'),
    )
    issue = models.CharField(max_length=300)
    description = models.TextField()
    software = models.ForeignKey(SoftwareIssue, on_delete=models.CASCADE)
    headquarter = models.ForeignKey(Headquarter, on_delete=models.CASCADE)
    browser = models.ForeignKey(BrowserIssue, on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='2',
    )
    type_issue = models.ForeignKey(TypeIssue, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='n',
    )
    dev = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, related_name='Developer')
    ticket = models.CharField(max_length=6, null=True, blank=True)
    reporter = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='Persons')
    image1 = models.ImageField(
        upload_to='uploads/', height_field=1000, width_field=1000,
        max_length=100, blank=True)
    image2 = models.ImageField(
        upload_to='uploads/s', height_field=1000, width_field=1000,
        max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.issue
