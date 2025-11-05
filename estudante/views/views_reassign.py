from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db import transaction
from django.utils import timezone
from estudante.models import Estudante, EstudanteClasse
from estudante.forms import EstudanteReassignForm
from custom.models import Ano, Classe, Periodo, Departamentu, Turma
from valor.models import Valor

# =============================================================================
# STUDENT REASSIGNMENT VIEWS
# =============================================================================

@login_required
def assigned_students_list(request):
    """Show all students who have been assigned to classes in active year"""
    try:
        active_ano = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        messages.error(request, 'Tinan Akadémiku Ativu la iha! Favor ativa tinan akadémiku dahulu.')
        return redirect('estudante_list')

    # Get filter parameters
    dept_filter = request.GET.get('dept', '')
    classe_filter = request.GET.get('classe', '')
    turma_filter = request.GET.get('turma', '')

    # Base queryset - all assigned students in active year
    estudante_classes = EstudanteClasse.objects.filter(
        ano=active_ano
    ).select_related('estudante', 'departamentu', 'classe', 'turma').order_by('classe__classe', 'turma__turma', 'estudante__nome')

    # Apply filters
    if dept_filter:
        estudante_classes = estudante_classes.filter(departamentu_id=dept_filter)

    if classe_filter:
        estudante_classes = estudante_classes.filter(classe_id=classe_filter)

    if turma_filter:
        estudante_classes = estudante_classes.filter(turma_id=turma_filter)

    # Get filter options with counts
    departments = EstudanteClasse.objects.filter(
        ano=active_ano
    ).values(
        'departamentu__id', 'departamentu__departamento', 'departamentu__sigla'
    ).annotate(count=Count('estudante', distinct=True)).order_by('departamentu__departamento')

    classes = []
    if dept_filter:
        classes = EstudanteClasse.objects.filter(
            ano=active_ano,
            departamentu_id=dept_filter
        ).values(
            'classe__id', 'classe__classe'
        ).annotate(count=Count('estudante', distinct=True)).order_by('classe__classe')

    turmas = []
    if classe_filter and dept_filter:
        turmas = EstudanteClasse.objects.filter(
            ano=active_ano,
            departamentu_id=dept_filter,
            classe_id=classe_filter
        ).values(
            'turma__id', 'turma__turma'
        ).annotate(count=Count('estudante', distinct=True)).order_by('turma__turma')

    # Check completion status for each student
    students_data = []
    complete_count = 0
    incomplete_count = 0

    for ec in estudante_classes:
        is_complete, completion_info = get_student_completion_status(ec)
        students_data.append({
            'estudante_classe': ec,
            'is_eligible': is_complete,
            'completion_info': completion_info
        })
        if is_complete:
            complete_count += 1
        else:
            incomplete_count += 1

    # print(students_data[0])

    context = {
        'page_title': 'Estudante ho Klase Iha Ona',
        'active_ano': active_ano,
        'students_data': students_data,
        'total_count': estudante_classes.count(),
        'complete_count': complete_count,
        'incomplete_count': incomplete_count,
        'departments': list(departments),
        'classes': list(classes),
        'turmas': list(turmas),
        'dept_filter': dept_filter,
        'classe_filter': classe_filter,
        'turma_filter': turma_filter,
    }
    return render(request, 'estudante/assigned_students_list.html', context)


