from django import forms
from tratamientos.models import TratamientoEstetico, MedidasZona, EvolucionTratamientoEstetico


class TratamientoEstaticoForm(forms.ModelForm):
    class Meta:
        model = TratamientoEstetico
        fields = ['paciente', 'historia_clinica', 'fecha_fin_planificada',
                  'objetivo_principal', 'zona_trabajo', 'tecnicas_descripcion',
                  'es_tratamiento_facial', 'usa_radiofrecuencia', 'activo']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'historia_clinica': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_fin_planificada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'objetivo_principal': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Objetivo principal del tratamiento',
                'required': True
            }),
            'zona_trabajo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Zonas de trabajo'
            }),
            'tecnicas_descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de técnicas a usar'
            }),
            'es_tratamiento_facial': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'usa_radiofrecuencia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'checked': True
            }),
        }


class MedidasZonaForm(forms.ModelForm):
    class Meta:
        model = MedidasZona
        fields = ['zona_corporal', 'numero_sesion', 'medida_cm', 'fecha_medicion', 'notas']
        widgets = {
            'zona_corporal': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'numero_sesion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'medida_cm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Medida en cm',
                'step': 0.1,
                'required': True
            }),
            'fecha_medicion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas sobre la medición'
            }),
        }


class EvolucionTratamientoEstaticoForm(forms.ModelForm):
    class Meta:
        model = EvolucionTratamientoEstetico
        fields = ['tratamiento', 'numero_sesion', 'fecha_sesion', 'cambios_visibles',
                  'satisfaccion_paciente', 'tecnica_utilizada', 'duracion_minutos',
                  'notas', 'recomendaciones']
        widgets = {
            'tratamiento': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'numero_sesion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de sesión',
                'min': 1,
                'required': True
            }),
            'fecha_sesion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'cambios_visibles': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Cambios visibles en el paciente'
            }),
            'satisfaccion_paciente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tecnica_utilizada': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Técnica utilizada en esta sesión',
                'required': True
            }),
            'duracion_minutos': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': 60,
                'min': 15
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas del terapeuta'
            }),
            'recomendaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Recomendaciones para la próxima sesión'
            }),
        }
