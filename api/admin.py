from django.contrib import admin
from api.models import Route, Stop


class StopInline(admin.TabularInline):
    model = Stop


class RouteAdmin(admin.ModelAdmin):
    inlines = [
        StopInline
    ]


admin.site.register(Route, RouteAdmin)
