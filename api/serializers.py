from rest_framework import serializers

from api.templatemodels import (
    RouteTemplate,
    LocationTemplate
)


class RouteTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteTemplate


class LocationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationTemplate
