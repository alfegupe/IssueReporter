from django import forms
from django.forms import modelformset_factory
from models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password'}),
    )


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
