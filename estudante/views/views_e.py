from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import JsonResponse
from estudante.models import Estudante, EstudanteUser, EstudanteClasse, EstudanteEncarregadu, EstudanteDokumentu, EstudanteTransfer
from estudante.forms import EstudanteForm, EstudanteClasseForm, EstudanteEncarregaduForm, EstudanteDokumentuForm, EstudanteTransferForm
from custom.models import Ano
from datetime import datetime

# =============================================================================
# ESTUDANTE CRUD
# =============================================================================

@login_required
def estudante_list(request):
    # Get filter parameters
    year_filter = request.GET.get('year', '')
    class_filter = request.GET.get('class_status', 'all')  # all, assigned, not_assigned
    dept_filter = request.GET.get('dept', '')  # department filter
    classe_filter = request.GET.get('classe', '')  # class filter
    turma_filter = request.GET.get('turma', '')  # turma filter

    # Base queryset - exclude transferred OUT students
    estudantes = Estudante.objects.filter(is_transfer=False)

    # Get the latest year by default if no filter
    if not year_filter and estudantes.exists():
        latest_year = estudantes.exclude(data_matricula__isnull=True).order_by('-data_matricula').first()
        if latest_year:
            year_filter = str(latest_year.data_matricula.year)

    # Apply year filter
    if year_filter:
        estudantes = estudantes.filter(data_matricula__year=year_filter)

    # Get active academic year for class assignment filter
    try:
        active_ano = Ano.objects.get(is_active=True)

        # Apply class assignment filter
        if class_filter == 'assigned':
            # Students who have class assignment for active year
            assigned_student_ids = EstudanteClasse.objects.filter(
                ano=active_ano
            ).values_list('estudante_id', flat=True)
            estudantes = estudantes.filter(id__in=assigned_student_ids)
        elif class_filter == 'not_assigned':
            # Students who don't have class assignment for active year
            assigned_student_ids = EstudanteClasse.objects.filter(
                ano=active_ano
            ).values_list('estudante_id', flat=True)
            estudantes = estudantes.exclude(id__in=assigned_student_ids)
        # 'all' shows all students (no additional filter)

        # Apply department filter (only for assigned students)
        if dept_filter and class_filter == 'assigned':
            dept_student_ids = EstudanteClasse.objects.filter(
                ano=active_ano,
                departamentu_id=dept_filter
            ).values_list('estudante_id', flat=True)
            estudantes = estudantes.filter(id__in=dept_student_ids)

            # Apply class filter (only when department is selected)
            if classe_filter:
                classe_student_ids = EstudanteClasse.objects.filter(
                    ano=active_ano,
                    departamentu_id=dept_filter,
                    classe_id=classe_filter
                ).values_list('estudante_id', flat=True)
                estudantes = estudantes.filter(id__in=classe_student_ids)

                # Apply turma filter (only when class is selected)
                if turma_filter:
                    turma_student_ids = EstudanteClasse.objects.filter(
                        ano=active_ano,
                        departamentu_id=dept_filter,
                        classe_id=classe_filter,
                        turma_id=turma_filter
                    ).values_list('estudante_id', flat=True)
                    estudantes = estudantes.filter(id__in=turma_student_ids)

    except Ano.DoesNotExist:
        active_ano = None

    # Get available years for filter dropdown
    years = Estudante.objects.exclude(data_matricula__isnull=True).dates('data_matricula', 'year', order='DESC')
    available_years = [date.year for date in years]

    # Get counts for each filter
    total_count = estudantes.count() if class_filter == 'all' else Estudante.objects.filter(data_matricula__year=year_filter if year_filter else None).count() if year_filter else Estudante.objects.count()

    if active_ano:
        all_students = Estudante.objects.all()
        if year_filter:
            all_students = all_students.filter(data_matricula__year=year_filter)

        assigned_student_ids = EstudanteClasse.objects.filter(ano=active_ano).values_list('estudante_id', flat=True)
        assigned_count = all_students.filter(id__in=assigned_student_ids).count()
        not_assigned_count = all_students.exclude(id__in=assigned_student_ids).count()

        # Get department counts
        from custom.models import Departamentu
        from django.db.models import Count
        dept_counts = EstudanteClasse.objects.filter(
            ano=active_ano
        ).values(
            'departamentu__id', 'departamentu__departamento', 'departamentu__sigla'
        ).annotate(count=Count('estudante', distinct=True)).order_by('departamentu__departamento')

        departments = list(dept_counts)

        # Get class counts (only when department is selected)
        classes = []
        if dept_filter and class_filter == 'assigned':
            classe_counts = EstudanteClasse.objects.filter(
                ano=active_ano,
                departamentu_id=dept_filter
            ).values(
                'classe__id', 'classe__classe'
            ).annotate(count=Count('estudante', distinct=True)).order_by('classe__classe')

            classes = list(classe_counts)

        # Get turma counts (only when class is selected)
        turmas = []
        if classe_filter and dept_filter and class_filter == 'assigned':
            turma_counts = EstudanteClasse.objects.filter(
                ano=active_ano,
                departamentu_id=dept_filter,
                classe_id=classe_filter
            ).values(
                'turma__id', 'turma__turma'
            ).annotate(count=Count('estudante', distinct=True)).order_by('turma__turma')

            turmas = list(turma_counts)
    else:
        assigned_count = 0
        not_assigned_count = 0
        departments = []
        classes = []
        turmas = []

    context = {
        'page_title': 'Estudante',
        'estudantes': estudantes,
        'available_years': available_years,
        'selected_year': year_filter,
        'class_filter': class_filter,
        'dept_filter': dept_filter,
        'classe_filter': classe_filter,
        'turma_filter': turma_filter,
        'active_ano': active_ano,
        'total_count': total_count,
        'assigned_count': assigned_count,
        'not_assigned_count': not_assigned_count,
        'departments': departments,
        'classes': classes,
        'turmas': turmas,
    }
    return render(request, 'estudante/estudante_list.html', context)

