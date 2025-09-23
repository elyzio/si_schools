from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# =============================================================================
# GEOGRAPHIC AND ADMINISTRATIVE MODELS
# =============================================================================

class Distrito(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distrito"
        ordering = ['nome']

class Subdistrito(models.Model):
    nome = models.CharField(max_length=100)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, related_name='subdistritos')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome} ({self.distrito.nome})"
    
    class Meta:
        verbose_name = "Subdistrito"
        verbose_name_plural = "Subdistrito"
        ordering = ['distrito__nome', 'nome']
        unique_together = ['nome', 'distrito']

class Suco(models.Model):
    nome = models.CharField(max_length=100)
    subdistrito = models.ForeignKey(Subdistrito, on_delete=models.CASCADE, related_name='sucos')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome} ({self.subdistrito.nome})"
    
    class Meta:
        verbose_name = "Suco"
        verbose_name_plural = "Suco"
        ordering = ['subdistrito__nome', 'nome']
        unique_together = ['nome', 'subdistrito']

class Aldeia(models.Model):
    nome = models.CharField(max_length=100)
    suco = models.ForeignKey(Suco, on_delete=models.CASCADE, related_name='aldeias')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome} ({self.suco.nome})"
    
    class Meta:
        verbose_name = "Aldeia"
        verbose_name_plural = "Aldeia"
        ordering = ['suco__nome', 'nome']
        unique_together = ['nome', 'suco']

# =============================================================================
# ACADEMIC STRUCTURE MODELS
# =============================================================================

class Ano(models.Model):
    ano = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.ano}"
    
    class Meta:
        verbose_name = "Ano Akademiku"
        verbose_name_plural = "Ano Akademiku"
        ordering = ['-ano']
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one active year
            Ano.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class Departamentu(models.Model):
    departamento = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=10, null=True, blank=True, unique=True, help_text="Abbreviation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.departamento
    
    class Meta:
        verbose_name = "Departmento"
        verbose_name_plural = "Departmento"
        ordering = ['departamento']

class Classe(models.Model):
    classe = models.CharField(max_length=50, unique=True)  # e.g., "Grade 7", "Class 10A"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.classe
    
    class Meta:
        verbose_name = "Klase"
        verbose_name_plural = "Klase"
        ordering = ['classe']

class Turma(models.Model):
    turma = models.CharField(max_length=50, unique=True)  # e.g., "A", "B", "C"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.turma
    
    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turma"
        ordering = ['turma']

class Periodo(models.Model):
    PERIODO_CHOICES = [
        ('1P', 'Primeiro Periodo'),
        ('2P', 'Segundo Periodo'),
        ('3P', 'Terseiro Periodo'),
        ('SEM', 'Semester'),
        ('AN', 'Annual'),
    ]
    period = models.CharField(max_length=10, choices=PERIODO_CHOICES, unique=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.get_period_display()
    
    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodo"
        ordering = ['period']

class Materia(models.Model):
    materia = models.CharField(max_length=100)
    departamentu = models.ForeignKey(Departamentu, on_delete=models.SET_NULL, null=True, blank=True)
    codigo = models.CharField(max_length=20, unique=True, help_text="Subject code")
    descricao = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.materia}"
    
    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplina"
        ordering = ['codigo']