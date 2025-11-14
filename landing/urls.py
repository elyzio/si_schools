from django.urls import path
from landing.views import *

urlpatterns = [
    path('kona-ba/', about_page, name='about_page'),
    path('informasaun/', information_page, name='information_page'),
    path('agenda/', agenda_page, name='agenda_page'),
    path('actividade/', activity_page, name='activity_page'),
    path('inf/desc/<int:pk>/', information_detail, name='information_detail'),
    path('estatistika/', statistics_page, name='statistics_page'),
]
