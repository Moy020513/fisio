from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from tratamientos.models import TratamientoEstetico, MedidasZona, EvolucionTratamientoEstetico
from tratamientos.forms import TratamientoEstaticoForm, MedidasZonaForm, EvolucionTratamientoEstaticoForm
from pacientes.models import Paciente


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
        context['medidas'] = tratamiento.medidaszona_set.all()
        context['evoluciones'] = tratamiento.evoluciontratamientoestetico_set.all()
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

