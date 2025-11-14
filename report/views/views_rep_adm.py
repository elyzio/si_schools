from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from fpdf import FPDF
from django.db.models import Count, Q
from estudante.models import Estudante, EstudanteClasse
from professor.models import Professor, ProfessorClasse
from custom.models import Ano, Classe, Departamentu
from django.contrib.auth.decorators import login_required


@login_required
def ProfessorExcelReport(request):
    """Generate Excel report with professor personal information in multiple sheets"""

    # Create workbook
    wb = Workbook()

    # Define common styles
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_alignment = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Fetch all professors
    professors = Professor.objects.select_related(
        'distrito', 'subdistrito', 'suco', 'aldeia'
    ).all()

    # Apply filters from GET parameters
    estadu = request.GET.get('estadu')
    nivel_akademiku = request.GET.get('nivel_akademiku')
    is_active = request.GET.get('is_active')
    distrito = request.GET.get('distrito')

    if estadu:
        professors = professors.filter(estadu=estadu)
    if nivel_akademiku:
        professors = professors.filter(nivel_akademiku=nivel_akademiku)
    if is_active:
        professors = professors.filter(is_active=(is_active.lower() == 'true'))
    if distrito:
        professors = professors.filter(distrito_id=distrito)

    # ===== SHEET 1: PERSONAL INFORMATION =====
    ws1 = wb.active
    ws1.title = "Personal Information"

    # Add title
    title_cell = ws1.cell(row=1, column=1)
    title_cell.value = "LISTA PROFESSOR - INFORMASAUN PERSONAL"
    title_cell.font = Font(bold=True, size=16)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws1.merge_cells(start_row=1, start_column=1, end_row=1, end_column=14)
    ws1.row_dimensions[1].height = 25

    # Define headers for sheet 1
    headers_personal = [
        'No.',
        'Naran',
        'Sexu',
        'Data Moris',
        'Fatin Moris',
        'Nasionalidade',
        'Distrito',
        'Subdistrito',
        'Suco',
        'Aldeia',
        'Hela Fatin',
        'Kontatu',
        'Email',
        'Estadu Civil'
    ]

    # Write headers
    for col_num, header in enumerate(headers_personal, 1):
        cell = ws1.cell(row=2, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = border

    # Write data
    for row_num, professor in enumerate(professors, 3):
        data = [
            row_num - 2,
            professor.nome,
            'Mane' if professor.sexu == 'M' else 'Feto',
            professor.data_moris.strftime('%d/%m/%Y') if professor.data_moris else '',
            professor.fatin_moris,
            professor.nacionalidade,
            professor.distrito.nome if professor.distrito else '',
            professor.subdistrito.nome if professor.subdistrito else '',
            professor.suco.nome if professor.suco else '',
            professor.aldeia.nome if professor.aldeia else '',
            professor.hela_fatin or '',
            professor.kontatu or '',
            professor.email or '',
            professor.get_estadu_civil_display() if professor.estadu_civil else ''
        ]

        for col_num, value in enumerate(data, 1):
            cell = ws1.cell(row=row_num, column=col_num)
            cell.value = value
            cell.border = border
            cell.alignment = Alignment(vertical="center")

    # Adjust column widths for sheet 1
    column_widths_personal = [5, 25, 8, 12, 20, 15, 15, 15, 15, 15, 30, 15, 25, 15]
    for col_num, width in enumerate(column_widths_personal, 1):
        ws1.column_dimensions[ws1.cell(row=2, column=col_num).column_letter].width = width

    # ===== SHEET 2: EMPLOYMENT INFORMATION =====
    ws2 = wb.create_sheet(title="Employment Information")

    # Add title
    title_cell2 = ws2.cell(row=1, column=1)
    title_cell2.value = "LISTA PROFESSOR - INFORMASAUN EMPREGU"
    title_cell2.font = Font(bold=True, size=16)
    title_cell2.alignment = Alignment(horizontal="center", vertical="center")
    ws2.merge_cells(start_row=1, start_column=1, end_row=1, end_column=9)
    ws2.row_dimensions[1].height = 25

    # Define headers for sheet 2
    headers_employment = [
        'No.',
        'Naran',
        'Numeru Funsionariu',
        'Estadu',
        'Grau Akademiku',
        'Data Kontratasaun',
        'Status',
        'Email',
        'Kontatu'
    ]

    # Write headers
    for col_num, header in enumerate(headers_employment, 1):
        cell = ws2.cell(row=2, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = border

    # Write data
    for row_num, professor in enumerate(professors, 3):
        data = [
            row_num - 2,
            professor.nome,
            professor.numero_funcionario or '',
            professor.get_estadu_display(),
            professor.grau_akademiku or '',
            professor.data_contratacao.strftime('%d/%m/%Y') if professor.data_contratacao else '',
            'Ativu' if professor.is_active else 'Inativu',
            professor.email or '',
            professor.kontatu or ''
        ]

        for col_num, value in enumerate(data, 1):
            cell = ws2.cell(row=row_num, column=col_num)
            cell.value = value
            cell.border = border
            cell.alignment = Alignment(vertical="center")

    # Adjust column widths for sheet 2
    column_widths_employment = [5, 25, 18, 15, 20, 15, 10, 25, 15]
    for col_num, width in enumerate(column_widths_employment, 1):
        ws2.column_dimensions[ws2.cell(row=2, column=col_num).column_letter].width = width

    filename = f"professor_report_{timezone.now().strftime('%Y%m%d_%H%M')}.xlsx"
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Save workbook to response
    wb.save(response)

    return response


@login_required
def ProfessorPDFReport(request, content):
    """Generate PDF report with professor employment information"""

    # Fetch all professors
    professors = Professor.objects.select_related(
        'distrito', 'subdistrito', 'suco', 'aldeia'
    ).all()

    # Apply filters from GET parameters
    estadu = request.GET.get('estadu')
    nivel_akademiku = request.GET.get('nivel_akademiku')
    is_active = request.GET.get('is_active')
    distrito = request.GET.get('distrito')

    if estadu:
        professors = professors.filter(estadu=estadu)
    if nivel_akademiku:
        professors = professors.filter(nivel_akademiku=nivel_akademiku)
    if is_active:
        professors = professors.filter(is_active=(is_active.lower() == 'true'))
    if distrito:
        professors = professors.filter(distrito_id=distrito)

    # Create PDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 10, 'RELATORIU KONTRATU PROFESSOR', 0, 1, 'C')
    pdf.ln(5)

    # Table header
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(54, 96, 146)
    pdf.set_text_color(255, 255, 255)

    # Column widths
    col_widths = [10, 45, 13, 27, 20, 30, 30, 25, 15, 35, 25]

    # Headers
    headers = ['No.', 'Naran', 'Sexu', 'No. Funsionariu', 'Estadu', 'Grau Akademiku','Nivel Akademiku',
               'Data Kontratu', 'Status', 'Email', 'Kontatu']

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, 1, 0, 'C', True)
    pdf.ln()

    # Table data
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(0, 0, 0)

    for idx, professor in enumerate(professors, 1):
        # Alternate row colors
        if idx % 2 == 0:
            pdf.set_fill_color(240, 240, 240)
        else:
            pdf.set_fill_color(255, 255, 255)

        data = [
            str(idx),
            professor.nome[:30],  # Truncate long names
            'M' if professor.sexu == 'M' else 'F',
            professor.numero_funcionario or '-',
            professor.get_estadu_display()[:15],
            professor.grau_akademiku[:20] if professor.grau_akademiku else '-',
            professor.nivel_akademiku[:20] if professor.nivel_akademiku else '-',
            professor.data_contratacao.strftime('%d/%m/%Y') if professor.data_contratacao else '-',
            'Ativu' if professor.is_active else 'Inativu',
            professor.email[:30] if professor.email else '-',
            professor.kontatu or '-'
        ]

        # Column alignments: L for left, C for center
        alignments = ['C', 'L', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'L', 'L']

        for i, value in enumerate(data):
            pdf.cell(col_widths[i], 7, value, 1, 0, alignments[i], True)
        pdf.ln()

    # Add signature section at bottom
    # Check if there's enough space on current page, otherwise add new page
    if pdf.get_y() > 160:  # If near bottom, add new page
        pdf.add_page()
    else:
        # Move to bottom of page if enough space
        remaining_space = 190 - pdf.get_y()  # 190 is near bottom of page
        if remaining_space > 40:  # Need at least 40mm for signature
            pdf.ln(remaining_space - 35)

    pdf.ln(10)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, '', 0, 1)

    # pdf.ln(10)
    # pdf.set_font('Arial', 'B', 11)
    # pdf.cell(0, 10, 'Date: ____/____/____', 0, 1, 'C')
    # pdf.cell(0, 10, '', 0, 1)

    # Signature line
    pdf.cell(0, 10, '_' * 40, 0, 1, 'C')
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'Diretor', 0, 1, 'C')

    # Generate response
    filename = f"professor_contract_report_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"

    # Get PDF bytes
    pdf_bytes = bytes(pdf.output())

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    if content == 'print':
        response['Content-Disposition'] = f'inline; filename="{filename}"'
    elif content == 'pdf':
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    # response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@login_required
def ProfessorDetailPDFReport(request, professor_id):
    """Generate detailed PDF report for a single professor with personal and employment information"""

    # Fetch professor
    try:
        professor = Professor.objects.select_related(
            'distrito', 'subdistrito', 'suco', 'aldeia'
        ).get(id=professor_id)
    except Professor.DoesNotExist:
        return HttpResponse("Professor not found", status=404)

    # Create PDF
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    # pdf.set_font('Arial', 'B', 16)
    # pdf.cell(0, 10, 'INFORMASAUN PROFESSOR', 0, 1, 'C')
    # pdf.ln(5)

    # Add professor image if exists
    if professor.imagem and professor.imagem.path:
        try:
            import os
            if os.path.exists(professor.imagem.path):
                # Place image on right side
                pdf.image(professor.imagem.path, x=150, y=30, w=40, h=50)
        except:
            pass

    # PERSONAL INFORMATION SECTION
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(54, 96, 146)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, 'INFORMASAUN PERSONAL', 0, 1, 'L', True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Personal info data
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Naran:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.nome, 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Sexu:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, 'Mane' if professor.sexu == 'M' else 'Feto', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Data Moris:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.data_moris.strftime('%d/%m/%Y') if professor.data_moris else '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Fatin Moris:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.fatin_moris or '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Nasionalidade:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.nacionalidade or '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Estadu Civil:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.get_estadu_civil_display() if professor.estadu_civil else '-', 0, 1)

    pdf.ln(3)

    # ADDRESS SECTION
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(54, 96, 146)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, 'ENDERESU', 0, 1, 'L', True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Distrito:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.distrito.nome if professor.distrito else '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Subdistrito:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.subdistrito.nome if professor.subdistrito else '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Suco:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.suco.nome if professor.suco else '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Aldeia:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.aldeia.nome if professor.aldeia else '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Hela Fatin:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 7, professor.hela_fatin or '-')

    pdf.ln(3)

    # CONTACT SECTION
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(54, 96, 146)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, 'KONTATU', 0, 1, 'L', True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Telefone:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.kontatu or '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Email:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.email or '-', 0, 1)

    pdf.ln(3)

    # EMPLOYMENT INFORMATION SECTION
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(54, 96, 146)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, 'INFORMASAUN EMPREGU', 0, 1, 'L', True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Numeru Funsionariu:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.numero_funcionario or '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Estadu:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.get_estadu_display(), 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Nivel Akademiku:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.get_nivel_akademiku_display(), 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Grau Akademiku:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.grau_akademiku or '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Data Kontratasaun:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, professor.data_contratacao.strftime('%d/%m/%Y') if professor.data_contratacao else '-', 0, 1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(50, 7, 'Status:', 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, 'Ativu' if professor.is_active else 'Inativu', 0, 1)

    # Date and signature at bottom
    pdf.ln(10)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f'Data: {timezone.now().strftime("%d/%m/%Y")}', 0, 1, 'R')
    pdf.ln(5)

    # Signature line
    pdf.cell(0, 10, '_' * 40, 0, 1, 'R')
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'Diretor', 0, 1, 'R')

    # Generate response
    filename = f"professor_detail_{professor.numero_funcionario or professor_id}_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"

    # Get PDF bytes
    pdf_bytes = bytes(pdf.output())

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    return response

