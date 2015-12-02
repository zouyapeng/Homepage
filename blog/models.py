import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=128)
    create_data = models.DateTimeField(editable=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(User,related_name='user_post')
    category = models.ManyToManyField(Category, related_name='category_post')
    content = models.TextField()
    create_date = models.DateTimeField(editable=False, auto_now_add=True)
    update_date = models.DateTimeField(editable=False, auto_now=True)

    def __unicode__(self):
        return self.title