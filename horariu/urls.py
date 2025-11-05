from django.urls import path
from horariu.views import *

urlpatterns = [
    # Loron URLs
    path('loron/', loron_list, name='loron_list'),
    path('loron/create/', loron_create, name='loron_create'),
    path('loron/<int:pk>/', loron_detail, name='loron_detail'),
    path('loron/<int:pk>/update/', loron_update, name='loron_update'),
    path('loron/<int:pk>/delete/', loron_delete, name='loron_delete'),

    # Horas URLs
    path('horas/', horas_list, name='horas_list'),
    path('horas/create/', horas_create, name='horas_create'),
    path('horas/<int:pk>/', horas_detail, name='horas_detail'),
    path('horas/<int:pk>/update/', horas_update, name='horas_update'),
    path('horas/<int:pk>/delete/', horas_delete, name='horas_delete'),

    # Horariu URLs
    path('', horariu_list, name='horariu_list'),
    path('create/', horariu_create, name='horariu_create'),
    path('<int:pk>/', horariu_detail, name='horariu_detail'),
    path('<int:pk>/update/', horariu_update, name='horariu_update'),
    path('<int:pk>/delete/', horariu_delete, name='horariu_delete'),

    # HorariuExame URLs
    path('exame/', horariuexame_list, name='horariuexame_list'),
    path('exame/create/', horariuexame_create, name='horariuexame_create'),
    path('exame/<int:pk>/', horariuexame_detail, name='horariuexame_detail'),
    path('exame/<int:pk>/update/', horariuexame_update, name='horariuexame_update'),
    path('exame/<int:pk>/delete/', horariuexame_delete, name='horariuexame_delete'),

    # HorariuValor URLs
    path('valor/', horariuvalor_list, name='horariuvalor_list'),
    path('valor/create/', horariuvalor_create, name='horariuvalor_create'),
    path('valor/<int:pk>/', horariuvalor_detail, name='horariuvalor_detail'),
    path('valor/<int:pk>/update/', horariuvalor_update, name='horariuvalor_update'),
    path('valor/<int:pk>/delete/', horariuvalor_delete, name='horariuvalor_delete'),

    # Horariu for Professors URLs
    path('professor/horariu/', HorariuListProf, name='horariu_list_prof'),

    path('estudante/horariu/', HorariuListEst, name='horariu_list_est'),
]