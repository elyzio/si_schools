from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch, Count, Avg
from valor.models import Valor
from valor.forms import ValorForm
from estudante.models import Estudante, EstudanteClasse
from custom.models import Ano, Departamentu, Classe, Turma, Materia, Periodo

# =============================================================================
# VALOR VIEWS
# =============================================================================

@login_required
def valor_report(request):
    """View all grades organized by class and period"""
    # Get filter parameters
    ano_filter = request.GET.get('ano', '')
    classe_filter = request.GET.get('classe', '')
    periodo_filter = request.GET.get('periodo', '')
    dept_filter = request.GET.get('dept', '')
    turma_filter = request.GET.get('turma', '')

    # Get all available years
    all_anos = Ano.objects.all().order_by('-ano')

    # Get active academic year as default
    try:
        active_ano = Ano.objects.get(is_active=True)
        if not ano_filter:
            ano_filter = str(active_ano.id)
    except Ano.DoesNotExist:
        if all_anos.exists():
            ano_filter = str(all_anos[0].id) if not ano_filter else ano_filter
        else:
            messages.error(request, 'Tinan Akadémiku la iha! Favor aumenta tinan akadémiku dahulu.')
            return redirect('home')

    # Get selected year object
    try:
        selected_ano = Ano.objects.get(id=ano_filter)
    except Ano.DoesNotExist:
        messages.error(request, 'Tinan Akadémiku la hetan!')
        return redirect('home')

    # Get all classes that have students in selected year
    classes = EstudanteClasse.objects.filter(
        ano=selected_ano
    ).values('classe__id', 'classe__classe').annotate(
        student_count=Count('estudante', distinct=True)
    ).order_by('classe__classe')

    # Get active periods (or all periods for past years)
    if selected_ano.is_active:
        periodos = Periodo.objects.filter(is_active=True).order_by('period')
    else:
        # For past years, show all periods
        periodos = Periodo.objects.all().order_by('period')

    # Set default filters: first class and first period
    if not classe_filter and classes.exists():
        classe_filter = str(classes[0]['classe__id'])

    if not periodo_filter and periodos.exists():
        periodo_filter = str(periodos[0].id)

    # Get departments for the selected class
    departments = []
    if classe_filter:
        departments = EstudanteClasse.objects.filter(
            ano=selected_ano,
            classe_id=classe_filter
        ).values(
            'departamentu__id', 'departamentu__departamento', 'departamentu__sigla'
        ).annotate(count=Count('estudante', distinct=True)).order_by('departamentu__departamento')

    # Get turmas for the selected class and department
    turmas = []
    if classe_filter and dept_filter:
        turmas = EstudanteClasse.objects.filter(
            ano=selected_ano,
            classe_id=classe_filter,
            departamentu_id=dept_filter
        ).values(
            'turma__id', 'turma__turma'
        ).annotate(count=Count('estudante', distinct=True)).order_by('turma__turma')

    # Get grades for the selected filters
    valores_queryset = Valor.objects.filter(
        estudante_classe__ano=selected_ano
    ).select_related(
        'estudante_classe__estudante',
        'estudante_classe__classe',
        'estudante_classe__turma',
        'estudante_classe__departamentu',
        'periodo',
        'materia'
    )

    if classe_filter:
        valores_queryset = valores_queryset.filter(estudante_classe__classe_id=classe_filter)

    if periodo_filter:
        valores_queryset = valores_queryset.filter(periodo_id=periodo_filter)

    if dept_filter:
        valores_queryset = valores_queryset.filter(estudante_classe__departamentu_id=dept_filter)

    if turma_filter:
        valores_queryset = valores_queryset.filter(estudante_classe__turma_id=turma_filter)

    # Get all unique materias for table headers (ordered)
    from collections import defaultdict, OrderedDict
    from django.db.models import Q

    # Get materias that appear in the filtered results
    materia_ids = valores_queryset.values_list('materia_id', flat=True).distinct()
    materias_list = Materia.objects.filter(id__in=materia_ids).order_by('codigo')

    # Group materias by type: common (no dept) and specific (with dept)
    materias_common = []
    materias_specific = []
    for materia in materias_list:
        if materia.departamentu:
            materias_specific.append(materia)
        else:
            materias_common.append(materia)

    # Group grades by student
    grades_by_student = OrderedDict()

    for valor in valores_queryset.order_by('estudante_classe__estudante__nome', 'materia__codigo'):
        student_key = valor.estudante_classe.estudante.id
        if student_key not in grades_by_student:
            grades_by_student[student_key] = {
                'info': {
                    'estudante': valor.estudante_classe.estudante,
                    'estudante_classe': valor.estudante_classe,
                },
                'grades_dict': {},  # materia_id: valor_object
                'common_grades': [],
                'specific_grades': [],
                'common_avg': 0,
                'specific_avg': 0,
                'total_avg': 0,
            }

        # Store grade by materia ID for easy lookup
        grades_by_student[student_key]['grades_dict'][valor.materia.id] = valor

        # Group by type
        if valor.materia.departamentu:
            grades_by_student[student_key]['specific_grades'].append(valor)
        else:
            grades_by_student[student_key]['common_grades'].append(valor)

    # Calculate averages for each student
    for student_id, data in grades_by_student.items():
        common_grades = data['common_grades']
        specific_grades = data['specific_grades']

        if common_grades:
            data['common_avg'] = round(sum(float(g.valor) for g in common_grades) / len(common_grades), 2)

        if specific_grades:
            data['specific_avg'] = round(sum(float(g.valor) for g in specific_grades) / len(specific_grades), 2)

        all_grades = common_grades + specific_grades
        if all_grades:
            data['total_avg'] = round(sum(float(g.valor) for g in all_grades) / len(all_grades), 2)

    # Calculate statistics
    total_students = len(grades_by_student)
    total_grades = valores_queryset.count()
    average_grade = valores_queryset.aggregate(avg=Avg('valor'))['avg']

    context = {
        'page_title': 'Relatóriu Valór',
        'all_anos': all_anos,
        'selected_ano': selected_ano,
        'active_ano': active_ano if 'active_ano' in locals() else None,
        'ano_filter': ano_filter,
        'classes': list(classes),
        'periodos': periodos,
        'departments': list(departments),
        'turmas': list(turmas),
        'classe_filter': classe_filter,
        'periodo_filter': periodo_filter,
        'dept_filter': dept_filter,
        'turma_filter': turma_filter,
        'grades_by_student': grades_by_student,
        'materias_common': materias_common,
        'materias_specific': materias_specific,
        'total_students': total_students,
        'total_grades': total_grades,
        'average_grade': round(average_grade, 2) if average_grade else 0,
    }
    return render(request, 'valor/valor_report.html', context)

