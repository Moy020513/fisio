from django import forms
from historiaclinica.models import HistoriaClinica, EjercioTerapeutico, EvolucionTratamiento, EstudioClinico


class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['paciente', 'diagnostico', 'pronostico', 'tratamiento_planificado',
                  'notas_arcos_movimiento', 'escala_eva', 'activo']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Diagnóstico del paciente',
                'required': True
            }),
            'pronostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Pronóstico esperado'
            }),
            'tratamiento_planificado': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del tratamiento planificado',
                'required': True
            }),
            'notas_arcos_movimiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas sobre arcos de movimiento'
            }),
            'escala_eva': forms.Select(attrs={
                'class': 'form-select'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'checked': True
            }),
        }
        labels = {
            'paciente': 'Paciente',
            'diagnostico': 'Diagnóstico',
            'pronostico': 'Pronóstico',
            'tratamiento_planificado': 'Tratamiento Planificado',
            'notas_arcos_movimiento': 'Notas de Arcos de Movimiento',
            'escala_eva': 'Escala EVA (0-10)',
            'activo': 'Activo',
        }


class EjercioTerapeuticoForm(forms.ModelForm):
    class Meta:
        model = EjercioTerapeutico
        fields = ['historia', 'nombre_ejercicio', 'descripcion', 'series',
                  'repeticiones', 'duracion_segundos', 'frecuencia',
                  'es_ejercicio_casa', 'dias_semana', 'notas']
        widgets = {
            'historia': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'nombre_ejercicio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del ejercicio',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada del ejercicio',
                'required': True
            }),
            'series': forms.NumberInput(attrs={
                'class': 'form-control',
                'value': 3,
                'min': 1
            }),
            'repeticiones': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 10-15',
                'required': True
            }),
            'duracion_segundos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duración en segundos (opcional)'
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 3 veces por semana'
            }),
            'es_ejercicio_casa': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'checked': True
            }),
            'dias_semana': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lunes, Miércoles, Viernes'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas adicionales'
            }),
        }


class EvolucionTratamientoForm(forms.ModelForm):
    class Meta:
        model = EvolucionTratamiento
        fields = ['historia', 'fecha_sesion', 'numero_sesion', 'escala_eva_sesion',
                  'notas_sesion', 'progreso', 'cambios_detectados',
                  'notas_arcos_actual', 'recomendaciones']
        widgets = {
            'historia': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_sesion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'numero_sesion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de sesión',
                'min': 1,
                'required': True
            }),
            'escala_eva_sesion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notas_sesion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas de la sesión',
                'required': True
            }),
            'progreso': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describe el progreso del paciente'
            }),
            'cambios_detectados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Cambios detectados en esta sesión'
            }),
            'notas_arcos_actual': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas de arcos de movimiento actuales'
            }),
            'recomendaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Recomendaciones para la próxima sesión'
            }),
        }


class EstudioClinicoForm(forms.ModelForm):
    class Meta:
        model = EstudioClinico
        # 'historia' se asigna en la vista; no debe estar en el formulario
        fields = ['tipo', 'fecha_estudio', 'descripcion', 'resultado', 'archivo']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_estudio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del estudio (opcional)'
            }),
            'resultado': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Resultados o hallazgos (opcional)'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'tipo': 'Tipo de estudio',
            'fecha_estudio': 'Fecha del estudio',
            'descripcion': 'Descripción',
            'resultado': 'Resultado',
            'archivo': 'Archivo adjunto',
        }
