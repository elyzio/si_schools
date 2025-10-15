from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Turma

# =============================================================================
# TURMA CRUD
# =============================================================================

@login_required
def turma_list(request):
    turmas = Turma.objects.all()
    context = {
        'page_title': 'Turma',
        'turmas': turmas,
    }
    return render(request, 'custom/turma/turma_list.html', context)

@login_required
def turma_create(request):
    if request.method == 'POST':
        turma = request.POST.get('turma')
        if turma:
            try:
                Turma.objects.create(turma=turma)
                messages.success(request, 'Turma created successfully!')
                return redirect('turma_list')
            except Exception as e:
                messages.error(request, f'Error creating turma: {str(e)}')
        else:
            messages.error(request, 'Turma is required!')

    context = {
        'page_title': 'Add Turma',
    }
    return render(request, 'custom/turma/turma_form.html', context)

@login_required
def turma_update(request, pk):
    turma = get_object_or_404(Turma, pk=pk)

    if request.method == 'POST':
        turma_value = request.POST.get('turma')
        if turma_value:
            try:
                turma.turma = turma_value
                turma.save()
                messages.success(request, 'Turma updated successfully!')
                return redirect('turma_list')
            except Exception as e:
                messages.error(request, f'Error updating turma: {str(e)}')
        else:
            messages.error(request, 'Turma is required!')

    context = {
        'page_title': 'Edit Turma',
        'turma': turma,
    }
    return render(request, 'custom/turma/turma_form.html', context)

@login_required
def turma_delete(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        try:
            turma.delete()
            messages.success(request, 'Turma deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting turma: {str(e)}')
    return redirect('turma_list')
