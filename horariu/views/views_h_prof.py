from collections import OrderedDict, defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from fpdf import FPDF
from horariu.models import Horariu


@login_required
def HorariuListProf(request):
    """List all Horariu records for the logged-in professor"""

    try:
        professor = request.user.professoruser.professor
    except:
        messages.error(request, 'Ita la rejista hanesan profesor')
        return redirect('home')
    
    horarius = Horariu.objects.by_professor(professor)
    # horarius = Horariu.objects.select_related(
    #     'loron', 'horas', 'classe', 'turma',
    #     'departamentu', 'professor_materia',
    #     'professor_materia__professor',
    #     'professor_materia__materia',
    #     'ano_academico'
    # ).order_by('loron__ordem', 'horas__horas_hahu')

    context = {
        'horarius': horarius,
        'page_title': 'Hau nia Horariu',
        'professor': professor,
    }
    return render(request, 'horariu/horariu/horariu_list.html', context)

@login_required
def HorariuTableProf(request):
    try:
        professor = request.user.professoruser.professor
    except Exception:
        messages.error(request, 'Ita la rejista hanesan profesor')
        return redirect('home')

    schedule_tables = _get_prof_schedule_tables(professor)
    
    # print(schedule_tables)

    context = {
        'page_title': 'Horariu hanorin',
        'professor': professor,
        'schedule_tables': schedule_tables,
    }
    return render(request, 'horariu/horaiu/horariu_table_design_prof.html', context)


def _safe_pdf_text(value):
    if value is None:
        return ''
    return str(value).encode('latin1', errors='replace').decode('latin1')


def _get_prof_schedule_tables(professor):
    horarius = (
        Horariu.objects.select_related(
            'loron', 'horas', 'classe', 'turma',
            'departamentu', 'professor_materia',
            'professor_materia__professor',
            'professor_materia__materia',
            'ano_academico'
        )
        .filter(
            professor_materia__professor=professor,
            is_active=True,
        )
        .order_by(
            'ano_academico__ano',
            'classe__classe',
            'professor_materia__materia__codigo',
            'horas__horas_hahu',
            'loron__ordem',
            'turma__turma',
        )
    )

    grouped = OrderedDict()
    for item in horarius:
        group_key = (
            item.ano_academico_id,
            item.classe_id,
            item.professor_materia_id,
        )
        group = grouped.setdefault(group_key, {
            'ano': item.ano_academico,
            'classe': item.classe,
            'professor_materia': item.professor_materia,
            'days_map': OrderedDict(),
            'hours_map': OrderedDict(),
            'cells_map': defaultdict(set),
        })

        group['days_map'].setdefault(item.loron_id, item.loron)
        group['hours_map'].setdefault(item.horas_id, item.horas)

        turma_label = item.turma.turma
        if item.departamentu and item.departamentu.sigla:
            turma_label = f"{turma_label} ({item.departamentu.sigla})"
        group['cells_map'][(item.horas_id, item.loron_id)].add(turma_label)

    schedule_tables = []
    for _, group in grouped.items():
        days = list(group['days_map'].values())
        hours = list(group['hours_map'].values())
        rows = []

        for index, hour in enumerate(hours, start=1):
            # row_label = (hour.obs or '').strip() or f'hor{index}'
            row_cells = []
            for day in days:
                values = sorted(group['cells_map'].get((hour.id, day.id), []))
                row_cells.append({
                    'value': ' / '.join(values),
                    'title': ' / '.join(values),
                })
            rows.append({
                # 'label': row_label,
                'hour': hour,
                'cells': row_cells,
            })

        pm = group['professor_materia']
        materia = pm.materia
        schedule_tables.append({
            'ano': group['ano'],
            'classe': group['classe'],
            'materia': materia,
            'days': days,
            'rows': rows,
        })
    return schedule_tables


@login_required
def HorariuTableProfPDF(request):
    try:
        professor = request.user.professoruser.professor
    except Exception:
        messages.error(request, 'Ita la rejista hanesan profesor')
        return redirect('home')

    schedule_tables = _get_prof_schedule_tables(professor)

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_margins(left=8, top=8, right=8)
    pdf.set_auto_page_break(auto=True, margin=8)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 7, _safe_pdf_text('Horariu Professor'), 0, 1, 'C')
    pdf.set_font('Arial', '', 8)
    pdf.cell(0, 5, _safe_pdf_text(professor.nome), 0, 1, 'C')
    pdf.cell(0, 4, _safe_pdf_text(f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M')}"), 0, 1, 'R')
    pdf.ln(1)

    if not schedule_tables:
        pdf.set_font('Arial', '', 9)
        pdf.cell(0, 7, _safe_pdf_text("Laiha dadus horariu ba professor ida-ne'e"), 1, 1, 'C')
    else:
        for table in schedule_tables:
            days = table['days']
            rows = table['rows']

            if not days:
                continue

            section_title = (
                f"{table['materia'].codigo} - {table['materia'].materia} | "
                f"Classe: {table['classe'].classe} | "
                f"Tinan: {table['ano'].ano if table['ano'] else '-'}"
            )

            required_h = 6 + 7 + max(len(rows), 1) * 8 + 4
            if pdf.get_y() + required_h > (pdf.h - pdf.b_margin):
                pdf.add_page()

            pdf.set_font('Arial', 'B', 8)
            pdf.cell(0, 6, _safe_pdf_text(section_title), 0, 1, 'L')

            usable_width = pdf.w - pdf.l_margin - pdf.r_margin
            first_col_w = 30
            day_col_w = (usable_width - first_col_w) / max(len(days), 1)
            row_h = 8

            pdf.set_font('Arial', 'B', 8)
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(first_col_w, row_h, 'Oras', 1, 0, 'C', True)
            for day in days:
                pdf.cell(day_col_w, row_h, _safe_pdf_text(day.get_loron_display()), 1, 0, 'C', True)
            pdf.ln()

            pdf.set_font('Arial', '', 7)
            if rows:
                for row in rows:
                    if pdf.get_y() + row_h > (pdf.h - pdf.b_margin):
                        pdf.add_page()
                        pdf.set_font('Arial', 'B', 8)
                        pdf.cell(first_col_w, row_h, 'Oras', 1, 0, 'C', True)
                        for day in days:
                            pdf.cell(day_col_w, row_h, _safe_pdf_text(day.get_loron_display()), 1, 0, 'C', True)
                        pdf.ln()
                        pdf.set_font('Arial', '', 7)

                    time_label = f"{row['hour'].horas_hahu.strftime('%H:%M')}-{row['hour'].horas_termina.strftime('%H:%M')}"
                    label = f"{time_label}"
                    # label = f"{row['label']} ({time_label})"
                    pdf.set_fill_color(245, 245, 245)
                    pdf.cell(first_col_w, row_h, _safe_pdf_text(label), 1, 0, 'C', True)

                    for cell in row['cells']:
                        pdf.set_fill_color(255, 255, 255)
                        pdf.cell(day_col_w, row_h, _safe_pdf_text(cell['value']), 1, 0, 'C', True)
                    pdf.ln()
            else:
                pdf.cell(0, row_h, _safe_pdf_text("Laiha oras ba tabela ida-ne'e"), 1, 1, 'C')

            pdf.ln(2)

    filename = f"horariu_professor_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf_bytes = bytes(pdf.output())
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=\"{filename}\"'
    return response
