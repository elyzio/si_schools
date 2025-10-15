from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from custom.models import Subdistrito, Suco, Aldeia

# =============================================================================
# AJAX VIEWS FOR DEPENDENT DROPDOWNS
# =============================================================================

@login_required
def ajax_subdistrito(request):
    distrito_id = request.GET.get('distrito_id')
    subdistritos = Subdistrito.objects.filter(distrito_id=distrito_id).order_by('nome')
    data = [{'id': s.id, 'name': s.nome} for s in subdistritos]
    return JsonResponse(data, safe=False)

@login_required
def ajax_suco(request):
    subdistrito_id = request.GET.get('subdistrito_id')
    sucos = Suco.objects.filter(subdistrito_id=subdistrito_id).order_by('nome')
    data = [{'id': s.id, 'name': s.nome} for s in sucos]
    return JsonResponse(data, safe=False)

@login_required
def ajax_aldeia(request):
    suco_id = request.GET.get('suco_id')
    aldeias = Aldeia.objects.filter(suco_id=suco_id).order_by('nome')
    data = [{'id': a.id, 'name': a.nome} for a in aldeias]
    return JsonResponse(data, safe=False)