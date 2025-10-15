from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Ano

# =============================================================================
# ANO CRUD
# =============================================================================

@login_required
def ano_list(request):
    anos = Ano.objects.all()
    context = {
        'page_title': 'Ano Akademiku',
        'anos': anos,
    }
    return render(request, 'custom/ano/ano_list.html', context)

@login_required
def ano_create(request):
    if request.method == 'POST':
        ano = request.POST.get('ano')
        is_active = request.POST.get('is_active') == 'on'
        if ano:
            try:
                Ano.objects.create(ano=int(ano), is_active=is_active)
                messages.success(request, 'Ano created successfully!')
                return redirect('ano_list')
            except Exception as e:
                messages.error(request, f'Error creating ano: {str(e)}')
        else:
            messages.error(request, 'Ano is required!')

    context = {
        'page_title': 'Add Ano Akademiku',
    }
    return render(request, 'custom/ano/ano_form.html', context)

@login_required
def ano_update(request, pk):
    ano = get_object_or_404(Ano, pk=pk)

    if request.method == 'POST':
        ano_value = request.POST.get('ano')
        is_active = request.POST.get('is_active') == 'on'
        if ano_value:
            try:
                ano.ano = int(ano_value)
                ano.is_active = is_active
                ano.save()
                messages.success(request, 'Ano updated successfully!')
                return redirect('ano_list')
            except Exception as e:
                messages.error(request, f'Error updating ano: {str(e)}')
        else:
            messages.error(request, 'Ano is required!')

    context = {
        'page_title': 'Edit Ano Akademiku',
        'ano': ano,
    }
    return render(request, 'custom/ano/ano_form.html', context)

@login_required
def ano_delete(request, pk):
    ano = get_object_or_404(Ano, pk=pk)
    if request.method == 'POST':
        try:
            ano.delete()
            messages.success(request, 'Ano deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting ano: {str(e)}')
    return redirect('ano_list')

@login_required
def ano_toggle_active(request, pk):
    ano = get_object_or_404(Ano, pk=pk)
    if request.method == 'POST':
        try:
            # Set this ano as active and all others as inactive
            Ano.objects.filter(is_active=True).update(is_active=False)
            ano.is_active = True
            ano.save()
            messages.success(request, f'Ano {ano.ano} is now active!')
        except Exception as e:
            messages.error(request, f'Error activating ano: {str(e)}')
    return redirect('ano_list')
