from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from konaba.models import KonaBa
from konaba.forms import KonaBaForm
from main.decorators import group_required

# =============================================================================
# KONABA VIEWS (Admin Only)
# =============================================================================

@login_required
@group_required('admin', 'director')
def konaba_list(request):
    konaba_list = KonaBa.objects.all()
    context = {
        'page_title': 'Kona Ba',
        'konaba_list': konaba_list,
    }
    return render(request, 'konaba/konaba_list.html', context)

@login_required
@group_required('admin', 'director')
def konaba_create(request):
    if request.method == 'POST':
        form = KonaBaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kona Ba kriadu ho susesu!')
            return redirect('konaba_list')
    else:
        form = KonaBaForm()

    return render(request, 'konaba/konaba_form.html', {'form': form})

@login_required
@group_required('admin', 'director')
def konaba_update(request, pk):
    konaba = get_object_or_404(KonaBa, pk=pk)

    if request.method == 'POST':
        form = KonaBaForm(request.POST, instance=konaba)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kona Ba atualiza ho susesu!')
            return redirect('konaba_list')
    else:
        form = KonaBaForm(instance=konaba)

    return render(request, 'konaba/konaba_form.html', {'form': form, 'konaba': konaba})

@login_required
@group_required('admin', 'director')
def konaba_delete(request, pk):
    konaba = get_object_or_404(KonaBa, pk=pk)

    if request.method == 'POST':
        konaba.delete()
        messages.success(request, 'Kona Ba hamos ho susesu!')
        return redirect('konaba_list')

    return render(request, 'konaba/konaba_confirm_delete.html', {'konaba': konaba})
