from django.urls import path
from .views import views_p, views_professoruser, views_professorclasse, views_professormateria, views_professordokumentu

urlpatterns = [
    # Professor URLs
    path('', views_p.professor_list, name='professor_list'),
    path('create/', views_p.professor_create, name='professor_create'),
    path('<int:pk>/', views_p.professor_detail, name='professor_detail'),
    path('<int:pk>/update/', views_p.professor_update, name='professor_update'),
    path('<int:pk>/delete/', views_p.professor_delete, name='professor_delete'),

    # ProfessorUser URLs
    path('professoruser/', views_professoruser.professoruser_list, name='professoruser_list'),
    path('professoruser/create/', views_professoruser.professoruser_create, name='professoruser_create'),
    path('professoruser/<int:pk>/', views_professoruser.professoruser_detail, name='professoruser_detail'),
    path('professoruser/<int:pk>/update/', views_professoruser.professoruser_update, name='professoruser_update'),
    path('professoruser/<int:pk>/delete/', views_professoruser.professoruser_delete, name='professoruser_delete'),

    # ProfessorClasse URLs
    path('professorclasse/', views_professorclasse.professorclasse_list, name='professorclasse_list'),
    path('professorclasse/create/', views_professorclasse.professorclasse_create, name='professorclasse_create'),
    path('professorclasse/<int:pk>/', views_professorclasse.professorclasse_detail, name='professorclasse_detail'),
    path('professorclasse/<int:pk>/update/', views_professorclasse.professorclasse_update, name='professorclasse_update'),
    path('professorclasse/<int:pk>/delete/', views_professorclasse.professorclasse_delete, name='professorclasse_delete'),

    # ProfessorMateria URLs
    path('professormateria/', views_professormateria.professormateria_list, name='professormateria_list'),
    path('professormateria/create/', views_professormateria.professormateria_create, name='professormateria_create'),
    path('professormateria/<int:pk>/', views_professormateria.professormateria_detail, name='professormateria_detail'),
    path('professormateria/<int:pk>/update/', views_professormateria.professormateria_update, name='professormateria_update'),
    path('professormateria/<int:pk>/delete/', views_professormateria.professormateria_delete, name='professormateria_delete'),

    # ProfessorDokumentu URLs
    path('professordokumentu/', views_professordokumentu.professordokumentu_list, name='professordokumentu_list'),
    path('professordokumentu/create/', views_professordokumentu.professordokumentu_create, name='professordokumentu_create'),
    path('professordokumentu/<int:pk>/', views_professordokumentu.professordokumentu_detail, name='professordokumentu_detail'),
    path('professordokumentu/<int:pk>/update/', views_professordokumentu.professordokumentu_update, name='professordokumentu_update'),
    path('professordokumentu/<int:pk>/delete/', views_professordokumentu.professordokumentu_delete, name='professordokumentu_delete'),

    # AJAX endpoints for dependent dropdowns
    path('ajax/subdistrito/', views_p.ajax_subdistrito, name='ajax_subdistrito'),
    path('ajax/suco/', views_p.ajax_suco, name='ajax_suco'),
    path('ajax/aldeia/', views_p.ajax_aldeia, name='ajax_aldeia'),
]