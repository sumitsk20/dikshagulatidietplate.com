from django import template
from django.shortcuts import get_list_or_404
from ..models import Category, Tag, Post

register = template.Library()

@register.inclusion_tag('blog/category_box.html')
def category_box(self=None):
        return {
                'all_category': get_list_or_404(Category),
        }

@register.inclusion_tag('blog/tag_cloud.html')
def tag_cloud(self=None):
        return {
                'all_tag': get_list_or_404(Tag),
        }

@register.inclusion_tag('blog/article_widget_group.html')
def article_widget_group(self=None):
	latest_post = Post.objects.active().order_by('-published_on')[:5]
	recently_updated = Post.objects.active().order_by('-last_updated')[:5]
	trending_post = Post.objects.active().order_by('-published_on')[:5]
        return {
                'latest_post':latest_post,
                'recently_updated': recently_updated,
                'trending_post':trending_post,
        }
