from django.contrib.auth.models import Permission, User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        source="user_permissions",
        queryset=Permission.objects.all(),
    )

    class Meta:
        model = User
        fields = ["url", "username", "email", "permissions"]
