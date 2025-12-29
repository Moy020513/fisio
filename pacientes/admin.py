from django.contrib import admin
from .models import (
    Paciente, EstudiosClinico, AntecedentePatologico,
    AntecedentesNoPatologicos, DatosNutricion
)


class EstudiosClinicoInline(admin.StackedInline):
    model = EstudiosClinico
    extra = 0


class AntecedentePatologicoInline(admin.StackedInline):
    model = AntecedentePatologico
    extra = 0


class AntecedentesNoPatologicosInline(admin.StackedInline):
    model = AntecedentesNoPatologicos
    extra = 0


class DatosNutricionInline(admin.StackedInline):
    model = DatosNutricion
    extra = 0


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'edad', 'genero', 'tipo_paciente', 'es_frecuente', 'telefono')
    list_filter = ('tipo_paciente', 'es_frecuente', 'genero', 'fecha_registro')
    search_fields = ('nombres', 'apellidos', 'email', 'telefono')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombres', 'apellidos', 'fecha_nacimiento', 'edad', 'genero')
        }),
        ('Contacto', {
            'fields': ('telefono', 'telefono_emergencia', 'email', 'domicilio')
        }),
        ('Información Médica', {
            'fields': ('alergias', 'grupo_sanguineo', 'rh', 'religion')
        }),
        ('Clasificación', {
            'fields': ('tipo_paciente', 'es_frecuente')
        }),
    )
    
    inlines = [
        EstudiosClinicoInline,
        AntecedentePatologicoInline,
        AntecedentesNoPatologicosInline,
        DatosNutricionInline,
    ]
    
    readonly_fields = ('fecha_registro', 'ultima_actualizacion')


@admin.register(EstudiosClinico)
class EstudiosClinicoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_actualizacion')
    search_fields = ('paciente__nombres', 'paciente__apellidos')


@admin.register(AntecedentePatologico)
class AntecedentePatologicoAdmin(admin.ModelAdmin):
    list_display = ('paciente',)
    search_fields = ('paciente__nombres', 'paciente__apellidos')


@admin.register(AntecedentesNoPatologicos)
class AntecedentesNoPatologicosAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'realiza_actividad_fisica', 'tipo_alimentacion')
    list_filter = ('realiza_actividad_fisica', 'tipo_alimentacion')
    search_fields = ('paciente__nombres', 'paciente__apellidos')


@admin.register(DatosNutricion)
class DatosNutricionAdmin(admin.ModelAdmin):
    list_display = ('paciente',)
    search_fields = ('paciente__nombres', 'paciente__apellidos')
