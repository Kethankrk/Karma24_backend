from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView, Response
from core.models import Workspace, User
from .serializer import CustomWorkSpaceSerializer
from core.serializer import UserProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


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
