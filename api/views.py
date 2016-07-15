from api.models import (
    Stop,
    Current
)

from pokemongo.settings import API_SECRET
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class GetLocation(APIView):
    def __init__(self):
        super(GetLocation, self).__init__()
        self.current = None
        self.max_index = None

    def get(self, request):
        context = {}
        if 'secret' in request.GET and request.GET['secret'] == API_SECRET:
            self.set_current()
            self.move()
            context['data'] = self.get_response()
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['data'] = 'Please supply api secret'
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

    def move(self):
        if self.current.travel_forward:
            self.move_forward()
        else:
            self.move_backward()
        self.set_travel_direction()
        self.check_index_reset()
        self.current.save()

    def set_current(self):
        current_set = Current.objects.all()
        if current_set.count() != 1:
            context = {}
            if current_set.count() == 0:
                context['data'] = 'No current route specified'
            elif current_set.count() > 1:
                context['data'] = 'More than one current route specified'
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            self.current = current_set[0]
            self.max_index = self.current.route.stop_set.count()

    def set_travel_direction(self):
        if self.current.backwards_loop and self.current.route_index == 1:
            self.current.travel_forward = True
        elif self.current.backwards_loop and self.current.route_index == self.max_index:
            self.current.travel_forward = False

    def check_index_reset(self):
        if self.current.route_index > self.max_index and not self.current.backwards_loop:
            self.current.route_index = 1

    def move_forward(self):
        if self.current.route_index < self.max_index:
            self.current.route_index += 1

    def move_backward(self):
        if self.current.route_index > 1:
            self.current.route_index -= 1

    def get_response(self):
        stop = Stop.objects.get(route=self.current.route, order=self.current.route_index)
        response = {
            'index': self.current.route_index,
            'travel': 'forward' if self.current.travel_forward else 'backward',
            'backwards loop': self.current.backwards_loop,
            'lat': stop.lat,
            'lng': stop.lng
        }
        return response
