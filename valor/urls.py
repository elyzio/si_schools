from django.urls import path
from valor.views import *

urlpatterns = [
    # Valor management
    path('', valor_list, name='valor_list'),
    path('report/', valor_report, name='valor_report'),
    path('estudante/<int:estudante_classe_pk>/', estudante_valor_detail, name='estudante_valor_detail'),
    path('estudante/<int:estudante_classe_pk>/add/', valor_create, name='valor_create'),
    path('graph/<int:estudante_pk>/', valor_graph, name='valor_graph'),
    path('<int:pk>/edit/', valor_update, name='valor_update'),
    path('<int:pk>/delete/', valor_delete, name='valor_delete'),
]
