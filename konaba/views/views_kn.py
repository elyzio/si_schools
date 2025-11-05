from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from konaba.models import KonaBa
from main.decorators import group_required

# =============================================================================
# KONABA VIEWS (Admin Only)
# =============================================================================

@login_required
@group_required('admin')
def konaba_list(request):
    konaba_list = KonaBa.objects.all()
    return render(request, 'konaba/konaba_list.html', {'konaba_list': konaba_list})

@login_required
@group_required('admin')
def konaba_create(request):
    if request.method == 'POST':
        titulu = request.POST.get('titulu')
        orden = request.POST.get('orden')
        deskrisaun = request.POST.get('deskrisaun')
        obs = request.POST.get('obs', '')
        is_active = request.POST.get('is_active') == 'on'

        KonaBa.objects.create(
            titulu=titulu,
            orden=orden,
            deskrisaun=deskrisaun,
            obs=obs,
            is_active=is_active
        )
        messages.success(request, 'Kona Ba kriadu ho susesu!')
        return redirect('konaba:konaba_list')

    return render(request, 'konaba/konaba_form.html')

@login_required
@group_required('admin')
def konaba_update(request, pk):
    konaba = get_object_or_404(KonaBa, pk=pk)

    if request.method == 'POST':
        konaba.titulu = request.POST.get('titulu')
        konaba.orden = request.POST.get('orden')
        konaba.deskrisaun = request.POST.get('deskrisaun')
        konaba.obs = request.POST.get('obs', '')
        konaba.is_active = request.POST.get('is_active') == 'on'
        konaba.save()

        messages.success(request, 'Kona Ba atualiza ho susesu!')
        return redirect('konaba:konaba_list')

    return render(request, 'konaba/konaba_form.html', {'konaba': konaba})

@login_required
@group_required('admin')
def konaba_delete(request, pk):
    konaba = get_object_or_404(KonaBa, pk=pk)

    if request.method == 'POST':
        konaba.delete()
        messages.success(request, 'Kona Ba hamos ho susesu!')
        return redirect('konaba:konaba_list')

    return render(request, 'konaba/konaba_confirm_delete.html', {'konaba': konaba})
