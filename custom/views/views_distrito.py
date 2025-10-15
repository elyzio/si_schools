from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Distrito

# =============================================================================
# DISTRITO CRUD
# =============================================================================

@login_required
def distrito_list(request):
    distritos = Distrito.objects.all()
    context = {
        'page_title': 'Distrito',
        'distritos': distritos,
    }
    return render(request, 'custom/distrito/distrito_list.html', context)

@login_required
def distrito_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            try:
                Distrito.objects.create(nome=nome)
                messages.success(request, 'Distrito created successfully!')
                return redirect('distrito_list')
            except Exception as e:
                messages.error(request, f'Error creating distrito: {str(e)}')
        else:
            messages.error(request, 'Nome is required!')

    context = {
        'page_title': 'Add Distrito',
    }
    return render(request, 'custom/distrito/distrito_form.html', context)

@login_required
def distrito_update(request, pk):
    distrito = get_object_or_404(Distrito, pk=pk)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            try:
                distrito.nome = nome
                distrito.save()
                messages.success(request, 'Distrito updated successfully!')
                return redirect('distrito_list')
            except Exception as e:
                messages.error(request, f'Error updating distrito: {str(e)}')
        else:
            messages.error(request, 'Nome is required!')

    context = {
        'page_title': 'Edit Distrito',
        'distrito': distrito,
    }
    return render(request, 'custom/distrito/distrito_form.html', context)

@login_required
def distrito_delete(request, pk):
    distrito = get_object_or_404(Distrito, pk=pk)
    if request.method == 'POST':
        try:
            distrito.delete()
            messages.success(request, 'Distrito deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting distrito: {str(e)}')
    return redirect('distrito_list')
