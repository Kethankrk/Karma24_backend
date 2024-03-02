from rest_framework.urls import path
from .views import (
    GetUserWorkspaces,
    UpdateUserProfile,
    GetAllUsers,
    GetDeadlinedTodos,
    FileUploadView,
)

urlpatterns = [
    path("get-workspaces/", GetUserWorkspaces.as_view()),
    path("profile/", UpdateUserProfile.as_view()),
    path("get/", GetAllUsers.as_view()),
    path("deadlines/", GetDeadlinedTodos.as_view()),
    path("upload/", FileUploadView.as_view()),
]
