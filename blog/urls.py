from django.conf.urls import url
from django.views.generic import TemplateView
import views


urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='blog/index.html'), name='index'),
    url(r'^$', views.BlogArchiveIndexView.as_view(), name='index'),
    url(
        r'^category/(?P<category_id>\d+)/$',
        views.BlogArchiveCategoryView.as_view(),
        name="archive-category"
    ),
    url(
        r'^(?P<year>\d{4})/$',
        views.BlogYearArchiveView.as_view(),
        name="archive-year"
    ),
    url(
        r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        views.BlogMonthArchiveView.as_view(),
        name="archive-month"
    ),
    url(
        r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$',
        views.BlogDateDetailView.as_view(),
        name="post"
    ),
]