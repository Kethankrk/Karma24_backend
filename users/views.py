from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView, Response
from core.models import Workspace, User
from .serializer import lol
from rest_framework_simplejwt.authentication import JWTAuthentication


class GetUserWorkspaces(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            o_workspace = user.owned_workspaces.all()
            m_workspace = user.joined_workspaces.all()

            return Response(
                {
                    "owned": lol(o_workspace, many=True).data,
                    "joined": lol(m_workspace, many=True).data,
                }
            )
        except Exception as e:
            return Response({"error": str(e)})
