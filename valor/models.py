from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from custom.models import Materia, Ano, Periodo
from estudante.models import EstudanteClasse

# =============================================================================
# GRADING MODELS
# =============================================================================

class Valor(models.Model):
    estudante_classe = models.ForeignKey(EstudanteClasse, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)])
    por_extenso = models.CharField(max_length=100, blank=True, help_text="Valor Por Extensu")
    obs = models.TextField(blank=True)
    data_avaliacao = models.DateField(default=timezone.now)
    is_lock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.estudante_classe.estudante.nome} - {self.materia.materia}: {self.valor}"
    
    class Meta:
        unique_together = ['estudante_classe', 'periodo', 'materia']
        verbose_name = "Valor"
        verbose_name_plural = "Valores"

# Will use maybe
class Klassifikasaun(models.Model):
    estudante_classe = models.ForeignKey(EstudanteClasse, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    # classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    # turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    # departamentu = models.ForeignKey(Departamentu, on_delete=models.CASCADE)
    classificasaun_turma = models.IntegerField(help_text="Rank Iha Turma")
    classificasaun_departamentu = models.IntegerField(help_text="Rank iha Departamentu")
    classificasaun_geral = models.IntegerField(help_text="Rank em geral")
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE)
    media_geral = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.estudante_classe.estudante.nome} - Rank: {self.classificasaun_geral}"
    
    class Meta:
        unique_together = ['estudante_classe', 'periodo', 'ano']
        verbose_name = "Klassifikasaun Estudante"
        verbose_name_plural = "Klassifikasaun Estudante"
