from django.contrib import admin
from .models import (
    TratamientoEstetico, ZonaCorporal, MedidasZona,
    EvolucionTratamientoEstetico, TecnicaTratamiento, TratamientoFacial,
    EstadoCuenta, Anticipo
)


class ZonaCorporalInline(admin.TabularInline):
    model = ZonaCorporal
    extra = 1


class MedidasZonaInline(admin.TabularInline):
    model = MedidasZona
    extra = 1


class EvolucionTratamientoEstaticoInline(admin.TabularInline):
    model = EvolucionTratamientoEstetico
    extra = 1


class TratamientoFacialInline(admin.StackedInline):
    model = TratamientoFacial
    extra = 0


@admin.register(TratamientoEstetico)
class TratamientoEstaticoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_inicio', 'es_tratamiento_facial', 'activo')
    list_filter = ('es_tratamiento_facial', 'activo', 'fecha_inicio')
    search_fields = ('paciente__nombres', 'paciente__apellidos')
    readonly_fields = ('fecha_inicio', 'fecha_actualizacion')
    
    fieldsets = (
        ('Paciente', {
            'fields': ('paciente', 'historia_clinica')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin_planificada', 'fecha_actualizacion')
        }),
        ('Detalles del Tratamiento', {
            'fields': ('objetivo_principal', 'zona_trabajo', 'tecnicas_descripcion')
        }),
        ('Características', {
            'fields': ('es_tratamiento_facial', 'usa_radiofrecuencia', 'activo')
        }),
    )
    
    inlines = [
        ZonaCorporalInline,
        EvolucionTratamientoEstaticoInline,
        TratamientoFacialInline,
    ]


@admin.register(ZonaCorporal)
class ZonaCorporalAdmin(admin.ModelAdmin):
    list_display = ('tratamiento', 'zona', 'descripcion_adicional')
    list_filter = ('zona',)
    search_fields = ('tratamiento__paciente__nombres', 'zona')
    
    inlines = [MedidasZonaInline]


@admin.register(MedidasZona)
class MedidasZonaAdmin(admin.ModelAdmin):
    list_display = ('zona_corporal', 'numero_sesion', 'medida_cm', 'fecha_medicion')
    list_filter = ('numero_sesion', 'fecha_medicion')
    search_fields = ('zona_corporal__tratamiento__paciente__nombres',)
    readonly_fields = ('obtener_cambio',)
    
    fieldsets = (
        ('Zona y Sesión', {
            'fields': ('zona_corporal', 'numero_sesion')
        }),
        ('Medida', {
            'fields': ('medida_cm', 'fecha_medicion')
        }),
        ('Cambio Respecto a Sesión Anterior', {
            'fields': ('obtener_cambio',),
            'classes': ('wide',)
        }),
        ('Notas', {
            'fields': ('notas',)
        }),
    )


@admin.register(EvolucionTratamientoEstetico)
class EvolucionTratamientoEsteticoAdmin(admin.ModelAdmin):
    list_display = ('tratamiento', 'numero_sesion', 'fecha_sesion', 'satisfaccion_paciente')
    list_filter = ('numero_sesion', 'fecha_sesion', 'satisfaccion_paciente')
    search_fields = ('tratamiento__paciente__nombres', 'tratamiento__paciente__apellidos')
    
    fieldsets = (
        ('Sesión', {
            'fields': ('tratamiento', 'numero_sesion', 'fecha_sesion')
        }),
        ('Técnica', {
            'fields': ('tecnica_utilizada', 'duracion_minutos')
        }),
        ('Resultados', {
            'fields': ('cambios_visibles', 'satisfaccion_paciente')
        }),
        ('Notas y Recomendaciones', {
            'fields': ('notas', 'recomendaciones')
        }),
    )


@admin.register(TecnicaTratamiento)
class TecnicaTratamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'es_radiofrecuencia', 'es_facial', 'es_masaje', 'activa')
    list_filter = ('es_radiofrecuencia', 'es_facial', 'es_masaje', 'activa')
    search_fields = ('nombre',)
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'duracion_minutos_tipica')
        }),
        ('Tipo de Técnica', {
            'fields': ('es_radiofrecuencia', 'es_facial', 'es_masaje', 'es_crio', 'es_cavitacion', 'otra_tipo')
        }),
        ('Indicaciones', {
            'fields': ('zonas_indicadas',)
        }),
        ('Estado', {
            'fields': ('activa',)
        }),
    )


@admin.register(TratamientoFacial)
class TratamientoFacialAdmin(admin.ModelAdmin):
    list_display = ('tratamiento_estetico', 'tipo_piel', 'usa_radiofrecuencia_facial')
    list_filter = ('tipo_piel', 'usa_radiofrecuencia_facial')
    search_fields = ('tratamiento_estetico__paciente__nombres',)
    
    fieldsets = (
        ('Tratamiento Estético', {
            'fields': ('tratamiento_estetico',)
        }),
        ('Tipo de Piel', {
            'fields': ('tipo_piel', 'problemas_piel')
        }),
        ('Técnicas Faciales', {
            'fields': ('usa_radiofrecuencia_facial', 'usa_microdermoabracion', 'usa_peelings')
        }),
        ('Objetivo', {
            'fields': ('objetivo_facial',)
        }),
    )


class AnticipoInline(admin.TabularInline):
    model = Anticipo
    extra = 1
    readonly_fields = ('fecha_registro',)


@admin.register(EstadoCuenta)
class EstadoCuentaAdmin(admin.ModelAdmin):
    list_display = ('tratamiento', 'costo_total', 'obtener_total_pagado', 'obtener_saldo_pendiente')
    search_fields = ('tratamiento__paciente__nombres', 'tratamiento__paciente__apellidos')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'obtener_total_pagado', 'obtener_saldo_pendiente')
    
    fieldsets = (
        ('Tratamiento', {
            'fields': ('tratamiento',)
        }),
        ('Costos', {
            'fields': ('costo_total', 'obtener_total_pagado', 'obtener_saldo_pendiente')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion')
        }),
    )
    
    inlines = [AnticipoInline]


@admin.register(Anticipo)
class AnticipoAdmin(admin.ModelAdmin):
    list_display = ('estado_cuenta', 'monto', 'fecha_pago', 'concepto')
    list_filter = ('fecha_pago',)
    search_fields = ('estado_cuenta__tratamiento__paciente__nombres', 'concepto')
    readonly_fields = ('fecha_registro',)
    
    fieldsets = (
        ('Estado de Cuenta', {
            'fields': ('estado_cuenta',)
        }),
        ('Información del Pago', {
            'fields': ('monto', 'fecha_pago', 'concepto')
        }),
        ('Notas', {
            'fields': ('notas',)
        }),
        ('Control', {
            'fields': ('fecha_registro',)
        }),
    )

