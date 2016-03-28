# -*- coding: utf-8 -*-
from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget
from django import forms


from models import Post, Category, Notice, Comment
# Register your models here.
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Post
        fields = '__all__'

class NoticeForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Notice
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['headline', 'create_date', 'pub_date','author', 'is_active']
    filter_horizontal = ('category',)

class NoticeAdmin(admin.ModelAdmin):
    form = NoticeForm
    list_display = ['headline']

admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Notice, NoticeAdmin)
