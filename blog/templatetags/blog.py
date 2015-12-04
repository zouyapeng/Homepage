import random
from django import template

from ..models import Post,Category

register = template.Library()

@register.inclusion_tag('blog/month_links_snippet.html')
def render_month_links():
    return {
        'dates': Post.objects.published().datetimes('pub_date', 'month', order='DESC'),
    }

@register.inclusion_tag('blog/category_link_snippet.html')
def render_category_links():
    return {
        'categorys': Category.objects.all(),
    }

@register.simple_tag
def random_label_color():
    colors = ['label-danger', 'label-warning', 'label-info', 'label-success', 'label-primary', 'label-default']
    return random.choice(colors)
