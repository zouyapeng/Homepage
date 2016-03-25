# -*- coding: utf-8 -*-
import os
import random
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
def upload(instance, filename):
    file_name = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    return os.path.join(settings.UPLOAD_TO, file_name)

def random_default_avatar():
    default = random.randint(1, 46)
    return "upload/default/%02d.png" % (default)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    enable_email = models.BooleanField(default=False)
    avatar = models.ImageField("avatar", upload_to=upload, default='upload/default.png')
    sex = models.CharField(choices=(('man', 'man'), ('female', 'female'), ('secrecy', 'secrecy')), max_length=10,
                           default='secrecy')
    birthday = models.DateField(null=True, blank=True)
    signature = models.TextField(null=True, blank=True)
    qq = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.user.username

class Company(models.Model):
    name = models.CharField(max_length=128)
    in_time = models.DateField()
    out_time = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=128)
    duty = models.TextField()
    leaving_reasons = models.TextField()

    def __unicode__(self):
        return self.name

class Project(models.Model):
    company = models.ForeignKey(Company, related_name='company_project')
    name = models.CharField(max_length=128)
    start_time = models.DateField()
    end_time = models.DateField()
    person_num = models.IntegerField()
    description = models.TextField()
    duty = models.TextField()

    def __unicode__(self):
        return self.name

