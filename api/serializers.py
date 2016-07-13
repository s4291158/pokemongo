from rest_framework import serializers

from api.models import (
    Route,
    Location
)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route


