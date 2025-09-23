from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Valor)
class ValorAdmin(admin.ModelAdmin):
    list_display = ('get_estudante_nome', 'get_estudante_emis', 'get_classe_turma', 'materia', 'periodo', 'valor', 'data_avaliacao', 'is_lock')
    list_filter = ('periodo', 'materia', 'data_avaliacao', 'is_lock', 'estudante_classe__ano', 'estudante_classe__departamentu', 'estudante_classe__classe')
    search_fields = ('estudante_classe__estudante__nome', 'estudante_classe__estudante__emis', 'materia__materia', 'materia__codigo')
    ordering = ('estudante_classe__estudante__nome', 'materia__codigo', 'periodo__period')
    list_per_page = 100
    readonly_fields = ('created_at', 'updated_at')

    def get_estudante_nome(self, obj):
        return obj.estudante_classe.estudante.nome
    get_estudante_nome.short_description = 'Nome Estudante'

    def get_estudante_emis(self, obj):
        return obj.estudante_classe.estudante.emis
    get_estudante_emis.short_description = 'EMIS'

    def get_classe_turma(self, obj):
        return f"{obj.estudante_classe.classe.classe}{obj.estudante_classe.turma.turma}"
    get_classe_turma.short_description = 'Classe/Turma'

@admin.register(Klassifikasaun)
class KlassifikasaunAdmin(admin.ModelAdmin):
    list_display = ('get_estudante_nome', 'get_estudante_emis', 'get_classe_turma', 'ano', 'periodo', 'classificasaun_geral', 'classificasaun_turma', 'classificasaun_departamentu', 'media_geral')
    list_filter = ('ano', 'periodo', 'estudante_classe__departamentu', 'estudante_classe__classe', 'estudante_classe__turma')
    search_fields = ('estudante_classe__estudante__nome', 'estudante_classe__estudante__emis')
    ordering = ('ano__ano', 'classificasaun_geral', 'estudante_classe__estudante__nome')
    list_per_page = 100
    readonly_fields = ('created_at', 'updated_at')

    def get_estudante_nome(self, obj):
        return obj.estudante_classe.estudante.nome
    get_estudante_nome.short_description = 'Nome Estudante'

    def get_estudante_emis(self, obj):
        return obj.estudante_classe.estudante.emis
    get_estudante_emis.short_description = 'EMIS'

    def get_classe_turma(self, obj):
        return f"{obj.estudante_classe.classe.classe}{obj.estudante_classe.turma.turma}"
    get_classe_turma.short_description = 'Classe/Turma'
