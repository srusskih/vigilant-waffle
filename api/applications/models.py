from django.contrib.auth import get_user_model
from django.db import models


class ApprovalStatus(models.IntegerChoices):
    PENDING = 0, "Pending"
    APPROVED = 1, "Approved"
    REJECTED = 2, "Rejected"


class Applicant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    job_title = models.CharField(max_length=254)
    resume_url = models.URLField(max_length=254)
    approve_status = models.PositiveSmallIntegerField(
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    approve_status_changed_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    approve_status_changed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]


class ApplicantComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    applicant = models.ForeignKey(
        "applications.Applicant",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    comment = models.TextField()

    class Meta:
        ordering = ["created_at"]
