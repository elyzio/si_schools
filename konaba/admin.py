from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(KonaBa)
class KonaBaAdmin(admin.ModelAdmin):
    list_display = ('titulu', 'orden', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('titulu', 'deskrisaun', 'obs')
    ordering = ('orden', 'titulu')
    list_editable = ('orden', 'is_active')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Informasaun)
class InformasaunAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipu_informasaun', 'is_published', 'data_publiku', 'get_author', 'data_kria')
    list_filter = ('tipu_informasaun', 'is_published', 'data_publiku', 'data_kria', 'author')
    search_fields = ('titulo', 'deskrisaun', 'obs')
    ordering = ('-data_publiku', 'titulo')
    list_editable = ('is_published',)
    readonly_fields = ('data_kria',)
    date_hierarchy = 'data_publiku'

    def get_author(self, obj):
        return obj.author.username if obj.author else 'No Author'
    get_author.short_description = 'Author'