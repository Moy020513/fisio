from django.db import models
from historiaclinica.models import HistoriaClinica
from pacientes.models import Paciente


class TratamientoEstetico(models.Model):
    """Tratamiento estético del paciente"""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='tratamientos_esteticos')
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='tratamientos_esteticos')
    
    # Fechas
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin_planificada = models.DateField(blank=True, null=True)
    
    # Detalles del tratamiento
    objetivo_principal = models.TextField()
    zona_trabajo = models.TextField()  # Ej: "Abdomen, cintura, espalda"
    
    # Técnicas a usar
    tecnicas_descripcion = models.TextField(blank=True, null=True)
    
    # Específico para tratamientos faciales
    es_tratamiento_facial = models.BooleanField(default=False)
    usa_radiofrecuencia = models.BooleanField(default=False)
    
    activo = models.BooleanField(default=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Tratamiento Estético'
        verbose_name_plural = 'Tratamientos Estéticos'
    
    def __str__(self):
        return f"Tratamiento Estético - {self.paciente}"


class ZonaCorporal(models.Model):
    """Zonas del cuerpo a trabajar en tratamientos estéticos"""
    ZONA_CHOICES = [
        ('abdomen_alto', 'Abdomen Alto'),
        ('cintura', 'Cintura'),
        ('abdomen_bajo', 'Abdomen Bajo'),
        ('espalda_alta', 'Espalda Alta'),
        ('zona_axilar', 'Zona Axilar'),
        ('espalda_baja', 'Espalda Baja'),
        ('piernas', 'Piernas'),
        ('femur_proximal', 'Parte Proximal de Fémur'),
        ('femur_medial', 'Parte Medial Fémur'),
        ('cadera_distal', 'Parte Distal de Cadera'),
        ('cara', 'Cara/Facial'),
        ('cuello', 'Cuello'),
        ('brazos', 'Brazos'),
        ('glúteos', 'Glúteos'),
        ('otra', 'Otra Zona'),
    ]
    
    tratamiento = models.ForeignKey(TratamientoEstetico, on_delete=models.CASCADE, related_name='zonas_corporales')
    zona = models.CharField(max_length=30, choices=ZONA_CHOICES)
    descripcion_adicional = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Zona Corporal'
        verbose_name_plural = 'Zonas Corporales'
        unique_together = ['tratamiento', 'zona']
    
    def __str__(self):
        return f"{self.tratamiento.paciente} - {self.get_zona_display()}"


class MedidasZona(models.Model):
    """Medidas de la zona corporal en diferentes sesiones"""
    NUMERO_SESION_CHOICES = [
        (1, 'Sesión 1 (Inicial)'),
        (3, 'Sesión 3-4'),
        (6, 'Sesión 6-7'),
    ]
    
    zona_corporal = models.ForeignKey(ZonaCorporal, on_delete=models.CASCADE, related_name='medidas')
    numero_sesion = models.IntegerField(choices=NUMERO_SESION_CHOICES)
    
    # Medidas en centímetros
    medida_cm = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_medicion = models.DateField()
    
    # Observaciones
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Medida de Zona'
        verbose_name_plural = 'Medidas de Zona'
        unique_together = ['zona_corporal', 'numero_sesion']
        ordering = ['numero_sesion']
    
    def __str__(self):
        return f"{self.zona_corporal.tratamiento.paciente} - {self.zona_corporal.get_zona_display()} - Sesión {self.numero_sesion}"
    
    def obtener_cambio(self):
        """Calcula el cambio en medidas respecto a la sesión anterior"""
        if self.numero_sesion == 1:
            return None
        
        numero_anterior = None
        if self.numero_sesion == 3:
            numero_anterior = 1
        elif self.numero_sesion == 6:
            numero_anterior = 3
        
        if numero_anterior:
            medida_anterior = MedidasZona.objects.filter(
                zona_corporal=self.zona_corporal,
                numero_sesion=numero_anterior
            ).first()
            
            if medida_anterior:
                return self.medida_cm - medida_anterior.medida_cm
        
        return None


class EvolucionTratamientoEstetico(models.Model):
    """Evolución del tratamiento estético con resultados de las sesiones"""
    tratamiento = models.ForeignKey(TratamientoEstetico, on_delete=models.CASCADE, related_name='evoluciones')
    
    numero_sesion = models.PositiveIntegerField()
    fecha_sesion = models.DateField()
    
    # Observaciones
    cambios_visibles = models.TextField(blank=True, null=True)
    satisfaccion_paciente = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        choices=[
            ('muy_satisfecho', 'Muy Satisfecho'),
            ('satisfecho', 'Satisfecho'),
            ('neutral', 'Neutral'),
            ('insatisfecho', 'Insatisfecho'),
        ]
    )
    
    # Técnica usada en esta sesión
    tecnica_utilizada = models.TextField()
    
    # Duración de la sesión
    duracion_minutos = models.PositiveIntegerField(default=60)
    
    # Notas del terapeuta
    notas = models.TextField(blank=True, null=True)
    recomendaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['numero_sesion']
        verbose_name = 'Evolución Tratamiento Estético'
        verbose_name_plural = 'Evoluciones Tratamiento Estético'
        unique_together = ['tratamiento', 'numero_sesion']
    
    def __str__(self):
        return f"{self.tratamiento.paciente} - Sesión Estética {self.numero_sesion}"


