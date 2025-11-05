from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, HTML, Div, Field
from crispy_forms.bootstrap import InlineRadios
from .models import Estudante, EstudanteUser, EstudanteClasse, EstudanteEncarregadu, EstudanteDokumentu, EstudanteTransfer
from custom.models import Distrito, Subdistrito, Suco, Aldeia, Ano, Departamentu, Classe, Turma
from django.utils import timezone

class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = [
            'emis', 'numero_estudante', 'nome', 'sexu', 'data_moris', 'fatin_moris',
            'nacionalidade', 'distrito', 'subdistrito', 'suco', 'aldeia',
            'kontatu', 'hela_fatin', 'data_matricula', 'imagem', 'is_active'
        ]
        widgets = {
            'emis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMIS Number'}),
            'numero_estudante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Number'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'sexu': forms.Select(attrs={'class': 'form-control'}),
            'data_moris': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fatin_moris': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Birth Place'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nationality'}),
            'distrito': forms.Select(attrs={'class': 'form-control'}),
            'subdistrito': forms.Select(attrs={'class': 'form-control'}),
            'suco': forms.Select(attrs={'class': 'form-control'}),
            'aldeia': forms.Select(attrs={'class': 'form-control'}),
            'kontatu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'hela_fatin': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'data_matricula': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Handle dependent dropdowns
        # First, check if this is a POST request with data (form submission)
        if self.data:
            # Form was submitted, preserve the dependent field options based on submitted data
            try:
                distrito_id = self.data.get('distrito')
                if distrito_id:
                    self.fields['subdistrito'].queryset = Subdistrito.objects.filter(distrito_id=distrito_id).order_by('nome')
                else:
                    self.fields['subdistrito'].queryset = Subdistrito.objects.none()

                subdistrito_id = self.data.get('subdistrito')
                if subdistrito_id:
                    self.fields['suco'].queryset = Suco.objects.filter(subdistrito_id=subdistrito_id).order_by('nome')
                else:
                    self.fields['suco'].queryset = Suco.objects.none()

                suco_id = self.data.get('suco')
                if suco_id:
                    self.fields['aldeia'].queryset = Aldeia.objects.filter(suco_id=suco_id).order_by('nome')
                else:
                    self.fields['aldeia'].queryset = Aldeia.objects.none()
            except (ValueError, TypeError):
                # If there's an error with the IDs, set empty querysets
                self.fields['subdistrito'].queryset = Subdistrito.objects.none()
                self.fields['suco'].queryset = Suco.objects.none()
                self.fields['aldeia'].queryset = Aldeia.objects.none()

        elif self.instance and self.instance.pk:
            # This is an edit form - populate dependent fields based on existing data
            if self.instance.distrito:
                self.fields['subdistrito'].queryset = Subdistrito.objects.filter(distrito=self.instance.distrito)
            else:
                self.fields['subdistrito'].queryset = Subdistrito.objects.none()

            if self.instance.subdistrito:
                self.fields['suco'].queryset = Suco.objects.filter(subdistrito=self.instance.subdistrito)
            else:
                self.fields['suco'].queryset = Suco.objects.none()

            if self.instance.suco:
                self.fields['aldeia'].queryset = Aldeia.objects.filter(suco=self.instance.suco)
            else:
                self.fields['aldeia'].queryset = Aldeia.objects.none()
        else:
            # This is a new form - start with empty querysets for dependent fields
            self.fields['subdistrito'].queryset = Subdistrito.objects.none()
            self.fields['suco'].queryset = Suco.objects.none()
            self.fields['aldeia'].queryset = Aldeia.objects.none()

        # Set default values
        self.fields['nacionalidade'].initial = 'Timorense'

        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Informasaun Estudante',
                Row(
                    Column(
                        Field('emis', placeholder='EMIS Number'),
                        HTML('<small class="text-muted">Sei uza hanesan username</small>'),
                        css_class='col-md-6'
                    ),
                    Column('numero_estudante', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Informasaun Pesoál',
                Row(
                    Column('nome', css_class='col-md-12'),
                ),
                Row(
                    Column('sexu', css_class='col-md-4'),
                    Column('data_moris', css_class='col-md-4'),
                    Column('fatin_moris', css_class='col-md-4'),
                ),
                Row(
                    Column('nacionalidade', css_class='col-md-6'),
                    Column('kontatu', css_class='col-md-6'),
                ),
            ),
            Fieldset(
                'Informasaun Enderesu',
                Row(
                    Column('distrito', css_class='col-md-3'),
                    Column('subdistrito', css_class='col-md-3'),
                    Column('suco', css_class='col-md-3'),
                    Column('aldeia', css_class='col-md-3'),
                ),
                Row(
                    Column('hela_fatin', css_class='col-md-12'),
                ),
            ),
            Fieldset(
                'Informasaun Matríkula',
                Row(
                    Column('data_matricula', css_class='col-md-6'),
                    Column('imagem', css_class='col-md-6'),
                ),
                Row(
                    Column(
                        Field('is_active', wrapper_class='form-check'),
                        css_class='col-md-12'
                    ),
                ),
            ),
            HTML('<div class="form-group mt-4"><button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Rai</button> <a href="{% url \'estudante_list\' %}" class="btn btn-secondary"><i class="fas fa-times"></i> Kansela</a></div>'),
        )

    def clean(self):
        cleaned_data = super().clean()
        distrito = cleaned_data.get('distrito')
        subdistrito = cleaned_data.get('subdistrito')
        suco = cleaned_data.get('suco')
        aldeia = cleaned_data.get('aldeia')

        # Validate address hierarchy
        if subdistrito and distrito:
            if subdistrito.distrito != distrito:
                self.add_error('subdistrito', 'O subdistrito selecionado não pertence ao distrito escolhido.')

        if suco and subdistrito:
            if suco.subdistrito != subdistrito:
                self.add_error('suco', 'O suco selecionado não pertence ao subdistrito escolhido.')

        if aldeia and suco:
            if aldeia.suco != suco:
                self.add_error('aldeia', 'A aldeia selecionada não pertence ao suco escolhido.')

        return cleaned_data

