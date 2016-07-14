from django.contrib import admin
from api.models import Route, Stop, Current


class StopInline(admin.TabularInline):
    model = Stop


class RouteAdmin(admin.ModelAdmin):
    inlines = [
        StopInline
    ]


class CurrentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        count = Current.objects.all.count()
        if count == 0:
            return True
        else:
            return False


admin.site.register(Route, RouteAdmin)
admin.site.register(Current)
