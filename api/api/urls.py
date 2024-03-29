from django.urls import include, path

from .router import router

urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "api/auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
]
