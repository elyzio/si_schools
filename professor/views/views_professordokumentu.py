from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from professor.models import ProfessorDokumentu
from professor.forms import ProfessorDokumentuForm

# =============================================================================
# PROFESSORDOKUMENTU VIEWS
# =============================================================================

@login_required
def professordokumentu_list(request):
    professordokumentus = ProfessorDokumentu.objects.all().select_related('professor').order_by('-created_at')
    context = {
        'page_title': 'Lista de Documentos dos Professores',
        'professordokumentus': professordokumentus,
    }
    return render(request, 'professor/professordokumentu/professordokumentu_list.html', context)

@login_required
def professordokumentu_create(request):
    if request.method == 'POST':
        form = ProfessorDokumentuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dokumentu aumenta ho suksesu!')
            return redirect('professordokumentu_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu.')
    else:
        form = ProfessorDokumentuForm()

    context = {
        'page_title': 'Adicionar Documento',
        'form': form,
    }
    return render(request, 'professor/professordokumentu/professordokumentu_form.html', context)

@login_required
def professordokumentu_detail(request, pk):
    professordokumentu = get_object_or_404(ProfessorDokumentu, pk=pk)
    context = {
        'page_title': f'Detalhes: {professordokumentu}',
        'professordokumentu': professordokumentu,
    }
    return render(request, 'professor/professordokumentu/professordokumentu_detail.html', context)

@login_required
def professordokumentu_update(request, pk):
    professordokumentu = get_object_or_404(ProfessorDokumentu, pk=pk)
    if request.method == 'POST':
        form = ProfessorDokumentuForm(request.POST, request.FILES, instance=professordokumentu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dokumentu hadia ho suksesu!')
            return redirect('professordokumentu_detail', pk=pk)
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu.')
    else:
        form = ProfessorDokumentuForm(instance=professordokumentu)

    context = {
        'page_title': f'Editar: {professordokumentu}',
        'form': form,
        'professordokumentu': professordokumentu,
    }
    return render(request, 'professor/professordokumentu/professordokumentu_form.html', context)

@login_required
def professordokumentu_delete(request, pk):
    professordokumentu = get_object_or_404(ProfessorDokumentu, pk=pk)
    if request.method == 'POST':
        professordokumentu.delete()
        messages.success(request, 'Dokumentu hamos ho suksesu!')
        return redirect('professordokumentu_list')

    context = {
        'page_title': 'Deletar Documento',
        'professordokumentu': professordokumentu,
    }
    return render(request, 'professor/professordokumentu/professordokumentu_confirm_delete.html', context)