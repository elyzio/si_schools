from django.urls import path
from django.contrib.auth import views as auth_views
from main.views import Home, Logout

urlpatterns = [
    path("", Home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name='auth/login.html'), name="login"),
    path("logout/", Logout, name="logout"),
]