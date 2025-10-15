from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from professor.models import ProfessorMateria
from professor.forms import ProfessorMateriaForm

# =============================================================================
# PROFESSORMATERIA VIEWS
# =============================================================================

@login_required
def professormateria_list(request):
    professormaterias = ProfessorMateria.objects.all().select_related(
        'professor', 'materia', 'classe'
    ).order_by('-created_at')
    context = {
        'page_title': 'Lista de Professor-Matéria',
        'professormaterias': professormaterias,
    }
    return render(request, 'professor/professormateria/professormateria_list.html', context)

@login_required
def professormateria_create(request):
    if request.method == 'POST':
        form = ProfessorMateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materia atribui ba profesor ho suksesu!')
            return redirect('professormateria_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu.')
    else:
        form = ProfessorMateriaForm()

    context = {
        'page_title': 'Atribuir Matéria ao Professor',
        'form': form,
    }
    return render(request, 'professor/professormateria/professormateria_form.html', context)

@login_required
def professormateria_detail(request, pk):
    professormateria = get_object_or_404(ProfessorMateria, pk=pk)
    context = {
        'page_title': f'Detalhes: {professormateria}',
        'professormateria': professormateria,
    }
    return render(request, 'professor/professormateria/professormateria_detail.html', context)

@login_required
def professormateria_update(request, pk):
    professormateria = get_object_or_404(ProfessorMateria, pk=pk)
    if request.method == 'POST':
        form = ProfessorMateriaForm(request.POST, instance=professormateria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atribuisaun hadia ho suksesu!')
            return redirect('professormateria_detail', pk=pk)
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu.')
    else:
        form = ProfessorMateriaForm(instance=professormateria)

    context = {
        'page_title': f'Editar: {professormateria}',
        'form': form,
        'professormateria': professormateria,
    }
    return render(request, 'professor/professormateria/professormateria_form.html', context)

@login_required
def professormateria_delete(request, pk):
    professormateria = get_object_or_404(ProfessorMateria, pk=pk)
    if request.method == 'POST':
        professormateria.delete()
        messages.success(request, 'Atribuisaun hamos ho suksesu!')
        return redirect('professormateria_list')

    context = {
        'page_title': 'Deletar Atribuição',
        'professormateria': professormateria,
    }
    return render(request, 'professor/professormateria/professormateria_confirm_delete.html', context)