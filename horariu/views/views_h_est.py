from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from horariu.models import Horariu
from horariu.forms import HorariuForm
from estudante.models import Estudante, EstudanteClasse
from custom.models import Ano


@login_required
def HorariuListEst(request):
    """List all Horariu records for the logged-in estudante"""

    try:
        estudante = request.user.estudanteuser.estudante
        # print(estudante.get_current_classe_turma())
    except:
        messages.error(request, 'Ita la rejista hanesan estudante')
        return redirect('home')
    
    ano_active = Ano.objects.filter(is_active=True).first()
    estudante_classe = EstudanteClasse.objects.filter(estudante=estudante, ano=ano_active).first()
    horarius = Horariu.objects.by_class(estudante_classe.classe, estudante_classe.departamentu, estudante_classe.turma,ano_active)
    print(horarius)

    context = {
        'horarius': horarius,
        'page_title': 'Hau nia Horariu',
        'estudante': estudante,
    }
    return render(request, 'horariu/horariu/horariu_list.html', context)

