from collections.abc import Iterable

import pytest
from django.contrib.auth.models import Permission, User
from rest_framework.test import APIClient

from applications.models import Applicant, ApplicantComment, ApprovalStatus

client = APIClient()


def _permissions_to_objects(permissions: list[str]) -> Iterable[Permission]:
    apps = set()
    code_names = set()
    for permission in permissions:
        app_label, codename = permission.split(":")
        apps.add(app_label)
        code_names.add(codename)
    permissions_objects = Permission.objects.filter(
        content_type__app_label__in=apps, codename__in=code_names
    )
    return permissions_objects


@pytest.fixture
def create_user(faker):
    def _func(permissions: list[str]) -> User:
        user: User = User.objects.create(username=faker.email())
        user.user_permissions.set(
            _permissions_to_objects(permissions=permissions)
        )
        return user

    return _func


@pytest.fixture
def user(django_user_model):
    yield django_user_model.objects.create(username="Test User")


@pytest.fixture
def applicant():
    yield Applicant.objects.create(
        **{
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "job_title": "Software Engineer",
            "resume_url": "https://example.com/resume.pdf",
        }
    )


@pytest.mark.django_db
def test_create_applicant(create_user):
    user = create_user(["applications:add_applicant"])

    payload = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "job_title": "Software Engineer",
        "resume_url": "https://example.com/resume.pdf",
    }

    client.force_login(user)
    response = client.post("/api/applicants/", payload)

    assert response.status_code == 201
    applicant = Applicant.objects.first()
    assert applicant is not None


@pytest.mark.django_db
def test_user_not_allowed_create_applicant(create_user):
    user = create_user(["api:view_applicant"])

    payload = {}

    client.force_login(user)
    response = client.post("/api/applicants/", payload)

    assert response.status_code == 403


@pytest.mark.django_db
def test_get_applicant(create_user, applicant):
    user = create_user(["applications:view_applicant"])
    client.force_login(user)
    response = client.get(f"/api/applicants/{applicant.id}", follow=True)

    assert response.status_code == 200
    assert dict(response.data) == {
        "id": applicant.id,
        "created_at": (
            applicant.created_at.replace(tzinfo=None).isoformat() + "Z"
        ),
        "updated_at": (
            applicant.updated_at.replace(tzinfo=None).isoformat() + "Z"
        ),
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "job_title": "Software Engineer",
        "resume_url": "https://example.com/resume.pdf",
        "approve_status": 0,
        "approve_status_changed_by": None,
        "approve_status_changed_at": None,
        "comments": f"http://testserver/api/applicants/{applicant.id}/comments/",  # noqa
        "url": f"http://testserver/api/applicants/{applicant.id}/",
    }


@pytest.mark.django_db
def test_not_allowed_get_applicant(create_user, applicant):
    user = create_user(["applications:add_applicant"])
    client.force_login(user)
    response = client.get(f"/api/applicants/{applicant.id}", follow=True)

    assert response.status_code == 403


@pytest.mark.django_db
def test_get_applicants(create_user, applicant):
    user = create_user(["applications:view_applicant"])
    client.force_login(user)
    response = client.get("/api/applicants/", follow=True)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert dict(response.data[0]) == {
        "url": f"http://testserver/api/applicants/{applicant.id}/",
        "id": applicant.id,
        "created_at": (
            applicant.created_at.replace(tzinfo=None).isoformat() + "Z"
        ),
        "updated_at": (
            applicant.updated_at.replace(tzinfo=None).isoformat() + "Z"
        ),
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "job_title": "Software Engineer",
        "resume_url": "https://example.com/resume.pdf",
        "approve_status": 0,
        "approve_status_changed_by": None,
        "approve_status_changed_at": None,
        "comments": f"http://testserver/api/applicants/{applicant.id}/comments/",  # noqa
    }


