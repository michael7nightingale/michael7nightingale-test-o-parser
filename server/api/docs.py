from django.urls import path, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg.openapi import Info, License


schema_view = get_schema_view(
    info=Info(
        title="Ozone Parser API",
        default_version="1",
        license=License("OFFICIAL")
    ),
    public=True,
    permission_classes=[AllowAny]
)


urlpatterns = [
    re_path(r'swagger/(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='swagger_format'),
    path(r"swagger/", schema_view.with_ui("swagger", cache_timeout=0), name='swagger'),
    path(r"redoc/", schema_view.with_ui("redoc", cache_timeout=0), name='redoc')
]
