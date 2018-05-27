from django.conf.urls import url
from . import views


urlpatterns = [
	#home-page
    #url(r'^$', views.index , name="index" ),
    url(r'^blog/$', views.post_list , name="index" ),
    url(r'^faq/$', views.faq , name="faq" ),
    url(r'^category/(?P<cat_slug>[a-zA-Z0-9-]+)/$', views.category_list_view , name="category" ),
    url(r'^tag/(?P<tag_slug>[a-zA-Z0-9-]+)/$', views.tag_list_view , name="tag" ),
    url(r'^(?P<post_slug>[a-zA-Z0-9-]+)/$', views.post_detail , name="post" ),

]
