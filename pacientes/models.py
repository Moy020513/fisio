from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Choices para selecciones
GENERO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro'),
]

GRUPO_SANGUINEO_CHOICES = [
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]

RH_CHOICES = [
    ('+', 'Positivo'),
    ('-', 'Negativo'),
]

TIPO_PACIENTE_CHOICES = [
    ('consulta_unica', 'Consulta Única (Masajes Relajantes)'),
    ('patologia', 'Patologías (Tratamiento Completo)'),
    ('estetico', 'Masajes Reductivos (Tratamientos Estéticos)'),
]

FRECUENCIA_EJERCICIO_CHOICES = [
    ('no', 'No realiza'),
    ('ocasional', 'Ocasional'),
    ('regular', '3-4 veces por semana'),
    ('intenso', 'Diario o casi diario'),
]

TIPO_DIETA_CHOICES = [
    ('omnivora', 'Omnívora'),
    ('vegetariana', 'Vegetariana'),
    ('vegana', 'Vegana'),
    ('cetogenica', 'Cetogénica'),
    ('mediterranea', 'Mediterránea'),
    ('otra', 'Otra'),
]

ESCALA_EVA_CHOICES = [(str(i), str(i)) for i in range(0, 11)]

class Paciente(models.Model):
    """Modelo principal de Paciente"""
    # Información básica
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    
    # Información de contacto
    telefono = models.CharField(max_length=20)
    telefono_emergencia = models.CharField(max_length=20, blank=True, null=True)
    domicilio = models.TextField()
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    
    # Información médica
    alergias = models.TextField(blank=True, null=True)
    grupo_sanguineo = models.CharField(max_length=3, choices=GRUPO_SANGUINEO_CHOICES, blank=True, null=True)
    rh = models.CharField(max_length=1, choices=RH_CHOICES, blank=True, null=True)
    religion = models.CharField(max_length=100, blank=True, null=True)
    
    # Tipo de paciente
    tipo_paciente = models.CharField(max_length=20, choices=TIPO_PACIENTE_CHOICES)
    es_frecuente = models.BooleanField(default=False)
    
    # Auditoría
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def nombre_completo(self):
        """Nombre y apellidos combinados para vistas y plantillas."""
        return f"{self.nombres} {self.apellidos}".strip()


class EstudiosClinico(models.Model):
    """Estudios clínicos del paciente"""
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='estudios_clinicos')
    
    # Estudios de imagen
    radiografias = models.FileField(upload_to='estudios/radiografias/', blank=True, null=True)
    resonancias = models.FileField(upload_to='estudios/resonancias/', blank=True, null=True)
    tomografia = models.FileField(upload_to='estudios/tomografia/', blank=True, null=True)
    ecografia = models.FileField(upload_to='estudios/ecografia/', blank=True, null=True)
    otros_estudios = models.FileField(upload_to='estudios/otros/', blank=True, null=True)
    descripcion_otros = models.TextField(blank=True, null=True)
    
    # Análisis sanguíneos
    analisis_sanguineos = models.FileField(upload_to='estudios/analisis_sanguineos/', blank=True, null=True)
    examen_general_orina = models.FileField(upload_to='estudios/examen_orina/', blank=True, null=True)
    perfil_hormonal = models.FileField(upload_to='estudios/perfil_hormonal/', blank=True, null=True)
    
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Estudio Clínico'
        verbose_name_plural = 'Estudios Clínicos'
    
    def __str__(self):
        return f"Estudios de {self.paciente}"


