from django.conf.urls import url
from django.views.generic import TemplateView
from blog.views import IndexView


urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='blog/index.html'), name='index'),
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^(?P<pk>\d+)/$', BlogDetailView.as_view(), name='blog_detail'),
]