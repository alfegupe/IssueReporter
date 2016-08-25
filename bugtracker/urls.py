from django.conf.urls import url
from .views import IndexView, LoginView, LogoutView, IssueListView, \
    IssueCreateView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^home/$', IssueListView.as_view(), name='home'),
    url(r'^create/$', IssueCreateView.as_view(), name='create'),
]

