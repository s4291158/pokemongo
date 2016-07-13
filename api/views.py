from rest_framework import viewsets

from api.templatemodels import (
    RouteTemplate,
    LocationTemplate
)

from api.serializers import (
    RouteTemplateSerializer,
    LocationTemplateSerializer
)


class RouteTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RouteTemplate.objects.all()
    serializer_class = RouteTemplateSerializer


route_template_list = RouteTemplateViewSet.as_view({
    'get': 'list',
})

route_template_detail = RouteTemplateViewSet.as_view({
    'get': 'retrieve',
})


class LocationTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LocationTemplate.objects.all()
    serializer_class = LocationTemplateSerializer


location_template_list = LocationTemplateViewSet.as_view({
    'get': 'list',
})

location_template_detail = LocationTemplateViewSet.as_view({
    'get': 'retrieve',
})
