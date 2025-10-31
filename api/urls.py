from rest_framework.routers import DefaultRouter
from .views import ExampleViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"examples", ExampleViewSet, basename="example")

urlpatterns = [
    path("", include(router.urls)),
]
