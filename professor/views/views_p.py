from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import JsonResponse
import random
import string
import re
from professor.models import Professor, ProfessorUser, ProfessorClasse
from professor.forms import ProfessorForm
from custom.models import Distrito, Subdistrito, Suco, Aldeia, Ano, Departamentu, Classe, Turma

# =============================================================================
# PROFESSOR VIEWS
# =============================================================================

@login_required
def professor_list(request):
    professors = Professor.objects.all().order_by('nome')
    context = {
        'page_title': 'Lista de Professores',
        'professors': professors,
    }
    return render(request, 'professor/professor_list.html', context)

@login_required
def professor_create(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create professor instance but don't save yet
                    professor = form.save(commit=False)
                    professor.save()

                    # Generate username from name (remove special characters)
                    nome = form.cleaned_data['nome']
                    first_name = nome.split()[0].lower() if nome else 'user'
                    # Remove special characters and spaces, keep only letters and numbers
                    clean_first_name = re.sub(r'[^a-z0-9]', '', first_name)
                    base_username = clean_first_name
                    username = base_username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}{counter}"
                        counter += 1

                    # Create user with default password
                    email = form.cleaned_data.get('email', '')
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='Password_123',
                        first_name=nome.split()[0] if nome else '',
                        last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else ''
                    )

                    # Add user to professor group
                    try:
                        professor_group = Group.objects.get(name='professor')
                    except Group.DoesNotExist:
                        professor_group = Group.objects.create(name='professor')

                    user.groups.add(professor_group)

                    # Link professor to user
                    ProfessorUser.objects.create(
                        professor=professor,
                        user=user
                    )


                    messages.success(request, f'Professor {nome} foi criado com sucesso! Username: {username}, Password: Password_123')
                    return redirect('professor_list')

            except Exception as e:
                messages.error(request, f'Erro ao criar professor: {str(e)}')
        else:
            # Form has validation errors
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ProfessorForm()

    context = {
        'page_title': 'Adicionar Professor',
        'form': form,
    }
    return render(request, 'professor/professor_form.html', context)

@login_required
def professor_detail(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    try:
        professor_user = ProfessorUser.objects.get(professor=professor)
        user = professor_user.user
    except ProfessorUser.DoesNotExist:
        user = None

    professor_classes = ProfessorClasse.objects.filter(professor=professor).select_related(
        'ano', 'departamentu', 'classe'
    )

    context = {
        'page_title': f'Professor: {professor.nome}',
        'professor': professor,
        'user': user,
        'professor_classes': professor_classes,
    }
    return render(request, 'professor/professor_detail.html', context)

@login_required
def professor_update(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profesor {professor.nome} hadia ho suksesu!')
            return redirect('professor_detail', pk=pk)
        else:
            messages.error(request, 'Favór hatán erru sira iha formulariu.')
    else:
        form = ProfessorForm(instance=professor)

    context = {
        'page_title': f'Hadia Profesor: {professor.nome}',
        'form': form,
        'professor': professor,
    }
    return render(request, 'professor/professor_form.html', context)

@login_required
def professor_delete(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        nome = professor.nome
        professor.delete()
        messages.success(request, f'Profesor {nome} hamos ho suksesu!')
        return redirect('professor_list')

    context = {
        'page_title': f'Hamos Profesor: {professor.nome}',
        'professor': professor,
    }
    return render(request, 'professor/professor_confirm_delete.html', context)


# =============================================================================
# AJAX VIEWS FOR DEPENDENT DROPDOWNS
# =============================================================================

@login_required
def ajax_subdistrito(request):
    distrito_id = request.GET.get('distrito_id')
    subdistritos = Subdistrito.objects.filter(distrito_id=distrito_id).order_by('nome')
    data = [{'id': s.id, 'name': s.nome} for s in subdistritos]
    return JsonResponse(data, safe=False)

@login_required
def ajax_suco(request):
    subdistrito_id = request.GET.get('subdistrito_id')
    sucos = Suco.objects.filter(subdistrito_id=subdistrito_id).order_by('nome')
    data = [{'id': s.id, 'name': s.nome} for s in sucos]
    return JsonResponse(data, safe=False)

@login_required
def ajax_aldeia(request):
    suco_id = request.GET.get('suco_id')
    aldeias = Aldeia.objects.filter(suco_id=suco_id).order_by('nome')
    data = [{'id': a.id, 'name': a.nome} for a in aldeias]
    return JsonResponse(data, safe=False)