def ReportGrafikuADM(request):
    """View for displaying graphics about students and teachers"""
    from estudante.models import EstudanteAlumni
    from professor.models import ProfessorMateria

    # Get current academic year (or latest)
    current_year = Ano.objects.filter(is_active=True).first()

    # Student statistics
    total_students = Estudante.objects.filter(is_active=True).count()
    active_enrollments = EstudanteClasse.objects.filter(ano=current_year).count() if current_year else 0
    transferred_students = Estudante.objects.filter(is_transfer=True).count()
    alumni_students = Estudante.objects.filter(is_alumni=True).count()

    # Students by gender
    male_students = Estudante.objects.filter(is_active=True, sexu='M').count()
    female_students = Estudante.objects.filter(is_active=True, sexu='F').count()

    # Students by class (current year)
    students_by_class = []
    if current_year:
        students_by_class = list(
            EstudanteClasse.objects.filter(ano=current_year)
            .values('classe__classe')
            .annotate(total=Count('id'))
            .order_by('classe__classe')
        )

    # Students by department
    students_by_dept = []
    if current_year:
        students_by_dept = list(
            EstudanteClasse.objects.filter(ano=current_year)
            .values('departamentu__departamento', 'departamentu__sigla')
            .annotate(total=Count('id'))
            .order_by('departamentu__sigla')
        )

    # Students by department and class (for table)
    students_dept_class = []
    if current_year:
        students_dept_class = list(
            EstudanteClasse.objects.filter(ano=current_year)
            .values('departamentu__departamento', 'classe__classe')
            .annotate(total=Count('id'))
            .order_by('departamentu__departamento', 'classe__classe')
        )

    # Students by district
    students_by_district = list(
        Estudante.objects.filter(is_active=True)
        .exclude(distrito__isnull=True)
        .values('distrito__nome')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Alumni by year and department
    try:
        alumni_by_year_dept = []
        alumni_records = EstudanteAlumni.objects.select_related('estudante', 'ano').all()
        alumni_data = {}

        for alumni in alumni_records:
            # Get the student's most recent class enrollment to determine department
            estudante_classe = EstudanteClasse.objects.filter(
                estudante=alumni.estudante
            ).select_related('departamentu').order_by('-ano__ano').first()

            if estudante_classe and estudante_classe.departamentu:
                key = (alumni.ano.ano, estudante_classe.departamentu.departamento)
                alumni_data[key] = alumni_data.get(key, 0) + 1

        # Convert to list format
        alumni_by_year_dept = [
            {
                'ano__ano': year,
                'estudante__estudanteclasse__departamentu__departamento': dept,
                'total': count
            }
            for (year, dept), count in sorted(alumni_data.items(), key=lambda x: (-x[0][0], x[0][1]))
        ]
    except Exception as e:
        print(f"Error fetching alumni data: {e}")
        alumni_by_year_dept = []

    # Teacher statistics
    total_teachers = Professor.objects.filter(is_active=True).count()

    # Teachers by status
    teachers_by_status = list(
        Professor.objects.filter(is_active=True)
        .values('estadu')
        .annotate(total=Count('id'))
    )

    # Teachers by gender
    male_teachers = Professor.objects.filter(is_active=True, sexu='M').count()
    female_teachers = Professor.objects.filter(is_active=True, sexu='F').count()

    # Teachers by academic level
    teachers_by_level = list(
        Professor.objects.filter(is_active=True)
        .values('nivel_akademiku')
        .annotate(total=Count('id'))
    )

    # Teachers by district
    teachers_by_district = list(
        Professor.objects.filter(is_active=True)
        .exclude(distrito__isnull=True)
        .values('distrito__nome')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Teachers by subject
    try:
        teachers_by_subject = list(
            ProfessorMateria.objects.filter(is_active=True, professor__is_active=True)
            .values('materia__materia')
            .annotate(total=Count('professor', distinct=True))
            .order_by('-total')
        )
    except Exception as e:
        print(f"Error fetching teachers by subject: {e}")
        teachers_by_subject = []

    # Teachers assigned to classes (current year)
    teachers_assigned = 0
    if current_year:
        teachers_assigned = ProfessorClasse.objects.filter(ano=current_year).values('professor').distinct().count()

    context = {
        'page_title':'Relatoriu Grafiku',
        'current_year': current_year,

        # Student data
        'total_students': total_students,
        'active_enrollments': active_enrollments,
        'transferred_students': transferred_students,
        'alumni_students': alumni_students,
        'male_students': male_students,
        'female_students': female_students,
        'students_by_class': students_by_class,
        'students_by_dept': students_by_dept,
        'students_dept_class': students_dept_class,
        'students_by_district': students_by_district,
        'alumni_by_year_dept': alumni_by_year_dept,

        # Teacher data
        'total_teachers': total_teachers,
        'teachers_by_status': teachers_by_status,
        'male_teachers': male_teachers,
        'female_teachers': female_teachers,
        'teachers_by_level': teachers_by_level,
        'teachers_assigned': teachers_assigned,
        'teachers_by_district': teachers_by_district,
        'teachers_by_subject': teachers_by_subject,
    }

    return render(request, 'report/graphics_dashboard.html', context)

@login_required
def ReportTableADM(request):
    """View for displaying count tables about students and teachers"""
    from estudante.models import EstudanteAlumni
    from professor.models import ProfessorMateria

    # Get current academic year (or latest)
    current_year = Ano.objects.filter(is_active=True).first()

    # Students by department and class (for table)
    students_dept_class = []
    if current_year:
        students_dept_class = list(
            EstudanteClasse.objects.filter(ano=current_year)
            .values('departamentu__departamento', 'classe__classe')
            .annotate(total=Count('id'))
            .order_by('departamentu__departamento', 'classe__classe')
        )

    # Students by district
    students_by_district = list(
        Estudante.objects.filter(is_active=True)
        .exclude(distrito__isnull=True)
        .values('distrito__nome')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Alumni by year and department
    try:
        alumni_by_year_dept = []
        alumni_records = EstudanteAlumni.objects.select_related('estudante', 'ano').all()
        alumni_data = {}

        for alumni in alumni_records:
            # Get the student's most recent class enrollment to determine department
            estudante_classe = EstudanteClasse.objects.filter(
                estudante=alumni.estudante
            ).select_related('departamentu').order_by('-ano__ano').first()

            if estudante_classe and estudante_classe.departamentu:
                key = (alumni.ano.ano, estudante_classe.departamentu.departamento)
                alumni_data[key] = alumni_data.get(key, 0) + 1

        # Convert to list format
        alumni_by_year_dept = [
            {
                'ano__ano': year,
                'estudante__estudanteclasse__departamentu__departamento': dept,
                'total': count
            }
            for (year, dept), count in sorted(alumni_data.items(), key=lambda x: (-x[0][0], x[0][1]))
        ]
    except Exception as e:
        print(f"Error fetching alumni data: {e}")
        alumni_by_year_dept = []

    # Teachers by academic level
    teachers_by_level = list(
        Professor.objects.filter(is_active=True)
        .values('nivel_akademiku')
        .annotate(total=Count('id'))
    )

    # Teachers by district
    teachers_by_district = list(
        Professor.objects.filter(is_active=True)
        .exclude(distrito__isnull=True)
        .values('distrito__nome')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Teachers by subject
    try:
        teachers_by_subject = list(
            ProfessorMateria.objects.filter(is_active=True, professor__is_active=True)
            .values('materia__materia')
            .annotate(total=Count('professor', distinct=True))
            .order_by('-total')
        )
    except Exception as e:
        print(f"Error fetching teachers by subject: {e}")
        teachers_by_subject = []

    context = {
        'page_title': 'Relatoriu Tabela',
        'current_year': current_year,
        'students_dept_class': students_dept_class,
        'students_by_district': students_by_district,
        'alumni_by_year_dept': alumni_by_year_dept,
        'teachers_by_level': teachers_by_level,
        'teachers_by_district': teachers_by_district,
        'teachers_by_subject': teachers_by_subject,
    }

    return render(request, 'report/tables_dashboard.html', context)

# Student Detail Views
@login_required
def student_dept_class_detail(request):
    """View students by department and class"""
    dept = request.GET.get('dept')
    classe = request.GET.get('class')
    current_year = Ano.objects.filter(is_active=True).first()

    students = EstudanteClasse.objects.filter(
        ano=current_year,
        departamentu__departamento=dept,
        classe__classe=classe
    ).select_related('estudante', 'departamentu', 'classe', 'turma')

    context = {
        'page_title': f'Students - {dept} - {classe}',
        'students': students,
        'dept': dept,
        'classe': classe,
        'current_year': current_year,
    }
    return render(request, 'report/est/dept_class_list.html', context)

@login_required
def student_district_detail(request):
    """View students by district"""
    district = request.GET.get('district')

    students = Estudante.objects.filter(
        is_active=True,
        distrito__nome=district
    ).select_related('distrito')

    context = {
        'page_title': f'Students from {district}',
        'students': students,
        'district': district,
    }
    return render(request, 'report/est/district_list.html', context)

@login_required
def alumni_year_dept_detail(request):
    """View alumni by year and department"""
    from estudante.models import EstudanteAlumni

    year = request.GET.get('year')
    dept = request.GET.get('dept')

    # Get alumni for the specified year
    alumni_list = EstudanteAlumni.objects.filter(
        ano__ano=year
    ).select_related('estudante', 'ano')

    # Filter by department
    filtered_alumni = []
    for alumni in alumni_list:
        estudante_classe = EstudanteClasse.objects.filter(
            estudante=alumni.estudante
        ).select_related('departamentu').order_by('-ano__ano').first()

        if estudante_classe and estudante_classe.departamentu and estudante_classe.departamentu.departamento == dept:
            filtered_alumni.append({
                'alumni': alumni,
                'estudante': alumni.estudante,
                'department': estudante_classe.departamentu.departamento
            })

    context = {
        'page_title': f'Alumni {year} - {dept}',
        'alumni_list': filtered_alumni,
        'year': year,
        'dept': dept,
    }
    return render(request, 'report/est/alumni_list.html', context)

# Teacher Detail Views
@login_required
def teacher_district_detail(request):
    """View teachers by district"""
    district = request.GET.get('district')

    teachers = Professor.objects.filter(
        is_active=True,
        distrito__nome=district
    ).select_related('distrito')

    context = {
        'page_title': f'Teachers from {district}',
        'teachers': teachers,
        'district': district,
    }
    return render(request, 'report/prof/district_list.html', context)

@login_required
def teacher_level_detail(request):
    """View teachers by academic level"""
    level = request.GET.get('level')

    teachers = Professor.objects.filter(
        is_active=True,
        nivel_akademiku=level
    )

    context = {
        'page_title': f'Teachers - {level}',
        'teachers': teachers,
        'level': level,
    }
    return render(request, 'report/prof/level_list.html', context)

@login_required
def teacher_subject_detail(request):
    """View teachers by subject"""
    from professor.models import ProfessorMateria

    subject = request.GET.get('subject')

    teacher_materias = ProfessorMateria.objects.filter(
        is_active=True,
        professor__is_active=True,
        materia__materia=subject
    ).select_related('professor', 'materia', 'classe')

    context = {
        'page_title': f'Teachers - {subject}',
        'teacher_materias': teacher_materias,
        'subject': subject,
    }
    return render(request, 'report/prof/subject_list.html', context)

