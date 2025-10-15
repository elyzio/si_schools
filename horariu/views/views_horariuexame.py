from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from horariu.models import HorariuExame
from horariu.forms import HorariuExameForm


@login_required
def horariuexame_list(request):
    """List all HorariuExame records with related data"""
    horariuexames = HorariuExame.objects.select_related(
        'loron', 'horas', 'departamentu', 'materia', 'ano_academico'
    ).order_by('loron__ordem', 'horas__horas_hahu')

    context = {
        'horariuexames': horariuexames,
        'title': 'Lista Horariu Exame'
    }
    return render(request, 'horariu/horariuexame/horariuexame_list.html', context)


@login_required
def horariuexame_create(request):
    """Create a new HorariuExame"""
    if request.method == 'POST':
        form = HorariuExameForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horariu Exame kria ho suksesu')
            return redirect('horariuexame_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorariuExameForm()

    context = {
        'form': form,
        'title': 'Kria Horariu Exame'
    }
    return render(request, 'horariu/horariuexame/horariuexame_form.html', context)


@login_required
def horariuexame_detail(request, pk):
    """View details of a specific HorariuExame"""
    horariuexame = get_object_or_404(
        HorariuExame.objects.select_related(
            'loron', 'horas', 'departamentu', 'materia', 'ano_academico'
        ),
        pk=pk
    )
    context = {
        'horariuexame': horariuexame,
        'title': 'Detallu Horariu Exame'
    }
    return render(request, 'horariu/horariuexame/horariuexame_detail.html', context)


@login_required
def horariuexame_update(request, pk):
    """Update an existing HorariuExame"""
    horariuexame = get_object_or_404(HorariuExame, pk=pk)

    if request.method == 'POST':
        form = HorariuExameForm(request.POST, instance=horariuexame)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horariu Exame hadia ho suksesu')
            return redirect('horariuexame_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorariuExameForm(instance=horariuexame)

    context = {
        'form': form,
        'horariuexame': horariuexame,
        'title': 'Hadia Horariu Exame'
    }
    return render(request, 'horariu/horariuexame/horariuexame_form.html', context)


@login_required
def horariuexame_delete(request, pk):
    """Delete a HorariuExame"""
    horariuexame = get_object_or_404(HorariuExame, pk=pk)

    if request.method == 'POST':
        horariuexame.delete()
        messages.success(request, 'Horariu Exame hamos ho suksesu')
        return redirect('horariuexame_list')

    context = {
        'horariuexame': horariuexame,
        'title': 'Hamos Horariu Exame'
    }
    return render(request, 'horariu/horariuexame/horariuexame_confirm_delete.html', context)