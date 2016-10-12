# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import SoftwareIssue, Headquarter, BrowserIssue, TypeIssue, \
    Person, Issue, StatusIssue, PriorityIssue, CategoryIssue, OsIssue, \
    ReproducibilityIssue


class PersonInLine(admin.StackedInline):
    model = Person
    can_delete = False
    formfield_overrides = {}


class UserAdmin(AuthUserAdmin):
    inlines = [PersonInLine]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register([
    SoftwareIssue, Headquarter, BrowserIssue, TypeIssue, Issue,
    StatusIssue, PriorityIssue, CategoryIssue, OsIssue, ReproducibilityIssue,
])
