from django.contrib import admin
from django.urls import path, include
from Mywork.views import add_workdetail
from django.http import HttpResponse
import sys

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', add_workdetail, name='add_workdetail'),
    path('Mywork/', include("Mywork.urls")),
    
    # Temporary route to check Python version
    path("check-python/", lambda request: HttpResponse(sys.version)),
]