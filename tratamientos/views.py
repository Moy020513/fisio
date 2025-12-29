from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from tratamientos.models import TratamientoEstetico, MedidasZona, EvolucionTratamientoEstetico, ZonaCorporal
from tratamientos.forms import TratamientoEstaticoForm, MedidasZonaForm, EvolucionTratamientoEstaticoForm
from pacientes.models import Paciente
from datetime import date


class TratamientoEstaticoListView(LoginRequiredMixin, ListView):
    """Lista de tratamientos estéticos."""
    model = TratamientoEstetico
    template_name = 'tratamientos/tratamiento_list.html'
    context_object_name = 'tratamientos'
    paginate_by = 20

    def get_queryset(self):
        queryset = TratamientoEstetico.objects.all().order_by('-fecha_inicio')
        activos = self.request.GET.get('activos')
        if activos == 'true':
            queryset = queryset.filter(activo=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_activos'] = TratamientoEstetico.objects.filter(activo=True).count()
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
            # Sesión 1
            self._crear_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s1'), 1)
            self._crear_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s1'), 1)
            self._crear_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s1'), 1)
            # Sesión 3-4
            self._crear_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s34'), 3)
            self._crear_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s34'), 3)
            self._crear_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s34'), 3)
            # Sesión 6-7
            self._crear_zona_medida(tratamiento, 'abdomen_alto', self.request.POST.get('abdomen_alto_s67'), 6)
            self._crear_zona_medida(tratamiento, 'cintura', self.request.POST.get('cintura_s67'), 6)
            self._crear_zona_medida(tratamiento, 'abdomen_bajo', self.request.POST.get('abdomen_bajo_s67'), 6)
        elif zona_principal == 'espalda':
            # Sesión 1
            self._crear_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s1'), 1)
            self._crear_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s1'), 1)
            self._crear_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s1'), 1)
            # Sesión 3-4
            self._crear_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s34'), 3)
            self._crear_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s34'), 3)
            self._crear_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s34'), 3)
            # Sesión 6-7
            self._crear_zona_medida(tratamiento, 'espalda_alta', self.request.POST.get('espalda_alta_s67'), 6)
            self._crear_zona_medida(tratamiento, 'zona_axilar', self.request.POST.get('zona_axilar_s67'), 6)
            self._crear_zona_medida(tratamiento, 'espalda_baja', self.request.POST.get('espalda_baja_s67'), 6)
        elif zona_principal == 'pierna':
            # Sesión 1
            self._crear_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s1'), 1)
            self._crear_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s1'), 1)
            self._crear_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s1'), 1)
            # Sesión 3-4
            self._crear_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s34'), 3)
            self._crear_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s34'), 3)
            self._crear_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s34'), 3)
            # Sesión 6-7
            self._crear_zona_medida(tratamiento, 'femur_proximal', self.request.POST.get('femur_proximal_s67'), 6)
            self._crear_zona_medida(tratamiento, 'femur_medial', self.request.POST.get('femur_medial_s67'), 6)
            self._crear_zona_medida(tratamiento, 'cadera_distal', self.request.POST.get('cadera_distal_s67'), 6)
        
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
        return context

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

