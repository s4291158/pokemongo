from rest_framework import viewsets

from api.models import (
    Route,
    Stop
)

from api.serializers import (
    RouteSerializer,
)

# <extra imports block>
from pokemongo.settings import API_SECRET
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# </extra>


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


route_list = RouteViewSet.as_view({
    'get': 'list',
})

route_detail = RouteViewSet.as_view({
    'get': 'retrieve',
})


# <extra views block>
class GetLocation(APIView):
    def get(self, request):
        context = {}
        if 'secret' in request.GET and request.GET['secret'] == API_SECRET:
            try:
                route = Route.objects.get(id=request.GET['route'])
            except KeyError:
                context['data'] = 'No route specified'
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            except (Route.DoesNotExist, ValueError):
                context['data'] = 'Route {} does not exist'.format(
                    request.GET['route']
                )
                return Response(context, status=status.HTTP_404_NOT_FOUND)

            old_index = route.index
            if old_index == route.stop_set.count():
                new_index = 1
            else:
                new_index = old_index + 1

            route.index = new_index
            route.save()

            stop = Stop.objects.get(route=route, order=route.index)

            context['data'] = {
                'index': new_index,
                'lat': stop.lat,
                'lng': stop.lng
            }
            return Response(context, status=status.HTTP_200_OK)

        else:
            context['data'] = 'Please supply api secret'
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

# </extra>
