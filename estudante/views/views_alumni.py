from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from estudante.models import EstudanteAlumni, Estudante
from custom.models import Ano

# =============================================================================
# ALUMNI VIEWS
# =============================================================================

@login_required
def alumni_list(request):
    """Show all alumni students"""
    # Get filter parameters
    ano_filter = request.GET.get('ano', '')
    search_query = request.GET.get('search', '')

    # Base queryset - all alumni
    alumni_queryset = EstudanteAlumni.objects.select_related(
        'estudante', 'ano'
    ).order_by('-data_alumni', 'estudante__nome')

    # Apply filters
    if ano_filter:
        alumni_queryset = alumni_queryset.filter(ano_id=ano_filter)

    if search_query:
        alumni_queryset = alumni_queryset.filter(
            Q(estudante__nome__icontains=search_query) |
            Q(estudante__emis__icontains=search_query)
        )

    # Get filter options - all graduation years
    graduation_years = EstudanteAlumni.objects.values(
        'ano__id', 'ano__ano'
    ).annotate(count=Count('id')).order_by('-ano__ano')

    # Statistics
    total_alumni = alumni_queryset.count()
    total_all_alumni = EstudanteAlumni.objects.count()

    context = {
        'page_title': 'Lista Alumni',
        'alumni_list': alumni_queryset,
        'total_alumni': total_alumni,
        'total_all_alumni': total_all_alumni,
        'graduation_years': list(graduation_years),
        'ano_filter': ano_filter,
        'search_query': search_query,
    }
    return render(request, 'estudante/alumni/alumni_list.html', context)


@login_required
def alumni_detail(request, pk):
    """Show detailed information about an alumni"""
    alumni = get_object_or_404(EstudanteAlumni, pk=pk)

    # Get all class history for this student
    from estudante.models import EstudanteClasse
    class_history = EstudanteClasse.objects.filter(
        estudante=alumni.estudante
    ).select_related('ano', 'departamentu', 'classe', 'turma').order_by('ano__ano')

    # Get final grade info (last class before alumni)
    final_class = class_history.filter(is_passa=True).last()

    context = {
        'page_title': f'Alumni - {alumni.estudante.nome}',
        'alumni': alumni,
        'class_history': class_history,
        'final_class': final_class,
    }
    return render(request, 'estudante/alumni/alumni_detail.html', context)
