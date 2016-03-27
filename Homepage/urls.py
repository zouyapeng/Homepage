"""Homepage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from accounts import urls as accounts_urls
from blog import urls as blog_urls
from django.views.generic import RedirectView,TemplateView
from settings import MEDIA_ROOT


urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('blog:index'), permanent=True), name='index'),
    url(r'^admin/$', TemplateView.as_view(template_name='admin.html')),
    url(r'^accounts/',include(accounts_urls, namespace='account')),
    url(r'^fucktv/', include(admin.site.urls)),
    url(r'^blog/',include(blog_urls, namespace='blog')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
]
