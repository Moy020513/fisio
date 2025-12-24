from django.contrib import admin
from .models import Terapeuta, Cita, AgendaDisponibilidad, CitasProximas
from django.utils import timezone
from datetime import timedelta


class AgendaDisponibilidadInline(admin.TabularInline):
    model = AgendaDisponibilidad
    extra = 1


@admin.register(Terapeuta)
class TerapeutaAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'email', 'telefono', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombres', 'apellidos', 'email')
    
    inlines = [AgendaDisponibilidadInline]


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'terapeuta', 'fecha_hora', 'estado', 'tipo_sesion')
    list_filter = ('estado', 'tipo_sesion', 'fecha_hora')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'terapeuta__nombres')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Paciente y Terapeuta', {
            'fields': ('paciente', 'terapeuta')
        }),
        ('Fecha y Hora', {
            'fields': ('fecha_hora', 'duracion_minutos')
        }),
        ('Detalles', {
            'fields': ('tipo_sesion', 'estado', 'motivo_cita', 'notas_adicionales')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:
            readonly.extend(['fecha_creacion'])
        return readonly


@admin.register(AgendaDisponibilidad)
class AgendaDisponibilidadAdmin(admin.ModelAdmin):
    list_display = ('terapeuta', 'get_dia_semana_display', 'hora_inicio', 'hora_fin', 'activo')
    list_filter = ('dia_semana', 'activo', 'terapeuta')
    search_fields = ('terapeuta__nombres', 'terapeuta__apellidos')
    
    fieldsets = (
        ('Terapeuta', {
            'fields': ('terapeuta',)
        }),
        ('Horario', {
            'fields': ('dia_semana', 'hora_inicio', 'hora_fin')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


# Crear admin personalizado para Citas Próximas
@admin.register(CitasProximas)
class CitasProximasAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'terapeuta', 'fecha_hora', 'estado')
    list_filter = ('estado', 'tipo_sesion')
    search_fields = ('paciente__nombres', 'paciente__apellidos')
    
    def get_queryset(self, request):
        """Filtra solo citas próximas (próximos 7 días)"""
        ahora = timezone.now()
        proxima_semana = ahora + timedelta(days=7)
        qs = super().get_queryset(request)
        return qs.filter(
            fecha_hora__gte=ahora,
            fecha_hora__lte=proxima_semana,
            estado__in=['disponible', 'ocupada']
        )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    readonly_fields = ('paciente', 'terapeuta', 'fecha_hora', 'estado', 'tipo_sesion')
    fieldsets = (
        ('Información de Cita', {
            'fields': ('paciente', 'terapeuta', 'fecha_hora')
        }),
        ('Estado', {
            'fields': ('estado', 'tipo_sesion')
        }),
    )
