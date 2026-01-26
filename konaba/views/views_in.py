from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from konaba.models import Informasaun
from konaba.forms import InformasaunForm
from main.decorators import group_required

# =============================================================================
# INFORMASAUN VIEWS (Admin Only)
# =============================================================================

@login_required
@group_required('admin', 'director')
def informasaun_list(request):
    informasaun_list = Informasaun.objects.all()
    context = {
        'informasaun_list': informasaun_list,
        'page_title': 'Informasaun'
    }
    return render(request, 'informasaun/informasaun_list.html', context)

@login_required
@group_required('admin', 'director')
def informasaun_create(request):
    if request.method == 'POST':
        form = InformasaunForm(request.POST, request.FILES)
        if form.is_valid():
            informasaun = form.save(commit=False)
            informasaun.author = request.user
            informasaun.save()
            messages.success(request, 'Informasaun kriadu ho susesu!')
            return redirect('informasaun_list')
    else:
        form = InformasaunForm()

    context = {
        "page_title": "Aumenta Informasaun",
        "form": form,
    }

    return render(request, 'informasaun/informasaun_form.html', context)
    
@login_required
@group_required('admin', 'director')
def informasaun_detail(request, pk):
    informasaun = get_object_or_404(Informasaun, pk=pk)

    if request.method == 'POST':
        form = InformasaunForm(request.POST, request.FILES, instance=informasaun)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informasaun atualiza ho susesu!')
            return redirect('informasaun_list')
    else:
        form = InformasaunForm(instance=informasaun)

    context = {
        "page_title": "Detallu Informasaun",
        "form": form,
        "info": informasaun,
    }

    return render(request, 'informasaun/informasaun_detail.html', context)

@login_required
@group_required('admin', 'director')
def informasaun_update(request, pk):
    informasaun = get_object_or_404(Informasaun, pk=pk)

    if request.method == 'POST':
        form = InformasaunForm(request.POST, request.FILES, instance=informasaun)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informasaun atualiza ho susesu!')
            return redirect('informasaun_list')
    else:
        form = InformasaunForm(instance=informasaun)

    context = {
        "page_title": "Hadia Informasaun",
        "form": form,
    }

    return render(request, 'informasaun/informasaun_form.html', context)

@login_required
@group_required('admin', 'director')
def informasaun_delete(request, pk):
    informasaun = get_object_or_404(Informasaun, pk=pk)

    if request.method == 'POST':
        informasaun.delete()
        messages.success(request, 'Informasaun hamos ho susesu!')
        return redirect('informasaun_list')

    return render(request, 'informasaun/informasaun_confirm_delete.html', {'informasaun': informasaun})

@login_required
@group_required('admin', 'director')
def informasaun_toggle_publish(request, pk):
    informasaun = get_object_or_404(Informasaun, pk=pk)
    informasaun.is_published = not informasaun.is_published

    # Update data_publiku when publishing
    if informasaun.is_published:
        informasaun.data_publiku = timezone.now()
        messages.success(request, f'Informasaun "{informasaun.titulo}" agora publiku!')
    else:
        messages.info(request, f'Informasaun "{informasaun.titulo}" agora draft!')

    informasaun.save()

    return redirect('informasaun_list')
