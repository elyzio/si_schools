from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Loron)
class LoronAdmin(admin.ModelAdmin):
    list_display = ('get_loron_display', 'loron', 'ordem')
    search_fields = ('loron',)
    ordering = ('ordem',)

@admin.register(Horas)
class HorasAdmin(admin.ModelAdmin):
    list_display = ('horas_hahu', 'horas_termina', 'obs')
    search_fields = ('obs',)
    ordering = ('horas_hahu',)

@admin.register(Horariu)
class HorariuAdmin(admin.ModelAdmin):
    list_display = ('get_professor_nome', 'get_materia', 'get_classe_turma', 'loron', 'horas', 'ano_academico', 'is_active')
    list_filter = ('ano_academico', 'loron', 'departamentu', 'classe', 'turma', 'is_active')
    search_fields = ('professor_materia__professor__nome', 'professor_materia__materia__materia', 'professor_materia__materia__codigo')
    ordering = ('ano_academico__ano', 'loron__ordem', 'horas__horas_hahu', 'classe__classe', 'turma__turma')
    readonly_fields = ('created_at', 'updated_at')

    def get_professor_nome(self, obj):
        return obj.professor_materia.professor.nome
    get_professor_nome.short_description = 'Professor'

    def get_materia(self, obj):
        return obj.professor_materia.materia.materia
    get_materia.short_description = 'Materia'

    def get_classe_turma(self, obj):
        return f"{obj.classe.classe}{obj.turma.turma}"
    get_classe_turma.short_description = 'Classe/Turma'

@admin.register(HorariuExame)
class HorariuExameAdmin(admin.ModelAdmin):
    list_display = ('materia', 'loron', 'horas', 'departamentu', 'ano_academico')
    list_filter = ('loron', 'departamentu', 'materia', 'ano_academico')
    search_fields = ('materia__materia', 'materia__codigo', 'observacoes')
    ordering = ('loron__ordem', 'horas__horas_hahu', 'materia__codigo')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(HorariuValor)
class HorariuValorAdmin(admin.ModelAdmin):
    list_display = ('data_hahu', 'data_termina', 'obs')
    list_filter = ('data_hahu',)
    search_fields = ('obs',)
    ordering = ('data_hahu',)
