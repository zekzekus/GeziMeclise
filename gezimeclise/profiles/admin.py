from django.contrib import admin
from gezimeclise.profiles.models import GeziUser


class GeziUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(GeziUser, GeziUserAdmin)