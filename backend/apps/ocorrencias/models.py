from django.db import models
from backend.apps.pessoal.models import Agente

class Ocorrencia(models.Model):
    """Modelo para registro de ocorrências policiais"""
    TIPOS_CRIME = [
        ('1456', 'Roubo de Veículo'),  # Código alinhado ao INFOCRIM
        ('7890', 'Porte Ilegal de Arma'),
        ('3456', 'Violência Doméstica'),
    ]
    
    tipo = models.CharField(max_length=4, choices=TIPOS_CRIME)
    data_registro = models.DateTimeField(auto_now_add=True)
    localizacao = models.CharField(max_length=100)
    agente_responsavel = models.ForeignKey(Agente, on_delete=models.PROTECT)
    descricao = models.TextField()
    fotos = models.JSONField(default=list)
    
    def __str__(self):
        return f"Ocorrência {self.id} - {self.get_tipo_display()}"

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
