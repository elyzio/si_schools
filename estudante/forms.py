from django import forms
from .models import Estudante, EstudanteUser, EstudanteClasse, EstudanteEncarregadu, EstudanteDokumentu, EstudanteTransfer
from custom.models import Distrito, Subdistrito, Suco, Aldeia, Ano, Departamentu, Classe, Turma

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
        fields = ['departamentu', 'classe', 'turma', 'data_enrollment']
        widgets = {
            'departamentu': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'data_enrollment': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'departamentu': 'Departamentu',
            'classe': 'Klase',
            'turma': 'Turma',
            'data_enrollment': 'Data Inskrisaun',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # All fields are required
        for field in self.fields:
            self.fields[field].required = True

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
