from django.db import models
from django.utils import timezone
from datetime import timedelta
from pacientes.models import Paciente


class CitasProximasManager(models.Manager):
    """Manager personalizado para filtrar citas próximas (próximos 7 días)"""
    def get_queryset(self):
        ahora = timezone.now()
        proxima_semana = ahora + timedelta(days=7)
        return super().get_queryset().filter(
            fecha_hora__gt=ahora,
            fecha_hora__lte=proxima_semana,
            estado__in=['disponible', 'ocupada']
        )


class Terapeuta(models.Model):
    """Terapeutas disponibles"""
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    especialidades = models.TextField()  # Ej: "Masajes relajantes, Fisioterapia deportiva"
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Terapeuta'
        verbose_name_plural = 'Terapeutas'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def nombre_completo(self):
        """Nombre y apellidos combinados para usar en vistas y plantillas."""
        return f"{self.nombres} {self.apellidos}".strip()


class Cita(models.Model):
    """Gestión de citas y agenda"""
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    
    TIPO_SESION_CHOICES = [
        ('sesion_regular', 'Sesión Regular'),
        ('sesion_estetica', 'Sesión Estética'),
        ('seguimiento', 'Seguimiento'),
        ('evaluacion', 'Evaluación Inicial'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    terapeuta = models.ForeignKey(Terapeuta, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Fecha y hora
    fecha_hora = models.DateTimeField()
    duracion_minutos = models.PositiveIntegerField(default=60)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    tipo_sesion = models.CharField(max_length=20, choices=TIPO_SESION_CHOICES)
    
    # Notas
    motivo_cita = models.TextField(blank=True, null=True)
    notas_adicionales = models.TextField(blank=True, null=True)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['fecha_hora']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        unique_together = ['terapeuta', 'fecha_hora']  # No puede haber 2 citas del mismo terapeuta a la misma hora
    
    def __str__(self):
        return f"{self.paciente} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
    
    def get_hora_fin(self):
        """Calcula la hora de finalización de la cita"""
        return self.fecha_hora + timedelta(minutes=self.duracion_minutos)
    
    def esta_proxima(self):
        """Verifica si la cita está próxima (dentro de 7 días)"""
        ahora = timezone.now()
        proxima_semana = ahora + timedelta(days=7)
        return ahora <= self.fecha_hora <= proxima_semana


class AgendaDisponibilidad(models.Model):
    """Horarios disponibles para citas"""
    terapeuta = models.ForeignKey(Terapeuta, on_delete=models.CASCADE, related_name='disponibilidades')
    
    DIA_SEMANA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    dia_semana = models.IntegerField(choices=DIA_SEMANA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Disponibilidad de Agenda'
        verbose_name_plural = 'Disponibilidades de Agenda'
        unique_together = ['terapeuta', 'dia_semana', 'hora_inicio']
    
    def __str__(self):
        return f"{self.terapeuta} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"


class CitasProximas(Cita):
    """Proxy de Cita para filtrar citas próximas (próximos 7 días)"""
    
    objects = CitasProximasManager()
    
    class Meta:
        verbose_name = 'Cita Próxima'
        verbose_name_plural = 'Citas Próximas'
        proxy = True  # Usamos proxy para filtrar de manera automática
    
    def __str__(self):
        return str(f"{self.paciente} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}")
