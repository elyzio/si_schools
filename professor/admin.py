from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('numero_funcionario', 'nome', 'estadu', 'nivel_akademiku', 'is_active', 'data_contratacao')
    list_filter = ('estadu', 'nivel_akademiku', 'is_active', 'sexu', 'data_contratacao')
    search_fields = ('nome', 'numero_funcionario', 'email', 'kontatu', 'grau_akademiku')
    ordering = ('nome',)
    list_per_page = 50

@admin.register(ProfessorUser)
class ProfessorUserAdmin(admin.ModelAdmin):
    list_display = ('get_professor_nome', 'get_professor_numero', 'get_username', 'created_at')
    search_fields = ('professor__nome', 'professor__numero_funcionario', 'user__username')
    ordering = ('professor__nome',)
    readonly_fields = ('created_at',)

    def get_professor_nome(self, obj):
        return obj.professor.nome
    get_professor_nome.short_description = 'Nome Professor'

    def get_professor_numero(self, obj):
        return obj.professor.numero_funcionario
    get_professor_numero.short_description = 'Número Funcionário'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

@admin.register(ProfessorMateria)
class ProfessorMateriaAdmin(admin.ModelAdmin):
    list_display = ('get_professor_nome', 'get_professor_numero', 'materia', 'classe', 'turma', 'is_active')
    list_filter = ('materia', 'classe', 'turma', 'is_active')
    search_fields = ('professor__nome', 'professor__numero_funcionario', 'materia__materia', 'materia__codigo')
    ordering = ('professor__nome', 'materia__codigo')

    def get_professor_nome(self, obj):
        return obj.professor.nome
    get_professor_nome.short_description = 'Nome Professor'

    def get_professor_numero(self, obj):
        return obj.professor.numero_funcionario
    get_professor_numero.short_description = 'Número Funcionário'

@admin.register(ProfessorClasse)
class ProfessorClasseAdmin(admin.ModelAdmin):
    list_display = ('get_professor_nome', 'get_professor_numero', 'ano', 'departamentu', 'classe', 'turma', 'is_class_teacher')
    list_filter = ('ano', 'departamentu', 'classe', 'turma', 'is_class_teacher')
    search_fields = ('professor__nome', 'professor__numero_funcionario')
    ordering = ('ano__ano', 'departamentu__departamento', 'classe__classe', 'turma__turma', 'professor__nome')

    def get_professor_nome(self, obj):
        return obj.professor.nome
    get_professor_nome.short_description = 'Nome Professor'

    def get_professor_numero(self, obj):
        return obj.professor.numero_funcionario
    get_professor_numero.short_description = 'Número Funcionário'

@admin.register(ProfessorDokumentu)
class ProfessorDokumentuAdmin(admin.ModelAdmin):
    list_display = ('get_professor_nome', 'get_professor_numero', 'tipo_dokumentu', 'file', 'created_at')
    list_filter = ('tipo_dokumentu', 'created_at')
    search_fields = ('professor__nome', 'professor__numero_funcionario', 'tipo_dokumentu')
    ordering = ('professor__nome', 'tipo_dokumentu')
    readonly_fields = ('created_at',)

    def get_professor_nome(self, obj):
        return obj.professor.nome
    get_professor_nome.short_description = 'Nome Professor'

    def get_professor_numero(self, obj):
        return obj.professor.numero_funcionario
    get_professor_numero.short_description = 'Número Funcionário'
