import os
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
def upload(instance, filename):
    file_name = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    return os.path.join(settings.UPLOAD_TO, file_name)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    avatar = models.ImageField("avatar", upload_to=upload, default="default.png")
    sex = models.CharField(choices=(('man', 'man'), ('female', 'female'), ('secrecy', 'secrecy')), max_length=10,
                           default='secrecy')
    birthday = models.DateField(null=True, blank=True)
    signature = models.TextField(null=True, blank=True)
    qq = models.CharField(null=True, blank=True, max_length=255)

