from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import JsonResponse
from estudante.models import Estudante, EstudanteUser, EstudanteClasse, EstudanteEncarregadu, EstudanteDokumentu, EstudanteTransfer
from estudante.forms import EstudanteForm, EstudanteClasseForm, EstudanteEncarregaduForm, EstudanteDokumentuForm, EstudanteTransferForm
from custom.models import Ano, Departamentu, Periodo
from datetime import datetime
from professor.models import ProfessorClasse, ProfessorMateria
from valor.forms import ValorProftoEstForm
from valor.models import Valor
from django.db.models import Count, Case, When, IntegerField

# Views for professors to manage students can be added here

@login_required
def EstudanteTurmaProfList(request):
    # Get filter parameters
    year_filter = request.GET.get('year', '')
    sexu_filter = request.GET.get('sexu', '')
    dept_filter = request.GET.get('dept', '')  # department filter
    classe_filter = request.GET.get('classe', '')  # class filter
    turma_filter = request.GET.get('turma', '')  # turma filter
    

    # Base queryset - exclude transferred OUT students
    professor = request.user.professoruser.professor
    profTurmas = ProfessorClasse.objects.filter(professor=professor)

    if not profTurmas.exists():
        profTurma = None
        estudanteTurma = EstudanteClasse.objects.none()
        estudanteTurmaStats = 0
    else:
        profTurma = profTurmas.first()
        # prof = profTurma
        estudanteTurma = EstudanteClasse.objects.filter(
            ano=profTurma.ano, 
            classe=profTurma.classe, 
            turma=profTurma.turma, 
            departamentu=profTurma.departamentu,
            estudante__sexu__icontains=sexu_filter
            ).select_related('estudante').order_by('estudante__nome')
        
        estudanteTurmaStats = EstudanteClasse.objects.filter(
            ano=profTurma.ano,
            classe=profTurma.classe,
            turma=profTurma.turma,
            departamentu=profTurma.departamentu
        ).aggregate(
            total_students=Count('estudante', distinct=True),
            total_male=Count('estudante', filter=Q(estudante__sexu='M'), distinct=True),
            total_female=Count('estudante', filter=Q(estudante__sexu='F'), distinct=True),
        )
    print(estudanteTurmaStats)

    context = {
        'page_title': 'Estudante',
        'estudantes': estudanteTurma,
        'professor': profTurma,
        'sexu_filter': sexu_filter,
        'estCountSexu': estudanteTurmaStats,
    }
    return render(request, 'estudante/prof/estudante_list.html', context)


