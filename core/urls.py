from rest_framework.urls import path
from .views import UserSignupView, TodoView, WorkspaceView, AddForumView


urlpatterns = [
    path("signup/", UserSignupView.as_view()),
    path("todo/", TodoView.as_view()),
    path("workspace/", WorkspaceView.as_view()),
    path("forum/", AddForumView.as_view()),
]
