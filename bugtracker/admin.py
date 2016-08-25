from django.contrib import admin

from .models import SoftwareIssue, Headquarter, BrowserIssue, TypeIssue, \
    Person, Issue

admin.site.register([
    SoftwareIssue, Headquarter, BrowserIssue, TypeIssue, Person, Issue
])
