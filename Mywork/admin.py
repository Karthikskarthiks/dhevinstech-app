from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Labour, Site, WorkDetail,Vendor

admin.site.register(Labour)
admin.site.register(Vendor)
admin.site.register(Site)
admin.site.register(WorkDetail)

