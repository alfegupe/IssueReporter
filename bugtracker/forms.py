# -*- encoding: utf-8 -*-

from django import forms
from django.forms import modelformset_factory
from models import *

"""
Functions - Validators
"""

def must_be_gt(value):
    if len(value) < 5:
        raise forms.ValidationError(
            'Este campo debe tener al menos 5 caracteres')
    return value


"""
Classes
"""

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password'}),
    )


class UpdateDataUserForm(forms.ModelForm):

    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        error_messages={
            'required': 'El email es requerido.',
            'invalid': 'Ingrese un email valido'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class UpdatePasswordUserForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password actual'}),
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Nuevo Password'}),
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Repita nuevo Password'}),
    )

    def clean(self):
        pass1 = self.cleaned_data['new_password']
        pass2 = self.cleaned_data['repeat_password']
        if len(pass1) < 5:
            raise forms.ValidationError(
                'El nuevo password debe tener al menos 5 caracteres')
        if pass1 != pass2:
            raise forms.ValidationError('Los passwords no coinciden.')
        return self.cleaned_data


class CreateIssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = [
         'issue', 'description', 'software', 'headquarter', 'browser',
         'priority', 'type_issue', 'image1', 'image2', 'status'
        ]
        widgets = {
            'issue': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Incidencia'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripcion',
                       'rows': 3}),
            'software': forms.Select(attrs={'class': 'form-control'}),
            'headquarter': forms.Select(attrs={'class': 'form-control'}),
            'browser': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'type_issue': forms.Select(attrs={'class': 'form-control'}),
        }


class UpdateIssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = [
         'issue', 'description', 'software', 'headquarter', 'browser',
         'priority', 'type_issue', 'image1', 'image2', 'status'
        ]
        widgets = {
            'issue': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Incidencia'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripcion',
                       'rows': 3}),
            'software': forms.Select(attrs={'class': 'form-control'}),
            'headquarter': forms.Select(attrs={'class': 'form-control'}),
            'browser': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'type_issue': forms.Select(attrs={'class': 'form-control'}),
        }


class SearchIssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = [
            'issue', 'software', 'headquarter', 'browser', 'priority',
            'type_issue', 'status'
        ]
        select_attr = {'class': 'form-control input-sm', 'required': False}
        widgets = {
            'issue': forms.TextInput(
                attrs={'class': 'form-control input-sm',
                       'placeholder': 'Buscar por nombre'}),
            'software': forms.Select(attrs=select_attr),
            'headquarter': forms.Select(attrs=select_attr),
            'browser': forms.Select(attrs=select_attr),
            'priority': forms.Select(attrs=select_attr),
            'type_issue': forms.Select(attrs=select_attr),
            'status': forms.Select(attrs=select_attr),
        }

    def __init__(self, *args, **kwargs):
        super(SearchIssueForm, self).__init__(*args, **kwargs)
        self.fields['software'].empty_label = '-- sistema'
        self.fields['headquarter'].empty_label = '-- sede'
        self.fields['browser'].empty_label = '-- navegador'
        self.fields['priority'].empty_label = '-- prioridad'
        self.fields['type_issue'].empty_label = '-- tipo'
        self.fields['status'].empty_label = '-- estado'