class EstudanteClasseForm(forms.ModelForm):
    class Meta:
        model = EstudanteClasse
        fields = ['departamentu', 'classe', 'turma', 'data_enrollment', 'is_mid_year_transfer', 'starting_period']
        widgets = {
            'departamentu': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'data_enrollment': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_mid_year_transfer': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_is_mid_year_transfer'}),
            'starting_period': forms.Select(attrs={'class': 'form-control'}, choices=[(1, 'Período 1'), (2, 'Período 2'), (3, 'Período 3')]),
        }
        labels = {
            'departamentu': 'Departamentu',
            'classe': 'Klase',
            'turma': 'Turma',
            'data_enrollment': 'Data Inskrisaun',
            'is_mid_year_transfer': 'Estudante Transfere iha Klaran Tinan?',
            'starting_period': 'Hahu husi Período',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Basic fields are required
        for field in ['departamentu', 'classe', 'turma', 'data_enrollment']:
            self.fields[field].required = True

        # Transfer fields are optional
        self.fields['is_mid_year_transfer'].required = False
        self.fields['starting_period'].required = False

        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('departamentu', css_class='col-md-4'),
                Column('classe', css_class='col-md-4'),
                Column('turma', css_class='col-md-4'),
            ),
            Row(
                Column('data_enrollment', css_class='col-md-12'),
            ),
            HTML('<hr>'),
            HTML('<h5><i class="fas fa-exchange-alt"></i> Informasaun Transfere (Opsionál)</h5>'),
            HTML('''
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    <strong>Nota:</strong> Se estudante ne\'e transfere iha klaran tinan akadémiku, favor seluk "Estudante Transfere iha Klaran Tinan?" no atu determina períodu ne\'ebé estudante hahu.
                </div>
            '''),
            Row(
                Column(
                    Field('is_mid_year_transfer', wrapper_class='form-check'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('starting_period', css_id='id_starting_period'),
                    HTML('<small class="form-text text-muted" id="periodHelp">Períodu ne\'ebé estudante hahu iha eskola ne\'e</small>'),
                    css_class='col-md-6',
                    css_id='startingPeriodGroup'
                ),
            ),
            HTML('''
                <script>
                    $(document).ready(function() {
                        // Toggle starting_period visibility based on is_mid_year_transfer
                        function togglePeriodField() {
                            if ($('#id_is_mid_year_transfer').is(':checked')) {
                                $('#startingPeriodGroup').show();
                                $('#id_starting_period').prop('disabled', false);
                            } else {
                                $('#startingPeriodGroup').hide();
                                $('#id_starting_period').val('1');
                                $('#id_starting_period').prop('disabled', true);
                            }
                        }

                        // Initial state
                        togglePeriodField();

                        // On change
                        $('#id_is_mid_year_transfer').change(function() {
                            togglePeriodField();
                        });
                    });
                </script>
            '''),
            HTML('<div class="form-group mt-4"><button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Rai</button> <a href="{% url \'estudante_detail\' estudante.pk %}" class="btn btn-secondary"><i class="fas fa-times"></i> Kansela</a></div>'),
        )

