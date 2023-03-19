from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class TaskManagerLoginView(LoginView):
    """Представление для входа пользователя"""

    template_name = "registration/login.html"
    form_class = AuthenticationForm


class TaskManagerLogoutView(LogoutView):
    """Представление для выхода пользователя"""

    template_name = "registration/logout.html"


class TaskManagerRegisterView(CreateView):
    """Представление для регистрации пользователя"""

    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("project-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=self.object.username, password=password)
        login(self.request, user)
        return response
