from django.db import models
from pacientes.models import Paciente
from django.core.validators import MinValueValidator, MaxValueValidator

class HistoriaClinica(models.Model):
    """Historia clínica del paciente con diagnóstico y tratamiento"""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historias_clinicas')
    
    # Evaluación
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Diagnóstico
    diagnostico = models.TextField()
    pronostico = models.TextField(blank=True, null=True)
    
    # Tratamiento principal
    tratamiento_planificado = models.TextField()
    
    # Arcos de movimiento
    notas_arcos_movimiento = models.TextField(blank=True, null=True)
    
    # Escalas
    escala_eva = models.CharField(
        max_length=2, 
        choices=[(str(i), str(i)) for i in range(0, 11)],
        blank=True,
        null=True,
        help_text="Escala de Dolor EVA (0-10)"
    )
    
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_evaluacion']
        verbose_name = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'
    
    def __str__(self):
        return f"Historia - {self.paciente} ({self.fecha_evaluacion.date()})"


class ArcosMovimiento(models.Model):
    """Registro detallado de arcos de movimiento"""
    historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='arcos_movimiento')
    
    articulation = models.CharField(max_length=100)  # Ej: "Cadera izquierda", "Rodilla derecha"
    flexion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    extension = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    abduccion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    adduccion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rotacion_interna = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rotacion_externa = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Arco de Movimiento'
        verbose_name_plural = 'Arcos de Movimiento'
    
    def __str__(self):
        return f"{self.historia.paciente} - {self.articulation}"


class PruebaFuncional(models.Model):
    """Pruebas funcionales específicas"""
    historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='pruebas_funcionales')
    
    tipo_prueba = models.CharField(max_length=200)  # Ej: "Test Lachman", "Test de Trendelenburg"
    resultado = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Prueba Funcional'
        verbose_name_plural = 'Pruebas Funcionales'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.historia.paciente} - {self.tipo_prueba}"


class EscalaDaniels(models.Model):
    """Escala de Daniels para evaluación muscular"""
    GRADO_CHOICES = [
        ('0', '0 - Parálisis'),
        ('1', '1 - Contracción visible/palpable sin movimiento'),
        ('2', '2 - Movimiento con eliminación de gravedad'),
        ('3', '3 - Movimiento contra gravedad'),
        ('4', '4 - Movimiento contra resistencia moderada'),
        ('5', '5 - Fuerza normal'),
    ]
    
    historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='escala_daniels')
    
    musculo = models.CharField(max_length=200)  # Ej: "Deltoides derecho"
    grado = models.CharField(max_length=1, choices=GRADO_CHOICES)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Escala de Daniels'
        verbose_name_plural = 'Escala de Daniels'
    
    def __str__(self):
        return f"{self.historia.paciente} - {self.musculo}: {self.grado}"


class EjercioTerapeutico(models.Model):
    """Ejercicios terapéuticos prescritos"""
    historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='ejercicios_terapeuticos')
    
    nombre_ejercicio = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # Dosificación
    series = models.PositiveIntegerField(default=3)
    repeticiones = models.CharField(max_length=50)  # Ej: "10-15"
    duracion_segundos = models.PositiveIntegerField(blank=True, null=True)
    frecuencia = models.CharField(max_length=100)  # Ej: "3 veces por semana"
    
    # Ejercicios para casa
    es_ejercicio_casa = models.BooleanField(default=True)
    dias_semana = models.CharField(max_length=100, blank=True, null=True)  # Ej: "Lunes, Miércoles, Viernes"
    
    notas = models.TextField(blank=True, null=True)
    fecha_prescripcion = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Ejercicio Terapéutico'
        verbose_name_plural = 'Ejercicios Terapéuticos'
    
    def __str__(self):
        return f"{self.historia.paciente} - {self.nombre_ejercicio}"


class EvolucionTratamiento(models.Model):
    """Seguimiento de la evolución del tratamiento"""
    historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='evoluciones')
    
    fecha_sesion = models.DateField()
    numero_sesion = models.PositiveIntegerField()
    
    # Evaluación en la sesión
    escala_eva_sesion = models.CharField(
        max_length=2,
        choices=[(str(i), str(i)) for i in range(0, 11)],
        blank=True,
        null=True,
        help_text="EVA al inicio de la sesión"
    )
    
    # Observaciones
    notas_sesion = models.TextField()
    progreso = models.TextField(blank=True, null=True)
    cambios_detectados = models.TextField(blank=True, null=True)
    
    # Arcos de movimiento en esta sesión
    notas_arcos_actual = models.TextField(blank=True, null=True)
    
    # Próximos pasos
    recomendaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_sesion']
        verbose_name = 'Evolución de Tratamiento'
        verbose_name_plural = 'Evoluciones de Tratamiento'
        unique_together = ['historia', 'numero_sesion']
    
    def __str__(self):
        return f"{self.historia.paciente} - Sesión {self.numero_sesion}"


class GraficoEvolucion(models.Model):
    """Datos para graficar la evolución del paciente"""
    historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='graficos_evolucion')
    
    fecha = models.DateField()
    numero_sesion = models.PositiveIntegerField()
    
    # Valores a graficar
    escala_eva = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    arcos_movimiento_grados = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fuerza_muscular = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    
    class Meta:
        ordering = ['fecha']
        verbose_name = 'Gráfico de Evolución'
        verbose_name_plural = 'Gráficos de Evolución'
    
    def __str__(self):
        return f"{self.historia.paciente} - {self.fecha}"


class EstudioClinico(models.Model):
    """Estudios clínicos asociados a una historia clínica"""
    TIPO_CHOICES = [
        ('radiografia', 'Radiografía'),
        ('resonancia', 'Resonancia'),
        ('tomografia', 'Tomografía'),
        ('ecografia', 'Ecografía'),
        ('analisis_sanguineos', 'Análisis sanguíneos'),
        ('examen_orina', 'Examen general de orina'),
        ('perfil_hormonal', 'Perfil hormonal'),
        ('otros', 'Otros'),
    ]

    historia = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='estudios_clinicos')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    fecha_estudio = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    resultado = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='estudios/', blank=True, null=True)

    class Meta:
        ordering = ['-fecha_estudio']
        verbose_name = 'Estudio clínico'
        verbose_name_plural = 'Estudios clínicos'

    def __str__(self):
        return f"{self.historia.paciente} - {self.get_tipo_display()} ({self.fecha_estudio})"
