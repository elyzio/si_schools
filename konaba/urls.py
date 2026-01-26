from django.urls import path
from konaba.views import *

urlpatterns = [
    # KonaBa URLs
    path('konaba/', konaba_list, name='konaba_list'),
    path('konaba/create/', konaba_create, name='konaba_create'),
    path('konaba/<int:pk>/update/', konaba_update, name='konaba_update'),
    path('konaba/<int:pk>/delete/', konaba_delete, name='konaba_delete'),

    # Informasaun URLs
    path('informasaun/', informasaun_list, name='informasaun_list'),
    path('informasaun/create/', informasaun_create, name='informasaun_create'),
    path('informasaun/<int:pk>/detail/', informasaun_detail, name='informasaun_detail'),
    path('informasaun/<int:pk>/update/', informasaun_update, name='informasaun_update'),
    path('informasaun/<int:pk>/delete/', informasaun_delete, name='informasaun_delete'),
    path('informasaun/<int:pk>/toggle-publish/', informasaun_toggle_publish, name='informasaun_toggle_publish'),
]
