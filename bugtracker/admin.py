# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import SoftwareIssue, Headquarter, BrowserIssue, TypeIssue, \
    Person, Issue, StatusIssue, PriorityIssue

admin.site.register([
    SoftwareIssue, Headquarter, BrowserIssue, TypeIssue, Person, Issue,
    StatusIssue, PriorityIssue,
])
