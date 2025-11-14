from django.shortcuts import render
from django.db.models import Count, Q
from estudante.models import Estudante, EstudanteClasse
from professor.models import Professor, ProfessorClasse
from custom.models import Ano, Classe, Departamentu

# Create your views here.

