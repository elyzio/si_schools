from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.db import transaction
from django.db.models import Prefetch, Count, Avg, F, Sum
from valor.models import Valor, Klassifikasaun
from valor.forms import ValorForm
from estudante.models import Estudante, EstudanteClasse
from custom.models import Ano, Departamentu, Classe, Turma, Materia, Periodo
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from fpdf import FPDF
from main.utils import InttoRoman
import io


def get_student_valor_data(estudante_pk, period_id, classe_id, ano_id):
    """
    Shared data retrieval function for both PDF and Excel exports.
    Returns a dictionary with all necessary data for export.
    """
    estudante = get_object_or_404(Estudante, pk=estudante_pk)
    ano_est = get_object_or_404(Ano, pk=ano_id)
    classe_est = get_object_or_404(Classe, pk=classe_id)
    period_est = get_object_or_404(Periodo, pk=period_id)
    estudante_classe = EstudanteClasse.objects.filter(
        estudante=estudante, ano=ano_est, classe=classe_est
    ).first()

    if not estudante_classe:
        raise ValueError("Estudante classe la hetan!")

    valores_list = Valor.objects.filter(
        estudante_classe=estudante_classe, periodo=period_est
    ).select_related(
        'materia', 'materia__departamentu'
    ).order_by(
        'materia__departamentu', 'materia__materia'
    )

    aggregates = valores_list.aggregate(
        total_valor=Sum('valor'),
        media_valor=Avg('valor')
    )

    total_valor = aggregates['total_valor'] or 0
    media_valor = round(aggregates['media_valor'], 2) if aggregates['media_valor'] else 0

    # Get ranking from Klassifikasaun or calculate
    ranking = []
    is_historical = False

    if not ano_est.is_active:
        try:
            klass = Klassifikasaun.objects.get(
                estudante_classe=estudante_classe,
                periodo=period_est,
                ano=ano_est
            )
            ranking = [{
                'rank': klass.classificasaun_turma,
                'estudante_nome': estudante.nome,
                'total_valor': total_valor,
                'roman_rank': InttoRoman(klass.classificasaun_turma),
                'rank_general': klass.classificasaun_geral,
                'rank_dept': klass.classificasaun_departamentu,
            }]
            is_historical = True
        except Klassifikasaun.DoesNotExist:
            is_historical = False

    if not is_historical:
        est_turma_classe = EstudanteClasse.objects.filter(
            ano=ano_est, classe=classe_est,
            turma=estudante_classe.turma,
            departamentu=estudante_classe.departamentu
        )

        cl_turma = (
            Valor.objects.filter(
                estudante_classe__in=est_turma_classe,
                periodo=period_est
            )
            .values(
                estudante_nome=F('estudante_classe__estudante__nome')
            )
            .annotate(
                total_valor=Sum('valor')
            )
            .order_by('-total_valor')
        )

        user_name = estudante.nome

        for idx, cl in enumerate(cl_turma, start=1):
            if cl['estudante_nome'] == user_name:
                ranking.append({
                    'rank': idx,
                    'estudante_nome': cl['estudante_nome'],
                    'total_valor': cl['total_valor'],
                    'roman_rank': InttoRoman(idx),
                })
                break

        # Only show ranking if has all 13 marks
        valor_count = valores_list.count()
        if valor_count < 13:
            ranking = []

    apr_valor_med = 0
    if period_est.period == '3 Periodo':
        apr_valor = Valor.objects.filter(
            estudante_classe=estudante_classe
        ).aggregate(
            total_apr_valor=Sum('valor'),
            media_apr_valor=Avg('valor')
        )
        apr_valor_tot = apr_valor['total_apr_valor']
        apr_valor_med = apr_valor['media_apr_valor']

    return {
        'estudante': estudante,
        'ano_est': ano_est,
        'classe_est': classe_est,
        'period_est': period_est,
        'estudante_classe': estudante_classe,
        'valores_list': valores_list,
        'total_valor': total_valor,
        'media_valor': media_valor,
        'ranking': ranking,
        'apr_valor_med': apr_valor_med,
    }


