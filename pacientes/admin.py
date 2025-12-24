from django.contrib import admin
from .models import (
    Paciente, EstudiosClinico, AntecedentePatologico,
    AntecedentePatologicoFemenino, AntecedenteCirugias,
    AntecedentesNoPatologicos, DatosNutricion
)


class EstudiosClinicoInline(admin.StackedInline):
    model = EstudiosClinico
    extra = 0


class AntecedentePatologicoInline(admin.TabularInline):
    model = AntecedentePatologico
    extra = 1


class AntecedentePatologicoFemeninoInline(admin.StackedInline):
    model = AntecedentePatologicoFemenino
    extra = 0


class AntecedenteCirugiasInline(admin.TabularInline):
    model = AntecedenteCirugias
    extra = 1


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
        AntecedenteCirugiasInline,
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
    list_display = ('paciente', 'patologia', 'tipo_antecedente', 'año_diagnostico')
    list_filter = ('patologia', 'tipo_antecedente')
    search_fields = ('paciente__nombres', 'paciente__apellidos')


@admin.register(AntecedentePatologicoFemenino)
class AntecedentePatologicoFemeninoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'en_menopausia', 'numero_partos')
    search_fields = ('paciente__nombres', 'paciente__apellidos')


@admin.register(AntecedenteCirugias)
class AntecedenteCirugiasAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'tipo_cirugia', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'tipo_cirugia')


@admin.register(AntecedentesNoPatologicos)
class AntecedentesNoPatologicosAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'realiza_actividad_fisica', 'tipo_alimentacion')
    list_filter = ('realiza_actividad_fisica', 'tipo_alimentacion')
    search_fields = ('paciente__nombres', 'paciente__apellidos')


@admin.register(DatosNutricion)
class DatosNutricionAdmin(admin.ModelAdmin):
    list_display = ('paciente',)
    search_fields = ('paciente__nombres', 'paciente__apellidos')
