from rest_framework.serializers import ModelSerializer, Serializer
from .models import User, UserProfile, Workspace, Todo, Forum, Pages, BlankPage, Message


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


class UserCreateProfileSerializer(Serializer):
    user = UserSerializer()
    profile = UserProfileSerializer()


class ForumSerializer(ModelSerializer):
    class Meta:
        model = Forum
        fields = "__all__"


class UserNameFromIdSerializer(ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "profile")


class TodoSerializer(ModelSerializer):

    class Meta:
        model = Todo
        fields = "__all__"


class TodoFullSerializer(ModelSerializer):
    assigned = UserNameFromIdSerializer(read_only=True)

    class Meta:
        model = Todo
        fields = "__all__"


class WorkspaceFullSerilalizer(ModelSerializer):
    class Meta:
        model = Workspace
        fields = "__all__"


class PageSerializer(ModelSerializer):
    class Meta:
        model = Pages
        fields = "__all__"


class BlankPageSerializer(ModelSerializer):
    class Meta:
        model = BlankPage
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    created_by = UserNameFromIdSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


class CreateMessageSerailizer(ModelSerializer):
    class Meta:
        model = Message
        fields = ["content", "forum"]


class CreateForumSerializer(ModelSerializer):
    class Meta:
        model = Forum
        fields = ["name", "description", "workspace"]
