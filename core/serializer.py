from rest_framework.serializers import ModelSerializer, Serializer
from .models import User, UserProfile, Workspace, Todo, Forum


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("phone", "image", "bio", "name")


class WorkspaceSerialiezr(ModelSerializer):
    class Meta:
        model = Workspace
        fields = ("name", "description")


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"


class UserCreateProfileSerializer(Serializer):
    user = UserSerializer()
    profile = UserProfileSerializer()


class ForumSerializer(ModelSerializer):
    class Meta:
        model = Forum
        fields = "__all__"
