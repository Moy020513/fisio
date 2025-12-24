# Sistema de Gestión de Fisioterapia

Sistema completo en Django para gestionar una clínica de fisioterapia con módulos para:
- Pacientes y su historia clínica
- Agenda de citas
- Tratamientos estéticos
- Evolución y seguimiento de pacientes

## Estructura del Proyecto

```
fisioterapia/
├── pacientes/              # App para gestión de pacientes
├── citas/                  # App para agenda de citas
├── historiaclinica/        # App para historia clínica y tratamiento
├── tratamientos/           # App para tratamientos estéticos
├── fisioterapia/           # Configuración principal
├── manage.py
└── requirements.txt
```

## Instalación

1. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Aplicar migraciones:**
```bash
python manage.py migrate
```

4. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

5. **Ejecutar servidor:**
```bash
python manage.py runserver
```

Accede a: http://127.0.0.1:8000/admin

## Aplicaciones y Modelos

### 1. **PACIENTES** (`pacientes/`)

#### Modelo Principal: `Paciente`
- Nombres, apellidos, fecha de nacimiento, edad, género
- Contacto: teléfono, email, domicilio, teléfono emergencia
- Información médica: alergias, grupo sanguíneo, RH, religión
- Tipo de paciente:
  - Consulta única (masajes relajantes)
  - Patologías (tratamiento completo)
  - Masajes reductivos (tratamientos estéticos)
- Control de pacientes frecuentes

#### Modelos Relacionados:

**EstudiosClinico**
- Radiografías, resonancias, tomografías, ecografías
- Análisis sanguíneos, examen general de orina
- Perfil hormonal

**AntecedentePatologico**
- Hipertensión, diabetes, cáncer, triglicéridos, obesidad
- Tiroides, SOP, menopausia
- Separación entre antecedentes personales y familiares

**AntecedentePatologicoFemenino**
- Fecha última menstruación
- Probabilidad de embarazo
- Número de partos
- Información de menopausia

**AntecedenteCirugias**
- Registro de todas las cirugías

**AntecedentesNoPatologicos**
- Actividad física (tipo y frecuencia)
- Alimentación (tipo de dieta)
- Sueño (horas y calidad)
- Hidratación
- Suplementación

**DatosNutricion**
- Detalles nutricionales
- Macronutrientes (proteínas, carbohidratos, lípidos)
- Consumo de carnes, legumbres

---

### 2. **CITAS** (`citas/`)

#### Modelo: `Cita`
- Paciente y terapeuta asignado
- Fecha y hora
- Duración (minutos)
- Estados:
  - Disponible
  - Ocupada
  - Cancelada
  - Completada
- Tipos de sesión:
  - Sesión regular
  - Sesión estética
  - Seguimiento
  - Evaluación inicial
- Notas y motivo de la cita

#### Modelo: `Terapeuta`
- Información de contacto
- Especialidades
- Estado (activo/inactivo)

#### Modelo: `AgendaDisponibilidad`
- Horarios disponibles por terapeuta
- Día de la semana y hora inicio/fin
- Permite crear patrones de disponibilidad

#### Modelo Proxy: `CitasProximas`
- Filtro automático de citas próximas (próximos 7 días)
- Acceso rápido en admin

---

### 3. **HISTORIA CLÍNICA** (`historiaclinica/`)

#### Modelo Principal: `HistoriaClinica`
- Diagnóstico
- Pronóstico
- Tratamiento planificado
- Notas de arcos de movimiento
- Escala EVA (0-10) de dolor

#### Modelos Relacionados:

**ArcosMovimiento**
- Registro de arcos de movimiento
- Articulación, ángulos de flexión, extensión, rotación
- Para evaluación funcional

**PruebaFuncional**
- Registro de pruebas específicas
- Ej: Test Lachman, Test Trendelenburg
- Fecha y resultado

**EscalaDaniels**
- Evaluación de fuerza muscular
- Grados del 0-5
- Por músculo evaluado

**EjercioTerapeutico**
- Ejercicios prescritos
- Dosificación (series, repeticiones)
- Indicación si es para hacer en casa
- Frecuencia semanal

**EvolucionTratamiento**
- Seguimiento sesión a sesión
- Escala EVA en cada sesión
- Progreso y cambios detectados
- Número de sesión

**GraficoEvolucion**
- Datos para graficar evolución
- Valores de EVA, arcos movimiento, fuerza
- Permite visualizar progreso

---

### 4. **TRATAMIENTOS ESTÉTICOS** (`tratamientos/`)

#### Modelo Principal: `TratamientoEstetico`
- Paciente y su historia clínica asociada
- Fechas de inicio y fin planificada
- Objetivo principal
- Zonas de trabajo
- Técnicas descritas
- Control de tratamientos faciales y radiofrecuencia

#### Modelos Relacionados:

