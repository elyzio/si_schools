from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Materia, Departamentu

# =============================================================================
# MATERIA CRUD
# =============================================================================

@login_required
def materia_list(request):
    materias = Materia.objects.select_related('departamentu').all()
    context = {
        'page_title': 'Disciplina',
        'materias': materias,
    }
    return render(request, 'custom/materia/materia_list.html', context)

@login_required
def materia_create(request):
    if request.method == 'POST':
        materia = request.POST.get('materia')
        codigo = request.POST.get('codigo')
        descricao = request.POST.get('descricao')
        departamentu_id = request.POST.get('departamentu')

        if materia and codigo:
            try:
                departamentu = None
                if departamentu_id:
                    departamentu = Departamentu.objects.get(pk=departamentu_id)

                Materia.objects.create(
                    materia=materia,
                    codigo=codigo,
                    descricao=descricao,
                    departamentu=departamentu
                )
                messages.success(request, 'Materia created successfully!')
                return redirect('materia_list')
            except Exception as e:
                messages.error(request, f'Error creating materia: {str(e)}')
        else:
            messages.error(request, 'Materia and Codigo are required!')

    context = {
        'page_title': 'Add Disciplina',
        'departamentus': Departamentu.objects.all(),
    }
    return render(request, 'custom/materia/materia_form.html', context)

@login_required
def materia_update(request, pk):
    materia = get_object_or_404(Materia, pk=pk)

    if request.method == 'POST':
        materia_value = request.POST.get('materia')
        codigo = request.POST.get('codigo')
        descricao = request.POST.get('descricao')
        departamentu_id = request.POST.get('departamentu')

        if materia_value and codigo:
            try:
                departamentu = None
                if departamentu_id:
                    departamentu = Departamentu.objects.get(pk=departamentu_id)

                materia.materia = materia_value
                materia.codigo = codigo
                materia.descricao = descricao
                materia.departamentu = departamentu
                materia.save()
                messages.success(request, 'Materia updated successfully!')
                return redirect('materia_list')
            except Exception as e:
                messages.error(request, f'Error updating materia: {str(e)}')
        else:
            messages.error(request, 'Materia and Codigo are required!')

    context = {
        'page_title': 'Edit Disciplina',
        'materia': materia,
        'departamentus': Departamentu.objects.all(),
    }
    return render(request, 'custom/materia/materia_form.html', context)

@login_required
def materia_delete(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    if request.method == 'POST':
        try:
            materia.delete()
            messages.success(request, 'Materia deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting materia: {str(e)}')
    return redirect('materia_list')
