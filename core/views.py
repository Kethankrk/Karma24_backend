from rest_framework.views import APIView, Response
from django.db import transaction
from .serializer import (
    UserCreateProfileSerializer,
    UserSerializer,
    UserProfileSerializer,
    TodoSerializer,
    WorkspaceSerialiezr,
    ForumSerializer,
    WorkspaceFullSerilalizer,
)
from .models import User, UserProfile, Todo, Forum, Message, Workspace
from rest_framework.generics import ListCreateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet


class UserSignupView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UserCreateProfileSerializer(data=data)

            if not serializer.is_valid():
                return Response({"error": "Invalid Data"}, status=400)
            with transaction.atomic():
                user = User.objects.create_user(**serializer.validated_data["user"])
                profile = UserProfile.objects.create(
                    user=user, **serializer.validated_data["profile"]
                )

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "profile": UserProfileSerializer(profile).data,
                },
                status=201,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class WorkspaceView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = WorkspaceSerialiezr(data=data)
            if not serializer.is_valid():
                return Response({"error": "Invalid data"}, status=400)
            with transaction.atomic():
                workspace = serializer.save()
                owners = data["owners"]
                if owners:
                    for owner in owners:
                        workspace.owners.add(owner)
                members = data["members"]
                if members:
                    for member in members:
                        workspace.members.add(member)
                workspace.save()

            return Response({"workspace": serializer.data}, status=200)

        except Exception as e:
            return Response({"error": str(e)})


class AddForumView(CreateAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


class UpdateWorkspaceView(UpdateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceFullSerilalizer


class TodoViews(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
