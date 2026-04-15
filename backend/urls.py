from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.views import home
from django.conf import settings
from django.conf.urls.static import static
from core.admin_views import ui_settings_view


schema_view = get_schema_view(
   openapi.Info(title="API", default_version='v1', description="API docs"),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/ui-settings/", ui_settings_view, name="admin_ui_settings"),

    path("admin/", admin.site.urls),
    path("", home),
    path("accounts/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("swagger<format>.json", schema_view.without_ui(cache_timeout=0)),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
