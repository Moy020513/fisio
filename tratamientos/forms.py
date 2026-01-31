from django import forms
from tratamientos.models import TratamientoEstetico, MedidasZona, EvolucionTratamientoEstetico, EstadoCuenta, Anticipo


class TratamientoEstaticoForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        historia_clinica = cleaned_data.get('historia_clinica')
        if paciente and historia_clinica:
            # Validar que la historia clínica pertenezca al paciente seleccionado
            if historia_clinica.paciente != paciente:
                self.add_error('historia_clinica', 'La historia clínica no pertenece al paciente seleccionado.')
            # Validar unicidad solo si ya existe un tratamiento con esa historia clínica para otro paciente
            existe = TratamientoEstetico.objects.filter(historia_clinica=historia_clinica).exclude(paciente=paciente).exists()
            if existe:
                self.add_error('historia_clinica', 'Ya existe un Tratamiento Estético con esta Historia clínica para otro paciente.')
        return cleaned_data
    # Zonas principales
    ZONA_PRINCIPAL_CHOICES = [
        ('', 'Seleccionar zona principal...'),
        ('abdomen', 'ABDOMEN'),
        ('espalda', 'ESPALDA'),
        ('pierna', 'PIERNA'),
    ]

    zona_principal = forms.ChoiceField(
        choices=ZONA_PRINCIPAL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'zona_principal',
            'onchange': 'mostrarZonasEspecificas(this.value)'
        })
    )

    # Campos para Abdomen
    abdomen_alto = forms.DecimalField(
        label='Abdomen alto (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'abdomen_alto'
        })
    )
    
    cintura = forms.DecimalField(
        label='Cintura (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'cintura'
        })
    )
    
    abdomen_bajo = forms.DecimalField(
        label='Abdomen bajo (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'abdomen_bajo'
        })
    )
    
    # Campos para Espalda
    espalda_alta = forms.DecimalField(
        label='Espalda alta (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'espalda_alta'
        })
    )
    
    zona_axilar = forms.DecimalField(
        label='Zona axilar (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'zona_axilar'
        })
    )
    
    espalda_baja = forms.DecimalField(
        label='Espalda baja (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'espalda_baja'
        })
    )
    
    # Campos para Pierna
    femur_proximal = forms.DecimalField(
        label='Parte proximal de fémur (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'femur_proximal'
        })
    )
    
    femur_medial = forms.DecimalField(
        label='Parte medial fémur (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'femur_medial'
        })
    )
    
    cadera_distal = forms.DecimalField(
        label='Parte distal de cadera (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'cadera_distal'
        })
    )
    
    # Campos para Sesión 1
    abdomen_alto_s1 = forms.DecimalField(
        label='Abdomen alto (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'abdomen_alto_s1'
        })
    )
    cintura_s1 = forms.DecimalField(
        label='Cintura (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'cintura_s1'
        })
    )
    abdomen_bajo_s1 = forms.DecimalField(
        label='Abdomen bajo (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'abdomen_bajo_s1'
        })
    )
    
    # Campos para Sesión 3-4
    abdomen_alto_s34 = forms.DecimalField(
        label='Abdomen alto (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'abdomen_alto_s34'
        })
    )
    cintura_s34 = forms.DecimalField(
        label='Cintura (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'cintura_s34'
        })
    )
    abdomen_bajo_s34 = forms.DecimalField(
        label='Abdomen bajo (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'abdomen_bajo_s34'
        })
    )
    
    # Campos para Sesión 6-7
    abdomen_alto_s67 = forms.DecimalField(
        label='Abdomen alto (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'abdomen_alto_s67'
        })
    )
    cintura_s67 = forms.DecimalField(
        label='Cintura (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'cintura_s67'
        })
    )
    abdomen_bajo_s67 = forms.DecimalField(
        label='Abdomen bajo (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'abdomen_bajo_s67'
        })
    )
    
    # Campos para Espalda Sesión 1
    espalda_alta_s1 = forms.DecimalField(
        label='Espalda alta (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'espalda_alta_s1'
        })
    )
    zona_axilar_s1 = forms.DecimalField(
        label='Zona axilar (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'zona_axilar_s1'
        })
    )
    espalda_baja_s1 = forms.DecimalField(
        label='Espalda baja (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'espalda_baja_s1'
        })
    )
    
    # Campos para Espalda Sesión 3-4
    espalda_alta_s34 = forms.DecimalField(
        label='Espalda alta (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'espalda_alta_s34'
        })
    )
    zona_axilar_s34 = forms.DecimalField(
        label='Zona axilar (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'zona_axilar_s34'
        })
    )
    espalda_baja_s34 = forms.DecimalField(
        label='Espalda baja (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'espalda_baja_s34'
        })
    )
    
    # Campos para Espalda Sesión 6-7
    espalda_alta_s67 = forms.DecimalField(
        label='Espalda alta (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'espalda_alta_s67'
        })
    )
    zona_axilar_s67 = forms.DecimalField(
        label='Zona axilar (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'zona_axilar_s67'
        })
    )
    espalda_baja_s67 = forms.DecimalField(
        label='Espalda baja (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'espalda_baja_s67'
        })
    )
    
    # Campos para Pierna Sesión 1
    femur_proximal_s1 = forms.DecimalField(
        label='Parte proximal de fémur (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'femur_proximal_s1'
        })
    )
    femur_medial_s1 = forms.DecimalField(
        label='Parte medial fémur (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'femur_medial_s1'
        })
    )
    cadera_distal_s1 = forms.DecimalField(
        label='Parte distal de cadera (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'cadera_distal_s1'
        })
    )
    
    # Campos para Pierna Sesión 3-4
    femur_proximal_s34 = forms.DecimalField(
        label='Parte proximal de fémur (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'femur_proximal_s34'
        })
    )
    femur_medial_s34 = forms.DecimalField(
        label='Parte medial fémur (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'femur_medial_s34'
        })
    )
    cadera_distal_s34 = forms.DecimalField(
        label='Parte distal de cadera (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'cadera_distal_s34'
        })
    )
    
    # Campos para Pierna Sesión 6-7
    femur_proximal_s67 = forms.DecimalField(
        label='Parte proximal de fémur (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'femur_proximal_s67'
        })
    )
    femur_medial_s67 = forms.DecimalField(
        label='Parte medial fémur (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'femur_medial_s67'
        })
    )
    cadera_distal_s67 = forms.DecimalField(
        label='Parte distal de cadera (cm)',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Medida en cm',
            'id': 'cadera_distal_s67'
        })
    )
    
    class Meta:
        model = TratamientoEstetico
        fields = ['paciente', 'historia_clinica',
                  'zona_trabajo', 'tecnicas_descripcion',
                  'es_tratamiento_facial', 'activo']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'historia_clinica': forms.Select(attrs={
                'class': 'form-select',
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
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'checked': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si es una edición (instance existe), cargar las medidas existentes
        if self.instance and self.instance.pk:
            tratamiento = self.instance
            zonas = tratamiento.zonas_corporales.all()
            
            # Detectar la zona principal basándose en las zonas existentes
            zonas_keys = [zona.zona for zona in zonas]
            if any(z in ['abdomen_alto', 'cintura', 'abdomen_bajo'] for z in zonas_keys):
                self.fields['zona_principal'].initial = 'abdomen'
            elif any(z in ['espalda_alta', 'zona_axilar', 'espalda_baja'] for z in zonas_keys):
                self.fields['zona_principal'].initial = 'espalda'
            elif any(z in ['femur_proximal', 'femur_medial', 'cadera_distal'] for z in zonas_keys):
                self.fields['zona_principal'].initial = 'pierna'
            
            for zona in zonas:
                zona_key = zona.zona
                for medida in zona.medidas.all():
                    sesion = medida.numero_sesion
                    if sesion == 1:
                        sufijo = '_s1'
                    elif sesion == 3:
                        sufijo = '_s34'
                    elif sesion == 6:
                        sufijo = '_s67'
                    else:
                        continue
                    
                    field_name = f"{zona_key}{sufijo}"
                    if field_name in self.fields:
                        self.fields[field_name].initial = float(medida.medida_cm)


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


class EstadoCuentaForm(forms.ModelForm):
    """Formulario para Estado de Cuenta"""
    
    class Meta:
        model = EstadoCuenta
        fields = ['costo_total']
        widgets = {
            'costo_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Costo total del tratamiento'
            }),
        }
        labels = {
            'costo_total': 'Costo Total del Tratamiento'
        }


class AnticipoForm(forms.ModelForm):
    """Formulario para registrar anticipos"""
    
    class Meta:
        model = Anticipo
        fields = ['monto', 'fecha_pago', 'concepto', 'notas']
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'fecha_pago': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Anticipo'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas adicionales (opcional)'
            }),
        }
        labels = {
            'monto': 'Monto del Anticipo',
            'fecha_pago': 'Fecha de Pago',
            'concepto': 'Concepto',
            'notas': 'Notas'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_pago'].input_formats = ['%Y-%m-%d']

