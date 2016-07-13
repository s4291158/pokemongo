from django.db import models


class RouteTemplate(models.Model):
    name = models.CharField(
        max_length=40,
        blank=True
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Route ' + str(self.id)


class LocationTemplate(models.Model):
    route = models.ForeignKey(
        RouteTemplate,
        on_delete=models.CASCADE
    )

    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lng)