**ZonaCorporal**
- Zonas a trabajar:
  - Abdomen alto, cintura, abdomen bajo
  - Espalda alta, zona axilar, espalda baja
  - Piernas (proximal, medial, distal de fémur)
  - Cara, cuello, brazos, glúteos

**MedidasZona**
- Medidas en cm por zona
- Captura en 3 momentos:
  - Sesión 1 (inicial)
  - Sesión 3-4
  - Sesión 6-7
- Cálculo automático de cambios
- Permite visualizar reducción de medidas

**EvolucionTratamientoEstetico**
- Seguimiento sesión a sesión
- Cambios visibles
- Satisfacción del paciente
- Técnica utilizada
- Duración de sesión
- Notas y recomendaciones

**TecnicaTratamiento**
- Catálogo de técnicas disponibles
- Radiofrecuencia, masajes, crioterapia, cavitación
- Peellings, microdermoabrasión
- Zonas indicadas
- Duración típica

**TratamientoFacial**
- Información específica para faciales
- Tipo de piel
- Problemas de piel detectados
- Técnicas faciales específicas
- Objetivo (rejuvenecimiento, arrugas, etc.)

---

## Flujos de Trabajo

### 1. Nuevo Paciente de Consulta Única (Masaje Relajante)
1. Crear paciente con tipo "Consulta Única"
2. Agendar cita disponible
3. Registrar cita como "ocupada"
4. Marcar cita como "completada" después

### 2. Paciente con Patología (Tratamiento Completo)
1. Crear paciente con tipo "Patologías"
2. Marcar como frecuente (es_frecuente = True)
3. Crear Historia Clínica:
   - Diagnóstico
   - Arcos de movimiento
   - Pruebas funcionales
   - Escala Daniels
   - Ejercicios terapéuticos
4. Agendar citas regulares
5. Registrar evolución en cada sesión
6. Graficar resultados

### 3. Paciente Estético (Masajes Reductivos)
1. Crear paciente con tipo "Masajes Reductivos"
2. Marcar como frecuente si aplica
3. Crear Tratamiento Estético:
   - Definir zonas de trabajo
   - Seleccionar técnicas
4. Registrar medidas iniciales (Sesión 1)
5. Agendar citas estéticas
6. Registrar medidas en sesiones 3-4 y 6-7
7. Documentar evolución y cambios visibles
8. Para faciales: crear Tratamiento Facial específico

### 4. Paciente Facial
1. Crear Tratamiento Estético con es_tratamiento_facial = True
2. Crear asociado TratamientoFacial con:
   - Tipo de piel
   - Problemas detectados
   - Técnicas (radiofrecuencia, peelings, etc.)
3. Seguir mismo flujo de medidas
4. Documentar cambios en piel

---

## Acceso al Admin

**URL:** `http://127.0.0.1:8000/admin`

### Secciones Disponibles:

**PACIENTES**
- Pacientes (con toda su información clínica integrada)
- Estudios Clínicos
- Antecedentes Patológicos
- Antecedentes Femeninos
- Cirugías
- Antecedentes No Patológicos
- Datos de Nutrición

**CITAS**
- Citas (agenda general)
- Citas Próximas (próximos 7 días)
- Terapeutas
- Disponibilidad de Agenda

**HISTORIA CLÍNICA**
- Historias Clínicas
- Arcos de Movimiento
- Pruebas Funcionales
- Escala de Daniels
- Ejercicios Terapéuticos
- Evoluciones de Tratamiento
- Gráficos de Evolución

**TRATAMIENTOS**
- Tratamientos Estéticos
- Zonas Corporales
- Medidas de Zona
- Evoluciones de Tratamiento Estético
- Técnicas de Tratamiento
- Tratamientos Faciales

---

## Próximas Fases de Desarrollo

- [ ] Crear vistas personalizadas para reportes
- [ ] Implementar gráficos de evolución
- [ ] Crear plantillas HTML para visualización
- [ ] Agregar API REST
- [ ] Sistema de reportes PDF
- [ ] Dashboard de seguimiento
- [ ] Notificaciones de citas
- [ ] Sistema de pagos
- [ ] Facturación

---

## Configuración de Base de Datos

Por defecto usa **SQLite**. Para producción, se recomienda cambiar a **PostgreSQL**:

1. Instalar: `pip install psycopg2-binary`
2. Modificar `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fisioterapia_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Notas Importantes

- Las relaciones OneToOneField en historia clínica están diseñadas para pacientes frecuentes
- Los modelos de evolución permiten registrar cambios sesión a sesión
- Las medidas de zonas corporales se capturan automáticamente en 3 momentos
- El admin está totalmente configurado con inlines para facilitar entrada de datos
- Todos los modelos tienen campos de auditoría (fecha_creacion, fecha_actualizacion)

---

## Soporte

Para preguntas o problemas, consultar la documentación oficial de Django:
https://docs.djangoproject.com/