class EstudanteEncarregaduForm(forms.ModelForm):
    class Meta:
        model = EstudanteEncarregadu
        fields = ['encarregadu', 'no_kontatu', 'email', 'relasaun', 'is_primary']
        widgets = {
            'encarregadu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naran Kompletu Encaregadu'}),
            'no_kontatu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+670 7777 7777'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'relasaun': forms.Select(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'encarregadu': 'Naran Encaregadu Edukasaun',
            'no_kontatu': 'Núm. Kontatu',
            'email': 'Email',
            'relasaun': 'Relasaun',
            'is_primary': 'Encaregadu Prinsipál?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Email is optional
        self.fields['email'].required = False

        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('encarregadu', css_class='col-md-6'),
                Column('relasaun', css_class='col-md-6'),
            ),
            Row(
                Column('no_kontatu', css_class='col-md-6'),
                Column(
                    Field('email', placeholder='email@example.com (Opsionál)'),
                    css_class='col-md-6'
                ),
            ),
            Row(
                Column(
                    Field('is_primary', wrapper_class='form-check'),
                    HTML('<small class="form-text text-muted">Seluk ida-ne\'e se encaregadu ne\'e maka encaregadu prinsipál.</small>'),
                    css_class='col-md-12'
                ),
            ),
            HTML('<div class="form-group mt-4"><button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Rai</button> <a href="{% url \'estudante_detail\' estudante.pk %}" class="btn btn-secondary"><i class="fas fa-times"></i> Kansela</a></div>'),
        )

class EstudanteDokumentuForm(forms.ModelForm):
    class Meta:
        model = EstudanteDokumentu
        fields = ['tipo_dokumentu', 'file', 'obs']
        widgets = {
            'tipo_dokumentu': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Nota kona-ba dokumentu (opsionál)'}),
        }
        labels = {
            'tipo_dokumentu': 'Tipu Dokumentu',
            'file': 'Dokumentu (PDF)',
            'obs': 'Observasaun',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obs is optional
        self.fields['obs'].required = False

        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('tipo_dokumentu', css_class='col-md-6'),
                Column(
                    Field('file', accept='application/pdf'),
                    HTML('<small class="form-text text-muted">Favor upload file PDF deit. Tamañu maksimum: 10MB</small>'),
                    css_class='col-md-6'
                ),
            ),
            Row(
                Column(
                    Field('obs', placeholder='Nota kona-ba dokumentu (opsionál)'),
                    css_class='col-md-12'
                ),
            ),
            HTML('<div class="form-group mt-4"><button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Rai</button> <a href="{% url \'estudante_detail\' estudante.pk %}" class="btn btn-secondary"><i class="fas fa-times"></i> Kansela</a></div>'),
        )

