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
    avatar = models.ImageField("avatar", upload_to=upload, default='upload/default.png')
    sex = models.CharField(choices=(('man', 'man'), ('female', 'female'), ('secrecy', 'secrecy')), max_length=10,
                           default='secrecy')
    birthday = models.DateField(null=True, blank=True)
    signature = models.TextField(null=True, blank=True)
    qq = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.user.username

