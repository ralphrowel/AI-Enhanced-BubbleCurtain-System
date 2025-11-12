from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExampleViewSet, DeviceViewSet, SignalViewSet

router = DefaultRouter()
router.register(r'example', ExampleViewSet, basename='example')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'signals', SignalViewSet, basename='signal')

urlpatterns = [
    path('', include(router.urls)),
]
