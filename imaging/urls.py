from django.urls import path
from . import views

urlpatterns = [
    path("capture/", views.capture_page, name="capture_page"),
    path("api/capture/", views.CaptureUploadView.as_view(), name="capture_upload"),
]
