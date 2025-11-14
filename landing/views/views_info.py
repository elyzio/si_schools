from django.shortcuts import render
from django.db.models import Count, Max, Prefetch
# from django.db.models import Max, Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from konaba.models import KonaBa, Informasaun
from estudante.models import Estudante, EstudanteClasse
from professor.models import Professor
from custom.models import Ano, Departamentu, Classe

# Create your views here.

def about_page(request):
    """Public About page using KonaBa content"""
    kona_ba_items = KonaBa.objects.filter(is_active=True).order_by('orden')

    context = {
        'kona_ba_items': kona_ba_items,
    }
    return render(request, 'landing/about.html', context)

def information_page(request):
    """Public Information page showing news"""
    # Get published information only
    informasaun_list = Informasaun.objects.filter(is_published=True).order_by('-data_publiku')

    # Separate by type
    news_list = informasaun_list.filter(tipu_informasaun='Informasaun')
    events = informasaun_list.filter(tipu_informasaun='Ajenda')[:5]
    activities = informasaun_list.filter(tipu_informasaun='Atividade')[:5]

    # Pagination for news
    paginator = Paginator(news_list, 9)  # 9 items per page (3 columns x 3 rows)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'events': events,
        'activities': activities,
        'news': events,
        'inf':'news',
        'page_title': 'Informasaun',
        'icn': 'newspaper'
    }
    return render(request, 'landing/information.html', context)

def agenda_page(request):
    """Public Information page showing events"""
    # Get published information only
    informasaun_list = Informasaun.objects.filter(is_published=True).order_by('-data_publiku')

    # Separate by type
    news = informasaun_list.filter(tipu_informasaun='Informasaun')[:5]
    events_list = informasaun_list.filter(tipu_informasaun='Ajenda')
    activities = informasaun_list.filter(tipu_informasaun='Atividade')[:5]

    # Pagination for events
    paginator = Paginator(events_list, 9)  # 9 items per page (3 columns x 3 rows)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'items': items,
        'activities': activities,
        'events': news,
        'inf':'event',
        'page_title': 'Agenda',
        'icn': 'calendar-alt'
    }
    return render(request, 'landing/information.html', context)

def activity_page(request):
    """Public Information page showing activities"""
    # Get published information only
    informasaun_list = Informasaun.objects.filter(is_published=True).order_by('-data_publiku')

    # Separate by type
    news = informasaun_list.filter(tipu_informasaun='Informasaun')[:5]
    events = informasaun_list.filter(tipu_informasaun='Ajenda')[:5]
    activities_list = informasaun_list.filter(tipu_informasaun='Atividade')

    # Pagination for activities
    paginator = Paginator(activities_list, 9)  # 9 items per page (3 columns x 3 rows)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'events': events,
        'items': items,
        'activities': news,
        'inf':'activity',
        'page_title': 'Actividade',
        'icn': 'running'
    }
    return render(request, 'landing/information.html', context)

def information_detail(request, pk):
    """Public Information detail page with recent posts"""
    from django.shortcuts import get_object_or_404

    # Get the main information item
    info = get_object_or_404(Informasaun, pk=pk, is_published=True)

    # Get recent posts by type (excluding current item)
    recent_news = Informasaun.objects.filter(
        is_published=True,
        tipu_informasaun='Informasaun'
    ).exclude(pk=pk).order_by('-data_publiku')[:3]

    recent_events = Informasaun.objects.filter(
        is_published=True,
        tipu_informasaun='Ajenda'
    ).exclude(pk=pk).order_by('-data_publiku')[:3]

    recent_activities = Informasaun.objects.filter(
        is_published=True,
        tipu_informasaun='Atividade'
    ).exclude(pk=pk).order_by('-data_publiku')[:3]

    context = {
        'info': info,
        'recent_news': recent_news,
        'recent_events': recent_events,
        'recent_activities': recent_activities,
    }
    return render(request, 'landing/information_detail.html', context)

