from django.conf.urls import url

from api.views import (
    route_list,
    route_detail,
    location_list,
    location_detail
)


urlpatterns = [
    url(r'^route/$', route_list, name='route_list'),
    url(r'^route/(?P<pk>[0-9]+)/?$', route_detail, name='route_detail'),
    url(r'^location/$', location_list, name='location_list'),
    url(r'^location/(?P<pk>[0-9]+)/?$', location_detail, name='location_detail'),
]
