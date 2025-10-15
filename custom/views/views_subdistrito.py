from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Distrito, Subdistrito

# =============================================================================
# SUBDISTRITO CRUD
# =============================================================================

@login_required
def subdistrito_list(request):
    subdistritos = Subdistrito.objects.select_related('distrito').all()
    context = {
        'page_title': 'Subdistrito',
        'subdistritos': subdistritos,
    }
    return render(request, 'custom/subdistrito/subdistrito_list.html', context)

@login_required
def subdistrito_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        distrito_id = request.POST.get('distrito')
        if nome and distrito_id:
            try:
                distrito = Distrito.objects.get(pk=distrito_id)
                Subdistrito.objects.create(nome=nome, distrito=distrito)
                messages.success(request, 'Subdistrito created successfully!')
                return redirect('subdistrito_list')
            except Exception as e:
                messages.error(request, f'Error creating subdistrito: {str(e)}')
        else:
            messages.error(request, 'All fields are required!')

    context = {
        'page_title': 'Add Subdistrito',
        'distritos': Distrito.objects.all(),
    }
    return render(request, 'custom/subdistrito/subdistrito_form.html', context)

@login_required
def subdistrito_update(request, pk):
    subdistrito = get_object_or_404(Subdistrito, pk=pk)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        distrito_id = request.POST.get('distrito')
        if nome and distrito_id:
            try:
                distrito = Distrito.objects.get(pk=distrito_id)
                subdistrito.nome = nome
                subdistrito.distrito = distrito
                subdistrito.save()
                messages.success(request, 'Subdistrito updated successfully!')
                return redirect('subdistrito_list')
            except Exception as e:
                messages.error(request, f'Error updating subdistrito: {str(e)}')
        else:
            messages.error(request, 'All fields are required!')

    context = {
        'page_title': 'Edit Subdistrito',
        'subdistrito': subdistrito,
        'distritos': Distrito.objects.all(),
    }
    return render(request, 'custom/subdistrito/subdistrito_form.html', context)

@login_required
def subdistrito_delete(request, pk):
    subdistrito = get_object_or_404(Subdistrito, pk=pk)
    if request.method == 'POST':
        try:
            subdistrito.delete()
            messages.success(request, 'Subdistrito deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting subdistrito: {str(e)}')
    return redirect('subdistrito_list')

