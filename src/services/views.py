from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.core.urlresolvers import reverse
from .models import Service


# Create your views here.
def services(request):
	all_services = Service.objects.active().order_by('name')
	context = Context({
		'all_services':all_services,
		'title': "Services"
		})

	return render(request, "services/services_list.html",context)

def service_detail(request , service_slug):
	service = get_object_or_404(Service,slug=service_slug )
	context = Context({
		'service':service,
		'title': service.name,
		})

	return render(request, "services/services_detail.html",context)