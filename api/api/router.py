from rest_framework import routers

from api.users.views import GroupViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