@login_required
def valor_list(request):
    """List students by class for grading in active year"""
    # Get active academic year
    try:
        active_ano = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        messages.error(request, 'Tinan Akadémiku Ativu la iha! Favor ativa tinan akadémiku dahulu.')
        return redirect('home')

    # Get filter parameters
    dept_filter = request.GET.get('dept', '')
    classe_filter = request.GET.get('classe', '')
    turma_filter = request.GET.get('turma', '')
    periodo_filter = request.GET.get('periodo', '')

    # Get active periods
    periodos = Periodo.objects.filter(is_active=True).order_by('period')

    # Set default period filter to first active period
    if not periodo_filter and periodos.exists():
        periodo_filter = str(periodos[0].id)

    # Get all students enrolled in the active year
    estudante_classes = EstudanteClasse.objects.filter(
        ano=active_ano
    ).select_related(
        'estudante', 'departamentu', 'classe', 'turma'
    ).order_by('departamentu__departamento', 'classe__classe', 'turma__turma', 'estudante__nome')

    # Apply filters
    if dept_filter:
        estudante_classes = estudante_classes.filter(departamentu_id=dept_filter)

        if classe_filter:
            estudante_classes = estudante_classes.filter(classe_id=classe_filter)

            if turma_filter:
                estudante_classes = estudante_classes.filter(turma_id=turma_filter)

    # Get grades count for each student in the selected period
    if periodo_filter:
        estudante_classes_with_grades = []
        for ec in estudante_classes:
            # Count grades for this student in selected period
            grades_count = Valor.objects.filter(
                estudante_classe=ec,
                periodo_id=periodo_filter
            ).count()

            # Attach grades info to the object
            ec.grades_count = grades_count
            ec.has_grades = grades_count > 0
            estudante_classes_with_grades.append(ec)

        estudante_classes = estudante_classes_with_grades

    # Get filter options
    from django.db.models import Count

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

    context = {
        'page_title': 'Valór Estudante',
        'estudante_classes': estudante_classes,
        'active_ano': active_ano,
        'periodos': periodos,
        'departments': list(departments),
        'classes': list(classes),
        'turmas': list(turmas),
        'dept_filter': dept_filter,
        'classe_filter': classe_filter,
        'turma_filter': turma_filter,
        'periodo_filter': periodo_filter,
    }
    return render(request, 'valor/valor_list.html', context)


