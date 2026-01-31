

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from tratamientos.models import TratamientoEstetico, MedidasZona, EvolucionTratamientoEstetico, ZonaCorporal, EstadoCuenta, Anticipo
from tratamientos.forms import TratamientoEstaticoForm, MedidasZonaForm, EvolucionTratamientoEstaticoForm, EstadoCuentaForm, AnticipoForm
from pacientes.models import Paciente
from datetime import date

# ...existing code...

# Colocar la vista de eliminación al final para asegurar importaciones
class TratamientoEstaticoDeleteView(LoginRequiredMixin, DeleteView):
    model = TratamientoEstetico
    template_name = 'tratamientos/tratamiento_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Tratamiento eliminado correctamente')
        return reverse_lazy('tratamientos:lista')


class TratamientoEstaticoListView(LoginRequiredMixin, ListView):
    """Lista de tratamientos estéticos."""
    model = TratamientoEstetico
    template_name = 'tratamientos/tratamiento_list.html'
    context_object_name = 'tratamientos'
    paginate_by = 20

    def get_queryset(self):
        queryset = TratamientoEstetico.objects.all().order_by('-fecha_inicio')
        
        # Filtro por estado
        activos = self.request.GET.get('activos')
        if activos == 'true':
            queryset = queryset.filter(activo=True)
        
        # Búsqueda por nombre del paciente
        buscar = self.request.GET.get('buscar', '').strip()
        if buscar:
            queryset = queryset.filter(
                paciente__nombres__icontains=buscar
            ) | queryset.filter(
                paciente__apellidos__icontains=buscar
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_activos'] = TratamientoEstetico.objects.filter(activo=True).count()
        context['buscar'] = self.request.GET.get('buscar', '')
        context['activos'] = self.request.GET.get('activos', '')
        return context


class TratamientoEstaticoDetailView(LoginRequiredMixin, DetailView):
    """Detalle de tratamiento estético."""
    model = TratamientoEstetico
    template_name = 'tratamientos/tratamiento_detail.html'
    context_object_name = 'tratamiento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tratamiento = self.get_object()
        context['zonas'] = tratamiento.zonas_corporales.all()
        context['evoluciones'] = tratamiento.evoluciones.all()
        return context


class TratamientoEstaticoCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo tratamiento estético."""
    model = TratamientoEstetico
    form_class = TratamientoEstaticoForm
    template_name = 'tratamientos/tratamiento_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Tratamiento Estético'
        context['accion'] = 'crear'
        return context

    def form_valid(self, form):
        # Guardar el tratamiento
        response = super().form_valid(form)
        tratamiento = self.object

        # Procesar zonas y medidas
        zona_principal = self.request.POST.get('zona_principal')

        if zona_principal == 'abdomen':
            self._crear_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s1'), 1)
            self._crear_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s1'), 1)
            self._crear_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s1'), 1)
            self._crear_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s34'), 3)
            self._crear_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s34'), 3)
            self._crear_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s34'), 3)
            self._crear_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s67'), 6)
            self._crear_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s67'), 6)
            self._crear_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s67'), 6)
        elif zona_principal == 'espalda':
            self._crear_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s1'), 1)
            self._crear_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s1'), 1)
            self._crear_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s1'), 1)
            self._crear_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s34'), 3)
            self._crear_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s34'), 3)
            self._crear_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s34'), 3)
            self._crear_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s67'), 6)
            self._crear_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s67'), 6)
            self._crear_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s67'), 6)
        elif zona_principal == 'pierna':
            self._crear_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s1'), 1)
            self._crear_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s1'), 1)
            self._crear_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s1'), 1)
            self._crear_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s34'), 3)
            self._crear_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s34'), 3)
            self._crear_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s34'), 3)
            self._crear_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s67'), 6)
            self._crear_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s67'), 6)
            self._crear_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s67'), 6)

        messages.success(self.request, 'Tratamiento creado correctamente')
        return response
    
    def _crear_zona_medida(self, tratamiento, zona_key, valor, numero_sesion):
        """Crear zona corporal y medida para la sesión especificada."""
        if not valor:
            return
        
        # Mapeo de claves a zona_corporal choices
        zona_mapping = {
            'abdomen_alto': 'abdomen_alto',
            'cintura': 'cintura',
            'abdomen_bajo': 'abdomen_bajo',
            'espalda_alta': 'espalda_alta',
            'zona_axilar': 'zona_axilar',
            'espalda_baja': 'espalda_baja',
            'femur_proximal': 'femur_proximal',
            'femur_medial': 'femur_medial',
            'cadera_distal': 'cadera_distal',
        }
        
        zona_choice = zona_mapping.get(zona_key)
        if not zona_choice:
            return
        
        # Crear o obtener la zona corporal
        zona_corporal, created = ZonaCorporal.objects.get_or_create(
            tratamiento=tratamiento,
            zona=zona_choice
        )
        
        # Crear la medida para la sesión especificada
        MedidasZona.objects.get_or_create(
            zona_corporal=zona_corporal,
            numero_sesion=numero_sesion,
            defaults={
                'medida_cm': float(valor),
                'fecha_medicion': date.today(),
            }
        )

    def get_success_url(self):
        return reverse_lazy('tratamientos:detalle', kwargs={'pk': self.object.pk})


class TratamientoEstaticoUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar tratamiento estético."""
    model = TratamientoEstetico
    form_class = TratamientoEstaticoForm
    template_name = 'tratamientos/tratamiento_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Tratamiento: {self.object.paciente.nombre_completo}'
        context['accion'] = 'editar'
        
        # Cargar medidas existentes para mostrar en el formulario
        tratamiento = self.object
        zonas = tratamiento.zonas_corporales.all()
        
        medidas_existentes = {}
        for zona in zonas:
            zona_key = zona.zona
            for medida in zona.medidas.all():
                sesion = medida.numero_sesion
                if sesion == 1:
                    sufijo = '_s1'
                elif sesion == 3:
                    sufijo = '_s34'
                elif sesion == 6:
                    sufijo = '_s67'
                else:
                    continue
                medidas_existentes[f"{zona_key}{sufijo}"] = float(medida.medida_cm)
        
        context['medidas_existentes'] = medidas_existentes
        return context
    
    def form_valid(self, form):
        # Guardar el tratamiento
        response = super().form_valid(form)
        tratamiento = self.object
        
        # Procesar zonas y medidas
        zona_principal = self.request.POST.get('zona_principal')
        
        if zona_principal == 'abdomen':
            self._actualizar_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s67'), 6)
            self._actualizar_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s67'), 6)
            self._actualizar_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s67'), 6)
        elif zona_principal == 'espalda':
            self._actualizar_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s67'), 6)
            self._actualizar_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s67'), 6)
            self._actualizar_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s67'), 6)
        elif zona_principal == 'pierna':
            self._actualizar_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s1'), 1)
            self._actualizar_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s34'), 3)
            self._actualizar_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s67'), 6)
            self._actualizar_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s67'), 6)
            self._actualizar_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s67'), 6)
        
        messages.success(self.request, 'Tratamiento actualizado correctamente')
        return response
    
    def _actualizar_zona_medida(self, tratamiento, zona_key, valor, numero_sesion):
        """Actualizar zona corporal y medida para la sesión especificada."""
        if not valor:
            return
        
        # Mapeo de claves a zona_corporal choices
        zona_mapping = {
            'abdomen_alto': 'abdomen_alto',
            'cintura': 'cintura',
            'abdomen_bajo': 'abdomen_bajo',
            'espalda_alta': 'espalda_alta',
            'zona_axilar': 'zona_axilar',
            'espalda_baja': 'espalda_baja',
            'femur_proximal': 'femur_proximal',
            'femur_medial': 'femur_medial',
            'cadera_distal': 'cadera_distal',
        }
        
        zona_choice = zona_mapping.get(zona_key)
        if not zona_choice:
            return
        
        # Crear o obtener la zona corporal
        zona_corporal, created = ZonaCorporal.objects.get_or_create(
            tratamiento=tratamiento,
            zona=zona_choice
        )
        
        # Actualizar o crear la medida para la sesión especificada
        medida, created = MedidasZona.objects.get_or_create(
            zona_corporal=zona_corporal,
            numero_sesion=numero_sesion,
            defaults={
                'medida_cm': float(valor),
                'fecha_medicion': date.today(),
            }
        )
        
        # Si ya existe, actualizar el valor
        if not created:
            medida.medida_cm = float(valor)
            medida.fecha_medicion = date.today()
            medida.save()

    def get_success_url(self):
        return reverse_lazy('tratamientos:detalle', kwargs={'pk': self.object.pk})


class MedidasZonaCreateView(LoginRequiredMixin, CreateView):
    """Agregar medidas de una zona corporal."""
    model = MedidasZona
    form_class = MedidasZonaForm
    template_name = 'tratamientos/medidas_form.html'

    def form_valid(self, form):
        tratamiento = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        medida = form.save(commit=False)
        medida.tratamiento = tratamiento
        medida.save()
        return redirect('tratamientos:detalle', pk=tratamiento.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamiento'] = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        context['titulo'] = 'Registrar Medidas'
        return context


class EvolucionEstaticoCreateView(LoginRequiredMixin, CreateView):
    """Registrar evolución de tratamiento estético."""
    model = EvolucionTratamientoEstetico
    form_class = EvolucionTratamientoEstaticoForm
    template_name = 'tratamientos/evolucion_form.html'

    def form_valid(self, form):
        tratamiento = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        evolucion = form.save(commit=False)
        evolucion.tratamiento = tratamiento
        evolucion.save()
        return redirect('tratamientos:detalle', pk=tratamiento.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamiento'] = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        context['titulo'] = 'Registrar Sesión'
        return context


class EstadoCuentaDetailView(LoginRequiredMixin, DetailView):
    """Ver estado de cuenta del tratamiento."""
    model = EstadoCuenta
    template_name = 'tratamientos/estado_cuenta_detail.html'
    context_object_name = 'estado_cuenta'
    
    def get_object(self):
        tratamiento = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        estado_cuenta, created = EstadoCuenta.objects.get_or_create(tratamiento=tratamiento)
        return estado_cuenta
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamiento'] = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        context['anticipos'] = context['estado_cuenta'].anticipos.all()
        context['total_pagado'] = context['estado_cuenta'].obtener_total_pagado()
        context['saldo_pendiente'] = context['estado_cuenta'].obtener_saldo_pendiente()
        return context


class EstadoCuentaUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar costo total del tratamiento."""
    model = EstadoCuenta
    form_class = EstadoCuentaForm
    template_name = 'tratamientos/estado_cuenta_form.html'
    
    def get_object(self):
        tratamiento = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        estado_cuenta, created = EstadoCuenta.objects.get_or_create(tratamiento=tratamiento)
        return estado_cuenta
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamiento'] = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Costo total actualizado correctamente')
        return reverse_lazy('tratamientos:estado_cuenta', kwargs={'tratamiento_pk': self.kwargs['tratamiento_pk']})


class AnticipoCreateView(LoginRequiredMixin, CreateView):
    """Registrar nuevo anticipo."""
    model = Anticipo
    form_class = AnticipoForm
    template_name = 'tratamientos/anticipo_form.html'
    
    def form_valid(self, form):
        tratamiento = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        estado_cuenta, created = EstadoCuenta.objects.get_or_create(tratamiento=tratamiento)
        
        anticipo = form.save(commit=False)
        anticipo.estado_cuenta = estado_cuenta
        anticipo.save()
        
        messages.success(self.request, 'Anticipo registrado correctamente')
        return redirect('tratamientos:estado_cuenta', tratamiento_pk=tratamiento.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamiento'] = get_object_or_404(TratamientoEstetico, pk=self.kwargs['tratamiento_pk'])
        context['titulo'] = 'Registrar Anticipo'
        return context


class AnticipoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar anticipo existente."""
    model = Anticipo
    form_class = AnticipoForm
    template_name = 'tratamientos/anticipo_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamiento'] = self.object.estado_cuenta.tratamiento
        context['titulo'] = 'Editar Anticipo'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Anticipo actualizado correctamente')
        return reverse_lazy('tratamientos:estado_cuenta', kwargs={'tratamiento_pk': self.object.estado_cuenta.tratamiento.pk})


class AnticipoDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar anticipo."""
    model = Anticipo
    template_name = 'tratamientos/anticipo_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tratamiento'] = self.object.estado_cuenta.tratamiento
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Anticipo eliminado correctamente')
        return reverse_lazy('tratamientos:estado_cuenta', kwargs={'tratamiento_pk': self.object.estado_cuenta.tratamiento.pk})


class TratamientoHistorialView(DetailView):
    model = TratamientoEstetico
    template_name = 'tratamientos/historial.html'
    context_object_name = 'tratamiento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zonas'] = self.object.zonas_corporales.all()
        context['evoluciones'] = self.object.evoluciones.all()
        return context



