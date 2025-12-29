from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.template.loader import render_to_string
from pacientes.models import Paciente, AntecedentePatologico, AntecedentesNoPatologicos
from pacientes.forms import (
    PacienteForm,
    AntecedentePatologicoForm,
    AntecedentesNoPatologicosForm,
    DatosNutricionForm,
)


class PacienteListView(LoginRequiredMixin, ListView):
    """Lista todos los pacientes del sistema."""
    model = Paciente
    template_name = 'pacientes/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Paciente.objects.all().order_by('-fecha_registro')
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            queryset = queryset.filter(
                Q(nombres__icontains=busqueda)
                | Q(apellidos__icontains=busqueda)
                | Q(telefono__icontains=busqueda)
                | Q(email__icontains=busqueda)
            )
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo_paciente=tipo)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pacientes'] = Paciente.objects.count()
        context['tipos_paciente'] = [
            ('consulta_unica', 'Consulta Única'),
            ('patologia', 'Patología'),
            ('estetico', 'Estético'),
            ('estetico_facial', 'Estético Facial'),
        ]
        context['busqueda'] = self.request.GET.get('busqueda', '')
        context['tipo_filtro'] = self.request.GET.get('tipo', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            table_html = render_to_string('pacientes/partials/_paciente_table.html', context=context, request=self.request)
            pagination_html = render_to_string('pacientes/partials/_paciente_pagination.html', context=context, request=self.request)
            return JsonResponse({
                'table': table_html,
                'pagination': pagination_html,
                'resultados': context['page_obj'].paginator.count,
            })
        return super().render_to_response(context, **response_kwargs)


class PacienteDetailView(LoginRequiredMixin, DetailView):
    """Detalle completo de un paciente."""
    model = Paciente
    template_name = 'pacientes/paciente_detail.html'
    context_object_name = 'paciente'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        context['antecedentes_pat'] = getattr(paciente, 'antecedentes_patologicos', None)
        context['antecedentes_no_pat'] = getattr(paciente, 'antecedentes_no_patologicos', None)
        context['nutricion'] = getattr(paciente, 'datos_nutricion', None)
        return context


class PacienteCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo paciente."""
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('pacientes:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nuevo Paciente'
        context['accion'] = 'crear'
        return context


class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar información del paciente."""
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_form.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('pacientes:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Paciente: {self.object.nombre_completo}'
        context['accion'] = 'editar'
        return context


class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar paciente."""
    model = Paciente
    template_name = 'pacientes/paciente_confirm_delete.html'
    success_url = reverse_lazy('pacientes:lista')
    pk_url_kwarg = 'pk'


class AntecedentesPatologicosListView(LoginRequiredMixin, ListView):
    """Listado de pacientes para gestionar antecedentes patológicos."""
    model = Paciente
    template_name = 'pacientes/antecedentes_pat_list.html'
    context_object_name = 'pacientes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Paciente.objects.all().order_by('-fecha_registro')
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            queryset = queryset.filter(
                Q(nombres__icontains=busqueda)
                | Q(apellidos__icontains=busqueda)
                | Q(telefono__icontains=busqueda)
                | Q(email__icontains=busqueda)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busqueda'] = self.request.GET.get('busqueda', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            table_html = render_to_string('pacientes/partials/_antecedentes_pat_table.html', context=context, request=self.request)
            pagination_html = render_to_string('pacientes/partials/_antecedentes_pat_pagination.html', context=context, request=self.request)
            return JsonResponse({
                'tabla': table_html,
                'paginacion': pagination_html,
                'total': context['page_obj'].paginator.count,
            })
        return super().render_to_response(context, **response_kwargs)


class AntecedentesNoPatologicosListView(LoginRequiredMixin, ListView):
    """Listado de pacientes para gestionar antecedentes no patológicos."""
    model = Paciente
    template_name = 'pacientes/antecedentes_no_pat_list.html'
    context_object_name = 'pacientes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Paciente.objects.all().order_by('-fecha_registro')
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            queryset = queryset.filter(
                Q(nombres__icontains=busqueda)
                | Q(apellidos__icontains=busqueda)
                | Q(telefono__icontains=busqueda)
                | Q(email__icontains=busqueda)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busqueda'] = self.request.GET.get('busqueda', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            table_html = render_to_string('pacientes/partials/_antecedentes_no_pat_table.html', context=context, request=self.request)
            pagination_html = render_to_string('pacientes/partials/_antecedentes_no_pat_pagination.html', context=context, request=self.request)
            return JsonResponse({
                'tabla': table_html,
                'paginacion': pagination_html,
                'total': context['page_obj'].paginator.count,
            })
        return super().render_to_response(context, **response_kwargs)


class AntecedentesPatologicosDetailView(LoginRequiredMixin, DetailView):
    """Ver antecedentes patológicos de un paciente."""
    model = Paciente
    template_name = 'pacientes/antecedentes_pat_detail.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        context['antecedentes_pat'] = getattr(paciente, 'antecedentes_patologicos', None)
        context['mostrar_campos_femeninos'] = paciente.genero == 'F'
        return context


class AntecedentesDetailView(LoginRequiredMixin, DetailView):
    """Ver antecedentes no patológicos."""
    model = Paciente
    template_name = 'pacientes/antecedentes_detail.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        context['antecedentes'] = getattr(paciente, 'antecedentes_no_patologicos', None)
        context['antecedentes_pat'] = getattr(paciente, 'antecedentes_patologicos', None)
        context['mostrar_campos_femeninos'] = paciente.genero == 'F'
        return context


class AntecedentesNoPatologicosDetailView(LoginRequiredMixin, DetailView):
    """Ver antecedentes no patológicos de un paciente."""
    model = Paciente
    template_name = 'pacientes/antecedentes_no_pat_detail.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        context['antecedentes'] = getattr(paciente, 'antecedentes_no_patologicos', None)
        return context


class AntecedentesPatologicosUpdateView(LoginRequiredMixin, UpdateView):
    """Crear o actualizar antecedentes patológicos."""
    model = AntecedentePatologico
    form_class = AntecedentePatologicoForm
    template_name = 'pacientes/antecedentes_pat_form.html'
    pk_url_kwarg = 'pk'

    def get_object(self):
        paciente = get_object_or_404(Paciente, pk=self.kwargs['pk'])
        antecedente = getattr(paciente, 'antecedentes_patologicos', None)
        if not antecedente:
            antecedente = AntecedentePatologico.objects.create(paciente=paciente)
        return antecedente

    def get_success_url(self):
        return reverse_lazy('pacientes:antecedentes-patologicos-lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Antecedentes patológicos guardados correctamente.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
        context['mostrar_campos_femeninos'] = self.object.paciente.genero == 'F'
        return context


class AntecedentesUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar antecedentes no patológicos."""
    model = AntecedentesNoPatologicos
    form_class = AntecedentesNoPatologicosForm
    template_name = 'pacientes/antecedentes_form.html'
    pk_url_kwarg = 'pk'

    def get_object(self):
        paciente = get_object_or_404(Paciente, pk=self.kwargs['pk'])
        antecedentes = getattr(paciente, 'antecedentes_no_patologicos', None)
        if not antecedentes:
            antecedentes = AntecedentesNoPatologicos.objects.create(paciente=paciente)
        return antecedentes

    def get_success_url(self):
        return reverse_lazy('pacientes:detalle', kwargs={'pk': self.object.paciente.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.object.paciente
        return context


class NutricionDetailView(LoginRequiredMixin, DetailView):
    """Ver datos de nutrición."""
    model = Paciente
    template_name = 'pacientes/nutricion_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        context['nutricion'] = getattr(paciente, 'datos_nutricion', None)
        return context


class NutricionCreateView(LoginRequiredMixin, CreateView):
    """Crear datos de nutrición."""
    model = None
    form_class = DatosNutricionForm
    template_name = 'pacientes/nutricion_form.html'

    def get_success_url(self):
        return reverse_lazy('pacientes:nutricion-detalle', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        from pacientes.models import Paciente
        context = super().get_context_data(**kwargs)
        context['paciente'] = get_object_or_404(Paciente, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        from pacientes.models import Paciente, DatosNutricion
        paciente = get_object_or_404(Paciente, pk=self.kwargs['pk'])
        nutricion = form.save(commit=False)
        nutricion.paciente = paciente
        nutricion.save()
        return redirect(self.get_success_url())
