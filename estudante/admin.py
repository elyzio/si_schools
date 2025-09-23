from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('emis', 'nome', 'numero_estudante', 'is_active', 'is_transfer', 'is_alumni', 'data_matricula')
    list_filter = ('is_active', 'is_transfer', 'is_alumni', 'sexu', 'data_matricula')
    search_fields = ('emis', 'nome', 'numero_estudante', 'kontatu')
    ordering = ('nome',)
    list_per_page = 50

@admin.register(EstudanteClasse)
class EstudanteClasseAdmin(admin.ModelAdmin):
    list_display = ('get_estudante_nome', 'get_estudante_emis', 'ano', 'departamentu', 'classe', 'turma', 'is_passa', 'data_enrollment')
    list_filter = ('ano', 'departamentu', 'classe', 'turma', 'is_passa')
    search_fields = ('estudante__nome', 'estudante__emis', 'ano__ano')
    ordering = ('ano__ano', 'departamentu__departamento', 'classe__classe', 'turma__turma', 'estudante__nome')
    list_per_page = 100
    readonly_fields = ('created_at', 'updated_at')

    def get_estudante_nome(self, obj):
        return obj.estudante.nome
    get_estudante_nome.short_description = 'Nome Estudante'

    def get_estudante_emis(self, obj):
        return obj.estudante.emis
    get_estudante_emis.short_description = 'EMIS'

@admin.register(EstudanteTransfer)
class EstudanteTransferAdmin(admin.ModelAdmin):
    list_display = ('get_estudante_nome', 'get_estudante_emis', 'from_eskola', 'ba_eskola', 'data_transfer', 'data_aseita')
    list_filter = ('data_transfer', 'data_aseita')
    search_fields = ('estudante__nome', 'estudante__emis', 'from_eskola', 'ba_eskola')
    ordering = ('-data_transfer',)
    readonly_fields = ('created_at',)

    def get_estudante_nome(self, obj):
        return obj.estudante.nome
    get_estudante_nome.short_description = 'Nome Estudante'

    def get_estudante_emis(self, obj):
        return obj.estudante.emis
    get_estudante_emis.short_description = 'EMIS'

@admin.register(EstudanteUser)
class EstudanteUserAdmin(admin.ModelAdmin):
    list_display = ('get_estudante_nome', 'get_estudante_emis', 'get_username', 'created_at')
    search_fields = ('estudante__nome', 'estudante__emis', 'user__username')
    ordering = ('estudante__nome',)
    readonly_fields = ('created_at',)

    def get_estudante_nome(self, obj):
        return obj.estudante.nome
    get_estudante_nome.short_description = 'Nome Estudante'

    def get_estudante_emis(self, obj):
        return obj.estudante.emis
    get_estudante_emis.short_description = 'EMIS'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

@admin.register(EstudanteDokumentu)
class EstudanteDokumentuAdmin(admin.ModelAdmin):
    list_display = ('get_estudante_nome', 'get_estudante_emis', 'tipo_dokumentu', 'file', 'created_at')
    list_filter = ('tipo_dokumentu', 'created_at')
    search_fields = ('estudante__nome', 'estudante__emis', 'tipo_dokumentu')
    ordering = ('estudante__nome', 'tipo_dokumentu')
    readonly_fields = ('created_at',)

    def get_estudante_nome(self, obj):
        return obj.estudante.nome
    get_estudante_nome.short_description = 'Nome Estudante'

    def get_estudante_emis(self, obj):
        return obj.estudante.emis
    get_estudante_emis.short_description = 'EMIS'
