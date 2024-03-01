from rest_framework.urls import path
from .views import GetUserWorkspaces, UpdateUserProfile, GetAllUsers

urlpatterns = [
    path("get-workspaces/", GetUserWorkspaces.as_view()),
    path("profile/", UpdateUserProfile.as_view()),
    path("get/", GetAllUsers.as_view()),
]
