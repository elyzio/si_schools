from django.contrib import admin
from custom.models import *

# Register your models here.

@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)

@admin.register(Subdistrito)
class SubdistritoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'distrito')
    list_filter = ('distrito',)
    search_fields = ('nome', 'distrito__nome')
    ordering = ('distrito__nome', 'nome')

@admin.register(Suco)
class SucoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'subdistrito', 'get_distrito')
    list_filter = ('subdistrito__distrito', 'subdistrito')
    search_fields = ('nome', 'subdistrito__nome', 'subdistrito__distrito__nome')
    ordering = ('subdistrito__distrito__nome', 'subdistrito__nome', 'nome')

    def get_distrito(self, obj):
        return obj.subdistrito.distrito.nome
    get_distrito.short_description = 'Distrito'

@admin.register(Aldeia)
class AldeiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'suco', 'get_subdistrito', 'get_distrito')
    list_filter = ('suco__subdistrito__distrito', 'suco__subdistrito', 'suco')
    search_fields = ('nome', 'suco__nome', 'suco__subdistrito__nome', 'suco__subdistrito__distrito__nome')
    ordering = ('suco__subdistrito__distrito__nome', 'suco__subdistrito__nome', 'suco__nome', 'nome')

    def get_subdistrito(self, obj):
        return obj.suco.subdistrito.nome
    get_subdistrito.short_description = 'Subdistrito'

    def get_distrito(self, obj):
        return obj.suco.subdistrito.distrito.nome
    get_distrito.short_description = 'Distrito'

@admin.register(Ano)
class AnoAdmin(admin.ModelAdmin):
    list_display = ('ano', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('ano',)
    ordering = ('-ano',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Departamentu)
class DepartamentuAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'created_at')
    search_fields = ('departamento',)
    ordering = ('departamento',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('classe', 'created_at')
    search_fields = ('classe',)
    ordering = ('classe',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('turma', 'created_at')
    search_fields = ('turma',)
    ordering = ('turma',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'materia', 'departamentu', 'created_at')
    list_filter = ('departamentu',)
    search_fields = ('codigo', 'materia', 'departamentu__departamento', 'descricao')
    ordering = ('codigo',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('period', 'is_active', 'created_at')
    list_filter = ('is_active', 'period')
    search_fields = ('period',)
    ordering = ('period',)
    readonly_fields = ('created_at', 'updated_at')

