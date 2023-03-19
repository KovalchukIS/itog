from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from task_manager_app.models import Project, Sprint, Task, Status


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        labels = {
            "name": _("Название"),
            "description": _("Описание"),
        }
        help_texts = {
            "name": _("Введите название проекта"),
            "description": _("Введите описание проекта"),
        }


class SprintForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Дата начала спринта",
        required=False,
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Дата окончания спринта",
        required=False,
    )

    class Meta:
        model = Sprint
        fields = ["name", "description", "start_date", "end_date", "project"]

        labels = {
            "name": _("Название"),
            "description": _("Описание"),
            "start_date": _("Дата начала"),
            "end_date": _("Дата окончания"),
            "project": _("Проект"),
        }
        help_texts = {
            "name": _("Введите название спринта"),
            "description": _("Введите описание спринта"),
            "start_date": _("Введите дату начала спринта"),
            "end_date": _("Введите дату окончания спринта"),
            "project": _("Выберите Проект спринта"),
        }
        template_name = "task_manager_app/templates/widget/date_picker.html"


class TaskForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Дата начала задачи",
        required=False,
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Дата окончания задачи",
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "sprint",
            "status",
            "assigned_to",
            "project",
        ]
        labels = {
            "name": _("Название"),
            "description": _("Описание"),
            "start_date": _("Дата начала"),
            "end_date": _("Дата окончания"),
            "sprint": _("Спринт"),
            "status": _("Статус"),
            "assigned_to": _("Исполнитель"),
            "project": _("Проект"),
        }
        help_texts = {
            "name": _("Введите название задачи"),
            "description": _("Введите описание задачи"),
            "start_date": _("Введите дату начала задачи"),
            "end_date": _("Введите дату окончания задачи"),
            "sprint": _("Выберите спринт"),
            "status": _("Выберите статус задачи"),
            "assigned_to": _("Выберите исполнителя задачи"),
            "project": _("Выберите проект задачи"),
        }


class TaskAssignForm(forms.Form):
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all())

    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop("task")
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = get_user_model().objects.exclude(
            id__in=self.task.assigned_users.all().values_list("id", flat=True)
        )

    def save(self):
        user = self.cleaned_data["user"]
        self.task.assigned_users.add(user)
        self.task.save()


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name", "rang_status"]
        labels = {
            "name": _("Название"),
            "rang_status": _("Очередность"),
        }
        help_texts = {
            "name": _("Введите название статуса"),
            "rang_status": _("Введите Очередность статуса"),
        }
