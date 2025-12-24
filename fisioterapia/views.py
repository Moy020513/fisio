from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente
from citas.models import Cita, CitasProximas
from historiaclinica.models import HistoriaClinica
from tratamientos.models import TratamientoEstetico


@login_required
def dashboard_view(request):
    """Vista del dashboard con estadísticas."""
    context = {
        'total_pacientes': Paciente.objects.count(),
        'total_citas': CitasProximas.objects.count(),
        'total_historias': HistoriaClinica.objects.count(),
        'total_tratamientos': TratamientoEstetico.objects.filter(activo=True).count(),
    }
    return render(request, 'dashboard.html', context)
