from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

import logging

from django.contrib.auth.models import User



class Project(models.Model):
    name = models.CharField(max_length=255, help_text="Название проекта", unique=True)
    description = models.TextField(blank=True, null=True, help_text="Описание проекта")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата создания проекта"
    )

    def __str__(self):
        return self.name


class Sprint(models.Model):
    name = models.CharField(max_length=255, help_text="Название спринта", unique=True)
    description = models.TextField(blank=True, null=True, help_text="Описание спринта")
    start_date = models.DateField(
        null=True, blank=True, help_text="Дата начала спринта"
    )
    end_date = models.DateField(
        null=True, blank=True, help_text="Дата окончания спринта"
    )
    project = models.ForeignKey(
        Project,
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sprints",
        help_text="Проект",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата создания проекта"
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(help_text="Название задачи", max_length=100, unique=True)
    description = models.TextField(help_text="Описание задачи", blank=True, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, help_text="Дата создания задачи"
    )
    updated_date = models.DateTimeField(
        auto_now=True, help_text="Дата обновления задачи"
    )  # ,default=False, blank=True, null=True, )
    start_date = models.DateField(blank=True, null=True, help_text="Дата начала")
    end_date = models.DateField(blank=True, null=True, help_text="Дата окончания")

    assigned_to = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="tasks_user",
        help_text="Назначено напользователя",
    )

    sprint = models.ForeignKey(
        Sprint,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="sprint_task",
        help_text="Спринт",
    )

    status = models.ForeignKey(
        max_length=20,
        to="task_manager_app.status",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="status_task",
        help_text="Статус задачи",
        default="Создана",
    )

    project = models.ForeignKey(
        to="task_manager_app.project",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="project_task",
        help_text="Проект задачи",
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["created_date"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:  # если задача уже сохранена в базе данных
            old_task = Task.objects.get(pk=self.pk)  # получаем старую версию задачи
            if (
                self.status != old_task.status
                or self.assigned_to != old_task.assigned_to
            ):  # если статус изменился
                TaskHistory.objects.create(
                    task=self, status=self.status, assigned_to=self.assigned_to
                )  # создаем запись в истории изменений
        super(Task, self).save(*args, **kwargs)

        logger = logging.getLogger(__name__)
        logger.info("Создана\Изменена задача")


class Status(models.Model):
    name = models.CharField(
        help_text="Наименование статуса", max_length=32, unique=True
    )
    rang_status = models.IntegerField(help_text="Очередь статуса", unique=True)

    class Meta:
        ordering = ["rang_status"]

    def __str__(self):
        return self.name


class TaskHistory(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="task_history",
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="user_task_history",
    )

    status = models.ForeignKey(
        to="task_manager_app.status",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="status_task_history",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task} - {self.created_at} - {self.status} - {self.assigned_to}"


class Notification(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="notification_task",
        help_text="Задача",
    )
    assigned_to = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="notification_user",
        help_text="Пользователь",
    )
    created_date = models.DateTimeField(
        auto_now_add=True, help_text="Дата создания уведомления"
    )

    def __str__(self):
        return f"{self.task.name} - {self.assigned_to.username}"
