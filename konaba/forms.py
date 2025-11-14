from django import forms
from konaba.models import KonaBa, Informasaun
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django_summernote.widgets import SummernoteWidget


class KonaBaForm(forms.ModelForm):
    class Meta:
        model = KonaBa
        fields = ['titulu', 'orden', 'deskrisaun', 'obs', 'is_active']
        labels = {
            'titulu': 'Titulu',
            'orden': 'Orden',
            'deskrisaun': 'Deskrisaun',
            'obs': 'Observasaun',
            'is_active': 'Ativu'
        }

        widgets = {
            # Use Summernote for 'deskrisaun'
            'obs': SummernoteWidget(attrs={
                'summernote': {
                    'width': '800px',
                    'height': '500px',
                    'toolbar': [
                        ['style', ['bold', 'italic', 'underline', 'clear']],
                        ['font', ['strikethrough', 'superscript', 'subscript']],
                        ['fontsize', ['fontsize']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['height', ['height']],
                        ['insert', ['link', 'table', 'hr']],
                        ['view', ['fullscreen', 'codeview', 'help']],
                    ],
                }
            }),
            # Optional: keep obs as simple textarea
            # 'obs': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observasaun (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('titulu', placeholder='Titulu'),
            Field('orden', placeholder='Orden'),
            Field('deskrisaun', rows=4, placeholder='Deskrisaun'),
            Field('obs', rows=3, placeholder='Observasaun (optional)'),
            Field('is_active'),
        )


class InformasaunForm(forms.ModelForm):
    class Meta:
        model = Informasaun
        fields = ['titulo', 'deskrisaun', 'image', 'tipu_informasaun', 'data_publiku', 'obs', 'is_published']
        widgets = {
            'data_publiku': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
            'obs': SummernoteWidget(attrs={
                'summernote': {
                    'width': '800px',
                    'height': '500px',
                    'toolbar': [
                        ['style', ['bold', 'italic', 'underline', 'clear']],
                        ['font', ['strikethrough', 'superscript', 'subscript']],
                        ['fontsize', ['fontsize']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['height', ['height']],
                        ['insert', ['link', 'table', 'hr']],
                        ['view', ['fullscreen', 'codeview', 'help']],
                    ],
                }
            }),
        }
        labels = {
            'titulo': 'Titulo',
            'deskrisaun': 'Deskrisaun',
            'image': 'Imajen',
            'tipu_informasaun': 'Tipu Informasaun',
            'data_publiku': 'Data Publiku',
            'obs': 'Observasaun',
            'is_published': 'Publiku'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('titulo', placeholder='Titulo'),
            Field('tipu_informasaun'),
            Field('deskrisaun', rows=4, placeholder='Deskrisaun'),
            Field('data_publiku'),
            Field('image'),
            Field('obs', rows=3, placeholder='Observasaun (optional)'),
            Field('is_published'),
        )
