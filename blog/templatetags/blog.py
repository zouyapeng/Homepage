# -*- coding: utf-8 -*-
import random
from django import template

from ..models import Post,Category,Notice,Comment

register = template.Library()


@register.inclusion_tag('blog/month_links_snippet.html')
def render_month_links():
    return {
        'dates': Post.objects.published().datetimes('pub_date', 'month', order='DESC'),
        # 'dates': Post.objects.published().dates('pub_date', 'month', order='DESC'),
    }

@register.inclusion_tag('blog/category_link_snippet.html')
def render_category_links():
    return {
        'categorys': Category.objects.all(),
    }

@register.inclusion_tag('blog/notice_link_snippet.html')
def render_notice_links():
    return {
        'notice': Notice.objects.last(),
    }

@register.inclusion_tag('blog/assess_link_snippet.html')
def render_assess_links():
    return {
        'assesses': Comment.objects.order_by('-create_date')[:5],
        # 'assesses': Comment.objects.all()[-5s:],
    }

@register.simple_tag
def random_label_color():
    colors = ['label-danger', 'label-warning', 'label-info', 'label-success', 'label-primary', 'label-default']
    return random.choice(colors)

@register.inclusion_tag('blog/friendly_link_snippet.html')
def render_friendly_links():
    return {}
