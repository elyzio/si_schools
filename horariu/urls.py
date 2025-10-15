from django.urls import path
from .views import views_loron, views_horas, views_horariu, views_horariuexame, views_horariuvalor

urlpatterns = [
    # Loron URLs
    path('loron/', views_loron.loron_list, name='loron_list'),
    path('loron/create/', views_loron.loron_create, name='loron_create'),
    path('loron/<int:pk>/', views_loron.loron_detail, name='loron_detail'),
    path('loron/<int:pk>/update/', views_loron.loron_update, name='loron_update'),
    path('loron/<int:pk>/delete/', views_loron.loron_delete, name='loron_delete'),

    # Horas URLs
    path('horas/', views_horas.horas_list, name='horas_list'),
    path('horas/create/', views_horas.horas_create, name='horas_create'),
    path('horas/<int:pk>/', views_horas.horas_detail, name='horas_detail'),
    path('horas/<int:pk>/update/', views_horas.horas_update, name='horas_update'),
    path('horas/<int:pk>/delete/', views_horas.horas_delete, name='horas_delete'),

    # Horariu URLs
    path('', views_horariu.horariu_list, name='horariu_list'),
    path('create/', views_horariu.horariu_create, name='horariu_create'),
    path('<int:pk>/', views_horariu.horariu_detail, name='horariu_detail'),
    path('<int:pk>/update/', views_horariu.horariu_update, name='horariu_update'),
    path('<int:pk>/delete/', views_horariu.horariu_delete, name='horariu_delete'),

    # HorariuExame URLs
    path('exame/', views_horariuexame.horariuexame_list, name='horariuexame_list'),
    path('exame/create/', views_horariuexame.horariuexame_create, name='horariuexame_create'),
    path('exame/<int:pk>/', views_horariuexame.horariuexame_detail, name='horariuexame_detail'),
    path('exame/<int:pk>/update/', views_horariuexame.horariuexame_update, name='horariuexame_update'),
    path('exame/<int:pk>/delete/', views_horariuexame.horariuexame_delete, name='horariuexame_delete'),

    # HorariuValor URLs
    path('valor/', views_horariuvalor.horariuvalor_list, name='horariuvalor_list'),
    path('valor/create/', views_horariuvalor.horariuvalor_create, name='horariuvalor_create'),
    path('valor/<int:pk>/', views_horariuvalor.horariuvalor_detail, name='horariuvalor_detail'),
    path('valor/<int:pk>/update/', views_horariuvalor.horariuvalor_update, name='horariuvalor_update'),
    path('valor/<int:pk>/delete/', views_horariuvalor.horariuvalor_delete, name='horariuvalor_delete'),
]