class AntecedentePatologico(models.Model):
    """Antecedentes patológicos personales y familiares"""
    TIPO_ANTECEDENTE_CHOICES = [
        ('personal', 'Personal'),
        ('familiar', 'Familiar de Primer Grado'),
    ]
    
    TIPO_PATOLOGIA_CHOICES = [
        ('hipertension', 'Hipertensión'),
        ('diabetes', 'Diabetes'),
        ('cancer', 'Cáncer'),
        ('trigliceridos', 'Triglicéridos Altos'),
        ('obesidad', 'Obesidad'),
        ('tiroides', 'Tiroides'),
        ('sop', 'SOP (Síndrome Ovario Poliquístico)'),
        ('menopausia', 'Menopausia'),
        ('otro', 'Otro'),
    ]
    
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='antecedentes_patologicos')
    
    # Antecedentes generales
    hipertension = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    cancer = models.BooleanField(default=False)
    trigliceridos = models.BooleanField(default=False)
    obesidad = models.BooleanField(default=False)
    tiroides = models.BooleanField(default=False)
    
    # Antecedentes específicos por género (se mostrarán según género)
    sop = models.BooleanField(default=False)  # SOP en mujeres
    menopausia = models.BooleanField(default=False)  # Menopausia en mujeres
    fecha_ultima_menstruacion = models.DateField(blank=True, null=True)  # Mujeres
    probabilidad_embarazo = models.BooleanField(default=False)  # Mujeres
    numero_partos = models.PositiveIntegerField(default=0)  # Mujeres
    
    # Cirugías
    cirugias = models.TextField(blank=True, null=True, help_text="Descripción de cirugías realizadas")
    
    # Notas adicionales
    notas = models.TextField(blank=True, null=True)
    
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Antecedente Patológico'
        verbose_name_plural = 'Antecedentes Patológicos'
    
    def __str__(self):
        return f"Antecedentes patológicos - {self.paciente}"


class AntecedentesNoPatologicos(models.Model):
    """Antecedentes no patológicos"""
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='antecedentes_no_patologicos')
    
    # Diagnóstico y Pronóstico
    diagnostico = models.TextField(blank=True, null=True)
    pronostico = models.TextField(blank=True, null=True)
    
    # Actividad física
    realiza_actividad_fisica = models.BooleanField(default=False)
    frecuencia_ejercicio = models.CharField(max_length=20, choices=FRECUENCIA_EJERCICIO_CHOICES, blank=True, null=True)
    tipo_ejercicio = models.TextField(blank=True, null=True)
    
    # Alimentación general
    tipo_alimentacion = models.CharField(max_length=20, choices=TIPO_DIETA_CHOICES, blank=True, null=True)
    regimen_alimenticio = models.TextField(blank=True, null=True)
    
    # Detalles nutricionales
    carnes = models.TextField(blank=True, null=True, help_text="Tipos de carnes consumidas")
    legumbres = models.TextField(blank=True, null=True, help_text="Legumbres consumidas")
    hidratos_carbono = models.TextField(blank=True, null=True)
    lipidos = models.TextField(blank=True, null=True)
    proteinas = models.TextField(blank=True, null=True)
    
    # Dieta con notas
    dieta = models.TextField(blank=True, null=True)
    notas_dieta = models.TextField(blank=True, null=True, help_text="Notas adicionales sobre la dieta")
    
    # Hidratación
    hidratacion = models.CharField(max_length=100, blank=True, null=True)
    litros_agua_diarios = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    
    # Sueño
    horas_sueno = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(24)])
    calidad_sueno = models.CharField(max_length=50, blank=True, null=True)
    
    # Suplementación
    suplementacion = models.TextField(blank=True, null=True)
    
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Antecedentes No Patológicos'
        verbose_name_plural = 'Antecedentes No Patológicos'
    
    def __str__(self):
        return f"Antecedentes no patológicos - {self.paciente}"


class DatosNutricion(models.Model):
    """Detalles nutricionales del paciente - Deprecated: Utilizar antecedentes_no_patologicos en su lugar"""
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='datos_nutricion')
    
    # Macronutrientes
    carnes = models.TextField(blank=True, null=True, help_text="Tipos de carnes consumidas")
    legumbres = models.TextField(blank=True, null=True, help_text="Legumbres consumidas")
    hidratos_carbono = models.TextField(blank=True, null=True)
    lipidos = models.TextField(blank=True, null=True)
    proteinas_cantidad = models.CharField(max_length=100, blank=True, null=True)
    
    # Hidratación
    hidratacion = models.TextField(blank=True, null=True)
    
    # Suplementación nutricional
    suplementacion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Datos de Nutrición'
        verbose_name_plural = 'Datos de Nutrición'
    
    def __str__(self):
        return f"Nutrición - {self.paciente}"
