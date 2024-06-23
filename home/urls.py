from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SmileCenterViewSet
from .views import ZoneListView
from .views import ServiceListView
from .views import CenterTypeListView
from django.contrib import admin
from django.urls import path, include

#Router for the viewset
router = DefaultRouter()
router.register(r'smilecenters', SmileCenterViewSet, basename='smilecenter')


urlpatterns = [
    path('', views.users, name = 'users'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('zones/', ZoneListView.as_view(), name='zone-list'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('center-types/', CenterTypeListView.as_view(), name='center-type-list'),

]