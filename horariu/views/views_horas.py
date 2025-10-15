from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from horariu.models import Horas
from horariu.forms import HorasForm


@login_required
def horas_list(request):
    """List all Horas records"""
    horas = Horas.objects.all().order_by('horas_hahu')
    # print(horas)
    context = {
        'object_list': horas,
        'title': 'Lista Oras'
    }
    return render(request, 'horariu/horas/horas_list.html', context)


@login_required
def horas_create(request):
    """Create a new Horas"""
    if request.method == 'POST':
        form = HorasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oras kria ho suksesu')
            return redirect('horas_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorasForm()

    context = {
        'form': form,
        'title': 'Kria Oras'
    }
    return render(request, 'horariu/horas/horas_form.html', context)


@login_required
def horas_detail(request, pk):
    """View details of a specific Horas"""
    horas = get_object_or_404(Horas, pk=pk)
    context = {
        'horas': horas,
        'title': 'Detallu Oras'
    }
    return render(request, 'horariu/horas/horas_detail.html', context)


@login_required
def horas_update(request, pk):
    """Update an existing Horas"""
    horas = get_object_or_404(Horas, pk=pk)

    if request.method == 'POST':
        form = HorasForm(request.POST, instance=horas)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oras hadia ho suksesu')
            return redirect('horas_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorasForm(instance=horas)

    context = {
        'form': form,
        'horas': horas,
        'title': 'Hadia Oras'
    }
    return render(request, 'horariu/horas/horas_form.html', context)


@login_required
def horas_delete(request, pk):
    """Delete a Horas"""
    horas = get_object_or_404(Horas, pk=pk)

    if request.method == 'POST':
        horas.delete()
        messages.success(request, 'Oras hamos ho suksesu')
        return redirect('horas_list')

    context = {
        'horas': horas,
        'title': 'Hamos Oras'
    }
    return render(request, 'horariu/horas/horas_confirm_delete.html', context)