from django.contrib import admin
from .models import Ocorrencia

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    """Configuração do admin para ocorrências"""
    list_display = ('id', 'tipo', 'data_registro', 'agente_responsavel')
    list_filter = ('tipo',)
    search_fields = ('descricao', 'localizacao')
