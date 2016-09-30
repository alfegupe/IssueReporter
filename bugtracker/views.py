# -*- encoding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.views.generic import ListView, DetailView, DeleteView, CreateView, \
    FormView, TemplateView, RedirectView, View
from django.views.generic.edit import UpdateView
from .models import Issue, Person
# Authentication imports
from django.contrib.auth import login, logout, authenticate, \
    update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from forms import LoginForm, CreateIssueForm, UpdateIssueForm, SearchIssueForm, \
    UpdateDataUserForm, UpdatePasswordUserForm, UpdateIssueAdminForm
from django.contrib import messages


def is_member(user, group):
    return user.groups.filter(name=group).exists()


class IndexView(TemplateView):
    template_name = "bugtracker/index.html"


class LoginView(View):
    form = LoginForm()
    message = None
    template = "auth/login.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            self.message = 'Usuario o password incorrectos'
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form, 'message': self.message}


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'u_name'


class UpdateDataUserView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/edit.html'
    form_class = UpdateDataUserForm

    def get_success_url(self):
        return reverse_lazy(
            'profile',
            kwargs={'u_name': self.request.user.username}
        )

    def get_object(self, queryset=None):
        return self.request.user

    def get_username(self):
        return self.request.user.username


def update_password(request):
    message = None
    form = UpdatePasswordUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_pass = form.cleaned_data['password']
            new_pass = form.cleaned_data['new_password']
            if authenticate(
                    username=request.user.username, password=current_pass
            ):
                request.user.set_password(new_pass)
                request.user.save()
                update_session_auth_hash(request, request.user)
                message = 'Password actualizado.'
            else:
                message = 'El password actual es incorrecto'

    context = {'form': form, 'message': message}
    return render(request, 'user/update_password.html', context)


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'bugtracker/issues.html'
    login_url = 'login'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(IssueListView, self).get_context_data(**kwargs)
        context['form_search'] = SearchIssueForm(data=self.request.GET)
        return context

    def get_queryset(self):
        query = self.get_params_search()
        if not self.request.user.is_superuser and \
                not is_member(self.request.user, 'Developer'):
            query['reporter'] = Person.objects.get(user=self.request.user)
        return self.model.objects.filter(**query).order_by(
            'priority', 'type_issue')

    def get_params_search(self):
        params = {}
        try:
            for key in self.request.GET:
                if self.request.GET[key] != '' and key != 'page':
                    k = key + '__contains' if key == 'issue' else key
                    params[k] = self.request.GET[key]
        except Exception as e:
            print e.message
        finally:
            return params


class IssueCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateIssueForm
    template_name = 'bugtracker/create.html'
    login_url = 'login'
    message = None
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            person = Person.objects.get(user=self.request.user)
            if not person or not \
                    is_member(self.request.user, 'Reporter'):
                messages.error(
                    self.request,
                    'Usuario no tiene permisos para reportar incidencias.'
                )
                return super(IssueCreateView, self).form_invalid(form)
            messages.success(
                self.request,
                'Incidencia ha sido creada correctamente.'
            )
            form.instance.reporter = person
            return super(IssueCreateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(IssueCreateView, self).form_invalid(form)


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    model = Issue
    slug_field = 'id'
    slug_url_kwarg = 'id_issue'
    template_name = 'bugtracker/update.html'
    form_class = UpdateIssueForm
    login_url = 'login'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser or \
                is_member(self.request.user, 'Developer'):
            self.form_class = UpdateIssueAdminForm

        return super(IssueUpdateView, self).get_context_data()

    def form_valid(self, form):
        try:
            person = Person.objects.get(user=self.request.user)
            if not person:
                messages.error(
                    self.request,
                    'Usuario no existe como Persona en la base de datos.'
                )
                return super(IssueUpdateView, self).form_invalid(form)
            if not self.request.user.is_superuser and \
                    not is_member(self.request.user, 'Developer') and \
                    not is_member(self.request.user, 'Reporter'):
                messages.error(
                    self.request,
                    'Usuario no tiene permisos para actualizar incidencias.'
                )
                return super(IssueUpdateView, self).form_invalid(form)

            form.instance.reporter = person
            messages.success(
                self.request,
                'Incidencia ha sido actualizada.'
            )
            return super(IssueUpdateView, self).form_valid(form)
        except Exception as e:
            print e.message
            return super(IssueUpdateView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser or \
                is_member(self.request.user, 'Developer'):
            self.form_class = UpdateIssueAdminForm
        return super(IssueUpdateView, self).post(request, *args, **kwargs)


class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'bugtracker/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id_issue'
