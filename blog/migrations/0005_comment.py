# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_auto_20151205_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('context', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(related_name='post_comment', to='blog.Post')),
                ('user', models.ForeignKey(related_name='user_comment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-create_date',),
                'get_latest_by': 'create_date',
            },
        ),
    ]
