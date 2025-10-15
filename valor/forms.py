from django import forms
from django.db import models as db_models
from .models import Valor
from custom.models import Materia, Periodo

class ValorForm(forms.ModelForm):
    class Meta:
        model = Valor
        fields = ['periodo', 'materia', 'valor', 'por_extenso', 'obs', 'data_avaliacao']
        widgets = {
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'materia': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'max': '10'
            }),
            'por_extenso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Por extenso (optional)'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações (optional)'}),
            'data_avaliacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'periodo': 'Períodu',
            'materia': 'Matéria',
            'valor': 'Valór (0-10)',
            'por_extenso': 'Valór Por Extensu',
            'obs': 'Observasaun',
            'data_avaliacao': 'Data Avaliasaun',
        }

    def __init__(self, *args, **kwargs):
        estudante_classe = kwargs.pop('estudante_classe', None)
        super().__init__(*args, **kwargs)

        # Make some fields optional
        self.fields['por_extenso'].required = False
        self.fields['obs'].required = False

        # Filter materia: Show both common subjects (no department) and department-specific subjects
        if estudante_classe:
            departamentu = estudante_classe.departamentu
            # Get common subjects (no department) OR subjects specific to this department
            available_materias = Materia.objects.filter(
                db_models.Q(departamentu__isnull=True) | db_models.Q(departamentu=departamentu)
            )

            self.fields['materia'].queryset = available_materias.order_by('codigo')
        else:
            # If no estudante_classe, show all subjects
            self.fields['materia'].queryset = Materia.objects.all().order_by('codigo')

        # Only show active periods
        self.fields['periodo'].queryset = Periodo.objects.filter(is_active=True)

        # If editing existing valor, disable period and materia fields to prevent changing the unique constraint
        if self.instance.pk:
            self.fields['periodo'].disabled = True
            self.fields['materia'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        # The unique constraint will be validated by Django automatically
        # But we can add custom validation if needed
        return cleaned_data
