from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from custom.models import Classe

# =============================================================================
# CLASSE CRUD
# =============================================================================

@login_required
def classe_list(request):
    classes = Classe.objects.all()
    context = {
        'page_title': 'Klase',
        'classes': classes,
    }
    return render(request, 'custom/classe/classe_list.html', context)

@login_required
def classe_create(request):
    if request.method == 'POST':
        classe = request.POST.get('classe')
        if classe:
            try:
                Classe.objects.create(classe=classe)
                messages.success(request, 'Classe created successfully!')
                return redirect('classe_list')
            except Exception as e:
                messages.error(request, f'Error creating classe: {str(e)}')
        else:
            messages.error(request, 'Classe is required!')

    context = {
        'page_title': 'Add Klase',
    }
    return render(request, 'custom/classe/classe_form.html', context)

@login_required
def classe_update(request, pk):
    classe = get_object_or_404(Classe, pk=pk)

    if request.method == 'POST':
        classe_value = request.POST.get('classe')
        if classe_value:
            try:
                classe.classe = classe_value
                classe.save()
                messages.success(request, 'Classe updated successfully!')
                return redirect('classe_list')
            except Exception as e:
                messages.error(request, f'Error updating classe: {str(e)}')
        else:
            messages.error(request, 'Classe is required!')

    context = {
        'page_title': 'Edit Klase',
        'classe': classe,
    }
    return render(request, 'custom/classe/classe_form.html', context)

@login_required
def classe_delete(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    if request.method == 'POST':
        try:
            classe.delete()
            messages.success(request, 'Classe deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting classe: {str(e)}')
    return redirect('classe_list')
