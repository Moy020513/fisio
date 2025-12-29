from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import datetime
import os
from django.conf import settings
from historiaclinica.models import HistoriaClinica, EjercioTerapeutico, EvolucionTratamiento, EstudioClinico, EscalaDaniels
from historiaclinica.forms import HistoriaClinicaForm, EjercioTerapeuticoForm, EvolucionTratamientoForm, EstudioClinicoForm, EscalaDanielsForm
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
        context['evaluaciones_daniels'] = historia.escala_daniels.all()
        return context


class HistoriaClinicaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva historia clínica para un paciente."""
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'historiaclinica/historiaclinica_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        EscalaDanielsFormSet = inlineformset_factory(
            HistoriaClinica, EscalaDaniels,
            form=EscalaDanielsForm,
            extra=3, can_delete=True
        )
        if self.request.POST:
            context['daniels_formset'] = EscalaDanielsFormSet(self.request.POST)
        else:
            context['daniels_formset'] = EscalaDanielsFormSet()
        context['paciente'] = get_object_or_404(Paciente, pk=self.kwargs['paciente_pk'])
        context['titulo'] = f'Nueva Historia Clínica: {context["paciente"].nombre_completo}'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        daniels_formset = context['daniels_formset']
        paciente = get_object_or_404(Paciente, pk=self.kwargs['paciente_pk'])
        historia = form.save(commit=False)
        historia.paciente = paciente
        historia.save()
        
        if daniels_formset.is_valid():
            daniels_formset.instance = historia
            daniels_formset.save()
        
        messages.success(self.request, 'Historia clínica creada exitosamente.')
        return redirect('historiaclinica:detalle', pk=historia.pk)


class HistoriaClinicaUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar historia clínica."""
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'historiaclinica/historiaclinica_form.html'
    success_url = reverse_lazy('historiaclinica:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        EscalaDanielsFormSet = inlineformset_factory(
            HistoriaClinica, EscalaDaniels,
            form=EscalaDanielsForm,
            extra=1, can_delete=True
        )
        if self.request.POST:
            context['daniels_formset'] = EscalaDanielsFormSet(self.request.POST, instance=self.object)
        else:
            context['daniels_formset'] = EscalaDanielsFormSet(instance=self.object)
        context['titulo'] = f'Editar Historia Clínica: {self.object.paciente.nombre_completo}'
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        daniels_formset = context['daniels_formset']
        historia = form.save()
        
        if daniels_formset.is_valid():
            daniels_formset.instance = historia
            daniels_formset.save()
        
        messages.success(self.request, 'Historia clínica actualizada exitosamente.')
        return redirect('historiaclinica:detalle', pk=historia.pk)


class HistoriaClinicaDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar historia clínica."""
    model = HistoriaClinica
    template_name = 'historiaclinica/historiaclinica_confirm_delete.html'
    context_object_name = 'historia'
    success_url = reverse_lazy('historiaclinica:lista')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Historia clínica eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


class HistoriaClinicaCreateGlobalView(LoginRequiredMixin, CreateView):
    """Crear historia clínica seleccionando el paciente desde el formulario."""
    model = HistoriaClinica
    form_class = HistoriaClinicaForm
    template_name = 'historiaclinica/historiaclinica_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        EscalaDanielsFormSet = inlineformset_factory(
            HistoriaClinica, EscalaDaniels,
            form=EscalaDanielsForm,
            extra=3, can_delete=True
        )
        if self.request.POST:
            context['daniels_formset'] = EscalaDanielsFormSet(self.request.POST)
        else:
            context['daniels_formset'] = EscalaDanielsFormSet()
        context['titulo'] = 'Nueva Historia Clínica'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        daniels_formset = context['daniels_formset']
        historia = form.save()
        
        if daniels_formset.is_valid():
            daniels_formset.instance = historia
            daniels_formset.save()
        
        messages.success(self.request, 'Historia clínica creada exitosamente.')
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
        messages.success(self.request, f'Ejercicio "{ejercio.nombre_ejercicio}" creado exitosamente.')
        return redirect('historiaclinica:detalle', pk=historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        context['titulo'] = 'Agregar Ejercicio Terapéutico'
        return context


class EjercioUpdateView(LoginRequiredMixin, UpdateView):
    """Editar ejercicio terapéutico."""
    model = EjercioTerapeutico
    form_class = EjercioTerapeuticoForm
    template_name = 'historiaclinica/ejercio_form.html'

    def form_valid(self, form):
        ejercio = form.save()
        messages.success(self.request, f'Ejercicio "{ejercio.nombre_ejercicio}" actualizado exitosamente.')
        return redirect('historiaclinica:detalle', pk=ejercio.historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = self.object.historia
        context['titulo'] = 'Editar Ejercicio'
        return context


class EjercioDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar ejercicio terapéutico."""
    model = EjercioTerapeutico
    template_name = 'historiaclinica/ejercio_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Ejercicio eliminado exitosamente.')
        return reverse_lazy('historiaclinica:detalle', kwargs={'pk': self.object.historia.pk})


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
        messages.success(self.request, f'Evolución de sesión {evolucion.numero_sesion} registrada exitosamente.')
        return redirect('historiaclinica:detalle', pk=historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        context['titulo'] = 'Registrar Evolución'
        return context


class EvolucionUpdateView(LoginRequiredMixin, UpdateView):
    """Editar evolución del tratamiento."""
    model = EvolucionTratamiento
    form_class = EvolucionTratamientoForm
    template_name = 'historiaclinica/evolucion_form.html'

    def form_valid(self, form):
        evolucion = form.save()
        messages.success(self.request, f'Evolución de sesión {evolucion.numero_sesion} actualizada exitosamente.')
        return redirect('historiaclinica:detalle', pk=evolucion.historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = self.object.historia
        context['titulo'] = 'Editar Evolución'
        return context


class EvolucionDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar evolución del tratamiento."""
    model = EvolucionTratamiento
    template_name = 'historiaclinica/evolucion_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Evolución eliminada exitosamente.')
        return reverse_lazy('historiaclinica:detalle', kwargs={'pk': self.object.historia.pk})


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
        messages.success(self.request, f'Estudio clínico "{estudio.get_tipo_display()}" registrado exitosamente.')
        return redirect('historiaclinica:detalle', pk=historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        context['titulo'] = 'Registrar Estudio Clínico'
        return context


class EstudioUpdateView(LoginRequiredMixin, UpdateView):
    """Editar estudio clínico."""
    model = EstudioClinico
    form_class = EstudioClinicoForm
    template_name = 'historiaclinica/estudio_form.html'

    def form_valid(self, form):
        estudio = form.save()
        messages.success(self.request, f'Estudio clínico "{estudio.get_tipo_display()}" actualizado exitosamente.')
        return redirect('historiaclinica:detalle', pk=estudio.historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = self.object.historia
        context['titulo'] = 'Editar Estudio Clínico'
        return context


class EstudioDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar estudio clínico."""
    model = EstudioClinico
    template_name = 'historiaclinica/estudio_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Estudio clínico eliminado exitosamente.')
        return reverse_lazy('historiaclinica:detalle', kwargs={'pk': self.object.historia.pk})


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


class EscalaDanielsListView(LoginRequiredMixin, ListView):
    """Lista de evaluaciones musculares (Escala Daniels)."""
    model = EscalaDaniels
    template_name = 'historiaclinica/daniels_list.html'
    context_object_name = 'evaluaciones'

    def get_queryset(self):
        historia = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        return historia.escala_daniels.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        return context


class EscalaDanielsCreateView(LoginRequiredMixin, CreateView):
    """Registrar evaluación muscular (Escala Daniels)."""
    model = EscalaDaniels
    form_class = EscalaDanielsForm
    template_name = 'historiaclinica/daniels_form.html'

    def form_valid(self, form):
        historia = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        evaluacion = form.save(commit=False)
        evaluacion.historia = historia
        evaluacion.save()
        messages.success(self.request, f'Evaluación muscular "{evaluacion.musculo}" registrada exitosamente.')
        return redirect('historiaclinica:detalle', pk=historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = get_object_or_404(HistoriaClinica, pk=self.kwargs['historia_pk'])
        context['titulo'] = 'Registrar Escala Daniels'
        return context


class EscalaDanielsUpdateView(LoginRequiredMixin, UpdateView):
    """Editar evaluación muscular (Escala Daniels)."""
    model = EscalaDaniels
    form_class = EscalaDanielsForm
    template_name = 'historiaclinica/daniels_form.html'

    def form_valid(self, form):
        evaluacion = form.save()
        messages.success(self.request, f'Evaluación muscular "{evaluacion.musculo}" actualizada exitosamente.')
        return redirect('historiaclinica:detalle', pk=evaluacion.historia.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = self.object.historia
        context['titulo'] = 'Editar Escala Daniels'
        return context


class EscalaDanielsDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar evaluación muscular (Escala Daniels)."""
    model = EscalaDaniels
    template_name = 'historiaclinica/daniels_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Evaluación muscular eliminada exitosamente.')
        return reverse_lazy('historiaclinica:detalle', kwargs={'pk': self.object.historia.pk})


class ExportarEjerciciosPDFView(LoginRequiredMixin, View):
    """Exportar ejercicios terapéuticos a PDF."""
    
    def get(self, request, historia_pk):
        historia = get_object_or_404(HistoriaClinica, pk=historia_pk)
        ejercicios = historia.ejercicios_terapeuticos.all()
        
        # Crear el objeto PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Contenedor de elementos
        elements = []
        
        # Agregar logo si existe
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'fisio.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1*inch, height=1*inch)
            elements.append(logo)
            elements.append(Spacer(1, 0.1*inch))
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.grey,
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        # Título
        elements.append(Paragraph('Ejercicios Terapéuticos', title_style))
        elements.append(Paragraph(f'Paciente: {historia.paciente.nombre_completo}', subtitle_style))
        elements.append(Paragraph(f'Fecha: {datetime.datetime.now().strftime("%d/%m/%Y")}', subtitle_style))
        elements.append(Spacer(1, 0.3*inch))
        
        if ejercicios:
            for idx, ejercicio in enumerate(ejercicios, 1):
                # Tabla para cada ejercicio
                data = [
                    [Paragraph(f'<b>Ejercicio {idx}: {ejercicio.nombre_ejercicio}</b>', styles['Heading2'])],
                    [Paragraph(f'<b>Descripción:</b> {ejercicio.descripcion}', styles['Normal'])],
                    [Paragraph(f'<b>Series:</b> {ejercicio.series} | <b>Repeticiones:</b> {ejercicio.repeticiones}', styles['Normal'])],
                    [Paragraph(f'<b>Frecuencia:</b> {ejercicio.frecuencia}', styles['Normal'])],
                ]
                
                if ejercicio.duracion_segundos:
                    data.append([Paragraph(f'<b>Duración:</b> {ejercicio.duracion_segundos} segundos', styles['Normal'])])
                
                data.append([Paragraph(f'<b>Lugar:</b> {"En casa" if ejercicio.es_ejercicio_casa else "En clínica"}', styles['Normal'])])
                
                if ejercicio.dias_semana:
                    data.append([Paragraph(f'<b>Días:</b> {ejercicio.dias_semana}', styles['Normal'])])
                
                if ejercicio.notas:
                    data.append([Paragraph(f'<b>Notas:</b> {ejercicio.notas}', styles['Normal'])])
                
                table = Table(data, colWidths=[6.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f0fe')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1a73e8')),
                ]))
                
                elements.append(table)
                elements.append(Spacer(1, 0.15*inch))
        else:
            elements.append(Paragraph('No hay ejercicios terapéuticos registrados.', styles['Normal']))
        
        # Construir PDF
        doc.build(elements)
        
        # Obtener el valor del buffer y preparar respuesta
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ejercicios_{historia.paciente.apellidos}_{datetime.datetime.now().strftime("%Y%m%d")}.pdf"'
        response.write(pdf)
        
        return response

