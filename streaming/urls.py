from django.urls import path
from . import views

urlpatterns = [
    path("stream/<str:room_name>/broadcast/", views.stream_broadcaster, name="stream_broadcast"),
    path("stream/<str:room_name>/view/", views.stream_viewer, name="stream_view"),
]
