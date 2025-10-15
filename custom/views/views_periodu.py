from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Periodo

# =============================================================================
# PERIODO CRUD
# =============================================================================

@login_required
def periodo_list(request):
    periodos = Periodo.objects.all()
    context = {
        'page_title': 'Periodo',
        'periodos': periodos,
    }
    return render(request, 'custom/periodo/periodo_list.html', context)

@login_required
def periodo_create(request):
    if request.method == 'POST':
        period = request.POST.get('period')
        is_active = request.POST.get('is_active') == 'on'
        if period:
            try:
                Periodo.objects.create(period=period, is_active=is_active)
                messages.success(request, 'Periodo created successfully!')
                return redirect('periodo_list')
            except Exception as e:
                messages.error(request, f'Error creating periodo: {str(e)}')
        else:
            messages.error(request, 'Period is required!')

    context = {
        'page_title': 'Add Periodo',
    }
    return render(request, 'custom/periodo/periodo_form.html', context)

@login_required
def periodo_update(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)

    if request.method == 'POST':
        period = request.POST.get('period')
        is_active = request.POST.get('is_active') == 'on'
        if period:
            try:
                periodo.period = period
                periodo.is_active = is_active
                periodo.save()
                messages.success(request, 'Periodo updated successfully!')
                return redirect('periodo_list')
            except Exception as e:
                messages.error(request, f'Error updating periodo: {str(e)}')
        else:
            messages.error(request, 'Period is required!')

    context = {
        'page_title': 'Edit Periodo',
        'periodo': periodo,
    }
    return render(request, 'custom/periodo/periodo_form.html', context)

@login_required
def periodo_delete(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    if request.method == 'POST':
        try:
            periodo.delete()
            messages.success(request, 'Periodo deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting periodo: {str(e)}')
    return redirect('periodo_list')

@login_required
def periodo_toggle_active(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    if request.method == 'POST':
        try:
            # Set this periodo as active and all others as inactive
            Periodo.objects.filter(is_active=True).update(is_active=False)
            periodo.is_active = True
            periodo.save()
            messages.success(request, f'Periodo {periodo.period} is now active!')
        except Exception as e:
            messages.error(request, f'Error activating periodo: {str(e)}')
    return redirect('periodo_list')

