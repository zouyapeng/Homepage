# -*- coding: utf-8 -*-

import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from uuslug import slugify
import thread

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
    hitcount = models.IntegerField(default=0)
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
        ordering = ('create_date',)
        get_latest_by = 'create_date'

    def generate_message(self):
        message = """\
            <html>
              <head></head>
              <body>
                <p>%s<br>
                   %s<br>
                   <a href="%s">%s</a>
                </p>
              </body>
            </html>
            """ % (u'您好!',
                   u'你最近评价的文章有了新的评价',
                   u'http://blog.zouyapeng.website' + self.post.get_absolute_url(),
                   self.post.headline)
        return message

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        now = datetime.datetime.now()
        prev_day = now - datetime.timedelta(days=30)
        comments = self.post.post_comment.filter(create_date__range=(prev_day, now))
        users = []
        for comment in comments:
            if comment.user not in users:
                users.append(comment.user)

        if self.post.author not in users:
            users.append(self.post.author)

        users.remove(self.user)

        for user in users:
            if user.user_profile.enable_email is True:
                thread.start_new_thread(user.user_profile.email_user, ('[Zouyapeng 博客]你有一条新消息', self.generate_message()))
                # user.user_profile.email_user()

    def get_absolute_url(self):
        kwargs = {
            'year': self.post.pub_date.year,
            'month': self.post.pub_date.strftime('%b').lower(),
            'day': self.post.pub_date.strftime('%d').lower(),
            'slug': self.post.slug,
        }
        return reverse('blog:post', kwargs=kwargs)

    def __unicode__(self):
        return "%s:%s" % (self.post.slug, self.context)
