from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from custom.models import Ano, Departamentu, Periodo
from estudante.models import Estudante, EstudanteClasse, EstudanteAlumni
from professor.models import Professor

# Create your views here.

# @login_required
def Home(request):
    ano_active = Ano.objects.filter(is_active=True).first()
    estudante_count = EstudanteClasse.objects.filter(estudante__is_alumni=False, estudante__is_transfer=False, estudante__is_active=True, ano=ano_active).count()
    dep_count = Departamentu.objects.all().count()
    prof_count = Professor.objects.filter(is_active=True).count()
    alumni_count = Estudante.objects.filter(is_active=False, is_alumni=True, is_transfer=False).count()

    if request.user.is_authenticated:
        # Logged-in user
        template = 'home/home.html'
    else:
        # Not logged in
        template = 'landing/home.html'

    context = {
        'page_title': 'Home',
        'user': request.user if request.user.is_authenticated else None,
        'est_count': estudante_count,
        'prof_count': prof_count,
        'dep_count': dep_count,
        'alumni_count': alumni_count,
    }
    return render(request, template, context)