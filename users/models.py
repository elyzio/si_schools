from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from custom.models import Distrito, Subdistrito, Suco, Aldeia

# =============================================================================
# PERSON BASE MODEL
# =============================================================================

class PersonInfo(models.Model):
    SEXU_CHOICES = [
        ('M', 'Mane'),
        ('F', 'Feto'),
    ]
    
    nome = models.CharField(max_length=255)
    sexu = models.CharField(max_length=1, choices=SEXU_CHOICES)
    data_moris = models.DateField()
    fatin_moris = models.CharField(max_length=255)
    nacionalidade = models.CharField(max_length=100, default='Timorense')
    
    # Address
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    subdistrito = models.ForeignKey(Subdistrito, on_delete=models.PROTECT)
    suco = models.ForeignKey(Suco, on_delete=models.PROTECT)
    aldeia = models.ForeignKey(Aldeia, on_delete=models.PROTECT)
    
    # Contact
    kontatu = models.CharField(max_length=20, blank=True)
    # email = models.EmailField(blank=True)
    hela_fatin = models.TextField(help_text="Full address")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def get_full_address(self):
        return f"{self.hela_fatin}, {self.aldeia.nome}, {self.suco.nome}, {self.subdistrito.nome}, {self.distrito.nome}"
