from django.db import models

class Agente(models.Model):
    """Modelo para agentes da GCM"""
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    lotacao = models.CharField(max_length=50)
    data_ingresso = models.DateField()
    
    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    class Meta:
        verbose_name = "Agente"
        verbose_name_plural = "Agentes"
