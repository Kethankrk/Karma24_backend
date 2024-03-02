from datetime import datetime
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.views import APIView, Response
from core.models import Workspace, User, Todo
from .serializer import (
    CustomWorkSpaceSerializer,
    CustomUserSerializer,
    UploadedFileSerializer,
)
from core.serializer import UserProfileSerializer, UserSerializer, TodoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet


class GetUserWorkspaces(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            o_workspace = user.owned_workspaces.all()
            m_workspace = user.joined_workspaces.all()

            return Response(
                {
                    "owned": CustomWorkSpaceSerializer(o_workspace, many=True).data,
                    "joined": CustomWorkSpaceSerializer(m_workspace, many=True).data,
                }
            )
        except Exception as e:
            return Response({"error": str(e)})


class UpdateUserProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UserProfileSerializer(data=data)
            if not serializer.is_valid():
                return Response({"error": "Invalid data"}, status=400)
            serializer.save()

            return Response({"profile": serializer.data})
        except Exception as e:
            return Response({"error": str(e)})

    def get(self, request, *args, **kwargs):
        try:
            profile = request.user.profile
            return Response(UserProfileSerializer(profile).data)
        except Exception as e:
            return Response({"error": str(e)})


class GetAllUsers(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            users = User.objects.all()
            data = CustomUserSerializer(users, many=True).data
            result = []

            for user in data:
                if user_id == user["id"]:
                    continue
                if not user["profile"]:
                    continue
                result.append(
                    {
                        "value": user["id"],
                        "label": user["profile"]["name"],
                    }
                )
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)})


class GetDeadlinedTodos(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            todos = Todo.objects.filter(
                assigned=user_id, due_date__lte=datetime.now(), completed=False
            )
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)})


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = UploadedFileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=201)

        return Response(file_serializer.errors, status=400)
