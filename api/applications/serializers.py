from rest_framework import serializers

from applications.models import Applicant, ApplicantComment


class ApplicantSerializer(serializers.ModelSerializer):
    comments = serializers.HyperlinkedIdentityField(
        view_name="applicantcomment-list",
        lookup_url_kwarg="applicant_id",
        read_only=True,
    )

    class Meta:
        model = Applicant
        fields = (
            "url",
            "comments",
            "id",
            "created_at",
            "updated_at",
            "name",
            "email",
            "phone",
            "job_title",
            "resume_url",
            "approve_status",
            "approve_status_changed_by",
            "approve_status_changed_at",
        )
        read_only_fields = (
            "id",
            "comments",
            "created_at",
            "updated_at",
            "approve_status_changed_by",
            "approve_status_changed_at",
        )


class ApplicantCommentSerializer(serializers.ModelSerializer):
    applicant = serializers.HyperlinkedRelatedField(
        view_name="applicant-detail",
        read_only=True,
    )
    author = serializers.HyperlinkedRelatedField(
        view_name="user-detail",
        read_only=True,
    )

    class Meta:
        model = ApplicantComment
        fields = (
            "id",
            "created_at",
            "applicant",
            "author",
            "comment",
        )
        read_only_fields = (
            "id",
            "created_at",
            "author",
        )
