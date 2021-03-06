from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from accounts.views import LoginView, LogoutView, RegistrationView, AboutView, Profile


urlpatterns = [
    url(r'^signup/$', RegistrationView.as_view(),name='signup'),
    url(r'^login/$', LoginView.as_view(),name='login'),
    url(r'^logout/$', LogoutView.as_view(),name='logout'),
    url(r'^profile/$', Profile.as_view(),name='profile'),
    url(r'^about/$', AboutView.as_view(),name='about')
]
