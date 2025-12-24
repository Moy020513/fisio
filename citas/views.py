from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from citas.models import Cita, Terapeuta, CitasProximas
from citas.forms import CitaForm, TerapeutaForm


class CitaListView(LoginRequiredMixin, ListView):
    """Lista todas las citas."""
    model = Cita
    template_name = 'citas/cita_list.html'
    context_object_name = 'citas'
    paginate_by = 20

    def get_queryset(self):
        queryset = Cita.objects.all().order_by('-fecha_hora')
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_citas'] = Cita.objects.count()
        context['citas_proximas'] = CitasProximas.objects.count()
        context['estados'] = ['disponible', 'ocupada', 'cancelada', 'completada']
        return context


class CitasProximasView(LoginRequiredMixin, ListView):
    """Citas próximas (próximos 7 días)."""
    model = CitasProximas
    template_name = 'citas/citas_proximas.html'
    context_object_name = 'citas'
    paginate_by = 20


class CitaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una cita."""
    model = Cita
    template_name = 'citas/cita_detail.html'
    context_object_name = 'cita'


class CitaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva cita."""
    model = Cita
    form_class = CitaForm
    template_name = 'citas/cita_form.html'
    success_url = reverse_lazy('citas:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Agendar Nueva Cita'
        context['accion'] = 'crear'
        return context


class CitaUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar cita."""
    model = Cita
    form_class = CitaForm
    template_name = 'citas/cita_form.html'
    success_url = reverse_lazy('citas:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Cita: {self.object.paciente.nombre_completo}'
        context['accion'] = 'editar'
        return context


class CitaDeleteView(LoginRequiredMixin, DeleteView):
    """Cancelar cita."""
    model = Cita
    template_name = 'citas/cita_confirm_delete.html'
    success_url = reverse_lazy('citas:lista')


class TerapeutaListView(LoginRequiredMixin, ListView):
    """Lista de terapeutas."""
    model = Terapeuta
    template_name = 'citas/terapeuta_list.html'
    context_object_name = 'terapeutas'
    paginate_by = 10


class TerapeutaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de terapeuta."""
    model = Terapeuta
    template_name = 'citas/terapeuta_detail.html'
    context_object_name = 'terapeuta'


class TerapeutaCreateView(LoginRequiredMixin, CreateView):
    """Agregar nuevo terapeuta."""
    model = Terapeuta
    form_class = TerapeutaForm
    template_name = 'citas/terapeuta_form.html'
    success_url = reverse_lazy('citas:terapeutas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nuevo Terapeuta'
        return context


class TerapeutaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar información de terapeuta."""
    model = Terapeuta
    form_class = TerapeutaForm
    template_name = 'citas/terapeuta_form.html'
    success_url = reverse_lazy('citas:terapeutas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Terapeuta: {self.object.nombre_completo}'
        return context
