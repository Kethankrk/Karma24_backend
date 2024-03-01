from rest_framework.urls import path
from .views import GetUserWorkspaces

urlpatterns = [
    path("get-workspaces/", GetUserWorkspaces.as_view()),
]
