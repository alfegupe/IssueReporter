from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, \
    FormView, TemplateView, RedirectView
from .models import Issue, Person
# Authentication imports
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.forms import forms


class IndexView(TemplateView):
    template_name = "bugtracker/index.html"


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"
    success_url = reverse_lazy("home")

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


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        else:
            return super(
                LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'bugtracker/issues.html'


class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = [
        'issue', 'description', 'software', 'headquarter', 'browser',
        'priority', 'type_issue', 'image1', 'image2'
    ]
    template_name = 'bugtracker/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            person = Person.objects.get(user=self.request.user)
            form.instance.reporter = person
        except:
            self.error_messages['caps'] = 'Hey, that CAPSLOCK is on!!!'
            return super(IssueCreateView, self).form_invalid(form)

        return super(IssueCreateView, self).form_valid(form)

class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'bugtracker/detail.html'
