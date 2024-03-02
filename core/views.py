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
    PageSerializer,
    BlankPageSerializer,
    MessageSerializer,
    CreateMessageSerailizer,
    CreateForumSerializer,
    TodoFullSerializer,
)
from .models import User, UserProfile, Todo, Forum, Message, Workspace, Pages, BlankPage
from rest_framework.generics import ListCreateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializer import CustomWorkSpaceSerializer


class UserSignupView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UserCreateProfileSerializer(data=data)

            if not serializer.is_valid(raise_exception=True):
                return Response({"error": "Invalid Data"}, status=400)
            with transaction.atomic():
                user = User.objects.create_user(**serializer.validated_data["user"])
                profile = UserProfile.objects.create(
                    user=user, **serializer.validated_data["profile"]
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "profile": UserProfileSerializer(profile).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=201,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class WorkspaceView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            data = request.query_params
            print(data)
            workspace_id = data["id"]
            workspace = Workspace.objects.get(id=workspace_id)
            return Response(CustomWorkSpaceSerializer(workspace).data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            data = request.data
            print(data)
            serializer = WorkspaceSerialiezr(data=data)
            if not serializer.is_valid():
                return Response({"error": "Invalid data"}, status=400)
            with transaction.atomic():
                workspace = serializer.save()
                owners = data["owners"]
                workspace.owners.add(user_id)
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
            return Response({"error": str(e)}, status=400)


class AddForumView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = CreateForumSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error": "Invalid data"}, status=400)
            forum = Forum.objects.create(created_by=user, **serializer.validated_data)

            return Response(ForumSerializer(forum).data, status=201)

        except Exception as e:
            return Response({"Error": str(e)}, status=400)


class UpdateWorkspaceView(UpdateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceFullSerilalizer


class TodoViews(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class PagesView(ModelViewSet):
    queryset = Pages.objects.all()
    serializer_class = PageSerializer


class BlankPageView(ModelViewSet):
    queryset = BlankPage.objects.all()
    serializer_class = BlankPageSerializer


class PageDetailsView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            data = request.query_params
            page = Pages.objects.get(id=int(data["id"]))
            if page.page_type == "TODO":
                page_details = page.todos.all()
                print("type todo")
                page_details_data = TodoFullSerializer(page_details, many=True).data
            else:
                try:
                    page_details = page.blank_page
                except Exception as e:
                    return Response(
                        {
                            "page": PageSerializer(page).data,
                            "details": {},
                        }
                    )
                print(page_details)
                page_details_data = BlankPageSerializer(page_details).data

            return Response(
                {"page": PageSerializer(page).data, "details": page_details_data}
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class GetForumView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            workspace = request.query_params["workspace"]
            forums = Forum.objects.filter(workspace=workspace)
            return Response(ForumSerializer(forums, many=True).data)
        except Exception as e:
            return Response({"Error": str(e)}, status=400)


class ForumMessagesView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params["id"]
            forums = Forum.objects.get(id=id)
            messages = forums.messages.all().order_by("-created_at")
            msg = MessageSerializer(messages, many=True).data
            return Response({"forum": ForumSerializer(forums).data, "messages": msg})
        except Exception as e:
            return Response({"Error": str(e)}, status=400)

    def post(self, request, *args, **kwargs):
        try:
            serializer = MessageSerializer(data=request.data)

            if not serializer.is_valid():
                return Response({"error": "Invalid data"}, status=400)
            user = User.objects.get(id=request.user.id)
            message = Message.objects.create(
                created_by=user, **serializer.validated_data
            )

            return Response(MessageSerializer(message).data, status=201)

        except Exception as e:
            return Response({"Error": str(e)}, status=400)
