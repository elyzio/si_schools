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

    # Estudante views
    path('est/valor/grafiku/', ValorEstList, name='valor_est_list'),
    path('est/valor/list/', ValorEstList2, name='valor_est_list2'),
    path('est/valor/Detail/<period_id>/<classe_id>/<ano_id>/', ValorEstDetail2, name='valor_est_detail2'),

    # Prof views
    # Estudante views
    path('est/p/valor/grafiku/<pk>/', ValorEstProfList, name='valor_est_p_list'),
    path('est/p/valor/list/<pk>/', ValorEstProfList2, name='valor_est_p_list2'),
    path('est/p/valor/Detail/<est_id>/<period_id>/<classe_id>/<ano_id>/', ValorEstProfDetail2, name='valor_est_p_detail2'),

    # Klassifikasaun - Finalize rankings
    path('finalize-year/<int:ano_id>/', finalize_year_rankings, name='finalize_year_rankings'),

    # Klassifikasaun - Rankings leaderboard
    path('rankings/', rankings_leaderboard, name='rankings_leaderboard'),
]
