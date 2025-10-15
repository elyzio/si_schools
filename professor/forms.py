from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Row, Column, Field
from crispy_forms.bootstrap import TabHolder, Tab, PrependedText, AppendedText
from .models import Professor, ProfessorClasse, ProfessorUser, ProfessorMateria, ProfessorDokumentu
from custom.models import Distrito, Subdistrito, Suco, Aldeia, Ano, Departamentu, Classe, Turma, Materia

class ProfessorForm(forms.ModelForm):
    # Personal Information
    # nome = forms.CharField(
    #     max_length=255,
    #     widget=forms.TextInput(attrs={'placeholder': 'Nome completo'}),
    #     label='Nome Completo'
    # )


    class Meta:
        model = Professor
        fields = [
            # Personal Information
            'nome', 'sexu', 'data_moris', 'fatin_moris', 'nacionalidade', 'estadu_civil',
            # Address
            'distrito', 'subdistrito', 'suco', 'aldeia', 'hela_fatin', 'kontatu',
            # Professional Information
            'numero_funcionario', 'estadu', 'data_contratacao', 'nivel_akademiku',
            'grau_akademiku', 'email', 'imagem'
        ]

        widgets = {
            'data_moris': forms.DateInput(attrs={'type': 'date'}),
            'data_contratacao': forms.DateInput(attrs={'type': 'date'}),
            'hela_fatin': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Endereço completo'}),
            'grau_akademiku': forms.TextInput(attrs={'placeholder': 'Ex: Licenciatura em Matemática'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@exemplo.com'}),
            'kontatu': forms.TextInput(attrs={'placeholder': '+670 1234 5678'}),
            'numero_funcionario': forms.TextInput(attrs={'placeholder': 'Número de funcionário'}),
            'fatin_moris': forms.TextInput(attrs={'placeholder': 'Local de nascimento'}),
        }

        labels = {
            'nome': 'Nome Completo',
            'sexu': 'Sexo',
            'data_moris': 'Data de Nascimento',
            'fatin_moris': 'Local de Nascimento',
            'nacionalidade': 'Nacionalidade',
            'estadu_civil': 'Estado Civil',
            'distrito': 'Distrito',
            'subdistrito': 'Subdistrito',
            'suco': 'Suco',
            'aldeia': 'Aldeia',
            'hela_fatin': 'Endereço Completo',
            'kontatu': 'Telefone/Contato',
            'numero_funcionario': 'Número de Funcionário',
            'estadu': 'Estado',
            'data_contratacao': 'Data de Contratação',
            'nivel_akademiku': 'Nível Acadêmico',
            'grau_akademiku': 'Grau Acadêmico',
            'email': 'Email',
            'imagem': 'Foto',
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

        # Set required fields
        required_fields = ['nome', 'sexu', 'data_moris', 'distrito', 'subdistrito', 'suco', 'aldeia', 'estadu', 'nivel_akademiku']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

        # Set default values
        self.fields['nacionalidade'].initial = 'Timorense'


        # Setup crispy forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'

        self.helper.layout = Layout(
            HTML('<h5 class="text-primary"><i class="fas fa-user"></i> Informações Pessoais</h5><hr>'),
            Row(
                Column('nome', css_class='form-group col-md-6 mb-0'),
                Column('sexu', css_class='form-group col-md-3 mb-0'),
                Column('data_moris', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fatin_moris', css_class='form-group col-md-6 mb-0'),
                Column('nacionalidade', css_class='form-group col-md-3 mb-0'),
                Column('estadu_civil', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('kontatu', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('imagem', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),

            HTML('<h5 class="text-primary mt-4"><i class="fas fa-map-marker-alt"></i> Informações de Endereço</h5><hr>'),
            Row(
                Column('distrito', css_class='form-group col-md-3 mb-0'),
                Column('subdistrito', css_class='form-group col-md-3 mb-0'),
                Column('suco', css_class='form-group col-md-3 mb-0'),
                Column('aldeia', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('hela_fatin', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),

            HTML('<h5 class="text-primary mt-4"><i class="fas fa-graduation-cap"></i> Informações Profissionais</h5><hr>'),
            Row(
                Column('numero_funcionario', css_class='form-group col-md-4 mb-0'),
                Column('estadu', css_class='form-group col-md-4 mb-0'),
                Column('data_contratacao', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nivel_akademiku', css_class='form-group col-md-6 mb-0'),
                Column('grau_akademiku', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Salvar Professor', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'professor_list\' %}" class="btn btn-secondary ml-2">Cancelar</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email is already used by another user
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Este email já está em uso por outro usuário.')
        return email

    def clean_numero_funcionario(self):
        numero = self.cleaned_data.get('numero_funcionario')
        if numero:
            # Check if employee number is already used
            existing_professor = Professor.objects.filter(numero_funcionario=numero)
            if self.instance and self.instance.pk:
                existing_professor = existing_professor.exclude(pk=self.instance.pk)
            if existing_professor.exists():
                raise forms.ValidationError('Este número de funcionário já está em uso.')
        return numero

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

class ProfessorUserForm(forms.ModelForm):
    class Meta:
        model = ProfessorUser
        fields = ['professor', 'user']
        labels = {
            'professor': 'Profesor',
            'user': 'Uzuariu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'professor',
            'user',
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'professoruser_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

class ProfessorClasseForm(forms.ModelForm):
    class Meta:
        model = ProfessorClasse
        fields = ['professor', 'ano', 'departamentu', 'classe', 'is_class_teacher']
        labels = {
            'professor': 'Profesor',
            'ano': 'Tinan',
            'departamentu': 'Departamentu',
            'classe': 'Klase',
            'is_class_teacher': 'Profesor Prinsipal Klase Nian',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary"><i class="fas fa-chalkboard-teacher"></i> Atribui Profesor ba Klase</h5><hr>'),
            Row(
                Column('professor', css_class='form-group col-md-6 mb-0'),
                Column('ano', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('departamentu', css_class='form-group col-md-6 mb-0'),
                Column('classe', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'is_class_teacher',
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'professorclasse_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

class ProfessorMateriaForm(forms.ModelForm):
    class Meta:
        model = ProfessorMateria
        fields = ['professor', 'materia', 'classe', 'is_active']
        labels = {
            'professor': 'Profesor',
            'materia': 'Materia',
            'classe': 'Klase',
            'is_active': 'Ativu',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary"><i class="fas fa-book"></i> Atribui Materia ba Profesor</h5><hr>'),
            Row(
                Column('professor', css_class='form-group col-md-6 mb-0'),
                Column('materia', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('classe', css_class='form-group col-md-6 mb-0'),
                Column('is_active', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'professormateria_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

class ProfessorDokumentuForm(forms.ModelForm):
    class Meta:
        model = ProfessorDokumentu
        fields = ['professor', 'tipo_dokumentu', 'file', 'obs']
        labels = {
            'professor': 'Profesor',
            'tipo_dokumentu': 'Tipu Dokumentu',
            'file': 'Dokumentu (PDF)',
            'obs': 'Observasaun',
        }
        widgets = {
            'obs': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observasaun kona ba dokumentu'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h5 class="text-primary"><i class="fas fa-file-pdf"></i> Dokumentu Profesor Nian</h5><hr>'),
            'professor',
            Row(
                Column('tipo_dokumentu', css_class='form-group col-md-6 mb-0'),
                Column('file', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'obs',
            HTML('<hr>'),
            Row(
                Column(
                    Submit('submit', 'Rai', css_class='btn btn-primary'),
                    HTML('<a href="{% url \'professordokumentu_list\' %}" class="btn btn-secondary ml-2">Kansela</a>'),
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            )
        )