def get_approval_status(period, avg_valor):
    """Determine student approval status"""
    if period.period == '3 Periodo':
        return 'Aprovado' if avg_valor > 6 else 'Reprovado'
    return '---'


def sanitize_text(text):
    """Remove or replace characters that FPDF can't handle"""
    if not text:
        return ''
    try:
        return str(text).encode('latin1', errors='replace').decode('latin1')
    except:
        return str(text)


@login_required
def export_student_valor_pdf(request, estudante_pk, period_id, classe_id, ano_id, ex_content):
    """Export student valor detail to PDF - based on ValorEstDetail2 data structure"""
    print(estudante_pk)
    try:
        data = get_student_valor_data(estudante_pk, period_id, classe_id, ano_id)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    estudante = data['estudante']
    ano_est = data['ano_est']
    period_est = data['period_est']
    estudante_classe = data['estudante_classe']
    valores_list = data['valores_list']
    total_valor = data['total_valor']
    media_valor = data['media_valor']
    ranking = data['ranking']
    apr_valor_med = data['apr_valor_med']

    # Create PDF with 30mm margins on all sides
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=30, top=30, right=30)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=30)

    # Title
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, 'VALORES', 0, 1, 'C')
    pdf.ln(5)

    # Student info
    pdf.set_font('Times', 'B', 12)
    pdf.cell(30, 6, 'Naran', 0, 0)
    pdf.cell(50, 6, sanitize_text(f': {estudante.nome}'), 0, 1)
    pdf.cell(30, 6, 'Emis', 0, 0)
    pdf.cell(50, 6, sanitize_text(f': {estudante.emis}'), 0, 1)
    pdf.cell(30, 6, 'No. Registo', 0, 0)
    pdf.cell(50, 6, sanitize_text(f': {estudante.numero_estudante}'), 0, 1)
    pdf.cell(30, 6, 'Ano', 0, 0)
    pdf.cell(50, 6, sanitize_text(f': {estudante_classe.ano.ano}'), 0, 1)
    pdf.cell(30, 6, 'Departamento', 0, 0)
    pdf.cell(50, 6, sanitize_text(f': {estudante_classe.departamentu.departamento}'), 0, 1)
    pdf.cell(30, 6, 'Classe', 0, 0)
    pdf.cell(50, 6, sanitize_text(f': {estudante_classe.classe.classe}'), 0, 1)
    pdf.cell(30, 6, 'Turma', 0, 0)
    pdf.cell(50, 6, sanitize_text(f': {estudante_classe.turma.turma}'), 0, 1)
    pdf.cell(30, 6, 'Periodo', 0, 0)
    pdf.cell(50, 6, sanitize_text(f': {period_est.period}'), 0, 1)
    pdf.ln(5)

    # Table header
    pdf.set_font('Times', 'B', 12)
    pdf.cell(10, 8, 'No', 1, 0, 'C')
    pdf.cell(70, 8, 'Materia', 1, 0, 'C')
    pdf.cell(30, 8, 'Valor', 1, 0, 'C')
    pdf.cell(30, 8, 'Por Extenso', 1, 1, 'C')

    # Table data
    pdf.set_font('Times', '', 12)
    for idx, val in enumerate(valores_list, start=1):
        pdf.cell(10, 7, str(idx), 1, 0, 'C')
        pdf.cell(70, 7, sanitize_text(val.materia.materia), 1, 0, 'L')
        pdf.cell(30, 7, sanitize_text(f"{val.valor:.2f}" if val.valor else '-'), 1, 0, 'C')
        pdf.cell(30, 7, sanitize_text(f"{val.por_extenso}" if val.por_extenso else '-'), 1, 1, 'C')

    y_start = pdf.get_y()
    x_start = pdf.get_x()

    pdf.set_font('Times', 'B', 12)
    # Total row
    pdf.cell(80, 7, 'Total', 1, 0, 'C', False)
    pdf.cell(30, 7, sanitize_text(f"{total_valor}"), 1, 1, 'C', False)
    # Media row
    pdf.cell(80, 7, 'Media', 1, 0, 'C', False)
    pdf.cell(30, 7, sanitize_text(f"{media_valor}"), 1, 1, 'C', False)

    if ranking:
        # Klasifikasaun row
        pdf.cell(80, 7, 'Klasifikasaun', 1, 0, 'C', False)
        pdf.cell(30, 7, sanitize_text(ranking[0]["roman_rank"]), 1, 1, 'C', False)
        
        # Draw merged cell spanning 3 rows (Total, Media, Klasifikasaun)
        pdf.set_xy(x_start + 110, y_start)  # Position after the 60mm cell (80+60=140)
        pdf.multi_cell(30, 21, get_approval_status(period_est, apr_valor_med), 1, 'C')  # height = 7 * 3 = 21mm
    else:
        # Draw merged cell spanning 2 rows only (Total, Media)
        pdf.set_xy(x_start + 110, y_start)
        pdf.multi_cell(30, 14, '---', 1, 'C')  # height = 7 * 2 = 14mm
    
    # Output PDF
    pdf_output = bytes(pdf.output())

    response = HttpResponse(pdf_output, content_type='application/pdf')
    # Sanitize filename
    safe_filename = sanitize_text(f'valor_{estudante.emis}_{estudante.nome}_{ano_est.ano}_{period_est.period}').replace(' ', '_')
    if ex_content == 'print':
        response['Content-Disposition'] = f'inline; filename="{safe_filename}.pdf"'
    else:
        response['Content-Disposition'] = f'attachment; filename="{safe_filename}.pdf"'

    return response


