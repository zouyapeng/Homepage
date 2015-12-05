from django.views.generic import(
    ArchiveIndexView, DateDetailView, MonthArchiveView, YearArchiveView, ListView, CreateView
)

from models import Post, Category


# Create your views here.
class BlogViewMixin(object):
    date_field = 'pub_date'

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        else:
            return Post.objects.published()

    def get_context_data(self, **kwargs):
        context = super(BlogViewMixin, self).get_context_data(**kwargs)
        # context['notice'] = Category.objects.last()
        return context

class BlogArchiveIndexView(BlogViewMixin, ArchiveIndexView):
    pass

class BlogArchiveCategoryView(BlogViewMixin, ListView):
    template_name = 'blog/post_archive_category.html'
    queryset = []

    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs['category'])
        if self.request.user.is_staff:
            return Post.objects.filter(category=category)
        else:
            return Post.objects.published().filter(category=category)

class BlogDateDetailView(BlogViewMixin, DateDetailView):
    pass

class BlogMonthArchiveView(BlogViewMixin, MonthArchiveView):
    pass

class BlogYearArchiveView(BlogViewMixin, YearArchiveView):
    make_object_list = True