class TecnicaTratamiento(models.Model):
    """Técnicas de tratamiento disponibles"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # Tipo de técnica
    es_radiofrecuencia = models.BooleanField(default=False)
    es_facial = models.BooleanField(default=False)
    es_masaje = models.BooleanField(default=False)
    es_crio = models.BooleanField(default=False)
    es_cavitacion = models.BooleanField(default=False)
    otra_tipo = models.CharField(max_length=200, blank=True, null=True)
    
    # Duración típica
    duracion_minutos_tipica = models.PositiveIntegerField(default=60)
    
    # Zonas recomendadas
    zonas_indicadas = models.TextField(help_text="Zonas del cuerpo donde se aplica típicamente")
    
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Técnica de Tratamiento'
        verbose_name_plural = 'Técnicas de Tratamiento'
    
    def __str__(self):
        return self.nombre


class TratamientoFacial(models.Model):
    """Información específica para tratamientos faciales"""
    tratamiento_estetico = models.OneToOneField(TratamientoEstetico, on_delete=models.CASCADE, related_name='tratamiento_facial')
    
    TIPO_PIEL_CHOICES = [
        ('normal', 'Normal'),
        ('seca', 'Seca'),
        ('grasa', 'Grasa'),
        ('mixta', 'Mixta'),
        ('sensible', 'Sensible'),
    ]
    
    tipo_piel = models.CharField(max_length=20, choices=TIPO_PIEL_CHOICES, blank=True, null=True)
    problemas_piel = models.TextField(blank=True, null=True)  # Ej: "Acné, manchas, flacidez"
    
    # Técnicas faciales específicas
    usa_radiofrecuencia_facial = models.BooleanField(default=False)
    usa_microdermoabracion = models.BooleanField(default=False)
    usa_peelings = models.BooleanField(default=False)
    
    objetivo_facial = models.TextField()  # Ej: "Rejuvenecimiento, reducción de arrugas"
    
    class Meta:
        verbose_name = 'Tratamiento Facial'
        verbose_name_plural = 'Tratamientos Faciales'
    
    def __str__(self):
        return f"Tratamiento Facial - {self.tratamiento_estetico.paciente}"


class EstadoCuenta(models.Model):
    """Estado de cuentas del tratamiento estético"""
    tratamiento = models.OneToOneField(TratamientoEstetico, on_delete=models.CASCADE, related_name='estado_cuenta')
    
    # Costo total del tratamiento
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Fecha de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Estado de Cuenta'
        verbose_name_plural = 'Estados de Cuenta'
    
    def __str__(self):
        return f"Estado de Cuenta - {self.tratamiento.paciente}"
    
    def obtener_total_pagado(self):
        """Calcula el total de anticipos pagados"""
        return sum(anticipo.monto for anticipo in self.anticipos.all())
    
    def obtener_saldo_pendiente(self):
        """Calcula el saldo pendiente"""
        return self.costo_total - self.obtener_total_pagado()


class Anticipo(models.Model):
    """Anticipos y pagos realizados para el tratamiento"""
    estado_cuenta = models.ForeignKey(EstadoCuenta, on_delete=models.CASCADE, related_name='anticipos')
    
    # Información del pago
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    
    # Detalles opcionales
    concepto = models.CharField(max_length=200, default='Anticipo', blank=True)
    notas = models.TextField(blank=True, null=True)
    
    # Control
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Anticipo'
        verbose_name_plural = 'Anticipos'
        ordering = ['fecha_pago']
    
    def __str__(self):
        return f"Anticipo ${self.monto} - {self.fecha_pago}"
