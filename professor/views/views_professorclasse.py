from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from professor.models import ProfessorClasse
from professor.forms import ProfessorClasseForm

# =============================================================================
# PROFESSORCLASSE VIEWS
# =============================================================================

@login_required
def professorclasse_list(request):
    professorclasses = ProfessorClasse.objects.all().select_related(
        'professor', 'ano', 'departamentu', 'classe'
    ).order_by('-created_at')
    context = {
        'page_title': 'Lista de Professor-Classe',
        'professorclasses': professorclasses,
    }
    return render(request, 'professor/professorclasse/professorclasse_list.html', context)

@login_required
def professorclasse_create(request):
    if request.method == 'POST':
        form = ProfessorClasseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profesor atribui ba klase ho suksesu!')
            return redirect('professorclasse_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu.')
    else:
        form = ProfessorClasseForm()

    context = {
        'page_title': 'Atribuir Professor à Classe',
        'form': form,
    }
    return render(request, 'professor/professorclasse/professorclasse_form.html', context)

@login_required
def professorclasse_detail(request, pk):
    professorclasse = get_object_or_404(ProfessorClasse, pk=pk)
    context = {
        'page_title': f'Detalhes: {professorclasse}',
        'professorclasse': professorclasse,
    }
    return render(request, 'professor/professorclasse/professorclasse_detail.html', context)

@login_required
def professorclasse_update(request, pk):
    professorclasse = get_object_or_404(ProfessorClasse, pk=pk)
    if request.method == 'POST':
        form = ProfessorClasseForm(request.POST, instance=professorclasse)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atribuisaun hadia ho suksesu!')
            return redirect('professorclasse_detail', pk=pk)
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu.')
    else:
        form = ProfessorClasseForm(instance=professorclasse)

    context = {
        'page_title': f'Editar: {professorclasse}',
        'form': form,
        'professorclasse': professorclasse,
    }
    return render(request, 'professor/professorclasse/professorclasse_form.html', context)

@login_required
def professorclasse_delete(request, pk):
    professorclasse = get_object_or_404(ProfessorClasse, pk=pk)
    if request.method == 'POST':
        professorclasse.delete()
        messages.success(request, 'Atribuisaun hamos ho suksesu!')
        return redirect('professorclasse_list')

    context = {
        'page_title': 'Deletar Atribuição',
        'professorclasse': professorclasse,
    }
    return render(request, 'professor/professorclasse/professorclasse_confirm_delete.html', context)