def EstudanteHanorinProfList(request):
    periodu_active = Periodo.objects.filter(is_active=True).first()
    active_ano = Ano.objects.filter(is_active=True).first()
    # Get filter parameters
    year_filter = request.GET.get('year', '')
    dept_filter = request.GET.get('dept_filter', '')  # department filter
    classe_filter = request.GET.get('classe_filter', '')  # class filter
    turma_filter = request.GET.get('turma_filter', '')  # turma filter
    periodo_filter = request.GET.get('periodo', '')

    periodos = Periodo.objects.all().order_by('period')
    if not periodo_filter and periodu_active:
        periodo_filter = str(periodu_active.id)
    elif not periodo_filter and periodos.exists():
        periodo_filter = str(periodos[0].id)
    
    professor = request.user.professoruser.professor
    profMaterias = ProfessorMateria.objects.filter(professor=professor, is_active=True)

    estudantes = EstudanteClasse.objects.none()

    profMateria = None
    departments = []
    classes = []
    turmas = []
    if profMaterias.exists():
        profMateria = profMaterias.first()
        # print(profMateria.materia)
        materia = profMateria.materia
        if materia.departamentu is None:
            estudantes = EstudanteClasse.objects.filter(ano=active_ano, classe=profMateria.classe).order_by('-departamentu', 'turma', 'estudante__nome')
        else:
            estudantes = EstudanteClasse.objects.filter(ano=active_ano, classe=profMateria.classe, departamentu=materia.departamentu).order_by('turma', 'estudante__nome')

        # depTeachEst = estudantes.distinct('departamentu__sigla')
        depTeachEst = EstudanteClasse.objects.filter(ano=active_ano, classe=profMateria.classe).values(
                'departamentu__id', 'departamentu__departamento', 'departamentu__sigla'
            ).annotate(count=Count('estudante', distinct=True)).order_by('departamentu__departamento')
        departments = list(depTeachEst)
        if dept_filter:
            estudante_dept_filter = estudantes.filter(departamentu__id__icontains=dept_filter)
            estudantes = estudante_dept_filter
        
            # clasTeachEst = estudantes.distinct('classe__classe')
            clasTeachEst = EstudanteClasse.objects.filter(ano=active_ano, classe=profMateria.classe,departamentu_id=dept_filter).values(
                    'classe__id', 'classe__classe'
                ).annotate(count=Count('estudante', distinct=True)).order_by('classe__classe')
            classes = list(clasTeachEst)
            if classe_filter:
                estudante_classe_filter = estudantes.filter(classe__id__icontains=classe_filter)
                estudantes = estudante_classe_filter
        
                # turmaTeachEst = estudantes.distinct('turma__turma')
                turmaTeachEst = EstudanteClasse.objects.filter(ano=active_ano, classe=profMateria.classe,departamentu_id=dept_filter,classe_id=classe_filter).values(
                        'turma__id', 'turma__turma'
                    ).annotate(count=Count('estudante', distinct=True)).order_by('turma__turma')
                turmas = list(turmaTeachEst)
                if turma_filter:
                    estudante_turma_filter = estudantes.filter(turma__id__icontains=turma_filter)
                    estudantes = estudante_turma_filter
        estudantesValores = []
        for est in estudantes:
            valor = Valor.objects.filter(estudante_classe=est, materia=materia, periodo__id=periodo_filter).first()
            # valor = vl
            estudantesValores.append((est, valor))

    context = {
        'page_title': 'Estudante Hanorin',
        'estudantes': estudantesValores,
        'dept_filter':dept_filter,
        'turma_filter':turma_filter,
        'classe_filter':classe_filter,
        'profMateria': profMateria,
        'profMaterias': profMaterias,
        'departments':departments,
        'classes':classes,
        'turmas':turmas,
        'page':'list',
        'periodu_active': periodu_active,
        'periodos': periodos,
        'periodo_filter': periodo_filter,
    }
    return render(request, 'estudante/prof/estudante_list_hanorin.html', context)

def EstdanteValorProfadd(request, pk, period_id):
    estudante = get_object_or_404(EstudanteClasse, pk=pk)
    period_est = get_object_or_404(Periodo, pk=period_id)
    print(estudante)
    prof = request.user.professoruser.professor
    profMateria = ProfessorMateria.objects.filter(professor=prof, is_active=True).first()
    if request.method == "POST":
        form = ValorProftoEstForm(request.POST, period_id=period_id)
        if form.is_valid():
            form_valor = form.save(commit=False)
            form_valor.estudante_classe = estudante
            form_valor.materia = profMateria.materia
            form_valor.save()
            messages.success(request, "Valor Added successfully.")
            return redirect('est_prof_hanorin_list')

    else:
        form = ValorProftoEstForm(period_id=period_id)
    context = {
        'page_title':'Add valor',
        'page':'form',
        'form':form,
        'period_est': period_est,
    }
    return render(request, 'estudante/prof/estudante_list_hanorin.html', context)

def EstdanteValorProfEdit(request, val_id):
    # estudante = get_object_or_404(EstudanteClasse, pk=pk)
    estudante_valor = get_object_or_404(Valor, pk=val_id)
    print(estudante_valor)
    prof = request.user.professoruser.professor
    profMateria = ProfessorMateria.objects.filter(professor=prof, is_active=True).first()
    if request.method == "POST":
        form = ValorProftoEstForm(request.POST, instance=estudante_valor)
        if form.is_valid():
            form.save()
            messages.success(request, "Valor updated successfully.")
            return redirect('est_prof_hanorin_list')

    else:
        form = ValorProftoEstForm(instance=estudante_valor)
    context = {
        'page_title':'Update valor',
        'page':'form',
        'form':form
    }
    return render(request, 'estudante/prof/estudante_list_hanorin.html', context)

def EstudanteValorProfLock(request, val_id):
    estudante_valor = get_object_or_404(Valor, pk=val_id)
    if request.method == "POST":
        # print(estudante_valor)
        estudante_valor.is_lock = True
        estudante_valor.save()
        messages.success(request, "Valor locked successfully.")
        return redirect('est_prof_hanorin_list')