@pytest.mark.django_db
def test_update_applicant(create_user, applicant):
    user = create_user(["applications:change_applicant"])
    client.force_login(user)
    response = client.put(
        f"/api/applicants/{applicant.id}/",
        {
            "id": applicant.id,
            "name": "John Doe Jr.",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "job_title": "Software Engineer",
            "resume_url": "https://example.com/resume.pdf",
            "approve_status": 0,
        },
        follow=True,
    )

    assert response.status_code == 200, response.content

    new_applicant = Applicant.objects.first()
    assert new_applicant.name == "John Doe Jr."

    assert dict(response.data) == {
        "url": f"http://testserver/api/applicants/{applicant.id}/",
        "id": applicant.id,
        "created_at": (
            applicant.created_at.replace(tzinfo=None).isoformat() + "Z"
        ),
        "updated_at": (
            new_applicant.updated_at.replace(tzinfo=None).isoformat() + "Z"
        ),
        "name": "John Doe Jr.",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "job_title": "Software Engineer",
        "resume_url": "https://example.com/resume.pdf",
        "approve_status": 0,
        "approve_status_changed_by": None,
        "approve_status_changed_at": None,
        "comments": f"http://testserver/api/applicants/{applicant.id}/comments/",  # noqa
    }


@pytest.mark.django_db
def test_should_not_able_to_update_applicant(create_user, applicant):
    user = create_user(["applications:view_applicant"])
    client.force_login(user)
    response = client.put(
        f"/api/applicants/{applicant.id}/",
        {
            "id": applicant.id,
            "name": "John Doe Jr.",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "job_title": "Software Engineer",
            "resume_url": "https://example.com/resume.pdf",
            "approve_status": 0,
        },
        follow=True,
    )

    assert response.status_code == 403, response.content


@pytest.mark.parametrize(
    "next_status", [ApprovalStatus.APPROVED, ApprovalStatus.REJECTED]
)
@pytest.mark.django_db
def test_should_approve_status_update_applicant(
    create_user, applicant, next_status
):
    user = create_user(["applications:change_applicant"])
    client.force_login(user)

    response = client.patch(
        f"/api/applicants/{applicant.id}/",
        {
            "approve_status": next_status,
        },
    )
    assert response.status_code == 200

    updated_applicant: Applicant = Applicant.objects.first()
    assert updated_applicant.approve_status == next_status
    assert updated_applicant.approve_status_changed_by == user
    assert updated_applicant.approve_status_changed_at is not None


@pytest.mark.django_db
def test_create_comment_to_applicant(create_user, applicant):
    user = create_user(["applications:add_applicantcomment"])
    client.force_login(user)

    response = client.post(
        f"/api/applicants/{applicant.id}/comments/",
        {
            "comment": "This is a comment",
        },
    )
    assert response.status_code == 201, response.content

    comments = list(ApplicantComment.objects.filter(applicant=applicant))
    assert len(comments) == 1
    assert comments[0].comment == "This is a comment"
    assert comments[0].author == user


@pytest.mark.django_db
def test_should_not_able_create_comment_to_applicant(create_user, applicant):
    user = create_user(["applications:view_applicantcomment"])
    client.force_login(user)

    response = client.post(
        f"/api/applicants/{applicant.id}/comments/",
        {
            "comment": "This is a comment",
        },
    )
    assert response.status_code == 403, response.content


def test_get_applicant_comments(create_user, applicant):
    user = create_user(["applications:view_applicantcomment"])
    client.force_login(user)

    response = client.get(f"/api/applicants/{applicant.id}/comments/")
    assert response.status_code == 200
    assert len(response.data) == 0

    comment = ApplicantComment.objects.create(
        applicant=applicant,
        author=user,
        comment="This is a comment",
    )

    response = client.get(f"/api/applicants/{applicant.id}/comments/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == comment.id


@pytest.mark.django_db
def test_should_not_allow_get_applicant_comments(create_user, applicant):
    user = create_user([])
    client.force_login(user)

    response = client.get(f"/api/applicants/{applicant.id}/comments/")
    assert response.status_code == 403, response.content
