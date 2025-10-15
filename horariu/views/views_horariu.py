from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from horariu.models import Horariu
from horariu.forms import HorariuForm


@login_required
def horariu_list(request):
    """List all Horariu records with related data"""
    horarius = Horariu.objects.select_related(
        'loron', 'horas', 'classe', 'turma',
        'departamentu', 'professor_materia',
        'professor_materia__professor',
        'professor_materia__materia',
        'ano_academico'
    ).order_by('loron__ordem', 'horas__horas_hahu')

    context = {
        'horarius': horarius,
        'title': 'Lista Horariu'
    }
    return render(request, 'horariu/horariu/horariu_list.html', context)


@login_required
def horariu_create(request):
    """Create a new Horariu"""
    if request.method == 'POST':
        form = HorariuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horariu kria ho suksesu')
            return redirect('horariu_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorariuForm()

    context = {
        'form': form,
        'title': 'Kria Horariu'
    }
    return render(request, 'horariu/horariu/horariu_form.html', context)


@login_required
def horariu_detail(request, pk):
    """View details of a specific Horariu"""
    horariu = get_object_or_404(
        Horariu.objects.select_related(
            'loron', 'horas', 'classe', 'turma',
            'departamentu', 'professor_materia',
            'professor_materia__professor',
            'professor_materia__materia',
            'ano_academico'
        ),
        pk=pk
    )
    context = {
        'horariu': horariu,
        'title': 'Detallu Horariu'
    }
    return render(request, 'horariu/horariu/horariu_detail.html', context)


@login_required
def horariu_update(request, pk):
    """Update an existing Horariu"""
    horariu = get_object_or_404(Horariu, pk=pk)

    if request.method == 'POST':
        form = HorariuForm(request.POST, instance=horariu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horariu hadia ho suksesu')
            return redirect('horariu_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorariuForm(instance=horariu)

    context = {
        'form': form,
        'horariu': horariu,
        'title': 'Hadia Horariu'
    }
    return render(request, 'horariu/horariu/horariu_form.html', context)


@login_required
def horariu_delete(request, pk):
    """Delete a Horariu"""
    horariu = get_object_or_404(Horariu, pk=pk)

    if request.method == 'POST':
        horariu.delete()
        messages.success(request, 'Horariu hamos ho suksesu')
        return redirect('horariu_list')

    context = {
        'horariu': horariu,
        'title': 'Hamos Horariu'
    }
    return render(request, 'horariu/horariu/horariu_confirm_delete.html', context)