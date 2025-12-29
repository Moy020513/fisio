from django.urls import path
from pacientes import views

app_name = 'pacientes'

urlpatterns = [
    # Pacientes
    path('', views.PacienteListView.as_view(), name='lista'),
    path('crear/', views.PacienteCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.PacienteDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.PacienteDeleteView.as_view(), name='eliminar'),

    # Listados de antecedentes
    path('antecedentes/patologicos/', views.AntecedentesPatologicosListView.as_view(), name='antecedentes-patologicos-lista'),
    path('antecedentes/no-patologicos/', views.AntecedentesNoPatologicosListView.as_view(), name='antecedentes-no-patologicos-lista'),

    # Antecedentes
    path('<int:pk>/antecedentes/patologicos/editar/', views.AntecedentesPatologicosUpdateView.as_view(), name='antecedentes-patologicos-editar'),
    path('<int:pk>/antecedentes/', views.AntecedentesDetailView.as_view(), name='antecedentes'),
    path('<int:pk>/antecedentes/editar/', views.AntecedentesUpdateView.as_view(), name='antecedentes-editar'),
    path('<int:pk>/antecedentes/no-patologicos/editar/', views.AntecedentesUpdateView.as_view(), name='antecedentes-no-patologicos-editar'),

    # Nutrición
    path('<int:pk>/nutricion/', views.NutricionDetailView.as_view(), name='nutricion-detalle'),
    path('<int:pk>/nutricion/crear/', views.NutricionCreateView.as_view(), name='nutricion-crear'),
]
