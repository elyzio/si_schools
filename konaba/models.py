from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# =============================================================================
# CONTENT MANAGEMENT MODELS
# =============================================================================

class KonaBa(models.Model):
    titulu = models.CharField(max_length=255)
    orden = models.IntegerField(default=0, help_text="Orden")
    deskrisaun = models.TextField()
    obs = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.titulu
    
    class Meta:
        verbose_name = "Kona Ba"
        verbose_name_plural = "Kona Ba"
        ordering = ['orden', 'titulu']

class Informasaun(models.Model):
    TIPU_CHOICES = [
        ('Informasaun', 'Informasaun'),
        ('Ajenda', 'Ajenda'),
        ('Atividade', 'Atividade'),
    ]
    
    titulo = models.CharField(max_length=255)
    deskrisaun = models.TextField()
    image = models.ImageField(upload_to='informasaun/', blank=True, null=True)
    tipu_informasaun = models.CharField(max_length=20, choices=TIPU_CHOICES, default='INFORMASAUN')
    data_kria = models.DateTimeField(auto_now_add=True)
    data_publiku = models.DateTimeField()
    obs = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Informasaun"
        verbose_name_plural = "Informasaun"
        ordering = ['-data_publiku']