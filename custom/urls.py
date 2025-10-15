from django.urls import path
from . import views

urlpatterns = [
    # Distrito URLs
    path('distrito/', views.distrito_list, name='distrito_list'),
    path('distrito/create/', views.distrito_create, name='distrito_create'),
    path('distrito/<int:pk>/update/', views.distrito_update, name='distrito_update'),
    path('distrito/<int:pk>/delete/', views.distrito_delete, name='distrito_delete'),

    # Subdistrito URLs
    path('subdistrito/', views.subdistrito_list, name='subdistrito_list'),
    path('subdistrito/create/', views.subdistrito_create, name='subdistrito_create'),
    path('subdistrito/<int:pk>/update/', views.subdistrito_update, name='subdistrito_update'),
    path('subdistrito/<int:pk>/delete/', views.subdistrito_delete, name='subdistrito_delete'),

    # Suco URLs
    path('suco/', views.suco_list, name='suco_list'),
    path('suco/create/', views.suco_create, name='suco_create'),
    path('suco/<int:pk>/update/', views.suco_update, name='suco_update'),
    path('suco/<int:pk>/delete/', views.suco_delete, name='suco_delete'),

    # Aldeia URLs
    path('aldeia/', views.aldeia_list, name='aldeia_list'),
    path('aldeia/create/', views.aldeia_create, name='aldeia_create'),
    path('aldeia/<int:pk>/update/', views.aldeia_update, name='aldeia_update'),
    path('aldeia/<int:pk>/delete/', views.aldeia_delete, name='aldeia_delete'),

    # Ano URLs
    path('ano/', views.ano_list, name='ano_list'),
    path('ano/create/', views.ano_create, name='ano_create'),
    path('ano/<int:pk>/update/', views.ano_update, name='ano_update'),
    path('ano/<int:pk>/delete/', views.ano_delete, name='ano_delete'),
    path('ano/<int:pk>/toggle-active/', views.ano_toggle_active, name='ano_toggle_active'),

    # Departamentu URLs
    path('departamentu/', views.departamentu_list, name='departamentu_list'),
    path('departamentu/create/', views.departamentu_create, name='departamentu_create'),
    path('departamentu/<int:pk>/update/', views.departamentu_update, name='departamentu_update'),
    path('departamentu/<int:pk>/delete/', views.departamentu_delete, name='departamentu_delete'),

    # Classe URLs
    path('classe/', views.classe_list, name='classe_list'),
    path('classe/create/', views.classe_create, name='classe_create'),
    path('classe/<int:pk>/update/', views.classe_update, name='classe_update'),
    path('classe/<int:pk>/delete/', views.classe_delete, name='classe_delete'),

    # Turma URLs
    path('turma/', views.turma_list, name='turma_list'),
    path('turma/create/', views.turma_create, name='turma_create'),
    path('turma/<int:pk>/update/', views.turma_update, name='turma_update'),
    path('turma/<int:pk>/delete/', views.turma_delete, name='turma_delete'),

    # Periodo URLs
    path('periodo/', views.periodo_list, name='periodo_list'),
    path('periodo/create/', views.periodo_create, name='periodo_create'),
    path('periodo/<int:pk>/update/', views.periodo_update, name='periodo_update'),
    path('periodo/<int:pk>/delete/', views.periodo_delete, name='periodo_delete'),
    path('periodo/<int:pk>/toggle-active/', views.periodo_toggle_active, name='periodo_toggle_active'),

    # Materia URLs
    path('materia/', views.materia_list, name='materia_list'),
    path('materia/create/', views.materia_create, name='materia_create'),
    path('materia/<int:pk>/update/', views.materia_update, name='materia_update'),
    path('materia/<int:pk>/delete/', views.materia_delete, name='materia_delete'),

    # AJAX URLs for dependent dropdowns
    path('ajax/subdistrito/', views.ajax_subdistrito, name='ajax_subdistrito'),
    path('ajax/suco/', views.ajax_suco, name='ajax_suco'),
    path('ajax/aldeia/', views.ajax_aldeia, name='ajax_aldeia'),
]