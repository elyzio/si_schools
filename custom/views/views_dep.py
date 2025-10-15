from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Departamentu

# =============================================================================
# DEPARTAMENTU CRUD
# =============================================================================

@login_required
def departamentu_list(request):
    departamentus = Departamentu.objects.all()
    context = {
        'page_title': 'Departmento',
        'departamentus': departamentus,
    }
    return render(request, 'custom/dep/departamentu_list.html', context)

@login_required
def departamentu_create(request):
    if request.method == 'POST':
        departamento = request.POST.get('departamento')
        sigla = request.POST.get('sigla')
        if departamento:
            try:
                Departamentu.objects.create(departamento=departamento, sigla=sigla)
                messages.success(request, 'Departamento created successfully!')
                return redirect('departamentu_list')
            except Exception as e:
                messages.error(request, f'Error creating departamento: {str(e)}')
        else:
            messages.error(request, 'Departamento is required!')

    context = {
        'page_title': 'Add Departmento',
    }
    return render(request, 'custom/dep/departamentu_form.html', context)

@login_required
def departamentu_update(request, pk):
    departamentu = get_object_or_404(Departamentu, pk=pk)

    if request.method == 'POST':
        departamento = request.POST.get('departamento')
        sigla = request.POST.get('sigla')
        if departamento:
            try:
                departamentu.departamento = departamento
                departamentu.sigla = sigla
                departamentu.save()
                messages.success(request, 'Departamento updated successfully!')
                return redirect('departamentu_list')
            except Exception as e:
                messages.error(request, f'Error updating departamento: {str(e)}')
        else:
            messages.error(request, 'Departamento is required!')

    context = {
        'page_title': 'Edit Departmento',
        'departamentu': departamentu,
    }
    return render(request, 'custom/dep/departamentu_form.html', context)

@login_required
def departamentu_delete(request, pk):
    departamentu = get_object_or_404(Departamentu, pk=pk)
    if request.method == 'POST':
        try:
            departamentu.delete()
            messages.success(request, 'Departamento deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting departamento: {str(e)}')
    return redirect('departamentu_list')
