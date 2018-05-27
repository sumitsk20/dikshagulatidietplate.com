from django import template
from django.shortcuts import render,get_list_or_404,get_object_or_404
from ..forms import AppointmentForm

register = template.Library()

@register.inclusion_tag('services/appointment_form.html')
def appointment_form(self=None):
	form = AppointmentForm()
        return {"form":form}