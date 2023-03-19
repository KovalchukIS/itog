from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from .models import Project, Sprint, Task, Status, TaskHistory, Notification
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
)


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Project.objects.create(
            name="Project 1", description="Description 1", created_at=date.today()
        )

    def test_name_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    # Add more tests for the other fields and methods





class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user("testuser", "test@example.com", "password")
        status = Status.objects.create(
            name="To Do", rang_status=2
        )
        project = Project.objects.create(
            name="Project 1", description="Description 1", created_at=date.today()
        )
        sprint = Sprint.objects.create(
            name="Sprint 1",
            description="Description 1",
            start_date=date.today(),
            end_date=date.today(),
            project=project,
            created_at=date.today(),
        )
        Task.objects.create(
            name="Task 1",
            description="Description 1",
            created_date=date.today(),
            assigned_to=user,
            sprint=sprint,
            status=status,
        )

    def test_name_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    # Add more tests for the other fields and methods


# Add more tests for the other models
