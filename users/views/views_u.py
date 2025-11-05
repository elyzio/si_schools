from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from professor.models import Professor
from estudante.models import Estudante
from django.contrib import messages
from users.forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from users.forms import EstudanteProfileForm
from professor.forms import ProfessorForm
from django.shortcuts import get_object_or_404

@login_required
def user_profile(request):
    context = {
        'page_title': 'User Profile',
        'page': 'list'
    }
    return render(request, 'users/users_profile.html', context)

def user_account(request):
    user = request.user

    if request.method == 'POST':
        if request.POST.get('b_user') == '1':
            email = request.POST.get('email')
            user.email = email

            if user.groups.filter(name='professor').exists():
                professor = Professor.objects.get(professoruser__user=user)
                professor.email = email
                professor.save()
            
            if  user.groups.filter(name='estudante').exists():
                estudante = Estudante.objects.get(estudanteuser__user=user)
                estudante.email = email
                estudante.save()
            user.save()
            messages.success(request, f'Konta {user.username} atualiza ho susesu!')
            return redirect('user_account')
        elif request.POST.get('b_user') == '2':
            form = CustomPasswordChangeForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha atualiza ho susesu!')
                return redirect('user_account')
            else:
                messages.error(request, 'Hahu eroru, favor verifica informasaun.')
    else:
        form = CustomPasswordChangeForm(user)
    context = {
        'page_title': 'User Account',
        'form_p': form,
        'page': 'list'
    }
    return render(request, 'users/users_account.html', context)

def ChangeUserPassword(request):
    user = request.user
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha atualiza ho susesu!')
            return redirect('user_account')
        else:
            messages.error(request, 'Hahu eroru, favor verifica informasaun.')
    else:
        form = CustomPasswordChangeForm(user)
    
    context = {
        'title': 'Troka Password',
        'form': form,
        'page': 'form'
    }

    return render(request, 'users/users_account.html', context)


@login_required
def UpdateEstudanteProfile(request):
    # estudante_user = get_object_or_404(User, pk=request.user.id)
    estudante = get_object_or_404(Estudante, pk=request.user.estudanteuser.estudante.id)

    if request.method == 'POST':
        form = EstudanteProfileForm(request.POST, request.FILES, instance=estudante)
        if form.is_valid():
            try:
                est_form = form.save(commit=False)
                est_user = request.user
                est_user.email = est_form.email
                est_user.save()
                est_form.save()
                messages.success(request, 'Estudante updated successfully!')
                return redirect('user_profile')
            except Exception as e:
                messages.error(request, f'Error updating estudante: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteProfileForm(instance=estudante)

    context = {
        'page_title': 'Update Profile Estudante',
        'form': form,
        'estudante': estudante,
        'page': 'form',
    }
    return render(request, 'users/users_profile.html', context)

@login_required
def UpdateProfessorProfile(request):
    professor = get_object_or_404(Professor, pk=request.user.professoruser.professor.id)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES, instance=professor)
        if form.is_valid():
            prof_form = form.save(commit=False)
            prof_user = request.user
            prof_user.email = prof_form.email
            prof_user.save()
            prof_form.save()
            messages.success(request, f'Profesor {professor.nome} hadia ho suksesu!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Favór hatán erru sira iha formulariu.')
    else:
        form = ProfessorForm(instance=professor)

    context = {
        'page_title': 'Update Profile Professor',
        'form': form,
        'professor': professor,
        'page': 'form',
    }
    return render(request, 'users/users_profile.html', context)