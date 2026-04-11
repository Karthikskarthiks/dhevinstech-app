from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

# DRF Router
router = DefaultRouter()
router.register(r'labours', views.LabourViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'workdetails-api', views.WorkDetailViewSet)

urlpatterns = [

    # ------recent db ----
    path('keep-alive/', keep_alive),

    # 🔥 Home URL → Add Page
    path('', views.add_workdetail, name='home'),

    # WorkDetail Pages
    path('list/', views.workdetail_list, name='workdetail_list'),
    path('detail/<int:pk>/', views.workdetail_detail, name='workdetail_detail'),
    path('edit/<int:pk>/', views.edit_workdetail, name='edit_workdetail'),
    path('delete/<int:pk>/', views.delete_workdetail, name='delete_workdetail'),
    path('export/csv/', views.export_workdetails_csv, name='export_workdetails_csv'),

    # Favicon
    path('favicon.ico', views.favicon, name='favicon'),

    # API Routes
    path('api/', include(router.urls)),
]