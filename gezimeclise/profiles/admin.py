from django.contrib import admin
from gezimeclise.profiles.models import GeziUser
from gezimeclise.profiles.models import Region

class GeziUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(GeziUser, GeziUserAdmin)
admin.site.register(Region)