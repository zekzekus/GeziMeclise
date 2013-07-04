from django.contrib import admin
from gezimeclise.profiles.models import GeziUser
from gezimeclise.profiles.models import Region, Report


class GeziUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(GeziUser, GeziUserAdmin)
admin.site.register(Region)
admin.site.register(Report)
