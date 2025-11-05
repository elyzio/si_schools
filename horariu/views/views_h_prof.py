from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from horariu.models import Horariu
from horariu.forms import HorariuForm


@login_required
def HorariuListProf(request):
    """List all Horariu records for the logged-in professor"""

    try:
        professor = request.user.professoruser.professor
    except:
        messages.error(request, 'Ita la rejista hanesan profesor')
        return redirect('home')
    
    horarius = Horariu.objects.by_professor(professor)
    # horarius = Horariu.objects.select_related(
    #     'loron', 'horas', 'classe', 'turma',
    #     'departamentu', 'professor_materia',
    #     'professor_materia__professor',
    #     'professor_materia__materia',
    #     'ano_academico'
    # ).order_by('loron__ordem', 'horas__horas_hahu')

    context = {
        'horarius': horarius,
        'page_title': 'Hau nia Horariu',
        'professor': professor,
    }
    return render(request, 'horariu/horariu/horariu_list.html', context)

