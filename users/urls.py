from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', user_profile, name='user_profile'),
    path('account/', user_account, name='user_account'),
    path('change-password/', ChangeUserPassword, name='change_password'),
    path('update/profile/professor/', UpdateProfessorProfile, name='update_profile_professor'),
    path('update/profile/estudante/', UpdateEstudanteProfile, name='update_profile_estudante'),
]