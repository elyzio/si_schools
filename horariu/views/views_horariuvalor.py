from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from horariu.models import HorariuValor
from horariu.forms import HorariuValorForm


@login_required
def horariuvalor_list(request):
    """List all HorariuValor records"""
    horariuvalors = HorariuValor.objects.all().order_by('data_hahu')
    context = {
        'horariuvalors': horariuvalors,
        'title': 'Lista Horariu Valor'
    }
    return render(request, 'horariu/horariuvalor/horariuvalor_list.html', context)


@login_required
def horariuvalor_create(request):
    """Create a new HorariuValor"""
    if request.method == 'POST':
        form = HorariuValorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horariu Valor kria ho suksesu')
            return redirect('horariuvalor_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorariuValorForm()

    context = {
        'form': form,
        'title': 'Kria Horariu Valor'
    }
    return render(request, 'horariu/horariuvalor/horariuvalor_form.html', context)


@login_required
def horariuvalor_detail(request, pk):
    """View details of a specific HorariuValor"""
    horariuvalor = get_object_or_404(HorariuValor, pk=pk)
    context = {
        'horariuvalor': horariuvalor,
        'title': 'Detallu Horariu Valor'
    }
    return render(request, 'horariu/horariuvalor/horariuvalor_detail.html', context)


@login_required
def horariuvalor_update(request, pk):
    """Update an existing HorariuValor"""
    horariuvalor = get_object_or_404(HorariuValor, pk=pk)

    if request.method == 'POST':
        form = HorariuValorForm(request.POST, instance=horariuvalor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horariu Valor hadia ho suksesu')
            return redirect('horariuvalor_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorariuValorForm(instance=horariuvalor)

    context = {
        'form': form,
        'horariuvalor': horariuvalor,
        'title': 'Hadia Horariu Valor'
    }
    return render(request, 'horariu/horariuvalor/horariuvalor_form.html', context)


@login_required
def horariuvalor_delete(request, pk):
    """Delete a HorariuValor"""
    horariuvalor = get_object_or_404(HorariuValor, pk=pk)

    if request.method == 'POST':
        horariuvalor.delete()
        messages.success(request, 'Horariu Valor hamos ho suksesu')
        return redirect('horariuvalor_list')

    context = {
        'horariuvalor': horariuvalor,
        'title': 'Hamos Horariu Valor'
    }
    return render(request, 'horariu/horariuvalor/horariuvalor_confirm_delete.html', context)