# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class SoftwareIssue(models.Model):
    software = models.CharField(max_length=200)

    class Meta:
        ordering = ('software',)

    def __unicode__(self):
        return self.software


class PriorityIssue(models.Model):
    priority = models.CharField(max_length=200)
    fa_icon = models.CharField(max_length=30, null=True)

    class Meta:
        ordering = ('priority',)

    def __unicode__(self):
        return self.priority


class StatusIssue(models.Model):
    status = models.CharField(max_length=200)
    show_in_main_list = models.BooleanField(default=True, blank=False)
    bg_color = models.CharField(max_length=7, null=True)

    class Meta:
        ordering = ('status',)

    def __unicode__(self):
        return self.status


class ReproducibilityIssue(models.Model):
    reproducibility = models.CharField(max_length=200)

    class Meta:
        ordering = ('reproducibility',)

    def __unicode__(self):
        return self.reproducibility


class Headquarter(models.Model):
    headquarter = models.CharField(max_length=200)

    class Meta:
        ordering = ('headquarter',)

    def __unicode__(self):
        return self.headquarter


class BrowserIssue(models.Model):
    browser = models.CharField(max_length=200)
    fa_icon = models.CharField(max_length=30, null=True)

    class Meta:
        ordering = ('browser',)

    def __unicode__(self):
        return self.browser


class OsIssue(models.Model):
    os = models.CharField(max_length=200)
    fa_icon = models.CharField(max_length=30, null=True)

    class Meta:
        ordering = ('os',)

    def __unicode__(self):
        return self.os


class TypeIssue(models.Model):
    type_issue = models.CharField(max_length=100)
    fa_icon = models.CharField(max_length=30, null=True)

    class Meta:
        ordering = ('type_issue',)

    def __unicode__(self):
        return self.type_issue


class CategoryIssue(models.Model):
    category_issue = models.CharField(max_length=100)

    class Meta:
        ordering = ('category_issue',)

    def __unicode__(self):
        return self.category_issue


class Person(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    cellphone = models.CharField(max_length=20, blank=True)
    extension = models.CharField(max_length=10, blank=True)
    headquarter = models.ForeignKey(Headquarter, on_delete=models.CASCADE)
    dev = models.BooleanField(default=False)

    class Meta:
        ordering = ('user__first_name',)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Issue(models.Model):
    issue = models.CharField(max_length=300,)
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
    evaluated = models.BooleanField(default=False)
    dev = models.ForeignKey(
        Person, on_delete=models.CASCADE, null=True, related_name='Developer')
    ticket = models.CharField(max_length=6, null=True, blank=True)
    sprint = models.CharField(max_length=6, null=True, blank=True)
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


class EvaluationComment(models.Model):
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='Evaluator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)


class IssueEvaluation(models.Model):
    class Meta:
        permissions = (
            ("can_view_results_evaluations", "Can view evaluations results"),
        )
    time_evaluation = models.TextField()
    resolve = models.TextField()
    difficulty = models.TextField()
    contact = models.TextField()
    satisfied = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='EvalUser')
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, null=True, related_name='EvalIssue')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)