# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import login_required
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic import(
    ArchiveIndexView, DateDetailView, MonthArchiveView, YearArchiveView, ListView, CreateView, RedirectView
)

from models import Post, Category, Comment

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

    def get_context_data(self, **kwargs):
        context = super(BlogViewMixin, self).get_context_data(**kwargs)
        context['category'] =  Category.objects.get(name=self.kwargs['category'])
        return context

class BlogDateDetailView(BlogViewMixin, DateDetailView):
    pass

class BlogMonthArchiveView(BlogViewMixin, MonthArchiveView):
    pass

class BlogYearArchiveView(BlogViewMixin, YearArchiveView):
    make_object_list = True

@login_required
def post_new_comment(request):
    if request.method == 'POST':
        redirect_to = request.GET['next']
        user = request.user
        post = Post.objects.get(id=int(request.POST['post_id']))
        context = request.POST['context']

        comment = Comment.objects.create(user=user, post=post, context=context)
        comment.save()

        return HttpResponseRedirect(redirect_to)

    return HttpResponseRedirect(force_text(reverse_lazy('blog:index')))