@login_required
def estudante_valor_detail(request, estudante_classe_pk):
    """View student's grades and basic information"""
    estudante_classe = get_object_or_404(
        EstudanteClasse.objects.select_related(
            'estudante', 'ano', 'departamentu', 'classe', 'turma'
        ),
        pk=estudante_classe_pk
    )
    estudante = estudante_classe.estudante

    # Get period filter parameter
    periodo_filter = request.GET.get('periodo', '')

    # Get all periods (both active and inactive to see old grades)
    periodos = Periodo.objects.all().order_by('period')

    # Set default to last/current active period if no filter
    if not periodo_filter and periodos.exists():
        # Try to get active period first, otherwise get the last period
        try:
            default_periodo = Periodo.objects.filter(is_active=True).first()
            if not default_periodo:
                default_periodo = periodos.last()
            periodo_filter = str(default_periodo.id)
        except:
            periodo_filter = str(periodos.last().id) if periodos.exists() else ''

    # Get grades for this student filtered by period
    valores_query = Valor.objects.filter(
        estudante_classe=estudante_classe
    ).select_related('periodo', 'materia')

    # Filter by selected period (always filter, no "all" option)
    if periodo_filter:
        valores = valores_query.filter(periodo_id=periodo_filter).order_by('materia__codigo')
        try:
            selected_periodo = Periodo.objects.get(id=periodo_filter)
        except Periodo.DoesNotExist:
            selected_periodo = None
    else:
        valores = []
        selected_periodo = None

    # Get available materias: common subjects (no department) + department-specific subjects
    from django.db.models import Q
    materias = Materia.objects.filter(
        Q(departamentu__isnull=True) | Q(departamentu=estudante_classe.departamentu)
    ).order_by('codigo')

    context = {
        'page_title': f'Valór - {estudante.nome}',
        'estudante': estudante,
        'estudante_classe': estudante_classe,
        'valores': valores,
        'materias': materias,
        'periodos': periodos,
        'periodo_filter': periodo_filter,
        'selected_periodo': selected_periodo,
    }
    return render(request, 'valor/estudante_valor_detail.html', context)


@login_required
def valor_create(request, estudante_classe_pk):
    """Add grade for a student"""
    estudante_classe = get_object_or_404(
        EstudanteClasse.objects.select_related(
            'estudante', 'ano', 'departamentu', 'classe', 'turma'
        ),
        pk=estudante_classe_pk
    )

    if request.method == 'POST':
        form = ValorForm(request.POST, estudante_classe=estudante_classe)
        if form.is_valid():
            try:
                with transaction.atomic():
                    valor = form.save(commit=False)
                    valor.estudante_classe = estudante_classe
                    valor.save()

                    messages.success(request, f'Valór ba {estudante_classe.estudante.nome} aumenta tiha ona!')
                    return redirect('estudante_valor_detail', estudante_classe_pk=estudante_classe.pk)
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ValorForm(estudante_classe=estudante_classe)

    # Get existing grades grouped by period and materia for JavaScript filtering
    from collections import defaultdict
    import json
    existing_grades = Valor.objects.filter(
        estudante_classe=estudante_classe
    ).values('periodo_id', 'materia_id')

    # Create a dictionary structure: {periodo_id: [materia_id1, materia_id2, ...]}
    grades_by_period = defaultdict(list)
    for grade in existing_grades:
        grades_by_period[grade['periodo_id']].append(grade['materia_id'])

    existing_grades_json = json.dumps({k: v for k, v in grades_by_period.items()})

    context = {
        'page_title': f'Aumenta Valór - {estudante_classe.estudante.nome}',
        'form': form,
        'estudante_classe': estudante_classe,
        'existing_grades_json': existing_grades_json,
    }
    return render(request, 'valor/valor_form.html', context)


