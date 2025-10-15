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
]
