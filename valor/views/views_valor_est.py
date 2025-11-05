from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Prefetch, Count, Avg, F, Sum
from valor.models import Valor
from valor.forms import ValorForm
from estudante.models import Estudante, EstudanteClasse
from custom.models import Ano, Departamentu, Classe, Turma, Materia, Periodo
from collections import defaultdict
import json
from django.core.serializers.json import DjangoJSONEncoder
from main.utils import InttoRoman

def ValorEstList(request):
    """List Valor records for estudantes with graphed data"""
    userest = request.user.estudanteuser.estudante
    estudante = userest
    ano = Ano.objects.filter(is_active=True).first()
    estudante_classes = EstudanteClasse.objects.filter(estudante=estudante)
    # print("Estudante:", estudante_class)
    
    # Example: build all averages for all anos
    valores_qs = (
        Valor.objects.filter(estudante_classe__in=estudante_classes)
        .values(
            estudante_nome=F('estudante_classe__estudante__nome'),
            ano_nome=F('estudante_classe__ano__ano'),
            classe_nome=F('estudante_classe__classe__classe'),
            periodo_nome=F('periodo__period'),
        )
        .annotate(media_valor=Avg('valor'))
        .order_by('estudante_nome', 'ano_nome', 'classe_nome', 'periodo_nome')
    )

    # Build nested dict:
    # valores_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(dict))) # three levels
    valores_dict = defaultdict(lambda: defaultdict(dict))
    # valores_dict = defaultdict(dict)

    for v in valores_qs:
        estudante = v['estudante_nome']
        ano_classe = f"{v['classe_nome']} ({v['ano_nome']})"
        periodo = v['periodo_nome']
        # classe = v['classe_nome']
        media = float(v['media_valor']) if v['media_valor'] is not None else None
        
        # valores_dict[ano_classe][periodo] = media
        valores_dict[estudante][ano_classe][periodo] = media
    valores_json = json.dumps(valores_dict, cls=DjangoJSONEncoder)
    print("Valores JSON:", valores_json)
    
    context = {
        'page_title': 'Hau nia Valores - Grafiku',
        'valores': valores_json,
        'estudante': estudante,
        'est_class': estudante_classes.filter(ano=ano).first(),
    }
    return render(request, 'valor/estudante/valor_list.html', context)

def ValorEstList2(request):
    """List Valor records for estudantes data with klassifikasaun"""
    from valor.models import Klassifikasaun

    userest = request.user.estudanteuser.estudante
    estudante = userest
    ano = Ano.objects.filter(is_active=True).first()
    estudante_classes = EstudanteClasse.objects.filter(estudante=estudante).order_by('-ano__ano')

    valores_list = (
        Valor.objects.filter(estudante_classe__in=estudante_classes)
        .values(
            estudante_nome=F('estudante_classe__estudante__nome'),
            ano_nome=F('estudante_classe__ano__ano'),
            classe_nome=F('estudante_classe__classe__classe'),
            periodo_nome=F('periodo__period'),
            ano_id=F('estudante_classe__ano__id'),
            classe_id=F('estudante_classe__classe__id'),
            period_id=F('periodo__id'),
            estudante_classe_id=F('estudante_classe__id'),
            ano_is_active=F('estudante_classe__ano__is_active'),
        )
        .annotate(media_valor=Avg('valor'))
        .annotate(total_valor=Sum('valor'))
        .order_by('estudante_nome', '-ano_nome', 'classe_nome', 'periodo_nome')
    )

    # Add klassifikasaun info to each valor record
    valores_with_klassifikasaun = []
    for val in valores_list:
        val_dict = dict(val)

        # Try to get klassifikasaun (only for inactive years)
        if not val['ano_is_active']:
            try:
                klass = Klassifikasaun.objects.get(
                    estudante_classe_id=val['estudante_classe_id'],
                    periodo_id=val['period_id'],
                    ano_id=val['ano_id']
                )
                val_dict['klassifikasaun_turma'] = klass.classificasaun_turma
                val_dict['klassifikasaun_turma_roman'] = InttoRoman(klass.classificasaun_turma)
                val_dict['has_klassifikasaun'] = True
            except Klassifikasaun.DoesNotExist:
                val_dict['klassifikasaun_turma'] = None
                val_dict['klassifikasaun_turma_roman'] = '-'
                val_dict['has_klassifikasaun'] = False
        else:
            # Active year - no klassifikasaun yet
            val_dict['klassifikasaun_turma'] = None
            val_dict['klassifikasaun_turma_roman'] = '-'
            val_dict['has_klassifikasaun'] = False

        valores_with_klassifikasaun.append(val_dict)

    context = {
        'page_title': 'Hau nia Valores',
        'valores_list': valores_with_klassifikasaun,
        'est_class': estudante_classes.filter(ano=ano).first(),
    }
    return render(request, 'valor/estudante/valor_list2.html', context)

def ValorEstDetail2(request, period_id, classe_id, ano_id):
    """List Detail Valor records for estudantes data by periodu, classe, ano
    SMART: Uses Valor (active year) or Klassifikasaun (historical year)"""
    from valor.models import Klassifikasaun

    userest = request.user.estudanteuser.estudante
    estudante = userest
    ano = Ano.objects.filter(is_active=True).first()
    ano_est = get_object_or_404(Ano, pk=ano_id)
    classe_est = get_object_or_404(Classe, pk=classe_id)
    period_est = get_object_or_404(Periodo, pk=period_id)
    estudante_classe = EstudanteClasse.objects.filter(estudante=estudante, ano=ano_est, classe=classe_est).first()

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

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # SMART LOGIC: Active or Historical?
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ranking = []
    is_historical = False

    if not ano_est.is_active:
        # HISTORICAL YEAR: Try to get from Klassifikasaun
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
            # No historical data, fall back to calculation
            is_historical = False

    if not is_historical:
        # ACTIVE YEAR or NO HISTORICAL DATA: Calculate from Valor (current logic)
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
        apr_valor = (
            Valor.objects.filter(
                estudante_classe=estudante_classe
            ).aggregate(
                total_apr_valor=Sum('valor'),
                media_apr_valor=Avg('valor')
            )
        )
        apr_valor_tot = apr_valor['total_apr_valor']
        apr_valor_med = apr_valor['media_apr_valor']

    context = {
        'page_title': 'Hau nia Detallu Valores',
        'valores': valores_list,
        'est_class': estudante_classe,
        'total_valor': total_valor,
        'media_valor': media_valor,
        'ranking': ranking,
        'apr_valor': apr_valor_med if period_est.period == '3 Periodo' else None,
        'period': period_est.period,
        'is_historical': is_historical,  # NEW: Tell template
        'ano_est': ano_est,  # NEW: For display
    }
    return render(request, 'valor/estudante/valor_detail2.html', context)