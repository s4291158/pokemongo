from django.conf.urls import url

from api.views import (
    route_template_list,
    route_template_detail,
    location_template_list,
    location_template_detail
)


urlpatterns = [
    url(r'^route_template/$', route_template_list, name='route_template_list'),
    url(r'^route_template/(?P<pk>[0-9]+)/?$', route_template_detail, name='route_template_detail'),
    url(r'^location_template/$', location_template_list, name='location_template_list'),
    url(r'^location_template/(?P<pk>[0-9]+)/?$', location_template_detail, name='location_template_detail'),
]
