from django.conf.urls import url

from api.views import (
    route_list,
    route_detail,
)

# <extra imports block>
from api.views import (
    GetLocation
)

urlpatterns = [
    url(r'^route/$', route_list, name='route_list'),
    url(r'^route/(?P<pk>[0-9]+)/?$', route_detail, name='route_detail'),
    url(r'^location/$', GetLocation.as_view())
]
