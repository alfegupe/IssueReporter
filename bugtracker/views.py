from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, \
    FormView, TemplateView, RedirectView, View
from django.views.generic.edit import UpdateView
from .models import Issue, Person
# Authentication imports
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django import forms
from forms import LoginForm, CreateIssueForm, UpdateIssueForm, SearchIssueForm
from django.contrib.auth.decorators import permission_required


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


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'bugtracker/issues.html'
    login_url = 'login'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IssueListView, self).get_context_data(**kwargs)
        context['form_search'] = SearchIssueForm(data=self.request.GET)
        return context

    def get_queryset(self):
        query = self.get_params_search()
        if not self.request.user.is_superuser:
            query['reporter'] = Person.objects.get(user=self.request.user)
        return self.model.objects.filter(**query)

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
    success_url = reverse_lazy('home')

    def has_add_permission(self, request, obj=None):
        return False

    def form_valid(self, form):
        try:
            person = Person.objects.get(user=self.request.user)
            form.instance.reporter = person
        except Exception as e:
            print e.message
            return super(IssueCreateView, self).form_invalid(form)

        return super(IssueCreateView, self).form_valid(form)


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    model = Issue
    slug_field = 'id'
    slug_url_kwarg = 'id_issue'
    template_name = 'bugtracker/update.html'
    form_class = UpdateIssueForm
    login_url = 'login'
    success_url = reverse_lazy('home')


class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'bugtracker/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id_issue'