@login_required
def estudante_create(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Save estudante
                    estudante = form.save()

                    # Auto-create user with EMIS as username and default password
                    username = estudante.emis
                    default_password = 'Password_123'

                    # Check if user already exists
                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(
                            username=username,
                            password=default_password,
                            first_name=estudante.nome.split()[0] if estudante.nome else '',
                            last_name=' '.join(estudante.nome.split()[1:]) if estudante.nome and len(estudante.nome.split()) > 1 else ''
                        )

                        # Add user to estudante group
                        estudante_group, created = Group.objects.get_or_create(name='estudante')
                        user.groups.add(estudante_group)

                        # Create EstudanteUser relation
                        EstudanteUser.objects.create(
                            estudante=estudante,
                            user=user
                        )

                        messages.success(request, f'Estudante created successfully! User account created with username: {username}')
                    else:
                        messages.warning(request, f'Estudante created but user with username {username} already exists!')

                return redirect('estudante_list')
            except Exception as e:
                messages.error(request, f'Error creating estudante: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteForm()

    context = {
        'page_title': 'Add Estudante',
        'form': form,
    }
    return render(request, 'estudante/estudante_form.html', context)

@login_required
def estudante_update(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)

    if request.method == 'POST':
        form = EstudanteForm(request.POST, request.FILES, instance=estudante)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Estudante updated successfully!')
                return redirect('estudante_list')
            except Exception as e:
                messages.error(request, f'Error updating estudante: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteForm(instance=estudante)

    context = {
        'page_title': 'Edit Estudante',
        'form': form,
        'estudante': estudante,
    }
    return render(request, 'estudante/estudante_form.html', context)

@login_required
def estudante_delete(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Delete associated user if exists
                try:
                    estudante_user = EstudanteUser.objects.get(estudante=estudante)
                    estudante_user.user.delete()
                    estudante_user.delete()
                except EstudanteUser.DoesNotExist:
                    pass

                estudante.delete()
                messages.success(request, 'Estudante deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting estudante: {str(e)}')
    return redirect('estudante_list')

@login_required
def estudante_detail(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)

    # Get user info if exists
    estudante_user = None
    try:
        estudante_user = EstudanteUser.objects.get(estudante=estudante)
    except EstudanteUser.DoesNotExist:
        pass

    # Get parent/guardian information
    encarregadu_list = EstudanteEncarregadu.objects.filter(estudante=estudante).order_by('-is_primary', 'encarregadu')

    # Get document information
    dokumentu_list = EstudanteDokumentu.objects.filter(estudante=estudante).order_by('tipo_dokumentu')

    # Get transfer information
    transfer_list = EstudanteTransfer.objects.filter(estudante=estudante).order_by('-data_transfer')

    context = {
        'page_title': 'Estudante Detail',
        'estudante': estudante,
        'estudante_user': estudante_user,
        'encarregadu_list': encarregadu_list,
        'dokumentu_list': dokumentu_list,
        'transfer_list': transfer_list,
    }
    return render(request, 'estudante/estudante_detail.html', context)

@login_required
def estudante_assign_classe(request, pk):
    """Assign student to a class for the active academic year"""
    estudante = get_object_or_404(Estudante, pk=pk)

    # Get active academic year
    try:
        active_ano = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        messages.error(request, 'Tinan Akadémiku Ativu la iha! Favor ativa tinan akadémiku dahulu.')
        return redirect('estudante_list')

    # Check if student already assigned to a class for this year
    existing_assignment = EstudanteClasse.objects.filter(
        estudante=estudante,
        ano=active_ano
    ).first()

    if request.method == 'POST':
        form = EstudanteClasseForm(request.POST, instance=existing_assignment)
        if form.is_valid():
            try:
                with transaction.atomic():
                    estudante_classe = form.save(commit=False)
                    estudante_classe.estudante = estudante
                    estudante_classe.ano = active_ano
                    estudante_classe.save()

                    if existing_assignment:
                        messages.success(request, f'Estudante {estudante.nome} nia inskrisaun ba klase update tiha ona!')
                    else:
                        messages.success(request, f'Estudante {estudante.nome} registu ona ba klase {estudante_classe.classe.classe}{estudante_classe.turma.turma}!')

                return redirect('estudante_list')
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteClasseForm(instance=existing_assignment)

    context = {
        'page_title': f'Rejista ba Klase - {estudante.nome}',
        'form': form,
        'estudante': estudante,
        'active_ano': active_ano,
        'existing_assignment': existing_assignment,
    }
    return render(request, 'estudante/estudante_assign_classe.html', context)

# =============================================================================
# ESTUDANTE ENCARREGADU (PARENT/GUARDIAN) CRUD
# =============================================================================

@login_required
def encarregadu_create(request, estudante_pk):
    """Add parent/guardian for a student"""
    estudante = get_object_or_404(Estudante, pk=estudante_pk)

    if request.method == 'POST':
        form = EstudanteEncarregaduForm(request.POST)
        if form.is_valid():
            try:
                encarregadu = form.save(commit=False)
                encarregadu.estudante = estudante
                encarregadu.save()
                messages.success(request, 'Encaregadu Edukasaun aumenta tiha ona!')
                return redirect('estudante_detail', pk=estudante.pk)
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteEncarregaduForm()

    context = {
        'page_title': f'Aumenta Encaregadu - {estudante.nome}',
        'form': form,
        'estudante': estudante,
    }
    return render(request, 'estudante/encarregadu_form.html', context)

@login_required
def encarregadu_update(request, pk):
    """Update parent/guardian information"""
    encarregadu = get_object_or_404(EstudanteEncarregadu, pk=pk)
    estudante = encarregadu.estudante

    if request.method == 'POST':
        form = EstudanteEncarregaduForm(request.POST, instance=encarregadu)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Encaregadu Edukasaun hadia tiha ona!')
                return redirect('estudante_detail', pk=estudante.pk)
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteEncarregaduForm(instance=encarregadu)

    context = {
        'page_title': f'Hadia Encaregadu - {estudante.nome}',
        'form': form,
        'estudante': estudante,
        'encarregadu': encarregadu,
    }
    return render(request, 'estudante/encarregadu_form.html', context)

@login_required
def encarregadu_delete(request, pk):
    """Delete parent/guardian information"""
    encarregadu = get_object_or_404(EstudanteEncarregadu, pk=pk)
    estudante_pk = encarregadu.estudante.pk

    if request.method == 'POST':
        try:
            encarregadu.delete()
            messages.success(request, 'Encaregadu Edukasaun hamoos tiha ona!')
        except Exception as e:
            messages.error(request, f'Erru wainhira hamoos: {str(e)}')

    return redirect('estudante_detail', pk=estudante_pk)

# =============================================================================
# ESTUDANTE DOKUMENTU (DOCUMENT) CRUD
# =============================================================================

@login_required
def dokumentu_create(request, estudante_pk):
    """Add document for a student"""
    estudante = get_object_or_404(Estudante, pk=estudante_pk)

    if request.method == 'POST':
        form = EstudanteDokumentuForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dokumentu = form.save(commit=False)
                dokumentu.estudante = estudante
                dokumentu.save()
                messages.success(request, 'Dokumentu aumenta tiha ona!')
                return redirect('estudante_detail', pk=estudante.pk)
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteDokumentuForm()

    context = {
        'page_title': f'Aumenta Dokumentu - {estudante.nome}',
        'form': form,
        'estudante': estudante,
    }
    return render(request, 'estudante/dokumentu_form.html', context)

@login_required
def dokumentu_update(request, pk):
    """Update document information"""
    dokumentu = get_object_or_404(EstudanteDokumentu, pk=pk)
    estudante = dokumentu.estudante

    if request.method == 'POST':
        form = EstudanteDokumentuForm(request.POST, request.FILES, instance=dokumentu)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Dokumentu hadia tiha ona!')
                return redirect('estudante_detail', pk=estudante.pk)
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteDokumentuForm(instance=dokumentu)

    context = {
        'page_title': f'Hadia Dokumentu - {estudante.nome}',
        'form': form,
        'estudante': estudante,
        'dokumentu': dokumentu,
    }
    return render(request, 'estudante/dokumentu_form.html', context)

@login_required
def dokumentu_delete(request, pk):
    """Delete document"""
    dokumentu = get_object_or_404(EstudanteDokumentu, pk=pk)
    estudante_pk = dokumentu.estudante.pk

    if request.method == 'POST':
        try:
            # Delete file if exists
            if dokumentu.file:
                dokumentu.file.delete()
            dokumentu.delete()
            messages.success(request, 'Dokumentu hamoos tiha ona!')
        except Exception as e:
            messages.error(request, f'Erru wainhira hamoos: {str(e)}')

    return redirect('estudante_detail', pk=estudante_pk)

# =============================================================================
# ESTUDANTE TRANSFER
# =============================================================================

@login_required
def transfer_create(request, estudante_pk):
    """Create transfer record for a student"""
    estudante = get_object_or_404(Estudante, pk=estudante_pk)

    # Get current school name from settings or use default
    from django.conf import settings
    current_school = getattr(settings, 'SCHOOL_NAME', 'Eskola Ne\'e')

    if request.method == 'POST':
        form = EstudanteTransferForm(request.POST, current_school=current_school)
        if form.is_valid():
            try:
                with transaction.atomic():
                    transfer = form.save(commit=False)
                    transfer.estudante = estudante
                    transfer.save()

                    # If transferring OUT, mark student as transferred
                    transfer_type = form.cleaned_data.get('transfer_type')
                    if transfer_type == 'OUT':
                        estudante.is_transfer = True
                        estudante.save()

                    messages.success(request, f'Transferénsia ba estudante {estudante.nome} rejista tiha ona!')
                    return redirect('estudante_detail', pk=estudante.pk)
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteTransferForm(current_school=current_school)

    context = {
        'page_title': f'Rejista Transferénsia - {estudante.nome}',
        'form': form,
        'estudante': estudante,
    }
    return render(request, 'estudante/transfer_form.html', context)

@login_required
def transfer_update(request, pk):
    """Update transfer record"""
    transfer = get_object_or_404(EstudanteTransfer, pk=pk)
    estudante = transfer.estudante

    from django.conf import settings
    current_school = getattr(settings, 'SCHOOL_NAME', 'Eskola Ne\'e')

    if request.method == 'POST':
        form = EstudanteTransferForm(request.POST, instance=transfer, current_school=current_school)
        if form.is_valid():
            try:
                with transaction.atomic():
                    transfer = form.save()

                    # Update student transfer status
                    transfer_type = form.cleaned_data.get('transfer_type')
                    if transfer_type == 'OUT':
                        estudante.is_transfer = True
                    else:
                        estudante.is_transfer = False
                    estudante.save()

                    messages.success(request, 'Transferénsia hadia tiha ona!')
                    return redirect('estudante_detail', pk=estudante.pk)
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteTransferForm(instance=transfer, current_school=current_school)

    context = {
        'page_title': f'Hadia Transferénsia - {estudante.nome}',
        'form': form,
        'estudante': estudante,
        'transfer': transfer,
    }
    return render(request, 'estudante/transfer_form.html', context)

@login_required
def transfer_delete(request, pk):
    """Delete transfer record and reactivate student if was transferred out"""
    transfer = get_object_or_404(EstudanteTransfer, pk=pk)
    estudante = transfer.estudante

    from django.conf import settings
    current_school = getattr(settings, 'SCHOOL_NAME', 'Eskola Ne\'e')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # If this was an OUT transfer, reactivate the student
                if transfer.from_eskola == current_school:
                    estudante.is_transfer = False
                    estudante.save()

                transfer.delete()
                messages.success(request, 'Transferénsia hamoos tiha ona!')
        except Exception as e:
            messages.error(request, f'Erru wainhira hamoos: {str(e)}')

    return redirect('estudante_detail', pk=estudante.pk)

@login_required
def transfer_list(request):
    """List all transferred students by year"""
    year_filter = request.GET.get('year', '')
    transfer_type_filter = request.GET.get('type', 'all')  # all, out, in

    from django.conf import settings
    current_school = getattr(settings, 'SCHOOL_NAME', 'Eskola Ne\'e')

    # Base queryset
    transfers = EstudanteTransfer.objects.select_related('estudante').all()

    # Get available years
    years = transfers.dates('data_transfer', 'year', order='DESC')
    available_years = [date.year for date in years]

    # Default to latest year if no filter
    if not year_filter and available_years:
        year_filter = str(available_years[0])

    # Apply year filter
    if year_filter:
        transfers = transfers.filter(data_transfer__year=year_filter)

    # Apply transfer type filter
    if transfer_type_filter == 'out':
        transfers = transfers.filter(from_eskola=current_school)
    elif transfer_type_filter == 'in':
        transfers = transfers.filter(ba_eskola=current_school)

    # Get counts
    total_count = transfers.count()
    out_count = transfers.filter(from_eskola=current_school).count()
    in_count = transfers.filter(ba_eskola=current_school).count()

    context = {
        'page_title': 'Estudante Transfere',
        'transfers': transfers,
        'available_years': available_years,
        'selected_year': year_filter,
        'transfer_type_filter': transfer_type_filter,
        'total_count': total_count,
        'out_count': out_count,
        'in_count': in_count,
        'current_school': current_school,
    }
    return render(request, 'estudante/transfer_list.html', context)
