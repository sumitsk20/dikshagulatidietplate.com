from django.conf.urls import url
from . import views


urlpatterns = [
	#home-page
    #url(r'^$', views.index , name="index" ),
    url(r'^$', views.services , name="services" ),
    url(r'^(?P<service_slug>[a-zA-Z0-9-]+)/$', views.service_detail , name="service_detail" ),


]
