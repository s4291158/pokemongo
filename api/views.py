from rest_framework import viewsets

from api.models import (
    Route,
    Location
)

from api.serializers import (
    RouteSerializer,
    LocationSerializer
)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


location_list = LocationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

location_detail = LocationViewSet.as_view({
     'get': 'retrieve',
     'put': 'update',
     'patch': 'partial_update',
     'delete': 'destroy'
})


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


route_list = RouteViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

route_detail = RouteViewSet.as_view({
     'get': 'retrieve',
     'put': 'update',
     'patch': 'partial_update',
     'delete': 'destroy'
})


