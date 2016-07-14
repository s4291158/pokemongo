from django.conf.urls import url

from api.views import (
    GetLocation
)

urlpatterns = [
    url(r'^location/$', GetLocation.as_view())
]
