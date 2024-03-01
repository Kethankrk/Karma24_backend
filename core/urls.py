from rest_framework.urls import path
from .views import (
    UserSignupView,
    WorkspaceView,
    AddForumView,
    UpdateWorkspaceView,
    TodoViews,
    PagesView,
    BlankPageView,
    PageDetailsView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"todo", TodoViews, basename="todo")
router.register(r"page", PagesView, basename="page")
router.register(r"blank-page", BlankPageView, basename="blankpage")

urlpatterns = [
    path("signup/", UserSignupView.as_view()),
    path("workspace/", WorkspaceView.as_view()),
    path("forum/", AddForumView.as_view()),
    path("workspace-edit/<int:pk>", UpdateWorkspaceView.as_view()),
    path("get-page/", PageDetailsView.as_view()),
] + router.urls
