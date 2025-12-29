from django import forms
from datetime import date
from pacientes.models import Paciente, AntecedentesNoPatologicos, DatosNutricion, AntecedentePatologico


class PacienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar formato compatible con input type="date" al editar
        if self.instance and self.instance.pk and self.instance.fecha_nacimiento:
            self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')
        # Asegurar formatos de entrada válidos
        self.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d']

    class Meta:
        model = Paciente
        fields = ['nombres', 'apellidos', 'fecha_nacimiento', 'edad', 'genero',
                  'telefono', 'telefono_emergencia', 'domicilio',
                  'alergias', 'grupo_sanguineo', 'religion',
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
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'required': True
                },
                format='%Y-%m-%d'
            ),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad',
                'min': 1,
                'max': 120,
                'readonly': 'readonly'
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
            'domicilio': 'Domicilio',
            'alergias': 'Alergias',
            'grupo_sanguineo': 'Grupo Sanguíneo',
            'religion': 'Religión',
            'tipo_paciente': 'Tipo de Paciente',
            'es_frecuente': 'Es Paciente Frecuente',
        }

    def clean(self):
        cleaned = super().clean()
        dob = cleaned.get('fecha_nacimiento')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            # Validación de rango razonable
            if age < 0 or age > 120:
                self.add_error('fecha_nacimiento', 'Fecha de nacimiento inválida.')
            else:
                cleaned['edad'] = age
        return cleaned


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

class AntecedentePatologicoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar fecha en formato YYYY-MM-DD si existe
        if self.instance and self.instance.pk and self.instance.fecha_ultima_menstruacion:
            self.fields['fecha_ultima_menstruacion'].initial = self.instance.fecha_ultima_menstruacion.strftime('%Y-%m-%d')
        # Asegurar formato de entrada
        self.fields['fecha_ultima_menstruacion'].input_formats = ['%Y-%m-%d']

        # Campos exclusivos para pacientes femeninas: al ser Masculino se marcan como no requeridos
        femeninos = [
            'sop',
            'menopausia',
            'probabilidad_embarazo',
            'fecha_ultima_menstruacion',
            'numero_partos',
        ]
        if self.instance and self.instance.pk:
            es_femenino = getattr(self.instance.paciente, 'genero', None) == 'F'
            for campo in femeninos:
                self.fields[campo].required = False
            if not es_femenino:
                # Para hombres, limpiar valores sensibles en la instancia visual
                self.initial.update({
                    'sop': False,
                    'menopausia': False,
                    'probabilidad_embarazo': False,
                    'fecha_ultima_menstruacion': None,
                    'numero_partos': 0,
                })

    class Meta:
        model = AntecedentePatologico
        fields = ['hipertension', 'diabetes', 'cancer', 'trigliceridos', 'obesidad', 'tiroides',
                  'sop', 'menopausia', 'fecha_ultima_menstruacion', 'probabilidad_embarazo',
                  'numero_partos', 'cirugias', 'notas']
        widgets = {
            'hipertension': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cancer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'trigliceridos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obesidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiroides': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sop': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'menopausia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_ultima_menstruacion': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),
            'probabilidad_embarazo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numero_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'cirugias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de cirugías realizadas'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas adicionales'
            }),
        }
        labels = {
            'hipertension': 'Hipertensión',
            'diabetes': 'Diabetes',
            'cancer': 'Cáncer',
            'trigliceridos': 'Triglicéridos Altos',
            'obesidad': 'Obesidad',
            'tiroides': 'Tiroides',
            'sop': 'SOP (Síndrome Ovario Poliquístico)',
            'menopausia': 'Menopausia',
            'fecha_ultima_menstruacion': 'Fecha de última menstruación',
            'probabilidad_embarazo': 'Probabilidad de Embarazo',
            'numero_partos': 'Número de Partos',
            'cirugias': 'Cirugías',
            'notas': 'Notas adicionales',
        }

    def clean(self):
        cleaned = super().clean()
        # Si el paciente no es femenino, limpiar todos los campos ginecológicos
        paciente = getattr(self.instance, 'paciente', None)
        es_femenino = paciente and paciente.genero == 'F'
        if not es_femenino:
            cleaned['sop'] = False
            cleaned['menopausia'] = False
            cleaned['probabilidad_embarazo'] = False
            cleaned['fecha_ultima_menstruacion'] = None
            cleaned['numero_partos'] = cleaned.get('numero_partos') or 0
        else:
            # Normalizar número de partos a 0 si viene vacío
            cleaned['numero_partos'] = cleaned.get('numero_partos') or 0
        return cleaned


class AntecedentesNoPatologicosForm(forms.ModelForm):
    class Meta:
        model = AntecedentesNoPatologicos
        fields = ['diagnostico', 'pronostico', 'realiza_actividad_fisica', 'frecuencia_ejercicio', 
              'tipo_ejercicio', 'tipo_alimentacion', 'regimen_alimenticio', 'carnes', 'legumbres',
                  'hidratos_carbono', 'lipidos', 'proteinas', 'dieta', 'hidratacion',
                  'horas_sueno', 'calidad_sueno', 'suplementacion']
        widgets = {
            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Diagnóstico'
            }),
            'pronostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Pronóstico'
            }),
            'realiza_actividad_fisica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'frecuencia_ejercicio': forms.Select(attrs={'class': 'form-select'}),
            'tipo_ejercicio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Tipo de ejercicio'
            }),
            'tipo_alimentacion': forms.Select(attrs={'class': 'form-select'}),
            'regimen_alimenticio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Régimen alimenticio'
            }),
            'carnes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Tipos de carnes'
            }),
            'legumbres': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Legumbres'
            }),
            'hidratos_carbono': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Hidratos de carbono'
            }),
            'lipidos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Lípidos'
            }),
            'proteinas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Proteínas'
            }),
            'dieta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la dieta'
            }),
            'hidratacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2-3 litros diarios'
            }),
            'horas_sueno': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 24
            }),
            'calidad_sueno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Buena, Regular, Mala'
            }),
            'suplementacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Suplementación'
            }),
        }
        labels = {
            'diagnostico': 'Diagnóstico',
            'pronostico': 'Pronóstico',
            'realiza_actividad_fisica': 'Realiza Actividad Física',
            'frecuencia_ejercicio': 'Frecuencia de Ejercicio',
            'tipo_ejercicio': 'Tipo de Ejercicio',
            'tipo_alimentacion': 'Tipo de Alimentación',
            'regimen_alimenticio': 'Régimen Alimenticio',
            'carnes': 'Carnes',
            'legumbres': 'Legumbres',
            'hidratos_carbono': 'Hidratos de Carbono',
            'lipidos': 'Lípidos',
            'proteinas': 'Proteínas',
            'dieta': 'Dieta',
            'notas_dieta': 'Notas de Dieta',
            'hidratacion': 'Hidratación',
            'litros_agua_diarios': 'Litros de Agua Diarios',
            'horas_sueno': 'Horas de Sueño',
            'calidad_sueno': 'Calidad del Sueño',
            'suplementacion': 'Suplementación',
        }