def statistics_page(request):
    """Public Statistics page with aggregated school data"""
    current_year = Ano.objects.filter(is_active=True).first()
       
    # Academic structure
    departments = Departamentu.objects.all()
    total_departments = departments.count()
    classes = Classe.objects.all()
    total_classes = classes.count()

    # Student statistics
    current_students = EstudanteClasse.objects.filter(ano=current_year)
    active_students = current_students.filter(estudante__is_active=True,estudante__is_transfer=False,estudante__is_alumni=False)
    total_act_student = active_students.count()
    # total_students = Estudante.objects.filter(is_active=True).count()
    # active_enrollments = EstudanteClasse.objects.filter(ano=current_year).count() if current_year else 0

    st_data = {}
    st_dept_data = []
    for dep in departments:
        dept_data = {
            'dep': dep,
            'clas': []
        }
        for cl in classes:
            cl_data = {
                'cl': cl,
                'cl_tot': active_students.filter(classe=cl, departamentu=dep).count()
            }
            dept_data['clas'].append(cl_data)
        st_dept_data.append(dept_data)

    # for st in st_dept_data:
        # print(f"DATA: {st['dep']}")


    # Gender distribution
    male_students = active_students.filter(estudante__sexu='M').count()
    female_students = active_students.filter(estudante__sexu='F').count()
    # male_students = Estudante.objects.filter(is_active=True, sexu='M').count()
    # female_students = Estudante.objects.filter(is_active=True, sexu='F').count()
    # print(f"total students: {total_act_student}, total female: {female_students}, total_male {male_students}")

    # Teacher statistics
    active_teacher = Professor.objects.filter(is_active=True)
    total_teachers = active_teacher.count()
    male_teachers = active_teacher.filter(sexu='M').count()
    female_teachers = active_teacher.filter(sexu='F').count()
    # print(f"total teacher: {total_teachers}, male teacher: {male_teachers}, female_teacher: {female_teachers}")

    # Students by department (for chart)
    students_by_dept = []
    if current_year:
        students_by_dept = list(
            active_students
            .values('departamentu__departamento', 'departamentu__sigla')
            .annotate(total=Count('id'))
            .order_by('departamentu__departamento')
        )
    # for stu in students_by_dept:
    #     print(stu)

    # Alumni statistics
    alumni_students = Estudante.objects.filter(is_active=False, is_transfer=False, is_alumni=True)
    total_alumni = alumni_students.count()
    male_alumni = alumni_students.filter(sexu='M').count()
    female_alumni = alumni_students.filter(sexu='F').count()

    # Alumni by department (get last enrollment department)
    alumni_by_dept = []
    alumni_with_dept = Estudante.objects.filter(
        is_alumni=True
    ).prefetch_related(
        Prefetch(
            'estudanteclasse_set',
            queryset=EstudanteClasse.objects.select_related(
                'departamentu'
            ).order_by('-ano__id'),
            to_attr='last_enrollment'
        )
    )

    # Count alumni by their last department
    dept_count = {}
    for student in alumni_with_dept:
        if student.last_enrollment:
            last_class = student.last_enrollment[0]
            dept_name = last_class.departamentu.departamento if last_class.departamentu else 'Unknown'
            dept_sigla = last_class.departamentu.sigla if last_class.departamentu else 'N/A'

            if dept_sigla not in dept_count:
                dept_count[dept_sigla] = {
                    'departamentu__departamento': dept_name,
                    'departamentu__sigla': dept_sigla,
                    'total': 0
                }
            dept_count[dept_sigla]['total'] += 1

    alumni_by_dept = list(dept_count.values())




    context = {
        'current_year': current_year,
        'total_students': total_act_student,
        'male_students': male_students,
        'female_students': female_students,
        'total_teachers': total_teachers,
        'male_teachers': male_teachers,
        'female_teachers': female_teachers,
        'total_alumni': total_alumni,
        'male_alumni': male_alumni,
        'female_alumni': female_alumni,
        'total_departments': total_departments,
        'total_classes': total_classes,
        'students_by_dept': students_by_dept,
        'alumni_by_dept': alumni_by_dept,
        'classe': classes,
        'st_dept_data': st_dept_data,
    }
    return render(request, 'landing/statistics.html', context)
