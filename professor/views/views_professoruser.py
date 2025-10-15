from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from professor.models import ProfessorUser
from professor.forms import ProfessorUserForm

# =============================================================================
# PROFESSORUSER VIEWS
# =============================================================================

@login_required
def professoruser_list(request):
    professorusers = ProfessorUser.objects.all().select_related('professor', 'user').order_by('-created_at')
    context = {
        'page_title': 'Lista de Professor-Usuário',
        'professorusers': professorusers,
    }
    return render(request, 'professor/professoruser/professoruser_list.html', context)

@login_required
def professoruser_create(request):
    if request.method == 'POST':
        form = ProfessorUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Relasaun Profesor-Uzuariu kria ho suksesu!')
            return redirect('professoruser_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu.')
    else:
        form = ProfessorUserForm()

    context = {
        'page_title': 'Adicionar Professor-Usuário',
        'form': form,
    }
    return render(request, 'professor/professoruser/professoruser_form.html', context)

@login_required
def professoruser_detail(request, pk):
    professoruser = get_object_or_404(ProfessorUser, pk=pk)
    context = {
        'page_title': f'Detalhes: {professoruser.professor.nome}',
        'professoruser': professoruser,
    }
    return render(request, 'professor/professoruser/professoruser_detail.html', context)

@login_required
def professoruser_update(request, pk):
    professoruser = get_object_or_404(ProfessorUser, pk=pk)
    if request.method == 'POST':
        form = ProfessorUserForm(request.POST, instance=professoruser)
        if form.is_valid():
            form.save()
            messages.success(request, 'Relasaun Profesor-Uzuariu hadia ho suksesu!')
            return redirect('professoruser_detail', pk=pk)
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu.')
    else:
        form = ProfessorUserForm(instance=professoruser)

    context = {
        'page_title': f'Editar: {professoruser.professor.nome}',
        'form': form,
        'professoruser': professoruser,
    }
    return render(request, 'professor/professoruser/professoruser_form.html', context)

@login_required
def professoruser_delete(request, pk):
    professoruser = get_object_or_404(ProfessorUser, pk=pk)
    if request.method == 'POST':
        professoruser.delete()
        messages.success(request, 'Relasaun Profesor-Uzuariu hamos ho suksesu!')
        return redirect('professoruser_list')

    context = {
        'page_title': 'Deletar Professor-Usuário',
        'professoruser': professoruser,
    }
    return render(request, 'professor/professoruser/professoruser_confirm_delete.html', context)