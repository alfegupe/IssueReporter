# -*- encoding: utf-8 -*-

from django.conf.urls import url
from .views import IndexView, LoginView, LogoutView, IssueListView, \
    IssueCreateView, IssueDetailView, IssueUpdateView, ProfileView, \
    UpdateDataUserView, update_password, EvaluationCommentCreate, ExportXlsx, \
    IssueEvaluationView, IssueEvaluationResultView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^profile/(?P<u_name>[-_\w]+)/$', ProfileView.as_view(),
        name="profile"),
    url(r'^update_user/$', UpdateDataUserView.as_view(), name="update_user"),
    url(r'^update_password/$', update_password, name="update_password"),
    url(r'^home/$', IssueListView.as_view(), name='home'),
    url(r'^create/$', IssueCreateView.as_view(), name='create'),
    url(r'^detail/(?P<id_issue>[-_\w]+)/$', IssueDetailView.as_view(),
        name='detail'),
    url(r'^update/(?P<id_issue>[-_\w]+)/$', IssueUpdateView.as_view(),
        name='update'),
    url(r'add_evaluation_comment/$', EvaluationCommentCreate.as_view()),
    url(r'xlsx/$', ExportXlsx.as_view(), name='xlsx'),
    url(r'^issue_evaluation/$', IssueEvaluationView.as_view(),
        name='issue_evaluation'),
    url(r'^issue_evaluation/result/$', IssueEvaluationResultView.as_view(),
        name="issue_evaluation_results"),
]
