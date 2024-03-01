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
)
from .models import User, UserProfile, Todo, Forum, Message, Workspace, Pages, BlankPage
from rest_framework.generics import ListCreateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken


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


class PagesView(ModelViewSet):
    queryset = Pages.objects.all()
    serializer_class = PageSerializer


class BlankPageView(ModelViewSet):
    queryset = BlankPage.objects.all()
    serializer_class = BlankPageSerializer


class PageDetailsView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            page = Pages.objects.get(id=int(data["id"]))
            if page.page_type == "TODO":
                page_details = page.todos.all()
                print("type todo")
                page_details_data = TodoSerializer(page_details, many=True).data
            else:
                page_details = page.blank_page.all()
                print(page_details)
                page_details_data = BlankPageSerializer(page_details, many=True).data

            return Response({"page": page_details_data})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
