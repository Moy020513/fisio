from django.urls import path
from historiaclinica import views

app_name = 'historiaclinica'

urlpatterns = [
    # Historias clínicas
    path('', views.HistoriaClinicaListView.as_view(), name='lista'),
    path('crear/', views.HistoriaClinicaCreateGlobalView.as_view(), name='crear-global'),
    path('crear/<int:paciente_pk>/', views.HistoriaClinicaCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.HistoriaClinicaDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.HistoriaClinicaUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.HistoriaClinicaDeleteView.as_view(), name='eliminar'),

    # Ejercicios
    path('<int:historia_pk>/ejercicios/', views.EjercioListView.as_view(), name='ejercios'),
    path('<int:historia_pk>/ejercicios/crear/', views.EjercioCreateView.as_view(), name='ejercio-crear'),
    path('ejercicios/<int:pk>/editar/', views.EjercioUpdateView.as_view(), name='ejercio-editar'),
    path('ejercicios/<int:pk>/eliminar/', views.EjercioDeleteView.as_view(), name='ejercio-eliminar'),

    # Evoluciones
    path('<int:historia_pk>/evoluciones/', views.EvolucionListView.as_view(), name='evoluciones'),
    path('<int:historia_pk>/evoluciones/crear/', views.EvolucionCreateView.as_view(), name='evolucion-crear'),
    path('evoluciones/<int:pk>/editar/', views.EvolucionUpdateView.as_view(), name='evolucion-editar'),
    path('evoluciones/<int:pk>/eliminar/', views.EvolucionDeleteView.as_view(), name='evolucion-eliminar'),

    # Estudios clínicos
    path('<int:historia_pk>/estudios/', views.EstudioListView.as_view(), name='estudios'),
    path('<int:historia_pk>/estudios/crear/', views.EstudioCreateView.as_view(), name='estudio-crear'),
    path('estudios/<int:pk>/editar/', views.EstudioUpdateView.as_view(), name='estudio-editar'),
    path('estudios/<int:pk>/eliminar/', views.EstudioDeleteView.as_view(), name='estudio-eliminar'),
    path('estudios/', views.EstudioGlobalListView.as_view(), name='estudios-global'),

    # Escala Daniels
    path('<int:historia_pk>/daniels/', views.EscalaDanielsListView.as_view(), name='daniels-lista'),
    path('<int:historia_pk>/daniels/crear/', views.EscalaDanielsCreateView.as_view(), name='daniels-crear'),
    path('daniels/<int:pk>/editar/', views.EscalaDanielsUpdateView.as_view(), name='daniels-editar'),
    path('daniels/<int:pk>/eliminar/', views.EscalaDanielsDeleteView.as_view(), name='daniels-eliminar'),
    
    # Exportar PDF
    path('<int:historia_pk>/ejercicios/pdf/', views.ExportarEjerciciosPDFView.as_view(), name='ejercicios-pdf'),
]
