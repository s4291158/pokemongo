from rest_framework import serializers

from api.models import (
    Route,
    Stop
)


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop


class RouteSerializer(serializers.ModelSerializer):
    stop_set = StopSerializer(many=True)

    class Meta:
        model = Route

