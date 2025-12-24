from django import forms
from pacientes.models import Paciente, AntecedentesNoPatologicos, DatosNutricion


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombres', 'apellidos', 'fecha_nacimiento', 'edad', 'genero',
                  'telefono', 'telefono_emergencia', 'email', 'domicilio',
                  'alergias', 'grupo_sanguineo', 'rh', 'religion',
                  'tipo_paciente', 'es_frecuente']
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan',
                'required': True
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pérez',
                'required': True
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad',
                'min': 1,
                'max': 120
            }),
            'genero': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3105551234',
                'required': True
            }),
            'telefono_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3105551234'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'domicilio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Calle 10 # 5-50',
                'rows': 3,
                'required': True
            }),
            'alergias': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Penicilina, Frutos secos',
                'rows': 2
            }),
            'grupo_sanguineo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'rh': forms.Select(attrs={
                'class': 'form-select'
            }),
            'religion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Católica'
            }),
            'tipo_paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'es_frecuente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'edad': 'Edad',
            'genero': 'Género',
            'telefono': 'Teléfono',
            'telefono_emergencia': 'Teléfono de Emergencia',
            'email': 'Correo Electrónico',
            'domicilio': 'Domicilio',
            'alergias': 'Alergias',
            'grupo_sanguineo': 'Grupo Sanguíneo',
            'rh': 'RH',
            'religion': 'Religión',
            'tipo_paciente': 'Tipo de Paciente',
            'es_frecuente': 'Es Paciente Frecuente',
        }


class AntecedentesNoPatologicosForm(forms.ModelForm):
    class Meta:
        model = AntecedentesNoPatologicos
        fields = ['realiza_actividad_fisica', 'frecuencia_ejercicio', 'tipo_ejercicio',
                  'tipo_alimentacion', 'descripcion_alimentacion', 'horas_sueno',
                  'calidad_sueno', 'litros_agua_diarios', 'usa_suplementos',
                  'suplementos_descripcion']
        widgets = {
            'realiza_actividad_fisica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'frecuencia_ejercicio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo_ejercicio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe los ejercicios que realiza'
            }),
            'tipo_alimentacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion_alimentacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe la alimentación habitual'
            }),
            'horas_sueno': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '7',
                'min': 1,
                'max': 24
            }),
            'calidad_sueno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Buena, Interrumpido, Insomnio'
            }),
            'litros_agua_diarios': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2.0',
                'step': 0.5
            }),
            'usa_suplementos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'suplementos_descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describe los suplementos'
            }),
        }


class DatosNutricionForm(forms.ModelForm):
    class Meta:
        model = DatosNutricion
        fields = ['carnes', 'legumbres', 'hidratos_carbono', 'lipidos',
                  'proteinas_cantidad', 'hidratacion', 'suplementacion']
        widgets = {
            'carnes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Tipos de carnes consumidas'
            }),
            'legumbres': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Legumbres consumidas'
            }),
            'hidratos_carbono': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Hidratos de carbono'
            }),
            'lipidos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Lípidos consumidos'
            }),
            'proteinas_cantidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 100g diarios'
            }),
            'hidratacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Información de hidratación'
            }),
            'suplementacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Información de suplementación'
            }),
        }
