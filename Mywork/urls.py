from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    LabourViewSet, SiteViewSet, WorkDetailViewSet,
    workdetail_list, add_workdetail, delete_workdetail

)

# DRF API Router
router = DefaultRouter()
router.register(r'labours', LabourViewSet)
router.register(r'sites', SiteViewSet)
router.register(r'workdetails', WorkDetailViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    

    # Template pages
    path('workdetails/', workdetail_list, name='workdetail_list'),
    path('', views.home, name='home'),
    path('', add_workdetail, name='add_workdetail'),
    path('workdetails/delete/<int:pk>/', delete_workdetail, name='delete_workdetail'),
]
