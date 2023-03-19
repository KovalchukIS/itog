from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    SprintCreateView,
    SprintUpdateView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskAssignView,
    TaskHistoryView,
    SprintListView,
    TaksListView,
    SprintDetailView,
    TaskDetailView,
    StatusListView,
    StatusDetailView,
    StatusCreateView,
    StatusUpdateView,
)

from .api_views import (
    ProjectViewSet,
    SprintViewSet,
    TaskViewSet,
    StatusViewSet,
    TaskHistoryViewSet,
    NotificationViewSet,
)

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/projects", ProjectViewSet)
router.register(r"api/sprints", SprintViewSet)
router.register(r"api/tasks", TaskViewSet)
router.register(r"api/statuses", StatusViewSet)
router.register(r"api/task_history", TaskHistoryViewSet)
router.register(r"api/notifications", NotificationViewSet)

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="home"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
    path(
        "projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project_update"
    ),
    path("sprints/", SprintListView.as_view(), name="sprints"),
    path("sprints/create/", SprintCreateView.as_view(), name="sprint_create"),
    path("sprints/<int:pk>/update/", SprintUpdateView.as_view(), name="sprint_update"),
    path("sprints/<int:pk>/", SprintDetailView.as_view(), name="sprint_detail"),
    path("tasks/", TaksListView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/assign/", TaskAssignView.as_view(), name="task_assign"),
    path("tasks/<int:pk>/history/", TaskHistoryView.as_view(), name="task_history"),
    path("status/", StatusListView.as_view(), name="status"),
    path("status/<int:pk>/", StatusDetailView.as_view(), name="status_detail"),
    path("status/create/", StatusCreateView.as_view(), name="status_create"),
    path("status/<int:pk>/update/", StatusUpdateView.as_view(), name="status_update"),
]

# from django.contrib.auth.views import LoginView, LogoutView
from .views import MySignupView, MyLogoutView, MyLoginView

urlpatterns += [
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    # path('register/', MySignupView.as_view(), name='register'),
]

urlpatterns += router.urls


################3
from .views import register

urlpatterns += [
    path("register/", register, name="register"),
]


#############
from .views import ProjectDeleteView, SprintDeleteView, StatusDeleteView

urlpatterns += [
    path(
        "project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"
    ),
    path("sprint/<int:pk>/delete/", SprintDeleteView.as_view(), name="sprint_delete"),
    path("status/<int:pk>/delete/", StatusDeleteView.as_view(), name="status_delete"),
]
