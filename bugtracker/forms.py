# -*- encoding: utf-8 -*-

from django import forms
from django.forms import modelformset_factory
from models import *

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
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}),
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
            'issue', 'description', 'software', 'os', 'headquarter', 'browser',
            'priority', 'type_issue', 'category_issue', 'image1', 'image2',
            'reproducibility_issue', 'steps_to_reproduce',
        ]
        widgets = {
            'issue': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Incidencia'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripción',
                       'rows': 5}),
            'steps_to_reproduce': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Pasos para replicar',
                       'rows': 4}),
            'software': forms.Select(attrs={'class': 'form-control'}),
            'os': forms.Select(attrs={'class': 'form-control'}),
            'headquarter': forms.Select(attrs={'class': 'form-control'}),
            'browser': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'type_issue': forms.Select(attrs={'class': 'form-control'}),
            'category_issue': forms.Select(attrs={'class': 'form-control'}),
            'reproducibility_issue': forms.Select(
                attrs={'class': 'form-control'}),
        }


class UpdateIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'id', 'issue', 'description', 'software', 'os', 'headquarter',
            'browser', 'priority', 'type_issue', 'category_issue', 'image1',
            'image2', 'reproducibility_issue', 'steps_to_reproduce', 'reporter'
        ]
        widgets = {
            'issue': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Incidencia'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripcion',
                       'rows': 5}),
            'steps_to_reproduce': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Pasos para replicar',
                       'rows': 4}),
            'software': forms.Select(attrs={'class': 'form-control'}),
            'os': forms.Select(attrs={'class': 'form-control'}),
            'headquarter': forms.Select(attrs={'class': 'form-control'}),
            'browser': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'type_issue': forms.Select(attrs={'class': 'form-control'}),
            'category_issue': forms.Select(attrs={'class': 'form-control'}),
            'reproducibility_issue': forms.Select(
                attrs={'class': 'form-control'}),
        }


class UpdateIssueAdminForm(forms.ModelForm):

    class Meta:
        model = Issue

        fields = [
            'id', 'issue', 'description', 'os', 'software', 'headquarter',
            'browser', 'priority', 'type_issue', 'category_issue', 'image1',
            'image2', 'status', 'dev', 'ticket', 'sprint', 'reproducibility_issue',
            'steps_to_reproduce', 'evaluation_comments', 'reporter',
        ]
        widgets = {
            'issue': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Incidencia'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripcion',
                       'rows': 5}),
            'steps_to_reproduce': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Pasos para replicar',
                       'rows': 4}),
            'evaluation_comments': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Comentarios del evaluador',
                       'rows': 3}),
            'software': forms.Select(attrs={'class': 'form-control'}),
            'os': forms.Select(attrs={'class': 'form-control'}),
            'headquarter': forms.Select(attrs={'class': 'form-control'}),
            'browser': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'type_issue': forms.Select(attrs={'class': 'form-control'}),
            'category_issue': forms.Select(attrs={'class': 'form-control'}),
            'reproducibility_issue': forms.Select(
                attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'ticket': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ticket'}),
            'sprint': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Sprint'}),
            'dev': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateIssueAdminForm, self).__init__(*args, **kwargs)

        self.fields['dev'] = forms.ModelChoiceField(
            queryset=Person.objects.filter(user__is_active=True, dev=True),
            widget=forms.Select(attrs={'class': 'form-control input-sm',
                                       'required': False})
        )
        self.fields['status'].queryset = StatusIssue.objects.exclude\
            (status__icontains='cerrada')


class SearchIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'id', 'issue', 'software', 'headquarter', 'sprint', 'priority',
            'type_issue', 'status', 'reporter', 'dev',
        ]
        select_attr = {'class': 'form-control input-sm', 'required': False}
        widgets = {
            'id': forms.TextInput(
                attrs={'class': 'form-control input-sm',
                       'placeholder': 'Buscar por id'}),
            'issue': forms.TextInput(
                attrs={'class': 'form-control input-sm',
                       'placeholder': 'Buscar por nombre'}),
            'software': forms.Select(attrs=select_attr),
            'headquarter': forms.Select(attrs=select_attr),
            'sprint': forms.TextInput(
                attrs={'class': 'form-control input-sm',
                       'placeholder': 'Buscar por sprint'}),
            'priority': forms.Select(attrs=select_attr),
            'type_issue': forms.Select(attrs=select_attr),
            'status': forms.Select(attrs=select_attr),
            'reporter': forms.Select(attrs=select_attr),
            'dev': forms.Select(attrs=select_attr),
        }

    def __init__(self, *args, **kwargs):
        super(SearchIssueForm, self).__init__(*args, **kwargs)
        self.fields['is_evaluated'] = \
            forms.BooleanField()
        self.fields['date_init'] = forms.DateField(
            widget=forms.TextInput(
                attrs={'class': 'form-control input-sm', 'id': 'date_init',
                       'placeholder': 'Fecha inicial'}))
        self.fields['date_end'] = forms.DateField(
            widget=forms.TextInput(
                attrs={'class': 'form-control input-sm', 'id': 'date_end',
                       'placeholder': 'Fecha Final'}))
        self.fields['software'].empty_label = '-- sistema'
        self.fields['headquarter'].empty_label = '-- sede'
        self.fields['priority'].empty_label = '-- prioridad'
        self.fields['type_issue'].empty_label = '-- tipo'
        self.fields['status'].empty_label = '-- estado'
        self.fields['reporter'].empty_label = '-- reportado por'
        self.fields['dev'] = forms.ModelChoiceField(
            queryset=Person.objects.filter(user__is_active=True, dev=True),
            widget=forms.Select(attrs={'class': 'form-control input-sm',
                                       'required': False})
        )
        self.fields['dev'].empty_label = '-- asignado a'


class CreateEvaluationComment(forms.ModelForm):
    class Meta:
        model = EvaluationComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Escriba aquí el comentario...',
                                             'rows': 5}),
        }


class CreateIssueEvaluation(forms.ModelForm):
    class Meta:
        model = IssueEvaluation
        fields = ['resolve', 'time_evaluation', 'difficulty',
                  'contact', 'satisfied']
        resolve_choices = [
            ('', '-- Selecciona una opción --'), ('3', 'Resuelta'), ('5', 'Fue resuelta parcialmente'),
            ('1', 'No resuelta')

        ]
        time_evaluation_choices = [
            ('', '-- Selecciona una opción --'), ('5', 'Muy rápido'), ('3', 'Rápido'),
            ('2', 'Lento'), ('1', 'Muy lento'),
        ]
        difficulty_choices = [
            ('', '-- Selecciona una opción --'), ('1', 'Muy fácil'),
            ('2', 'Fácil'), ('3', 'Difícil'), ('5', 'Muy difícil')
        ]
        contact_choices = [
            ('', '-- Selecciona una opción --'), ('3', 'Celular'), ('4', 'Chat'), ('2', 'Correo electrónico'),
            ('1', 'Extensión telefónica'), ('6', 'Personalmente'), ('5', 'Ninguno')


        ]
        satisfied_choices = [
            ('', '-- Selecciona una opción --',), ('5', 'Muy satisfecho'),
            ('3', 'Satisfecho'), ('2', 'Insatisfecho'), ('1', 'Muy insatisfecho')
        ]
        widgets = {
            'resolve': forms.Select(choices=resolve_choices,
                                    attrs={'class': 'form-control'}),
            'time_evaluation': forms.Select(choices=time_evaluation_choices,
                                            attrs={'class': 'form-control'}),
            'difficulty': forms.Select(choices=difficulty_choices,
                                            attrs={'class': 'form-control'}),
            'contact': forms.Select(choices=contact_choices,
                                            attrs={'class': 'form-control'}),
            'satisfied': forms.Select(choices=satisfied_choices,
                                            attrs={'class': 'form-control'}),
            }
