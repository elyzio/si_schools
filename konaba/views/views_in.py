from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from konaba.models import Informasaun
from main.decorators import group_required

# =============================================================================
# INFORMASAUN VIEWS (Admin Only)
# =============================================================================

@login_required
@group_required('admin')
def informasaun_list(request):
    informasaun_list = Informasaun.objects.all()
    return render(request, 'informasaun/informasaun_list.html', {'informasaun_list': informasaun_list})

@login_required
@group_required('admin')
def informasaun_create(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        deskrisaun = request.POST.get('deskrisaun')
        tipu_informasaun = request.POST.get('tipu_informasaun')
        data_publiku = request.POST.get('data_publiku')
        obs = request.POST.get('obs', '')
        is_published = request.POST.get('is_published') == 'on'

        informasaun = Informasaun.objects.create(
            titulo=titulo,
            deskrisaun=deskrisaun,
            tipu_informasaun=tipu_informasaun,
            data_publiku=data_publiku,
            obs=obs,
            is_published=is_published,
            author=request.user
        )

        if 'image' in request.FILES:
            informasaun.image = request.FILES['image']
            informasaun.save()

        messages.success(request, 'Informasaun kriadu ho susesu!')
        return redirect('konaba:informasaun_list')

    return render(request, 'informasaun/informasaun_form.html')

@login_required
@group_required('admin')
def informasaun_update(request, pk):
    informasaun = get_object_or_404(Informasaun, pk=pk)

    if request.method == 'POST':
        informasaun.titulo = request.POST.get('titulo')
        informasaun.deskrisaun = request.POST.get('deskrisaun')
        informasaun.tipu_informasaun = request.POST.get('tipu_informasaun')
        informasaun.data_publiku = request.POST.get('data_publiku')
        informasaun.obs = request.POST.get('obs', '')
        informasaun.is_published = request.POST.get('is_published') == 'on'

        if 'image' in request.FILES:
            informasaun.image = request.FILES['image']

        informasaun.save()

        messages.success(request, 'Informasaun atualiza ho susesu!')
        return redirect('konaba:informasaun_list')

    return render(request, 'informasaun/informasaun_form.html', {'informasaun': informasaun})

@login_required
@group_required('admin')
def informasaun_delete(request, pk):
    informasaun = get_object_or_404(Informasaun, pk=pk)

    if request.method == 'POST':
        informasaun.delete()
        messages.success(request, 'Informasaun hamos ho susesu!')
        return redirect('konaba:informasaun_list')

    return render(request, 'informasaun/informasaun_confirm_delete.html', {'informasaun': informasaun})