@login_required
def next_year_assigned_students_list(request):
    """Show all students who have been assigned to classes for NEXT academic year"""
    try:
        active_ano = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        messages.error(request, 'Tinan Akadémiku Ativu la iha! Favor ativa tinan akadémiku dahulu.')
        return redirect('estudante_list')

    # Get next year
    next_year_value = active_ano.ano + 1
    try:
        next_ano = Ano.objects.get(ano=next_year_value)
    except Ano.DoesNotExist:
        messages.warning(request, f'Tinan akadémiku {next_year_value} seidauk kria iha sistema.')
        # Create empty context
        context = {
            'page_title': 'Estudante Reinskrisaun ba Tinan Tuir Mai',
            'active_ano': active_ano,
            'next_ano': None,
            'students_data': [],
            'total_count': 0,
            'complete_count': 0,
            'incomplete_count': 0,
            'departments': [],
            'classes': [],
            'turmas': [],
        }
        return render(request, 'estudante/next_year_assigned_list.html', context)

    # Get filter parameters
    dept_filter = request.GET.get('dept', '')
    classe_filter = request.GET.get('classe', '')
    turma_filter = request.GET.get('turma', '')

    # Base queryset - all assigned students for NEXT year
    estudante_classes = EstudanteClasse.objects.filter(
        ano=next_ano
    ).select_related('estudante', 'departamentu', 'classe', 'turma').order_by('classe__classe', 'turma__turma', 'estudante__nome')

    # Apply filters
    if dept_filter:
        estudante_classes = estudante_classes.filter(departamentu_id=dept_filter)

    if classe_filter:
        estudante_classes = estudante_classes.filter(classe_id=classe_filter)

    if turma_filter:
        estudante_classes = estudante_classes.filter(turma_id=turma_filter)

    # Get filter options with counts
    departments = EstudanteClasse.objects.filter(
        ano=next_ano
    ).values(
        'departamentu__id', 'departamentu__departamento', 'departamentu__sigla'
    ).annotate(count=Count('estudante', distinct=True)).order_by('departamentu__departamento')

    classes = []
    if dept_filter:
        classes = EstudanteClasse.objects.filter(
            ano=next_ano,
            departamentu_id=dept_filter
        ).values(
            'classe__id', 'classe__classe'
        ).annotate(count=Count('estudante', distinct=True)).order_by('classe__classe')

    turmas = []
    if classe_filter and dept_filter:
        turmas = EstudanteClasse.objects.filter(
            ano=next_ano,
            departamentu_id=dept_filter,
            classe_id=classe_filter
        ).values(
            'turma__id', 'turma__turma'
        ).annotate(count=Count('estudante', distinct=True)).order_by('turma__turma')

    # Get current year assignment info for comparison
    students_data = []
    promoted_count = 0

    for ec in estudante_classes:
        # Get current year assignment
        current_assignment = EstudanteClasse.objects.filter(
            estudante=ec.estudante,
            ano=active_ano
        ).first()

        is_promoted = current_assignment and current_assignment.is_passa

        students_data.append({
            'estudante_classe': ec,
            'current_assignment': current_assignment,
            'is_promoted': is_promoted,
        })

        if is_promoted:
            promoted_count += 1

    context = {
        'page_title': 'Estudante Reinskrisaun ba Tinan Tuir Mai',
        'active_ano': active_ano,
        'next_ano': next_ano,
        'students_data': students_data,
        'total_count': estudante_classes.count(),
        'promoted_count': promoted_count,
        'departments': list(departments),
        'classes': list(classes),
        'turmas': list(turmas),
        'dept_filter': dept_filter,
        'classe_filter': classe_filter,
        'turma_filter': turma_filter,
    }
    return render(request, 'estudante/next_year_assigned_list.html', context)


