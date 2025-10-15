from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Suco, Aldeia

# =============================================================================
# ALDEIA CRUD
# =============================================================================

@login_required
def aldeia_list(request):
    aldeias = Aldeia.objects.select_related('suco', 'suco__subdistrito', 'suco__subdistrito__distrito').all()
    context = {
        'page_title': 'Aldeia',
        'aldeias': aldeias,
    }
    return render(request, 'custom/aldeia/aldeia_list.html', context)

@login_required
def aldeia_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        suco_id = request.POST.get('suco')
        if nome and suco_id:
            try:
                suco = Suco.objects.get(pk=suco_id)
                Aldeia.objects.create(nome=nome, suco=suco)
                messages.success(request, 'Aldeia created successfully!')
                return redirect('aldeia_list')
            except Exception as e:
                messages.error(request, f'Error creating aldeia: {str(e)}')
        else:
            messages.error(request, 'All fields are required!')

    context = {
        'page_title': 'Add Aldeia',
        'sucos': Suco.objects.select_related('subdistrito', 'subdistrito__distrito').all(),
    }
    return render(request, 'custom/aldeia/aldeia_form.html', context)

@login_required
def aldeia_update(request, pk):
    aldeia = get_object_or_404(Aldeia, pk=pk)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        suco_id = request.POST.get('suco')
        if nome and suco_id:
            try:
                suco = Suco.objects.get(pk=suco_id)
                aldeia.nome = nome
                aldeia.suco = suco
                aldeia.save()
                messages.success(request, 'Aldeia updated successfully!')
                return redirect('aldeia_list')
            except Exception as e:
                messages.error(request, f'Error updating aldeia: {str(e)}')
        else:
            messages.error(request, 'All fields are required!')

    context = {
        'page_title': 'Edit Aldeia',
        'aldeia': aldeia,
        'sucos': Suco.objects.select_related('subdistrito', 'subdistrito__distrito').all(),
    }
    return render(request, 'custom/aldeia/aldeia_form.html', context)

@login_required
def aldeia_delete(request, pk):
    aldeia = get_object_or_404(Aldeia, pk=pk)
    if request.method == 'POST':
        try:
            aldeia.delete()
            messages.success(request, 'Aldeia deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting aldeia: {str(e)}')
    return redirect('aldeia_list')