class EstudanteTransferForm(forms.ModelForm):
    TRANSFER_TYPE_CHOICES = [
        ('OUT', 'Sai husi Eskola Ne\'e'),
        ('IN', 'Tama husi Eskola Seluk'),
    ]

    transfer_type = forms.ChoiceField(
        choices=TRANSFER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Tipu Transferénsia'
    )

    class Meta:
        model = EstudanteTransfer
        fields = ['transfer_type', 'from_eskola', 'ba_eskola', 'data_transfer', 'data_aseita', 'obs']
        widgets = {
            'from_eskola': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naran Eskola Anterior'}),
            'ba_eskola': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naran Eskola Destinasaun'}),
            'data_transfer': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_aseita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observasaun (opsionál)'}),
        }
        labels = {
            'from_eskola': 'Husi Eskola',
            'ba_eskola': 'Ba Eskola',
            'data_transfer': 'Data Transfere',
            'data_aseita': 'Data Simu (ba estudante tama)',
            'obs': 'Observasaun',
        }

    def __init__(self, *args, **kwargs):
        self.current_school = kwargs.pop('current_school', 'Eskola Ne\'e')
        super().__init__(*args, **kwargs)

        # Set initial transfer type based on instance
        if self.instance and self.instance.pk:
            # Determine transfer type from existing data
            if self.instance.from_eskola == self.current_school:
                self.initial['transfer_type'] = 'OUT'
            else:
                self.initial['transfer_type'] = 'IN'

        # Obs and data_aseita are optional
        self.fields['obs'].required = False
        self.fields['data_aseita'].required = False

        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'transferForm'
        self.helper.layout = Layout(
            Fieldset(
                '',
                InlineRadios('transfer_type'),
                HTML('''
                    <small class="form-text text-muted">
                        <strong>SAI:</strong> Estudante transfere SAI husi eskola ne\'e ba eskola seluk<br>
                        <strong>TAMA:</strong> Estudante TAMA husi eskola seluk ba eskola ne\'e
                    </small>
                '''),
            ),
            HTML('<hr>'),
            Row(
                Column(
                    Field('from_eskola', css_id='id_from_eskola'),
                    HTML('<small class="form-text text-muted" id="fromEskolaHelp"></small>'),
                    css_class='col-md-6',
                    css_id='fromEskolaGroup'
                ),
                Column(
                    Field('ba_eskola', css_id='id_ba_eskola'),
                    HTML('<small class="form-text text-muted" id="baEskolaHelp"></small>'),
                    css_class='col-md-6',
                    css_id='baEskolaGroup'
                ),
            ),
            Row(
                Column('data_transfer', css_class='col-md-6'),
                Column(
                    Field('data_aseita'),
                    HTML('<small class="form-text text-muted">Deit ba estudante TAMA</small>'),
                    css_class='col-md-6',
                    css_id='dataAseitaGroup'
                ),
            ),
            Row(
                Column(
                    Field('obs', placeholder='Observasaun (opsionál)'),
                    css_class='col-md-12'
                ),
            ),
            HTML('''
                <div class="alert alert-default-warning">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>Nota importante:</strong>
                    <ul class="mb-0 mt-2">
                        <li>Se ita seluk <strong>SAI</strong>, estudante sei marka hanesan "transfere" no SEI LA hatudu iha lista estudante ativu.</li>
                        <li>Se ita seluk <strong>TAMA</strong>, estudante sei kontinua ativu iha lista estudante.</li>
                        <li>Ita bele hamoos transferénsia depois atu ativa estudante fali se presiza.</li>
                    </ul>
                </div>
            '''),
            HTML('<div class="form-group mt-4"><button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Rai</button> <a href="{% url \'estudante_detail\' estudante.pk %}" class="btn btn-secondary"><i class="fas fa-times"></i> Kansela</a></div>'),
        )

    def clean(self):
        cleaned_data = super().clean()
        transfer_type = cleaned_data.get('transfer_type')
        from_eskola = cleaned_data.get('from_eskola')
        ba_eskola = cleaned_data.get('ba_eskola')

        # Auto-fill school names based on transfer type
        if transfer_type == 'OUT':
            cleaned_data['from_eskola'] = self.current_school
            if not ba_eskola:
                self.add_error('ba_eskola', 'Favor hatama naran eskola destinasaun.')
        elif transfer_type == 'IN':
            cleaned_data['ba_eskola'] = self.current_school
            if not from_eskola:
                self.add_error('from_eskola', 'Favor hatama naran eskola anterior.')

        return cleaned_data


class EstudanteReassignForm(forms.ModelForm):
    """Form for reassigning student to next grade/year"""

    class Meta:
        model = EstudanteClasse
        fields = ['departamentu', 'classe', 'turma', 'data_enrollment']
        widgets = {
            'departamentu': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'data_enrollment': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'departamentu': 'Departamentu',
            'classe': 'Klase Foun',
            'turma': 'Turma',
            'data_enrollment': 'Data Inskrisaun',
        }

    def __init__(self, *args, **kwargs):
        self.next_grade_name = kwargs.pop('next_grade_name', None)
        self.current_estudante_classe = kwargs.pop('current_estudante_classe', None)
        self.back_url_name = kwargs.pop('back_url_name', 'estudante_list')
        super().__init__(*args, **kwargs)

        # Pre-select next grade if available
        if self.next_grade_name:
            try:
                next_classe = Classe.objects.get(classe=self.next_grade_name)
                self.fields['classe'].initial = next_classe
                self.fields['classe'].widget.attrs['readonly'] = True
            except Classe.DoesNotExist:
                pass

        # Pre-fill department and turma from current assignment
        if self.current_estudante_classe:
            self.fields['departamentu'].initial = self.current_estudante_classe.departamentu
            self.fields['turma'].initial = self.current_estudante_classe.turma

        # Set default enrollment date to today
        self.fields['data_enrollment'].initial = timezone.now().date()

        # All fields are required
        for field in self.fields:
            self.fields[field].required = True

        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('departamentu', css_class='col-md-4'),
                Column('classe', css_class='col-md-4'),
                Column('turma', css_class='col-md-4'),
            ),
            Row(
                Column('data_enrollment', css_class='col-md-12'),
            ),
            HTML(f'''
                <div class="form-group mt-4">
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-check"></i> Konfirma Reasignasaun
                    </button>
                    <a href="{{% url '{self.back_url_name}' %}}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Kansela
                    </a>
                </div>
            '''),
        )
