from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# DRF Router
router = DefaultRouter()
router.register(r'labours', views.LabourViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'workdetails-api', views.WorkDetailViewSet)

urlpatterns = [

    # 🔥 Home URL → Add Page
    path('', views.add_workdetail, name='home'),

    # WorkDetail Pages
    path('list/', views.workdetail_list, name='workdetail_list'),
    path('edit/<int:pk>/', views.edit_workdetail, name='edit_workdetail'),
    path('delete/<int:pk>/', views.delete_workdetail, name='delete_workdetail'),

    # API Routes
    path('api/', include(router.urls)),
]