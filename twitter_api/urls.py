from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from dj_rest_auth.views import PasswordResetConfirmView
from core_apps.users.views import CustomUserDetailsView


schema_view = get_schema_view(
    openapi.Info(
        title="Twitter Clone API",
        default_version="v1",
        description="API endpoint for Twitter Clone API",
        contact=openapi.Contact(email="amirwmr@yahoo.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/user", CustomUserDetailsView.as_view(), name="user_details"),
    path("api/v1/auth/", include("dj_rest_auth.urls"),),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls"),),
    path("api/v1/auth/password/reset/confirm/<uuid64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("api/v1/profile/", include("core_apps.profiles.urls"))
]

admin.site.site_header = "Twitter Clone API Admin"

admin.site.site_title = "Twitter Clone API Portal"

admin.site.index_title = "Welcome to Twitter Clone API Portal"