from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from accounts.views import LoginView, LogoutView, RegistrationView


urlpatterns = [
    url(r'^signup/$', RegistrationView.as_view(),name='signup'),
    url(r'^login/$', LoginView.as_view(),name='login'),
    url(r'^logout/$', LogoutView.as_view(),name='logout')
    # url(r'^index/$',login_required(TemplateView.as_view(template_name='base.html'), login_url=reverse_lazy("accounts:login")), name='index'),
]
