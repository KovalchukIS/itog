from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Project, Sprint, Task, Status, TaskHistory
from .forms.forms import ProjectForm, SprintForm, TaskForm, TaskAssignForm, StatusForm

from .forms.auth_forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = "projects"
    template_name = "project_list.html"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = "project"
    template_name = "project_detail.html"


class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("home")
    template_name = "project_form.html"
    success_message = "Project successfully created!"


class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    # success_url = reverse_lazy('projects/', args=[self.object.project.id])
    template_name = "project_form.html"
    success_message = "Project successfully updated!"

    def get_success_url(self):
        return reverse_lazy("project_detail", args=[self.object.pk])


################
class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    context_object_name = "status"
    template_name = "status_list.html"


class StatusDetailView(LoginRequiredMixin, DetailView):
    model = Status
    context_object_name = "status"
    template_name = "status_detail.html"


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("home")
    template_name = "status_form.html"
    success_message = "status successfully created!"


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    # success_url = reverse_lazy('projects/', args=[self.object.project.id])
    template_name = "status_form.html"
    success_message = "Status successfully updated!"

    def get_success_url(self):
        return reverse_lazy("status_detail", args=[self.object.pk])

    ###############################


class SprintListView(LoginRequiredMixin, ListView):
    model = Sprint
    context_object_name = "sprints"
    template_name = "sprint_list.html"


class TaksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "task"
    template_name = "task_list.html"


class SprintDetailView(LoginRequiredMixin, DetailView):
    model = Sprint
    context_object_name = "sprint"
    template_name = "sprint_detail.html"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "task_detail.html"


######################
class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("home")
    template_name = "project_form.html"
    success_message = "Project successfully created!"


class SprintCreateView(CreateView):
    model = Sprint
    form_class = SprintForm
    template_name = "sprint_form.html"
    # fields = ['name', 'description', 'start_date', 'end_date', 'project']
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        sprint = form.save(commit=False)
        sprint.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("sprint_detail", kwargs={"pk": self.object.pk})


class SprintUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Sprint
    form_class = SprintForm
    template_name = "sprint_form.html"
    success_message = "Sprint successfully updated!"

    def get_success_url(self):
        return reverse_lazy("sprint_detail", args=[self.object.pk])


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_message = "Task successfully created!"

    def form_valid(self, form):
        sprint = form.save(commit=False)
        sprint.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("task_detail", args=[self.object.pk])


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_message = "Task successfully updated!"

    def get_success_url(self):
        return reverse_lazy("task_detail", args=[self.object.pk])


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("project-list")
    success_message = "Task successfully deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class TaskAssignView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskAssignForm
    template_name = "task/assign.html"
    success_message = "Task was assigned successfully"

    def get_success_url(self):
        return reverse_lazy("task_detail", args=[self.object.pk])

    def form_valid(self, form):
        # Assign the task to the selected user
        task_id = self.kwargs["pk"]
        task = get_object_or_404(Task, id=task_id)

        task.assigned_to = form.cleaned_data["assigned_to"]
        task.save()

        # Add a success message
        messages.success(self.request, self.success_message)

        return super().form_valid(form)


class TaskHistoryView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_history = TaskHistory.objects.filter(task=self.object).order_by(
            "-created_at"
        )
        context["task_history"] = task_history
        return context



class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("home")
    template_name = "project_confirm_delete.html"


def home(request):
    return render(request, "home.html")


class SprintDeleteView(LoginRequiredMixin, DeleteView):
    model = Sprint
    success_url = reverse_lazy("sprints")
    template_name = "sprint_confirm_delete.html"


def home(request):
    return render(request, "home.html")


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    success_url = reverse_lazy("status")
    template_name = "status_confirm_delete.html"



class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super().form_valid(form)
        return self.form_invalid(form)


class MyLogoutView(LogoutView):
    template_name = "registration/logout.html"
    next_page = reverse_lazy("home")


class MySignupView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    #################


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms.auth_forms import SignUpForm


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Создаем нового пользователя
            user = form.save(commit=False)
            # Добавляем email
            user.email = form.cleaned_data["email"]
            # Сохраняем пользователя
            user.save()
            # Выполняем вход на сайт
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/register.html", {"form": form})