def get_student_completion_status(estudante_classe):
    """
    Check if student has completed all required marks for all periods
    AND check if student's average meets passing requirements
    Handles mid-year transfer students who start in P2 or P3
    Returns: (is_eligible, completion_info)
    """
    # Get all periods (should be 3)
    periods = Periodo.objects.all().order_by('period')

    # Get total number of subjects for this student's department
    from custom.models import Materia
    total_materias = Materia.objects.filter(
        departamentu=estudante_classe.departamentu
    ).count()

    # Get expected periods for this student (handles transfers)
    expected_period_numbers = estudante_classe.get_expected_periods()
    required_marks_per_period = 13
    required_total_marks = estudante_classe.get_required_marks_count()

    completion_info = {
        'total_periods': len(expected_period_numbers),
        'completed_periods': 0,
        'period_details': [],
        'total_marks': 0,
        'required_marks_per_period': required_marks_per_period,
        'required_total_marks': required_total_marks,
        'average_score': None,
        'can_pass': False,
        'pass_reason': '',
        'final_score': None,
        'needs_compensation': False,
        'is_transfer': estudante_classe.is_mid_year_transfer,
        'starting_period': estudante_classe.starting_period,
    }

    period_number = 1
    for period in periods:
        # For transfer students, skip periods before their starting period
        if estudante_classe.is_mid_year_transfer and period_number < estudante_classe.starting_period:
            period_number += 1
            continue

        # Count marks for this period
        marks_count = Valor.objects.filter(
            estudante_classe=estudante_classe,
            periodo=period
        ).count()

        period_complete = marks_count >= required_marks_per_period

        completion_info['period_details'].append({
            'period': period,
            'period_number': period_number,
            'marks_count': marks_count,
            'required': required_marks_per_period,
            'is_complete': period_complete,
            'is_expected': period_number in expected_period_numbers
        })

        completion_info['total_marks'] += marks_count
        if period_complete:
            completion_info['completed_periods'] += 1

        period_number += 1

    # Student must have all marks complete for their expected periods
    marks_complete = completion_info['completed_periods'] >= len(expected_period_numbers)

    if marks_complete:
        # Calculate or update average
        if not estudante_classe.average_score:
            estudante_classe.update_average()

        completion_info['average_score'] = estudante_classe.average_score

        # Check if student can pass
        can_pass, reason, final_score = estudante_classe.check_can_pass()
        completion_info['can_pass'] = can_pass
        completion_info['pass_reason'] = reason
        completion_info['final_score'] = final_score

        # Check if needs compensation (for display purposes only)
        if estudante_classe.average_score:
            avg = float(estudante_classe.average_score)
            completion_info['needs_compensation'] = False  # Not needed anymore since min is 6.0

    # Student is eligible for reassignment if marks are complete AND can pass
    is_eligible = marks_complete and completion_info['can_pass']

    return is_eligible, completion_info


@login_required
def reassign_grade_10_list(request):
    """List all Grade 10 students assigned in active year with reassignment option"""
    try:
        active_ano = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        messages.error(request, 'Tinan Akadémiku Ativu la iha! Favor ativa tinan akadémiku dahulu.')
        return redirect('estudante_list')

    # Get Grade 10 class
    try:
        grade_10 = Classe.objects.get(classe='10 Ano')
    except Classe.DoesNotExist:
        messages.error(request, 'Klase 10 Ano la iha iha sistema! Favor aumenta klase 10 Ano dahulu.')
        return redirect('estudante_list')

    # Get all students assigned to Grade 10 in active year
    estudante_classes = EstudanteClasse.objects.filter(
        ano=active_ano,
        classe=grade_10
    ).select_related('estudante', 'departamentu', 'turma').order_by('estudante__nome')

    # Check completion status for each student
    students_data = []
    eligible_count = 0
    not_eligible_count = 0

    for ec in estudante_classes:
        is_complete, completion_info = get_student_completion_status(ec)
        students_data.append({
            'estudante_classe': ec,
            'is_eligible': is_complete,
            'completion_info': completion_info
        })
        if is_complete:
            eligible_count += 1
        else:
            not_eligible_count += 1
    
    print(students_data)

    context = {
        'page_title': 'Reinskrisaun Estudante Klase 10',
        'active_ano': active_ano,
        'grade': '10',
        'next_grade': '11',
        'students_data': students_data,
        'eligible_count': eligible_count,
        'not_eligible_count': not_eligible_count,
    }
    return render(request, 'estudante/reassign_grade_list.html', context)