@login_required
def export_student_valor_excel(request, estudante_pk, period_id, classe_id, ano_id):
    """Export student valor detail to Excel - same as PDF export"""
    try:
        data = get_student_valor_data(estudante_pk, period_id, classe_id, ano_id)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    estudante = data['estudante']
    ano_est = data['ano_est']
    period_est = data['period_est']
    estudante_classe = data['estudante_classe']
    valores_list = data['valores_list']
    total_valor = data['total_valor']
    media_valor = data['media_valor']
    ranking = data['ranking']
    apr_valor_med = data['apr_valor_med']

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Valores"

    # Define styles
    header_font = Font(bold=True, size=12)
    header_alignment = Alignment(horizontal="center", vertical="center")
    info_font = Font(bold=True, size=11)
    data_alignment = Alignment(horizontal="center", vertical="center")
    border_style = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Title
    ws.merge_cells('A1:D1')
    ws['A1'] = 'VALORES'
    ws['A1'].font = Font(bold=True, size=14)
    ws['A1'].alignment = Alignment(horizontal="center")

    # Student info
    row_num = 3
    ws[f'A{row_num}'] = 'Naran'
    ws[f'B{row_num}'] = f': {estudante.nome}'
    ws[f'A{row_num}'].font = info_font

    row_num += 1
    ws[f'A{row_num}'] = 'Emis'
    ws[f'B{row_num}'] = f': {estudante.emis}'
    ws[f'A{row_num}'].font = info_font

    row_num += 1
    ws[f'A{row_num}'] = 'No. Registo'
    ws[f'B{row_num}'] = f': {estudante.numero_estudante}'
    ws[f'A{row_num}'].font = info_font

    row_num += 1
    ws[f'A{row_num}'] = 'Ano'
    ws[f'B{row_num}'] = f': {estudante_classe.ano.ano}'
    ws[f'A{row_num}'].font = info_font

    row_num += 1
    ws[f'A{row_num}'] = 'Departamento'
    ws[f'B{row_num}'] = f': {estudante_classe.departamentu.departamento}'
    ws[f'A{row_num}'].font = info_font

    row_num += 1
    ws[f'A{row_num}'] = 'Classe'
    ws[f'B{row_num}'] = f': {estudante_classe.classe.classe}'
    ws[f'A{row_num}'].font = info_font

    row_num += 1
    ws[f'A{row_num}'] = 'Turma'
    ws[f'B{row_num}'] = f': {estudante_classe.turma.turma}'
    ws[f'A{row_num}'].font = info_font

    row_num += 1
    ws[f'A{row_num}'] = 'Periodo'
    ws[f'B{row_num}'] = f': {period_est.period}'
    ws[f'A{row_num}'].font = info_font

    # Table headers (start 2 rows after info)
    row_num += 2
    headers = ['No', 'Materia', 'Valor', 'Por Extenso']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=row_num, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = border_style

    # Data rows
    row_num += 1
    for idx, val in enumerate(valores_list, start=1):
        ws.cell(row=row_num, column=1, value=idx)
        ws.cell(row=row_num, column=2, value=val.materia.materia)
        ws.cell(row=row_num, column=3, value=float(val.valor) if val.valor else 0)
        ws.cell(row=row_num, column=4, value=val.por_extenso if val.por_extenso else '-')

        # Apply styles
        for col_num in range(1, 5):
            cell = ws.cell(row=row_num, column=col_num)
            cell.alignment = data_alignment if col_num != 2 else Alignment(horizontal="left", vertical="center")
            cell.border = border_style

        row_num += 1

    # Summary rows with merged cells
    summary_start_row = row_num
    # Total row
    ws.merge_cells(f'A{row_num}:B{row_num}')
    ws.cell(row=row_num, column=1, value='Total')
    ws.cell(row=row_num, column=1).font = info_font
    ws.cell(row=row_num, column=1).alignment = data_alignment
    # Apply border to all merged cells
    for col in range(1, 3):
        ws.cell(row=row_num, column=col).border = border_style

    ws.cell(row=row_num, column=3, value=f'{total_valor:.2f}')
    ws.cell(row=row_num, column=3).font = info_font
    ws.cell(row=row_num, column=3).alignment = data_alignment
    ws.cell(row=row_num, column=3).border = border_style

    # Media row
    row_num += 1
    ws.merge_cells(f'A{row_num}:B{row_num}')
    ws.cell(row=row_num, column=1, value='Media')
    ws.cell(row=row_num, column=1).font = info_font
    ws.cell(row=row_num, column=1).alignment = data_alignment
    # Apply border to all merged cells
    for col in range(1, 3):
        ws.cell(row=row_num, column=col).border = border_style

    ws.cell(row=row_num, column=3, value=f'{media_valor:.2f}')
    ws.cell(row=row_num, column=3).font = info_font
    ws.cell(row=row_num, column=3).alignment = data_alignment
    ws.cell(row=row_num, column=3).border = border_style

    # Klasifikasaun row
    if ranking:
        row_num += 1
        ws.merge_cells(f'A{row_num}:B{row_num}')
        ws.cell(row=row_num, column=1, value='Klasifikasaun')
        ws.cell(row=row_num, column=1).font = info_font
        ws.cell(row=row_num, column=1).alignment = data_alignment
        # Apply border to all merged cells
        for col in range(1, 3):
            ws.cell(row=row_num, column=col).border = border_style

        ws.cell(row=row_num, column=3, value=ranking[0]['roman_rank'])
        ws.cell(row=row_num, column=3).font = info_font
        ws.cell(row=row_num, column=3).alignment = data_alignment
        ws.cell(row=row_num, column=3).border = border_style

        # Merge cell for approval status spanning 3 rows (Total, Media, Klasifikasaun)
        ws.merge_cells(f'D{summary_start_row}:D{row_num}')
        approval_status = (
            'Aprovado' if apr_valor_med > 6 else 'Reprovado'
        ) if period_est.period == '3 Periodo' else '---'
        ws.cell(row=summary_start_row, column=4, value=approval_status)
        ws.cell(row=summary_start_row, column=4).font = info_font
        ws.cell(row=summary_start_row, column=4).alignment = data_alignment
        # Apply border to all merged cells
        for r in range(summary_start_row, row_num + 1):
            ws.cell(row=r, column=4).border = border_style
    else:
        # Merge cell for approval status spanning 2 rows only (Total, Media)
        ws.merge_cells(f'D{summary_start_row}:D{row_num}')
        ws.cell(row=summary_start_row, column=4, value='---')
        ws.cell(row=summary_start_row, column=4).font = info_font
        ws.cell(row=summary_start_row, column=4).alignment = data_alignment
        # Apply border to all merged cells
        for r in range(summary_start_row, row_num + 1):
            ws.cell(row=r, column=4).border = border_style

    # Adjust column widths
    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['B'].width = 50
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 20

    # Save to BytesIO
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="valor_{estudante.emis}_{estudante.nome}.xlsx"'

    return response
