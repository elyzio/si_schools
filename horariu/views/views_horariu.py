from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from collections import OrderedDict, defaultdict
from fpdf import FPDF
from horariu.models import Horariu
from horariu.forms import HorariuForm
from custom.models import Materia


@login_required
def horariu_list(request):
    """List all Horariu records with related data"""
    horarius = Horariu.objects.select_related(
        'loron', 'horas', 'classe', 'turma',
        'departamentu', 'professor_materia',
        'professor_materia__professor',
        'professor_materia__materia',
        'ano_academico'
    ).order_by('loron__ordem', 'horas__horas_hahu')

    context = {
        'horarius': horarius,
        'title': 'Lista Horariu'
    }
    return render(request, 'horariu/horariu/horariu_list.html', context)


@login_required
def horariu_create(request):
    """Create a new Horariu"""
    if request.method == 'POST':
        form = HorariuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horariu kria ho suksesu')
            return redirect('horariu_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorariuForm()

    context = {
        'form': form,
        'title': 'Kria Horariu'
    }
    return render(request, 'horariu/horariu/horariu_form.html', context)


@login_required
def horariu_detail(request, pk):
    """View details of a specific Horariu"""
    horariu = get_object_or_404(
        Horariu.objects.select_related(
            'loron', 'horas', 'classe', 'turma',
            'departamentu', 'professor_materia',
            'professor_materia__professor',
            'professor_materia__materia',
            'ano_academico'
        ),
        pk=pk
    )
    context = {
        'horariu': horariu,
        'title': 'Detallu Horariu'
    }
    return render(request, 'horariu/horariu/horariu_detail.html', context)


@login_required
def horariu_update(request, pk):
    """Update an existing Horariu"""
    horariu = get_object_or_404(Horariu, pk=pk)

    if request.method == 'POST':
        form = HorariuForm(request.POST, instance=horariu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horariu hadia ho suksesu')
            return redirect('horariu_list')
        else:
            messages.error(request, 'Favor hadiak erru sira iha formulariu')
    else:
        form = HorariuForm(instance=horariu)

    context = {
        'form': form,
        'horariu': horariu,
        'title': 'Hadia Horariu'
    }
    return render(request, 'horariu/horariu/horariu_form.html', context)


@login_required
def horariu_delete(request, pk):
    """Delete a Horariu"""
    horariu = get_object_or_404(Horariu, pk=pk)

    if request.method == 'POST':
        horariu.delete()
        messages.success(request, 'Horariu hamos ho suksesu')
        return redirect('horariu_list')

    context = {
        'horariu': horariu,
        'title': 'Hamos Horariu'
    }
    return render(request, 'horariu/horariu/horariu_confirm_delete.html', context)

def horariu_table(request):
    materia = Materia.objects.all().order_by('codigo')
    horarius = Horariu.objects.select_related(
        'loron', 'horas', 'classe', 'turma',
        'departamentu', 'professor_materia',
        'professor_materia__professor',
        'professor_materia__materia',
        'ano_academico'
    ).order_by('loron__ordem', 'horas__horas_hahu')

    days_map = OrderedDict()
    hours_map = OrderedDict()
    grouped_rows = OrderedDict()
    code_name_map = {}

    for item in horarius:
        days_map.setdefault(item.loron_id, item.loron)
        hours_map.setdefault(item.horas_id, item.horas)

        group_key = (item.classe_id, item.departamentu_id)
        group_data = grouped_rows.setdefault(group_key, {
            'classe': item.classe,
            'departamentu': item.departamentu,
            'turmas': OrderedDict(),
        })

        class_rows = group_data['turmas']
        cell_map = class_rows.setdefault(item.turma, defaultdict(set))
        subject_code = item.professor_materia.materia.codigo
        subject_name = item.professor_materia.materia.materia
        code_name_map.setdefault(subject_code, subject_name)
        cell_map[(item.loron_id, item.horas_id)].add(subject_code)

    hours = list(hours_map.values())
    days = list(days_map.values())
    morning_hours = [h for h in hours if h.horas_hahu.hour < 12]
    afternoon_hours = [h for h in hours if h.horas_hahu.hour >= 12]

    def build_table_groups(hours_subset):
        
        table_groups = []
        for _, group_data in grouped_rows.items():
            classe = group_data['classe']
            departamentu = group_data['departamentu']
            turma_map = group_data['turmas']
            dept_code = (departamentu.sigla or departamentu.departamento or "").strip().lower()
            group_label = f"{classe.classe} {dept_code}".strip()

            rows = []
            for turma, cell_map in turma_map.items():
                cells = []
                for day in days:
                    for hour_index, hour in enumerate(hours_subset):
                        values = sorted(cell_map.get((day.id, hour.id), []))
                        subject_names = " / ".join(
                            [code_name_map.get(code, code) for code in values]
                        )
                        cells.append({
                            'value': " / ".join(values),
                            'subject_names': subject_names,
                            'day_code': day.loron,
                            'is_day_start': hour_index == 0,
                        })

                rows.append({
                    'turma': turma,
                    'cells': cells,
                })

            table_groups.append({
                'classe': classe,
                'departamentu': departamentu,
                'group_label': group_label,
                'rows': rows,
            })
        return table_groups

    materia_rows = []
    materia_items = list(materia)
    for i in range(0, len(materia_items), 6):
        row = materia_items[i:i + 6]
        while len(row) < 6:
            row.append(None)
        materia_rows.append(row)

    context = {
        'page_title': 'Tabela Horariu',
        'horarius': horarius,
        'days': days,
        'materia_rows': materia_rows,
        'sections': [
            {
                'label': 'Dader',
                'hours': morning_hours,
                'total_cols': len(days) * len(morning_hours),
                'table_groups': build_table_groups(morning_hours),
            },
            {
                'label': 'Tarde',
                'hours': afternoon_hours,
                'total_cols': len(days) * len(afternoon_hours),
                'table_groups': build_table_groups(afternoon_hours),
            },
        ],
    }
    return render(request, 'horariu/horaiu/horariu_table_design.html', context)


def _safe_pdf_text(value):
    if value is None:
        return ''
    return str(value).encode('latin1', errors='replace').decode('latin1')


def _general_horariu_grid(horarius, hours_subset):
    days_map = OrderedDict()
    grouped_rows = OrderedDict()

    for item in horarius:
        days_map.setdefault(item.loron_id, item.loron)
        group_key = (item.classe_id, item.departamentu_id)
        group_data = grouped_rows.setdefault(group_key, {
            'classe': item.classe,
            'departamentu': item.departamentu,
            'turmas': OrderedDict(),
        })
        class_rows = group_data['turmas']
        cell_map = class_rows.setdefault(item.turma, defaultdict(set))
        subject_code = item.professor_materia.materia.codigo
        cell_map[(item.loron_id, item.horas_id)].add(subject_code)

    days = list(days_map.values())
    table_groups = []
    for _, group_data in grouped_rows.items():
        classe = group_data['classe']
        departamentu = group_data['departamentu']
        turma_map = group_data['turmas']
        dept_code = (departamentu.sigla or departamentu.departamento or '').strip().lower()
        group_label = f"{classe.classe} {dept_code}".strip()

        rows = []
        for turma, cell_map in turma_map.items():
            cells = []
            for day in days:
                for hour in hours_subset:
                    values = sorted(cell_map.get((day.id, hour.id), []))
                    cells.append(" / ".join(values))
            rows.append({
                'turma': turma,
                'cells': cells,
            })

        table_groups.append({
            'group_label': group_label,
            'rows': rows,
        })

    return days, table_groups


@login_required
def horariu_table_pdf(request, period=None):
    period_value = (period or request.GET.get('period') or request.GET.get('session') or 'morning').lower()
    if period_value not in {'morning', 'afternoon'}:
        return HttpResponseBadRequest("Invalid period. Use 'morning' or 'afternoon'.")

    horarius = Horariu.objects.select_related(
        'loron', 'horas', 'classe', 'turma',
        'departamentu', 'professor_materia',
        'professor_materia__professor',
        'professor_materia__materia',
        'ano_academico'
    ).order_by('loron__ordem', 'horas__horas_hahu')

    hours_map = OrderedDict()
    for item in horarius:
        hours_map.setdefault(item.horas_id, item.horas)
    all_hours = list(hours_map.values())

    if period_value == 'morning':
        selected_hours = [h for h in all_hours if h.horas_hahu.hour < 12]
        period_label = 'Dader'
    else:
        selected_hours = [h for h in all_hours if h.horas_hahu.hour >= 12]
        period_label = 'Tarde'

    if not selected_hours:
        return HttpResponseBadRequest(f"No hours found for {period_value} period.")

    days, table_groups = _general_horariu_grid(horarius, selected_hours)
    if not days:
        return HttpResponseBadRequest("No day data found for horariu.")

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_margins(left=6, top=8, right=6)
    pdf.set_auto_page_break(auto=True, margin=8)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 7, _safe_pdf_text(f'Horariu Geral - {period_label}'), 0, 1, 'C')
    pdf.set_font('Arial', '', 8)
    pdf.cell(0, 5, _safe_pdf_text(f'Generated: {timezone.now().strftime("%Y-%m-%d %H:%M")}'), 0, 1, 'R')
    pdf.ln(1)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    class_w = 20
    obs_w = 10
    slot_count = len(days) * len(selected_hours)
    slot_w = (usable_width - class_w - obs_w) / max(slot_count, 1)
    row_h = 6
    header_h = 7

    day_colors = {
        'SEG': (232, 239, 0),
        'TER': (196, 0, 0),
        'QUA': (232, 239, 0),
        'QUI': (134, 198, 66),
        'SEX': (143, 164, 199),
        'SAB': (111, 45, 156),
    }

    def draw_header():
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(class_w, header_h, 'Classe', 1, 0, 'C', True)
        for day in days:
            day_label = _safe_pdf_text(day.get_loron_display())
            pdf.cell(slot_w * len(selected_hours), header_h, day_label, 1, 0, 'C', True)
        pdf.cell(obs_w, header_h, 'OBS', 1, 1, 'C', True)

    draw_header()

    for group in table_groups:
        required_h = row_h * (1 + len(group['rows']))
        if pdf.get_y() + required_h > (pdf.h - pdf.b_margin):
            pdf.add_page()
            draw_header()

        pdf.set_font('Arial', 'B', 7)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(class_w, row_h, _safe_pdf_text(group['group_label']), 1, 0, 'C', True)

        for day in days:
            r, g, b = day_colors.get(day.loron, (230, 230, 230))
            for _ in selected_hours:
                pdf.set_fill_color(r, g, b)
                pdf.cell(slot_w, row_h, '', 1, 0, 'C', True)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(obs_w, row_h, '', 1, 1, 'C', True)

        pdf.set_font('Arial', '', 7)
        for row in group['rows']:
            if pdf.get_y() + row_h > (pdf.h - pdf.b_margin):
                pdf.add_page()
                draw_header()

            pdf.set_fill_color(255, 255, 255)
            pdf.cell(class_w, row_h, _safe_pdf_text(row['turma'].turma), 1, 0, 'C', True)
            for value in row['cells']:
                pdf.set_fill_color(222, 222, 222)
                pdf.cell(slot_w, row_h, _safe_pdf_text(value), 1, 0, 'C', True)
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(obs_w, row_h, '', 1, 1, 'C', True)

    # Materia legend (all materia) in multi-column layout to keep it compact.
    materia_items = list(
        Materia.objects.order_by('codigo').values_list('codigo', 'materia')
    )
    if materia_items:
        if pdf.get_y() + 10 > (pdf.h - pdf.b_margin):
            pdf.add_page()

        pdf.ln(2)
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(0, 6, _safe_pdf_text('Codigo Disciplina'), 0, 1, 'L')

        legend_col_count = 6
        legend_col_w = usable_width / legend_col_count
        legend_row_h = 6
        pdf.set_font('Arial', '', 7)

        for index, (code, name) in enumerate(materia_items):
            if index > 0 and index % legend_col_count == 0:
                pdf.ln()
                if pdf.get_y() + legend_row_h > (pdf.h - pdf.b_margin):
                    pdf.add_page()
                    pdf.set_font('Arial', 'B', 8)
                    pdf.cell(0, 6, _safe_pdf_text('Codigo Disciplina (continua)'), 0, 1, 'L')
                    pdf.set_font('Arial', '', 7)

            label = _safe_pdf_text(f"{code} - {name}")
            pdf.cell(legend_col_w, legend_row_h, label, 1, 0, 'L', False)

        remainder = len(materia_items) % legend_col_count
        if remainder:
            for _ in range(legend_col_count - remainder):
                pdf.cell(legend_col_w, legend_row_h, '', 1, 0, 'L', False)
        pdf.ln()

    filename = f"horariu_geral_{period_value}_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf_bytes = bytes(pdf.output())
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=\"{filename}\"'
    return response
