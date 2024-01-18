from datetime import datetime

from rest_framework import permissions, viewsets

from applications.models import Applicant, ApplicantComment
from applications.serializers import (
    ApplicantCommentSerializer,
    ApplicantSerializer,
)


class ApplicantModelsPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class ApplicantViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [ApplicantModelsPermissions]

    def perform_update(self, serializer: ApplicantSerializer):
        instance: Applicant = serializer.instance
        if (
            instance.approve_status
            != serializer.validated_data["approve_status"]
        ):
            serializer.save(
                approve_status_changed_by=self.request.user,
                approve_status_changed_at=datetime.now(),
            )
        else:
            serializer.save()


class CommentsModelsPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
    }


class ApplicantCommentViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    lookup_url_kwarg = "applicant_id"
    queryset = ApplicantComment.objects.all()
    serializer_class = ApplicantCommentSerializer
    permission_classes = [
        CommentsModelsPermissions,
    ]

    def get_queryset(self):
        return self.queryset.filter(applicant_id=self.kwargs["applicant_id"])

    def perform_create(self, serializer: ApplicantCommentSerializer):
        serializer.save(
            author=self.request.user,
            applicant_id=self.kwargs["applicant_id"],
        )
