from django import template
from django.shortcuts import render,get_list_or_404,get_object_or_404
from ..models import Service

register = template.Library()

@register.inclusion_tag('layout/navbar.html')
def navigation(self=None):
        return {
                'all_services': Service.objects.active()[:3],
        }