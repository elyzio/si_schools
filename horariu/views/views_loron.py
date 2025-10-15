from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from horariu.models import Loron
from horariu.forms import LoronForm


@login_required
def loron_list(request):
    """List all Loron records"""
    lorons = Loron.objects.all().order_by('ordem')
    context = {
        'object_list': lorons,
        'title': 'Lista Loron'
    }
    return render(request, 'horariu/loron/loron_list.html', context)


@login_required
def loron_create(request):
    """Create a new Loron"""
    if request.method == 'POST':
        form = LoronForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loron kria ho suksesu')
            return redirect('loron_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = LoronForm()

    context = {
        'form': form,
        'title': 'Kria Loron'
    }
    return render(request, 'horariu/loron/loron_form.html', context)


@login_required
def loron_detail(request, pk):
    """View details of a specific Loron"""
    loron = get_object_or_404(Loron, pk=pk)
    context = {
        'loron': loron,
        'title': 'Detallu Loron'
    }
    return render(request, 'horariu/loron/loron_detail.html', context)


@login_required
def loron_update(request, pk):
    """Update an existing Loron"""
    loron = get_object_or_404(Loron, pk=pk)

    if request.method == 'POST':
        form = LoronForm(request.POST, instance=loron)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loron hadia ho suksesu')
            return redirect('loron_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = LoronForm(instance=loron)

    context = {
        'form': form,
        'loron': loron,
        'title': 'Hadia Loron'
    }
    return render(request, 'horariu/loron/loron_form.html', context)


@login_required
def loron_delete(request, pk):
    """Delete a Loron"""
    loron = get_object_or_404(Loron, pk=pk)

    if request.method == 'POST':
        loron.delete()
        messages.success(request, 'Loron hamos ho suksesu')
        return redirect('loron_list')

    context = {
        'loron': loron,
        'title': 'Hamos Loron'
    }
    return render(request, 'horariu/loron/loron_confirm_delete.html', context)