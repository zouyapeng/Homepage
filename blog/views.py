from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from blog.models import Post, Category

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-update_date')