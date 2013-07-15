from django.contrib import admin
from gezimeclise.causes.models import Cause, Comments


class CauseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'region', 'is_active')
    list_editable = ('is_active',)
admin.site.register(Cause, CauseAdmin)


admin.site.register(Comments)