@login_required
def reassign_grade_11_list(request):
    """List all Grade 11 students assigned in active year with reassignment option"""
    try:
        active_ano = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        messages.error(request, 'Tinan Akadémiku Ativu la iha! Favor ativa tinan akadémiku dahulu.')
        return redirect('estudante_list')

    # Get Grade 11 class
    try:
        grade_11 = Classe.objects.get(classe='11 Ano')
    except Classe.DoesNotExist:
        messages.error(request, 'Klase 11 Ano la iha iha sistema! Favor aumenta klase 11 Ano dahulu.')
        return redirect('estudante_list')

    # Get all students assigned to Grade 11 in active year
    estudante_classes = EstudanteClasse.objects.filter(
        ano=active_ano,
        classe=grade_11
    ).select_related('estudante', 'departamentu', 'turma').order_by('estudante__nome')

    # Check completion status for each student
    students_data = []
    eligible_count = 0
    not_eligible_count = 0

    for ec in estudante_classes:
        is_complete, completion_info = get_student_completion_status(ec)
        students_data.append({
            'estudante_classe': ec,
            'is_eligible': is_complete,
            'completion_info': completion_info
        })
        if is_complete:
            eligible_count += 1
        else:
            not_eligible_count += 1

    context = {
        'page_title': 'Reinskrisaun Estudante Klase 11',
        'active_ano': active_ano,
        'grade': '11',
        'next_grade': '12',
        'students_data': students_data,
        'eligible_count': eligible_count,
        'not_eligible_count': not_eligible_count,
    }
    return render(request, 'estudante/reassign_grade_list.html', context)


@login_required
def reassign_grade_12_list(request):
    """List all Grade 12 students assigned in active year with reassignment option"""
    try:
        active_ano = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        messages.error(request, 'Tinan Akadémiku Ativu la iha! Favor ativa tinan akadémiku dahulu.')
        return redirect('estudante_list')

    # Get Grade 12 class
    try:
        grade_12 = Classe.objects.get(classe='12 Ano')
    except Classe.DoesNotExist:
        messages.error(request, 'Klase 12 Ano la iha iha sistema! Favor aumenta klase 12 Ano dahulu.')
        return redirect('estudante_list')

    # Get all students assigned to Grade 12 in active year
    estudante_classes = EstudanteClasse.objects.filter(
        ano=active_ano,
        classe=grade_12
    ).select_related('estudante', 'departamentu', 'turma').order_by('estudante__nome')

    # Check completion status for each student
    students_data = []
    eligible_count = 0
    not_eligible_count = 0

    for ec in estudante_classes:
        is_complete, completion_info = get_student_completion_status(ec)
        students_data.append({
            'estudante_classe': ec,
            'is_eligible': is_complete,
            'completion_info': completion_info,
            'is_final_grade': True  # Grade 12 is the final grade
        })
        if is_complete:
            eligible_count += 1
        else:
            not_eligible_count += 1

    context = {
        'page_title': 'Reinskrisaun Estudante Klase 12',
        'active_ano': active_ano,
        'grade': '12',
        'next_grade': 'Alumni',
        'students_data': students_data,
        'eligible_count': eligible_count,
        'not_eligible_count': not_eligible_count,
    }
    return render(request, 'estudante/reassign_grade_list.html', context)


