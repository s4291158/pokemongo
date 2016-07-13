from django.db import models


class Route(models.Model):
    name = models.CharField(
        max_length=40,
        blank=True
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Route ' + self.id


class Location(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE
    )

    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lng)
