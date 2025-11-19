from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from fpdf import FPDF
from django.db.models import Count, Q
from estudante.models import Estudante, EstudanteClasse
# from professor.models import Professor, ProfessorClasse
from custom.models import Ano, Classe, Departamentu
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os

# Custom PDF class with page numbers
class PDF(FPDF):
    def footer(self):
        # Position at 15mm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'B', 10)  # Bold, size 10
        self.set_text_color(0, 0, 0)  # Blue color matching header
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def EstudanteListPDF(request, content):
    """Generate PDF report with professor employment information"""

    # Fetch all professors
    estudantes = Estudante.objects.select_related(
        'distrito', 'subdistrito', 'suco', 'aldeia'
    ).filter(is_transfer=False)

    # Apply filters from GET parameters
    class_status_filter = request.GET.get('class_status')
    dept_filter = request.GET.get('dept')
    classe_filter = request.GET.get('classe')
    turma_filter = request.GET.get('turma')
    year_filter = request.GET.get('year')

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
        estudantes_assigned = EstudanteClasse.objects.filter(
            ano=active_ano
        ).values_list('estudante_id', flat=True)

        # Apply class assignment filter
        if class_status_filter == 'assigned':
            # Students who have class assignment for active year
            assigned_student_ids = EstudanteClasse.objects.filter(
                ano=active_ano
            ).values_list('estudante_id', flat=True)
            estudantes = estudantes.filter(id__in=assigned_student_ids)
        elif class_status_filter == 'not_assigned':
            # Students who don't have class assignment for active year
            assigned_student_ids = EstudanteClasse.objects.filter(
                ano=active_ano
            ).values_list('estudante_id', flat=True)
            estudantes = estudantes.exclude(id__in=assigned_student_ids)
        # 'all' shows all students (no additional filter)

        # Apply department filter (only for assigned students)
        if dept_filter and class_status_filter == 'assigned':
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


    # Create PDF
    pdf = PDF(orientation='L', unit='mm', format='A4')
    pdf.set_margins(30, 30, 30)  # Left, Top, Right margins = 30mm
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=30)  # Bottom margin = 30mm
    pdf.alias_nb_pages()  # Enable {nb} for total page count

    # Add header image
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo-header-landscape.jpg')
    if os.path.exists(logo_path):
        # Center the image (A4 landscape width is 297mm)
        pdf.image(logo_path, x=25, y=20, w=250)  # Adjust w (width) as needed

    pdf.ln(23)  # Space after logo

    # Add separator line
    pdf.set_draw_color(0, 0, 0)  # Blue color for separator
    pdf.set_line_width(1)  # Line thickness
    pdf.line(30, pdf.get_y(), 267, pdf.get_y())  # Draw horizontal line from left to right margin

    # Reset draw color to black for table borders
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)  # Reset to default line width
    pdf.ln(5)

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'RELATORIO LISTA ESTUDANTE EM {active_ano}', 0, 1, 'C')
    pdf.ln(5)

    # Table header
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(54, 96, 146)
    pdf.set_text_color(255, 255, 255)

    # Column widths
    col_widths = [10, 30, 30, 45, 15, 25, 25, 25]

    # Headers
    headers = ['No.', 'Emis', 'Nu. Rejistu', 'Naran', 'Sexu', 'Data Matrikula','Distrito',
               'Kontatu']

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, 1, 0, 'C', True)
    pdf.ln()

    # Table data
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(0, 0, 0)

    for idx, estudante in enumerate(estudantes, 1):
        # Alternate row colors
        if idx % 2 == 0:
            pdf.set_fill_color(240, 240, 240)
        else:
            pdf.set_fill_color(255, 255, 255)

        data = [
            str(idx),
            estudante.emis,
            estudante.numero_estudante,
            estudante.nome,
            'M' if estudante.sexu == 'M' else 'F',
            estudante.data_matricula.strftime('%d/%m/%Y') if estudante.data_matricula else '-',
            estudante.distrito.nome,
            # estudante.email[:30] if estudante.email else '-',
            estudante.kontatu or '-'
        ]

        # Column alignments: L for left, C for center
        alignments = ['C', 'L', 'L', 'L', 'C', 'C', 'C', 'C']

        for i, value in enumerate(data):
            pdf.cell(col_widths[i], 7, value, 1, 0, alignments[i], True)
        pdf.ln()

    # Add signature section
    # A4 landscape = 210mm height, with 30mm top + 30mm bottom margin = 150mm usable
    signature_height = 30  # Space needed for signature
    page_bottom = 210 - 30  # 180mm (page height - bottom margin)

    # Check if there's enough space on current page for signature
    if pdf.get_y() + signature_height > page_bottom:
        pdf.add_page()
        pdf.ln(10)
    else:
        pdf.ln(15)  # Add some space before signature

    # Signature line
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, '_' * 40, 0, 1, 'C')
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 5, 'Diretor', 0, 1, 'C')

    # Generate response
    filename = f"Lista_matrikula_estudante_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"

    # Get PDF bytes
    pdf_bytes = bytes(pdf.output())

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    if content == 'print':
        response['Content-Disposition'] = f'inline; filename="{filename}"'
    elif content == 'pdf':
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    # response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response