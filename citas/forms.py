from django import forms
from django.utils import timezone
from citas.models import Cita, Terapeuta


class CitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].required = False
        self.fields['paciente'].empty_label = 'Sin paciente'
        # Mostrar valor existente en formato compatible con datetime-local
        if self.instance and self.instance.pk and self.instance.fecha_hora:
            local_dt = timezone.localtime(self.instance.fecha_hora)
            self.fields['fecha_hora'].initial = local_dt.strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Cita
        fields = ['paciente', 'terapeuta', 'fecha_hora', 'duracion_minutos',
                  'tipo_sesion', 'estado', 'motivo_cita', 'notas_adicionales']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'terapeuta': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_hora': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'required': True
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'duracion_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': 60,
                'min': 15,
                'step': 15
            }),
            'tipo_sesion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'motivo_cita': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Motivo de la cita'
            }),
            'notas_adicionales': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales'
            }),
        }
        labels = {
            'paciente': 'Paciente',
            'terapeuta': 'Terapeuta',
            'fecha_hora': 'Fecha y Hora',
            'duracion_minutos': 'Duración (minutos)',
            'tipo_sesion': 'Tipo de Sesión',
            'estado': 'Estado',
            'motivo_cita': 'Motivo de la Cita',
            'notas_adicionales': 'Notas Adicionales',
        }

        input_formats = {
            'fecha_hora': ['%Y-%m-%dT%H:%M'],
        }


class TerapeutaForm(forms.ModelForm):
    class Meta:
        model = Terapeuta
        fields = ['nombres', 'apellidos', 'email', 'telefono',
                  'especialidades', 'activo']
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del terapeuta',
                'required': True
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del terapeuta',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3105551234',
                'required': True
            }),
            'especialidades': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Masajes relajantes, Fisioterapia deportiva',
                'required': True
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'checked': True
            }),
        }
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'especialidades': 'Especialidades',
            'activo': 'Activo',
        }
