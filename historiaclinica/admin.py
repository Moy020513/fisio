from django.contrib import admin
from .models import (
    HistoriaClinica, ArcosMovimiento, PruebaFuncional,
    EscalaDaniels, EjercioTerapeutico, EvolucionTratamiento,
    GraficoEvolucion, EstudioClinico
)


class ArcosMovimientoInline(admin.TabularInline):
    model = ArcosMovimiento
    extra = 1


class PruebaFuncionalInline(admin.TabularInline):
    model = PruebaFuncional
    extra = 1


class EscalaDanielsInline(admin.TabularInline):
    model = EscalaDaniels
    extra = 1


class EjercioTerapeuticoInline(admin.StackedInline):
    model = EjercioTerapeutico
    extra = 1


class EvolucionTratamientoInline(admin.TabularInline):
    model = EvolucionTratamiento
    extra = 1


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_evaluacion', 'diagnostico', 'escala_eva', 'activo')
    list_filter = ('activo', 'fecha_evaluacion', 'escala_eva')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'diagnostico')
    
    fieldsets = (
        ('Paciente e Información General', {
            'fields': ('paciente', 'fecha_evaluacion', 'fecha_actualizacion')
        }),
        ('Diagnóstico y Pronóstico', {
            'fields': ('diagnostico', 'pronostico')
        }),
        ('Tratamiento', {
            'fields': ('tratamiento_planificado', 'notas_arcos_movimiento')
        }),
        ('Evaluación', {
            'fields': ('escala_eva', 'activo')
        }),
    )
    
    inlines = [
        ArcosMovimientoInline,
        PruebaFuncionalInline,
        EscalaDanielsInline,
        EjercioTerapeuticoInline,
        EvolucionTratamientoInline,
    ]
    
    readonly_fields = ('fecha_evaluacion', 'fecha_actualizacion')


@admin.register(ArcosMovimiento)
class ArcosMovimientoAdmin(admin.ModelAdmin):
    list_display = ('historia', 'articulation', 'flexion', 'extension')
    search_fields = ('historia__paciente__nombres', 'articulation')


@admin.register(PruebaFuncional)
class PruebaFuncionalAdmin(admin.ModelAdmin):
    list_display = ('historia', 'tipo_prueba', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('historia__paciente__nombres', 'tipo_prueba')


@admin.register(EscalaDaniels)
class EscalaDanielsAdmin(admin.ModelAdmin):
    list_display = ('historia', 'musculo', 'grado')
    list_filter = ('grado',)
    search_fields = ('historia__paciente__nombres', 'musculo')


@admin.register(EjercioTerapeutico)
class EjercioTerapeuticoAdmin(admin.ModelAdmin):
    list_display = ('historia', 'nombre_ejercicio', 'series', 'repeticiones', 'es_ejercicio_casa')
    list_filter = ('es_ejercicio_casa', 'fecha_prescripcion')
    search_fields = ('historia__paciente__nombres', 'nombre_ejercicio')


@admin.register(EvolucionTratamiento)
class EvolucionTratamientoAdmin(admin.ModelAdmin):
    list_display = ('historia', 'numero_sesion', 'fecha_sesion', 'escala_eva_sesion')
    list_filter = ('fecha_sesion',)
    search_fields = ('historia__paciente__nombres',)


@admin.register(GraficoEvolucion)
class GraficoEvolucionAdmin(admin.ModelAdmin):
    list_display = ('historia', 'numero_sesion', 'fecha', 'escala_eva')
    list_filter = ('fecha',)
    search_fields = ('historia__paciente__nombres',)


@admin.register(EstudioClinico)
class EstudioClinicoAdmin(admin.ModelAdmin):
    list_display = ('historia', 'tipo', 'fecha_estudio')
    list_filter = ('tipo', 'fecha_estudio')
    search_fields = (
        'historia__paciente__nombres',
        'historia__paciente__apellidos',
        'descripcion',
        'resultado'
    )
