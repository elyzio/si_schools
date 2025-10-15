from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Subdistrito, Suco

# =============================================================================
# SUCO CRUD
# =============================================================================

@login_required
def suco_list(request):
    sucos = Suco.objects.select_related('subdistrito', 'subdistrito__distrito').all()
    context = {
        'page_title': 'Suco',
        'sucos': sucos,
    }
    return render(request, 'custom/suco/suco_list.html', context)

@login_required
def suco_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        subdistrito_id = request.POST.get('subdistrito')
        if nome and subdistrito_id:
            try:
                subdistrito = Subdistrito.objects.get(pk=subdistrito_id)
                Suco.objects.create(nome=nome, subdistrito=subdistrito)
                messages.success(request, 'Suco created successfully!')
                return redirect('suco_list')
            except Exception as e:
                messages.error(request, f'Error creating suco: {str(e)}')
        else:
            messages.error(request, 'All fields are required!')

    context = {
        'page_title': 'Add Suco',
        'subdistritos': Subdistrito.objects.select_related('distrito').all(),
    }
    return render(request, 'custom/suco/suco_form.html', context)

@login_required
def suco_update(request, pk):
    suco = get_object_or_404(Suco, pk=pk)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        subdistrito_id = request.POST.get('subdistrito')
        if nome and subdistrito_id:
            try:
                subdistrito = Subdistrito.objects.get(pk=subdistrito_id)
                suco.nome = nome
                suco.subdistrito = subdistrito
                suco.save()
                messages.success(request, 'Suco updated successfully!')
                return redirect('suco_list')
            except Exception as e:
                messages.error(request, f'Error updating suco: {str(e)}')
        else:
            messages.error(request, 'All fields are required!')

    context = {
        'page_title': 'Edit Suco',
        'suco': suco,
        'subdistritos': Subdistrito.objects.select_related('distrito').all(),
    }
    return render(request, 'custom/suco/suco_form.html', context)

@login_required
def suco_delete(request, pk):
    suco = get_object_or_404(Suco, pk=pk)
    if request.method == 'POST':
        try:
            suco.delete()
            messages.success(request, 'Suco deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting suco: {str(e)}')
    return redirect('suco_list')

