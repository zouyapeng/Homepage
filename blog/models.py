import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.active().filter(pub_date__lte=datetime.datetime.now())

    def active(self):
        return self.filter(is_active=True)

class Category(models.Model):
    name = models.CharField(max_length=128)
    create_data = models.DateTimeField(editable=False, auto_now_add=True)

    def get_absolute_url(self):
        kwargs = {
            'category_id': self.id,
        }
        return reverse('blog:archive-category', kwargs=kwargs)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    headline = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='pub_date')
    is_active = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, related_name='category_post')
    content = models.TextField()
    pub_date = models.DateTimeField()
    create_date = models.DateTimeField(editable=False, auto_now_add=True)
    update_date = models.DateTimeField(editable=False, auto_now=True)
    author = models.ForeignKey(User,related_name='user_post')

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        kwargs = {
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%b').lower(),
            'day': self.pub_date.strftime('%d').lower(),
            'slug': self.slug,
        }
        return reverse('blog:post', kwargs=kwargs)