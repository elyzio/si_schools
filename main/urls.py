from django.urls import path
from main.views.views_h import Home


urlpatterns = [
    path("", Home, name="home"),
]