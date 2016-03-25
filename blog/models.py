# -*- coding: utf-8 -*-

import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from uuslug import slugify

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.active().filter(pub_date__lte=timezone.now())

    def active(self):
        return self.filter(is_active=True)

class Notice(models.Model):
    headline = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(editable=False, auto_now_add=True)

    def __unicode__(self):
        return self.headline

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

class Category(models.Model):
    name = models.CharField(max_length=128)
    create_data = models.DateTimeField(editable=False, auto_now_add=True)

    def get_absolute_url(self):
        kwargs = {
            'category': self.name,
        }
        return reverse('blog:archive-category', kwargs=kwargs)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    headline = models.CharField(max_length=200)
    slug = models.SlugField(editable=False, unique_for_date='pub_date')
    is_active = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, related_name='category_post')
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(editable=False, auto_now_add=True)
    update_date = models.DateTimeField(editable=False, auto_now=True)
    author = models.ForeignKey(User,related_name='user_post')

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.headline)
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        kwargs = {
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%b').lower(),
            'day': self.pub_date.strftime('%d').lower(),
            'slug': self.slug,
        }
        return reverse('blog:post', kwargs=kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comment')
    post = models.ForeignKey(Post, related_name='post_comment')
    context = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-create_date',)
        get_latest_by = 'create_date'

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        comments = self.post.post_comment.all()
        emails = list(set([comment.user.email for comment in comments ]))
        emails.remove(self.user.email)
        emails.remove(self.post.author.email)

    def get_absolute_url(self):
        kwargs = {
            'year': self.post.pub_date.year,
            'month': self.post.pub_date.strftime('%b').lower(),
            'day': self.post.pub_date.strftime('%d').lower(),
            'slug': self.post.slug,
        }
        return reverse('blog:post', kwargs=kwargs)

    def __unicode__(self):
        return self.create_date.strftime('%H:%M:%S')
