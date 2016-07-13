from django.db import models


class Route(models.Model):
    name = models.CharField(
        max_length=40,
        blank=True
    )

    index = models.IntegerField(
        default=0  # 0 means not started yet
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Route ' + str(self.id)


class Stop(models.Model):
    route = models.ForeignKey(
        'api.Route',
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField(
        default=1
    )

    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lng)

    class Meta:
        unique_together = (('route', 'order'),)
