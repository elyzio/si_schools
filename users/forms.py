from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _
from estudante.models import Estudante
from custom.models import Distrito, Subdistrito, Suco, Aldeia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column, HTML, Field


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            HTML(""" <div class="row"> """),
            Column(Field('old_password', css_class='form-control'), css_class="col"),
            HTML(""" </div> """),
            HTML(""" <div class="row mt-2"> """),
            Column(Field('new_password1', css_class='form-control'), css_class="col"),
            HTML(""" </div> """),
            HTML(""" <div class="row mt-2"> """),
            Column(Field('new_password2', css_class='form-control'), css_class="col"),
            HTML(""" </div> """),
            # Submit('submit', 'Change Password', css_class='btn btn-primary mt-2')
        )

class EstudanteProfileForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = [
            'emis', 'numero_estudante', 'nome', 'sexu', 'data_moris', 'fatin_moris',
            'nacionalidade', 'distrito', 'subdistrito', 'suco', 'aldeia',
            'kontatu', 'hela_fatin', 'imagem'
        ]
        widgets = {
            'emis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMIS Number', 'disabled': 'disabled'}),
            'numero_estudante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Number', 'disabled': 'disabled'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'disabled': 'disabled'}),
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
            # 'data_matricula': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            # 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
                        css_class='col-md-6 form-disable'
                    ),
                    Column('numero_estudante', css_class='col-md-6 form-disable'),
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
                'Informasaun Seluk',
                Row(
                    Column('imagem', css_class='col-md-6'),
                ),
            ),
            HTML('<div class="form-group mt-4"><button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Rai</button> <a href="{% url \'user_profile\' %}" class="btn btn-secondary"><i class="fas fa-times"></i> Kansela</a></div>'),
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