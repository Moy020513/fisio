from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from historiaclinica.models import HistoriaClinica, EjercioTerapeutico, EvolucionTratamiento, EstudioClinico
from historiaclinica.forms import HistoriaClinicaForm, EjercioTerapeuticoForm, EvolucionTratamientoForm, EstudioClinicoForm
from pacientes.models import Paciente
from django.db.models import Q


class HistoriaClinicaListView(LoginRequiredMixin, ListView):
    """Lista historias clínicas."""
    model = HistoriaClinica
    template_name = 'historiaclinica/historiaclinica_list.html'
    context_object_name = 'historias'
    paginate_by = 20

    def get_queryset(self):
        return HistoriaClinica.objects.all().order_by('-fecha_evaluacion')


class HistoriaClinicaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de historia clínica."""
    model = HistoriaClinica
    template_name = 'historiaclinica/historiaclinica_detail.html'
    context_object_name = 'historia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        historia = self.get_object()
        context['ejercicios'] = historia.ejercicios_terapeuticos.all()
        context['evoluciones'] = historia.evoluciones.all()
        context['estudios'] = historia.estudios_clinicos.all()
        return context


class HistoriaClinicaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva historia clínica para un paciente."""
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'historiaclinica/historiaclinica_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = get_object_or_404(Paciente, pk=self.kwargs['paciente_pk'])
        context['titulo'] = f'Nueva Historia Clínica: {context["paciente"].nombre_completo}'
        return context

    def form_valid(self, form):
        paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_pk'])
        historia = form.save(commit=False)
        historia.paciente = paciente
        historia.save()
        return redirect('historiaclinica:detalle', pk=historia.pk)


class HistoriaClinicaUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar historia clínica."""
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'historiaclinica/historiaclinica_form.html'
    success_url = reverse_lazy('historiaclinica:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Historia Clínica: {self.object.paciente.nombre_completo}'
        return context


class HistoriaClinicaCreateGlobalView(LoginRequiredMixin, CreateView):
    """Crear historia clínica seleccionando el paciente desde el formulario."""
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'historiaclinica/historiaclinica_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Historia Clínica'
        return context

    def form_valid(self, form):
        historia = form.save()
        return redirect('historiaclinica:detalle', pk=historia.pk)


class EjercioListView(LoginRequiredMixin, ListView):
    """Lista ejercicios de una historia clínica."""
    model = EjercioTerapeutico
    template_name = 'historiaclinica/ejercio_list.html'
    context_object_name = 'ejercicios'

    def get_queryset(self):
        historia = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        return historia.ejercicios_terapeuticos.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        return context


class EjercioCreateView(LoginRequiredMixin, CreateView):
    """Agregar ejercicio terapéutico."""
    model = EjercioTerapeutico
    form_class = EjercioTerapeuticoForm
    template_name = 'historiaclinica/ejercio_form.html'

    def form_valid(self, form):
        historia = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        ejercio = form.save(commit=False)
        ejercio.historia = historia
        ejercio.save()
        return redirect('historiaclinica:detalle', pk=historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        context['titulo'] = 'Agregar Ejercicio Terapéutico'
        return context


class EvolucionListView(LoginRequiredMixin, ListView):
    """Lista evoluciones de un tratamiento."""
    model = EvolucionTratamiento
    template_name = 'historiaclinica/evolucion_list.html'
    context_object_name = 'evoluciones'

    def get_queryset(self):
        historia = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        return historia.evoluciones.all().order_by('-fecha_sesion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        return context


class EvolucionCreateView(LoginRequiredMixin, CreateView):
    """Registrar evolución del tratamiento."""
    model = EvolucionTratamiento
    form_class = EvolucionTratamientoForm
    template_name = 'historiaclinica/evolucion_form.html'

    def form_valid(self, form):
        historia = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        evolucion = form.save(commit=False)
        evolucion.historia = historia
        evolucion.save()
        return redirect('historiaclinica:detalle', pk=historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        context['titulo'] = 'Registrar Evolución'
        return context


class EstudioListView(LoginRequiredMixin, ListView):
    """Lista de estudios clínicos de una historia clínica."""
    model = EstudioClinico
    template_name = 'historiaclinica/estudio_list.html'
    context_object_name = 'estudios'

    def get_queryset(self):
        historia = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        return historia.estudios_clinicos.all().order_by('-fecha_estudio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        return context


class EstudioCreateView(LoginRequiredMixin, CreateView):
    """Registrar un estudio clínico."""
    model = EstudioClinico
    form_class = EstudioClinicoForm
    template_name = 'historiaclinica/estudio_form.html'

    def form_valid(self, form):
        historia = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        estudio = form.save(commit=False)
        estudio.historia = historia
        estudio.save()
        return redirect('historiaclinica:detalle', pk=historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        context['titulo'] = 'Registrar Estudio Clínico'
        return context


class EstudioGlobalListView(LoginRequiredMixin, ListView):
    """Exploración global de estudios clínicos con filtros."""
    model = EstudioClinico
    template_name = 'historiaclinica/estudios_global.html'
    context_object_name = 'estudios'
    paginate_by = 25

    def get_queryset(self):
        qs = EstudioClinico.objects.select_related('historia__paciente').all()
        tipo = self.request.GET.get('tipo')
        paciente_query = self.request.GET.get('paciente')
        desde = self.request.GET.get('desde')
        hasta = self.request.GET.get('hasta')

        if tipo:
            qs = qs.filter(tipo=tipo)
        if paciente_query:
            qs = qs.filter(
                Q(historia__paciente__nombres__icontains=paciente_query) |
                Q(historia__paciente__apellidos__icontains=paciente_query)
            )
        if desde:
            qs = qs.filter(fecha_estudio__gte=desde)
        if hasta:
            qs = qs.filter(fecha_estudio__lte=hasta)

        return qs.order_by('-fecha_estudio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TIPO_CHOICES'] = EstudioClinico.TIPO_CHOICES
        context['filtros'] = {
            'tipo': self.request.GET.get('tipo', ''),
            'paciente': self.request.GET.get('paciente', ''),
            'desde': self.request.GET.get('desde', ''),
            'hasta': self.request.GET.get('hasta', ''),
        }
        return context