@login_required
def reassign_student(request, estudante_classe_id):
    """Reassign student to next grade for next academic year using form"""
    estudante_classe = get_object_or_404(EstudanteClasse, pk=estudante_classe_id)
    current_grade = estudante_classe.classe.classe

    # Check if student is eligible
    is_eligible, completion_info = get_student_completion_status(estudante_classe)

    if not is_eligible:
        error_msg = f'Estudante {estudante_classe.estudante.nome} la bele reinskrisaun! '

        # Check what's missing
        if completion_info['total_marks'] < completion_info['required_total_marks']:
            error_msg += f'Presiza {completion_info["required_total_marks"]} valor, maibé iha {completion_info["total_marks"]} deit. '
        elif not completion_info['can_pass']:
            error_msg += completion_info['pass_reason']
            if completion_info['needs_compensation']:
                error_msg += ' Bele hatama kompensasaun atitude (0-2 pontos) ka aprova manual.'

        messages.error(request, error_msg)
        return redirect(f'reassign_grade_{current_grade.replace(" Ano", "").replace(" ", "_")}_list')

    # Determine next grade
    if current_grade == '10 Ano':
        next_grade_name = '11 Ano'
    elif current_grade == '11 Ano':
        next_grade_name = '12 Ano'
    elif current_grade == '12 Ano':
        next_grade_name = 'Alumni'
    else:
        messages.error(request, f'Klase {current_grade} la bele reasigna!')
        return redirect('estudante_list')

    # Handle Grade 12 -> Alumni separately (no form needed)
    if current_grade == '12 Ano':
        try:
            with transaction.atomic():
                from estudante.models import EstudanteAlumni

                # Get current year
                current_ano = estudante_classe.ano

                # Update student status
                estudante_classe.estudante.is_active = False
                estudante_classe.estudante.is_alumni = True
                estudante_classe.estudante.save()

                # Create alumni record
                EstudanteAlumni.objects.create(
                    estudante=estudante_classe.estudante,
                    data_alumni=timezone.now().date(),
                    ano=current_ano,
                    obs=f'Graduado husi klase {current_grade} iha tinan {current_ano.ano}'
                )

                # Mark current assignment as passed
                estudante_classe.is_passa = True
                estudante_classe.save()

                messages.success(request,
                    f'Estudante {estudante_classe.estudante.nome} graduadu ona! '
                    f'Agora maka Alumni tinan {current_ano.ano}.'
                )
        except Exception as e:
            messages.error(request, f'Erru wainhira halo alumni: {str(e)}')

        return redirect('assigned_students_list')

    # Determine back URL
    grade_num = current_grade.replace(' Ano', '')
    back_url_name = f'reassign_grade_{grade_num}_list'

    # For grades 10 and 11, use form
    if request.method == 'POST':
        form = EstudanteReassignForm(
            request.POST,
            next_grade_name=next_grade_name,
            current_estudante_classe=estudante_classe,
            back_url_name=back_url_name
        )
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Get next academic year (create if doesn't exist)
                    current_ano = estudante_classe.ano
                    next_year_value = current_ano.ano + 1
                    next_ano, created = Ano.objects.get_or_create(ano=next_year_value)

                    # Check if student already assigned to next year
                    existing_assignment = EstudanteClasse.objects.filter(
                        estudante=estudante_classe.estudante,
                        ano=next_ano
                    ).first()

                    if existing_assignment:
                        messages.warning(request,
                            f'Estudante {estudante_classe.estudante.nome} iha ona inskrisaun ba tinan {next_ano.ano}!'
                        )
                    else:
                        # Create new assignment for next year using form data
                        new_assignment = form.save(commit=False)
                        new_assignment.estudante = estudante_classe.estudante
                        new_assignment.ano = next_ano
                        new_assignment.save()

                        # Mark current assignment as passed
                        estudante_classe.is_passa = True
                        estudante_classe.save()

                        messages.success(request,
                            f'Estudante {estudante_classe.estudante.nome} reinskrisaun ona ba '
                            f'klase {new_assignment.classe.classe} iha tinan akadémiku {next_ano.ano}!'
                        )

                    return redirect(f'reassign_grade_{current_grade.replace(" Ano", "")}_list')

            except Exception as e:
                messages.error(request, f'Erru wainhira reasigna: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstudanteReassignForm(
            next_grade_name=next_grade_name,
            current_estudante_classe=estudante_classe,
            back_url_name=back_url_name
        )

    context = {
        'page_title': f'Reinskrisaun Estudante - {estudante_classe.estudante.nome}',
        'form': form,
        'estudante_classe': estudante_classe,
        'next_grade_name': next_grade_name,
        'current_grade': current_grade,
        'back_url_name': back_url_name,
    }
    return render(request, 'estudante/reassign_form.html', context)
