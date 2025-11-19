from django.urls import path
from estudante.views import *

urlpatterns = [
    # Estudante CRUD
    path('', estudante_list, name='estudante_list'),
    path('create/', estudante_create, name='estudante_create'),
    path('update/<int:pk>/', estudante_update, name='estudante_update'),
    path('delete/<int:pk>/', estudante_delete, name='estudante_delete'),
    path('detail/<int:pk>/', estudante_detail, name='estudante_detail'),

    # Estudante Class Assignment
    path('assign-classe/<int:pk>/', estudante_assign_classe, name='estudante_assign_classe'),

    # Estudante Encarregadu (Parent/Guardian) CRUD
    path('<int:estudante_pk>/encarregadu/create/', encarregadu_create, name='encarregadu_create'),
    path('encarregadu/update/<int:pk>/', encarregadu_update, name='encarregadu_update'),
    path('encarregadu/delete/<int:pk>/', encarregadu_delete, name='encarregadu_delete'),

    # Estudante Dokumentu (Document) CRUD
    path('<int:estudante_pk>/dokumentu/create/', dokumentu_create, name='dokumentu_create'),
    path('dokumentu/update/<int:pk>/', dokumentu_update, name='dokumentu_update'),
    path('dokumentu/delete/<int:pk>/', dokumentu_delete, name='dokumentu_delete'),

    # Estudante Transfer
    path('<int:estudante_pk>/transfer/create/', transfer_create, name='transfer_create'),
    path('transfer/update/<int:pk>/', transfer_update, name='transfer_update'),
    path('transfer/delete/<int:pk>/', transfer_delete, name='transfer_delete'),
    path('transfer/list/', transfer_list, name='transfer_list'),

    # Professor Views
    path('professor/turma/',EstudanteTurmaProfList, name='est_prof_turma_list'),
    path('professor/hanorin/',EstudanteHanorinProfList, name='est_prof_hanorin_list'),
    path('professor/hanorin/valor/add/<str:pk>/<int:period_id>/',EstdanteValorProfadd, name='est_prof_valor_add'),
    path('professor/hanorin/valor/edit/<str:val_id>',EstdanteValorProfEdit, name='est_prof_valor_edit'),
    path('professor/hanorin/valor/lock/<str:val_id>',EstudanteValorProfLock, name='est_prof_valor_lock'),

    # Student Reassignment
    path('assigned/', assigned_students_list, name='assigned_students_list'),
    path('assigned/next-year/', next_year_assigned_students_list, name='next_year_assigned_students_list'),
    path('reassign/grade-10/', reassign_grade_10_list, name='reassign_grade_10_list'),
    path('reassign/grade-11/', reassign_grade_11_list, name='reassign_grade_11_list'),
    path('reassign/grade-12/', reassign_grade_12_list, name='reassign_grade_12_list'),
    path('reassign/student/<int:estudante_classe_id>/', reassign_student, name='reassign_student'),

    # Alumni
    path('alumni/', alumni_list, name='alumni_list'),
    path('alumni/<int:pk>/', alumni_detail, name='alumni_detail'),

    # Export
    path('export/<str:content>', EstudanteListPDF, name='export_est_list')
]
