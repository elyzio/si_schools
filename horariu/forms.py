from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Row, Column, Field
from .models import Loron, Horas, Horariu, HorariuExame, HorariuValor

class LoronForm(forms.ModelForm):
    class Meta:
        model = Loron
        fields = ['loron']
        labels = {
            'loron': 'Loron',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'loron',
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'loron_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

class HorasForm(forms.ModelForm):
    class Meta:
        model = Horas
        fields = ['horas_hahu', 'horas_termina', 'obs']
        labels = {
            'horas_hahu': 'Oras Hahu',
            'horas_termina': 'Oras Remata',
            'obs': 'Observasaun',
        }
        widgets = {
            'horas_hahu': forms.TimeInput(attrs={'type': 'time'}),
            'horas_termina': forms.TimeInput(attrs={'type': 'time'}),
            'obs': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observasaun'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary"><i class="fas fa-clock"></i> Informasaun Oras</h5><hr>'),
            Row(
                Column('horas_hahu', css_class='form-group col-md-6 mb-0'),
                Column('horas_termina', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'obs',
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'horas_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

class HorariuForm(forms.ModelForm):
    class Meta:
        model = Horariu
        fields = ['loron', 'horas', 'classe', 'turma', 'departamentu', 'professor_materia', 'ano_academico', 'is_active', 'obs']
        labels = {
            'loron': 'Loron',
            'horas': 'Oras',
            'classe': 'Klase',
            'turma': 'Turma',
            'departamentu': 'Departamentu',
            'professor_materia': 'Profesor-Materia',
            'ano_academico': 'Tinan Akademiku',
            'is_active': 'Ativu',
            'obs': 'Observasaun',
        }
        widgets = {
            'obs': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observasaun kona ba horariu'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary"><i class="fas fa-calendar-alt"></i> Kria Horariu</h5><hr>'),
            Row(
                Column('loron', css_class='form-group col-md-4 mb-0'),
                Column('horas', css_class='form-group col-md-4 mb-0'),
                Column('ano_academico', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('departamentu', css_class='form-group col-md-4 mb-0'),
                Column('classe', css_class='form-group col-md-4 mb-0'),
                Column('turma', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('professor_materia', css_class='form-group col-md-8 mb-0'),
                Column('is_active', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'obs',
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'horariu_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

class HorariuExameForm(forms.ModelForm):
    class Meta:
        model = HorariuExame
        fields = ['loron', 'horas', 'departamentu', 'materia', 'ano_academico', 'observacoes']
        labels = {
            'loron': 'Loron',
            'horas': 'Oras',
            'departamentu': 'Departamentu',
            'materia': 'Materia',
            'ano_academico': 'Tinan Akademiku',
            'observacoes': 'Observasaun',
        }
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observasaun kona ba exame'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary"><i class="fas fa-file-alt"></i> Horariu Exame</h5><hr>'),
            Row(
                Column('loron', css_class='form-group col-md-4 mb-0'),
                Column('horas', css_class='form-group col-md-4 mb-0'),
                Column('ano_academico', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('departamentu', css_class='form-group col-md-6 mb-0'),
                Column('materia', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observacoes',
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'horariuexame_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

class HorariuValorForm(forms.ModelForm):
    class Meta:
        model = HorariuValor
        fields = ['data_hahu', 'data_termina', 'obs']
        labels = {
            'data_hahu': 'Data Hahu',
            'data_termina': 'Data Remata',
            'obs': 'Observasaun',
        }
        widgets = {
            'data_hahu': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_termina': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'obs': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observasaun'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary"><i class="fas fa-calendar-check"></i> Valor Horariu</h5><hr>'),
            Row(
                Column('data_hahu', css_class='form-group col-md-6 mb-0'),
                Column('data_termina', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'obs',
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'horariuvalor_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )