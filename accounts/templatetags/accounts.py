# -*- coding: utf-8 -*-
import random
from django import template

from ..models import Company, Project, UserProfile

register = template.Library()


# @register.inclusion_tag('blog/month_links_snippet.html')
# def render_month_links():
#     return {
#         'dates': Post.objects.published().datetimes('pub_date', 'month', order='DESC'),
#         # 'dates': Post.objects.published().dates('pub_date', 'month', order='DESC'),
#     }
#
# @register.inclusion_tag('blog/category_link_snippet.html')
# def render_category_links():
#     return {
#         'categorys': Category.objects.all(),
#     }
#
# @register.inclusion_tag('blog/notice_link_snippet.html')
# def render_notice_links():
#     return {
#         'notice': Notice.objects.last(),
#     }
#
# @register.inclusion_tag('blog/assess_link_snippet.html')
# def render_assess_links():
#     return {
#         'assesses': Comment.objects.all()[:5],
#     }

@register.inclusion_tag('accounts/adout_work_link_snippet.html')
def render_work_links(tag):
    return {
        'tag':tag,
        'companys': Company.objects.all(),
        'projects':Company.objects.get(id=tag).company_project.all()
    }
