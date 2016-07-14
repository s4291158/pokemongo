from api.models import (
    Route,
    Stop,
    Current
)

from pokemongo.settings import API_SECRET
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class GetLocation(APIView):
    def get(self, request):
        context = {}
        if 'secret' in request.GET and request.GET['secret'] == API_SECRET:
            current_set = Current.objects.all()
            if current_set.count() != 1:
                if current_set.count() == 0:
                    context['data'] = 'No current route specified'
                elif current_set.count() > 1:
                    context['data'] = 'More than one current route specified'
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                current = current_set[0]

            old_index = current.route_index
            if old_index == current.route.stop_set.count():
                new_index = 1
            else:
                new_index = old_index + 1

            current.route_index = new_index
            current.save()

            stop = Stop.objects.get(route=current.route, order=new_index)

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