@login_required
def valor_update(request, pk):
    """Update grade"""
    valor = get_object_or_404(Valor.objects.select_related('estudante_classe__estudante'), pk=pk)
    estudante_classe = valor.estudante_classe

    # Check if grade is locked
    if valor.is_lock:
        messages.error(request, 'Valór ne\'e taka tiha ona! La bele hadia.')
        return redirect('estudante_valor_detail', estudante_classe_pk=estudante_classe.pk)

    if request.method == 'POST':
        form = ValorForm(request.POST, instance=valor, estudante_classe=estudante_classe)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Valór hadia tiha ona!')
                return redirect('estudante_valor_detail', estudante_classe_pk=estudante_classe.pk)
            except Exception as e:
                messages.error(request, f'Erru wainhira rai: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ValorForm(instance=valor, estudante_classe=estudante_classe)

    context = {
        'page_title': f'Hadia Valór - {estudante_classe.estudante.nome}',
        'form': form,
        'estudante_classe': estudante_classe,
        'valor': valor,
    }
    return render(request, 'valor/valor_form.html', context)


@login_required
def valor_delete(request, pk):
    """Delete grade"""
    valor = get_object_or_404(Valor.objects.select_related('estudante_classe'), pk=pk)
    estudante_classe_pk = valor.estudante_classe.pk

    # Check if grade is locked
    if valor.is_lock:
        messages.error(request, 'Valór ne\'e taka tiha ona! La bele hamoos.')
        return redirect('estudante_valor_detail', estudante_classe_pk=estudante_classe_pk)

    if request.method == 'POST':
        try:
            valor.delete()
            messages.success(request, 'Valór hamoos tiha ona!')
        except Exception as e:
            messages.error(request, f'Erru wainhira hamoos: {str(e)}')

    return redirect('estudante_valor_detail', estudante_classe_pk=estudante_classe_pk)


@login_required
def valor_graph(request, estudante_pk):
    """Show student grades progression graph across years and periods"""
    estudante = get_object_or_404(Estudante, pk=estudante_pk)

    # Get all enrollments for this student (across all years)
    enrollments = EstudanteClasse.objects.filter(
        estudante=estudante
    ).select_related('ano', 'classe', 'departamentu').order_by('ano__ano')

    # Get all periods ordered
    periodos = Periodo.objects.all().order_by('period')

    # Prepare data structure for chart
    from collections import defaultdict
    import json

    # Data structure: {year: {periodo: avg_grade}}
    data_by_year = defaultdict(dict)
    years = []

    for enrollment in enrollments:
        year = enrollment.ano.ano
        if year not in years:
            years.append(year)

        # Get all grades for this enrollment
        valores = Valor.objects.filter(
            estudante_classe=enrollment
        ).select_related('periodo')

        # Calculate average per period
        period_grades = defaultdict(list)
        for valor in valores:
            period_grades[valor.periodo.period].append(float(valor.valor))

        # Calculate averages
        for period, grades in period_grades.items():
            if grades:
                avg = sum(grades) / len(grades)
                data_by_year[year][period] = round(avg, 2)

    # Prepare data for Chart.js
    datasets = []
    period_list = [p.period for p in periodos]

    # Create dataset for each period
    for periodo in periodos:
        period_data = []
        for year in years:
            period_data.append(data_by_year[year].get(periodo.period, None))

        datasets.append({
            'label': periodo.period,
            'data': period_data,
            'borderWidth': 2,
            'fill': False,
        })

    chart_data = {
        'labels': years,  # X-axis: years
        'datasets': datasets
    }

    # Get current enrollment (latest year)
    current_enrollment = enrollments.last() if enrollments.exists() else None

    context = {
        'page_title': f'Gráfiku Valór - {estudante.nome}',
        'estudante': estudante,
        'estudante_classe': current_enrollment,
        'chart_data': json.dumps(chart_data) if years else None,
        'enrollments': enrollments,
    }
    return render(request, 'valor/valor_graph.html', context)
