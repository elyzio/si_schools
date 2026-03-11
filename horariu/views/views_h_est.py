from collections import OrderedDict, defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from fpdf import FPDF
from horariu.models import Horariu
from estudante.models import EstudanteClasse
from custom.models import Ano


@login_required
def HorariuListEst(request):
    """List all Horariu records for the logged-in estudante"""

    try:
        estudante = request.user.estudanteuser.estudante
        # print(estudante.get_current_classe_turma())
    except:
        messages.error(request, 'Ita la rejista hanesan estudante')
        return redirect('home')
    
    ano_active = Ano.objects.filter(is_active=True).first()
    estudante_classe = EstudanteClasse.objects.filter(estudante=estudante, ano=ano_active).first()
    horarius = Horariu.objects.by_class(
        estudante_classe.classe,
        estudante_classe.departamentu,
        estudante_classe.turma,
        ano_active,
    )

    context = {
        'horarius': horarius,
        'page_title': 'Hau nia Horariu',
        'estudante': estudante,
    }
    return render(request, 'horariu/horariu/horariu_list.html', context)

@login_required
def HorariuTableEst(request):
    try:
        estudante = request.user.estudanteuser.estudante
    except Exception:
        messages.error(request, 'Ita la rejista hanesan estudante')
        return redirect('home')

    ano_active = Ano.objects.filter(is_active=True).first()
    if not ano_active:
        messages.error(request, 'Laiha ano akademiku ativo')
        return redirect('home')

    estudante_classe = (
        EstudanteClasse.objects.select_related('classe', 'turma', 'departamentu', 'ano')
        .filter(estudante=estudante, ano=ano_active)
        .first()
    )
    if not estudante_classe:
        messages.error(request, 'Laiha klase/turma estudante nian ba ano ativo')
        return redirect('home')

    horarius = (
        Horariu.objects.select_related(
            'loron', 'horas', 'classe', 'turma',
            'departamentu', 'professor_materia',
            'professor_materia__materia',
            'ano_academico'
        )
        .filter(
            classe=estudante_classe.classe,
            turma=estudante_classe.turma,
            departamentu=estudante_classe.departamentu,
            ano_academico=ano_active,
            is_active=True,
        )
        .order_by('horas__horas_hahu', 'loron__ordem')
    )

    days_map = OrderedDict()
    hours_map = OrderedDict()
    cell_map = defaultdict(set)
    code_name_map = {}

    for item in horarius:
        days_map.setdefault(item.loron_id, item.loron)
        hours_map.setdefault(item.horas_id, item.horas)

        code = item.professor_materia.materia.codigo
        name = item.professor_materia.materia.materia
        code_name_map.setdefault(code, name)
        cell_map[(item.horas_id, item.loron_id)].add(code)

    days = list(days_map.values())
    hours = list(hours_map.values())

    schedule_rows = []
    for index, hour in enumerate(hours, start=1):
        # row_label = (hour.obs or '').strip() or f'hor{index}'
        cells = []
        for day in days:
            codes = sorted(cell_map.get((hour.id, day.id), []))
            cells.append({
                'value': ' / '.join(codes),
                'subject_names': ' / '.join(code_name_map.get(code, code) for code in codes),
            })
        schedule_rows.append({
            # 'label': row_label,
            'cells': cells,
            'hour': hour,
        })

    # print(schedule_rows)

    context = {
        'page_title': 'Horariu Estudante',
        'estudante': estudante,
        'estudante_classe': estudante_classe,
        'ano_active': ano_active,
        'days': days,
        'schedule_rows': schedule_rows,
    }
    return render(request, 'horariu/horaiu/horariu_table_design_est.html', context)


def _safe_pdf_text(value):
    if value is None:
        return ''
    return str(value).encode('latin1', errors='replace').decode('latin1')


