from django.contrib import admin
from .models import Labour, Site, WorkDetail, Vendor

@admin.register(WorkDetail)
class WorkDetailAdmin(admin.ModelAdmin):
    list_display = ['date', 'vendor', 'site']
    filter_horizontal = ['labours']  # safer ManyToMany handling

admin.site.register(Labour)
admin.site.register(Vendor)
admin.site.register(Site)