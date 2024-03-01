from rest_framework.serializers import ModelSerializer, Serializer
from core.models import Workspace


class lol(ModelSerializer):
    class Meta:
        model = Workspace
        fields = "__all__"