@login_required
def HorariuTableEstPDF(request):
    try:
        estudante = request.user.estudanteuser.estudante
    except Exception:
        messages.error(request, 'Ita la rejista hanesan estudante')
        return redirect('home')

    ano_active = Ano.objects.filter(is_active=True).first()
    if not ano_active:
        messages.error(request, 'Laiha ano akademiku ativo')
        return redirect('home')

    estudante_classe = (
        EstudanteClasse.objects.select_related('classe', 'turma', 'departamentu', 'ano')
        .filter(estudante=estudante, ano=ano_active)
        .first()
    )
    if not estudante_classe:
        messages.error(request, 'Laiha klase/turma estudante nian ba ano ativo')
        return redirect('home')

    horarius = (
        Horariu.objects.select_related(
            'loron', 'horas', 'classe', 'turma',
            'departamentu', 'professor_materia',
            'professor_materia__materia',
            'ano_academico'
        )
        .filter(
            classe=estudante_classe.classe,
            turma=estudante_classe.turma,
            departamentu=estudante_classe.departamentu,
            ano_academico=ano_active,
            is_active=True,
        )
        .order_by('horas__horas_hahu', 'loron__ordem')
    )

    days_map = OrderedDict()
    hours_map = OrderedDict()
    cell_map = defaultdict(set)
    code_name_map = {}

    for item in horarius:
        days_map.setdefault(item.loron_id, item.loron)
        hours_map.setdefault(item.horas_id, item.horas)
        code = item.professor_materia.materia.materia
        # code = item.professor_materia.materia.codigo
        name = item.professor_materia.materia.materia
        code_name_map.setdefault(code, name)
        cell_map[(item.horas_id, item.loron_id)].add(code)

    days = list(days_map.values())
    hours = list(hours_map.values())

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_margins(left=8, top=8, right=8)
    pdf.set_auto_page_break(auto=True, margin=8)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 7, _safe_pdf_text('Horariu Estudante'), 0, 1, 'C')
    pdf.set_font('Arial', '', 8)
    sub_header = (
        f"{estudante.nome} | "
        f"{estudante_classe.classe.classe} {estudante_classe.turma.turma} - "
        f"{estudante_classe.departamentu.sigla or estudante_classe.departamentu.departamento} | "
        f"{ano_active.ano}"
    )
    pdf.cell(0, 5, _safe_pdf_text(sub_header), 0, 1, 'C')
    pdf.cell(0, 4, _safe_pdf_text(f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M')}"), 0, 1, 'R')
    pdf.ln(1)

    if not days or not hours:
        pdf.set_font('Arial', '', 9)
        pdf.cell(0, 7, _safe_pdf_text("Laiha dadus horariu ba estudante ida-ne'e"), 1, 1, 'C')
    else:
        usable_width = pdf.w - pdf.l_margin - pdf.r_margin
        first_col_w = 25
        day_col_w = (usable_width - first_col_w) / max(len(days), 1)
        row_h = 8

        # Header
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(first_col_w, row_h, 'Oras', 1, 0, 'C', True)
        for day in days:
            pdf.cell(day_col_w, row_h, _safe_pdf_text(day.get_loron_display()), 1, 0, 'C', True)
        pdf.ln()

        # Body
        pdf.set_font('Arial', '', 7)
        for index, hour in enumerate(hours, start=1):
            # row_label = (hour.obs or '').strip() or f'hor{index}'
            time_label = f"{hour.horas_hahu.strftime('%H:%M')}-{hour.horas_termina.strftime('%H:%M')}"
            label = f"{time_label}"

            if pdf.get_y() + row_h > (pdf.h - pdf.b_margin):
                pdf.add_page()
                pdf.set_font('Arial', 'B', 8)
                pdf.cell(first_col_w, row_h, 'Oras', 1, 0, 'C', True)
                for day in days:
                    pdf.cell(day_col_w, row_h, _safe_pdf_text(day.get_loron_display()+'d'), 1, 0, 'C', True)
                pdf.ln()
                pdf.set_font('Arial', '', 7)

            pdf.set_fill_color(245, 245, 245)
            pdf.cell(first_col_w, row_h, _safe_pdf_text(label), 1, 0, 'C', True)

            for day in days:
                codes = sorted(cell_map.get((hour.id, day.id), []))
                cell_value = " / ".join(codes)
                pdf.set_fill_color(255, 255, 255)
                pdf.cell(day_col_w, row_h, _safe_pdf_text(cell_value), 1, 0, 'C', True)
            pdf.ln()

    # if code_name_map:
    #     pdf.ln(2)
    #     pdf.set_font('Arial', 'B', 8)
    #     pdf.cell(0, 5, _safe_pdf_text('Codigo Disciplina'), 0, 1, 'L')
    #     pdf.set_font('Arial', '', 7)

    #     legend_items = [f"{code} - {code_name_map[code]}" for code in sorted(code_name_map.keys())]
    #     for item in legend_items:
    #         if pdf.get_y() + 4 > (pdf.h - pdf.b_margin):
    #             pdf.add_page()
    #         pdf.cell(0, 4, _safe_pdf_text(item), 0, 1, 'L')

    filename = f"horariu_estudante_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf_bytes = bytes(pdf.output())
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=\"{filename}\"'
    return response
