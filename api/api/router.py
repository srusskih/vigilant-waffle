from rest_framework import routers

from applications.views import ApplicantCommentViewSet, ApplicantViewSet
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"applicants", ApplicantViewSet, basename="applicant")
router.register(
    r"applicants/(?P<applicant_id>\d+)/comments",
    ApplicantCommentViewSet,
    basename="applicantcomment",
)
