from rest_framework.serializers import ModelSerializer, Serializer
from core.models import Workspace, User
from core.serializer import UserProfileSerializer, PageSerializer, ForumSerializer
from .models import UploadedFile


class CustomUserSerializer(ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "profile")


class CustomWorkSpaceSerializer(ModelSerializer):
    owners = CustomUserSerializer(many=True)
    members = CustomUserSerializer(many=True)
    pages = PageSerializer(many=True)
    forum = ForumSerializer(many=True)

    class Meta:
        model = Workspace
        fields = "__all__"


class UploadedFileSerializer(ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"
