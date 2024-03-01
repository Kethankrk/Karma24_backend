from rest_framework.serializers import ModelSerializer, Serializer
from core.models import Workspace, User
from core.serializer import UserProfileSerializer


class CustomUserSerializer(ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "profile")


class CustomWorkSpaceSerializer(ModelSerializer):
    owners = CustomUserSerializer(many=True)

    class Meta:
        model = Workspace
        fields = "__all__"
