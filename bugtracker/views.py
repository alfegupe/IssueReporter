from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, \
    FormView, TemplateView, RedirectView, View
from .models import Issue, Person
# Authentication imports
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django import forms
from forms import LoginForm, CreateIssueForm


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

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'bugtracker/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'u_name'


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'bugtracker/issues.html'
    login_url = 'login'
    paginate_by = 10


class IssueCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateIssueForm
    template_name = 'bugtracker/create.html'
    login_url = 'login'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            person = Person.objects.get(user=self.request.user)
            form.instance.reporter = person
        except Exception as e:
            print e.message
            return super(IssueCreateView, self).form_invalid(form)

        return super(IssueCreateView, self).form_valid(form)


class IssueUpdateView(LoginRequiredMixin, CreateView):
    model = Issue
    slug_field = 'id'
    template_name = 'bugtracker/update.html'
    login_url = 'login'
    success_url = reverse_lazy('home')


class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'bugtracker/detail.html'
