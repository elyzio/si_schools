from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from custom.models import Ano, Classe, Turma, Departamentu, Materia
from professor.models import ProfessorMateria

# =============================================================================
# SCHEDULE MODELS
# =============================================================================

class Loron(models.Model):
    DIAS_CHOICES = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    
    loron = models.CharField(max_length=3, choices=DIAS_CHOICES, unique=True)
    ordem = models.IntegerField(default=1, help_text="Order for sorting (1=Monday, 2=Tuesday, etc.)")
    
    def __str__(self):
        return self.get_loron_display()
    
    def save(self, *args, **kwargs):
        # Automatically set ordem based on day
        ordem_map = {
            'SEG': 1, 'TER': 2, 'QUA': 3, 'QUI': 4, 
            'SEX': 5, 'SAB': 6, 'DOM': 7
        }
        if not self.ordem:
            self.ordem = ordem_map.get(self.loron, 1)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Loron"
        verbose_name_plural = "Loron"
        ordering = ['ordem']

class Horas(models.Model):
    horas_hahu = models.TimeField(help_text="Oras Hahu")
    horas_termina = models.TimeField(help_text="Oras Termina")
    obs = models.TextField()
    # periodo_nome = models.CharField(max_length=50, help_text="Periodo (e.g., '1st Period')")
    
    def __str__(self):
        return f"{self.horas_hahu} - {self.horas_termina}"
    
    class Meta:
        verbose_name = "Oras"
        verbose_name_plural = "Oras"
        ordering = ['horas_hahu']

# Fixed Manager with correct field names
class HorariuManager(models.Manager):
    
    def current_year(self):
        """Returns only schedules for the current active academic year"""
        try:
            # Use 'Ano' model instead of 'AnoAcademico'
            current_year = Ano.objects.get(is_active=True)
            return self.filter(ano_academico=current_year, is_active=True)
        except Ano.DoesNotExist:
            return self.none()
    
    def by_class(self, classe, turma, ano_academico=None):
        """Returns schedule for a specific class and section, ordered by day and time"""
        if not ano_academico:
            try:
                ano_academico = Ano.objects.get(is_active=True)
            except Ano.DoesNotExist:
                pass
        
        queryset = self.filter(classe=classe, turma=turma, is_active=True)
        if ano_academico:
            queryset = queryset.filter(ano_academico=ano_academico)
        
        # Use correct field names: loron__ordem and horas__horas_hahu
        return queryset.order_by('loron__ordem', 'horas__horas_hahu')
    
    def by_professor(self, professor, ano_academico=None):
        """Returns schedule for a specific professor"""
        if not ano_academico:
            try:
                ano_academico = Ano.objects.get(is_active=True)
            except Ano.DoesNotExist:
                pass
        
        queryset = self.filter(professor_materia__professor=professor, is_active=True)
        if ano_academico:
            queryset = queryset.filter(ano_academico=ano_academico)
        
        return queryset.order_by('loron__ordem', 'horas__horas_hahu')
    
    def by_day(self, loron, ano_academico=None):
        """Returns all schedules for a specific day, ordered by time and class"""
        if not ano_academico:
            try:
                ano_academico = Ano.objects.get(is_active=True)
            except Ano.DoesNotExist:
                pass
        
        queryset = self.filter(loron=loron, is_active=True)
        if ano_academico:
            queryset = queryset.filter(ano_academico=ano_academico)
        
        # Order by time first, then by class (adjust 'classe__nome' based on your Classe model)
        return queryset.order_by('horas__horas_hahu', 'classe__id')  # Using id as fallback

class Horariu(models.Model):
    objects = HorariuManager()
    loron = models.ForeignKey(Loron, on_delete=models.CASCADE)
    horas = models.ForeignKey(Horas, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    departamentu = models.ForeignKey(Departamentu, on_delete=models.CASCADE)
    professor_materia = models.ForeignKey(ProfessorMateria, on_delete=models.CASCADE)
    ano_academico = models.ForeignKey(Ano, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    obs = models.TextField(blank=True, null=True, help_text="Special notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # Fixed string representation
        loron_name = self.loron.get_loron_display()
        classe_name = str(self.classe)
        turma_name = str(self.turma)
        materia_name = str(self.professor_materia.materia)
        
        return f"{loron_name} - {classe_name}{turma_name} ({materia_name})"
    
    class Meta:
        unique_together = [
            ['loron', 'horas', 'classe', 'turma'],  # One subject per time slot per class
            ['loron', 'horas', 'professor_materia'],  # Professor can't be in two places at once
        ]
        verbose_name = "Horariu"
        verbose_name_plural = "Horariu"

class HorariuExame(models.Model):
    loron = models.ForeignKey(Loron, on_delete=models.CASCADE)
    horas = models.ForeignKey(Horas, on_delete=models.CASCADE)
    departamentu = models.ForeignKey(Departamentu, on_delete=models.CASCADE, null=True, blank=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    ano_academico = models.ForeignKey(Ano, on_delete=models.CASCADE, null=True, blank=True)
    observacoes = models.TextField(blank=True, help_text="Special notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Exame: {self.materia} - {self.loron.get_loron_display()} {self.horas}"
    
    class Meta:
        unique_together = ['loron', 'horas', 'materia', 'ano_academico']
        verbose_name = "Horariu Exame"
        verbose_name_plural = "Horariu Exame"
        ordering = ['loron__ordem', 'horas__horas_hahu']

class HorariuValor(models.Model):
    data_hahu = models.DateTimeField(help_text="Start date and time")
    data_termina = models.DateTimeField(help_text="End date and time")
    obs = models.TextField(blank=True, help_text="Special notes")
    
    def __str__(self):
        return f"{self.data_hahu} - {self.data_termina}"
    
    class Meta:
        verbose_name = "Horariu Valor"
        verbose_name_plural = "Horariu Valor"
        ordering = ['data_hahu']

