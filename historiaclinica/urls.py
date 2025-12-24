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

    # Ejercicios
    path('<int:historia_pk>/ejercicios/', views.EjercioListView.as_view(), name='ejercios'),
    path('<int:historia_pk>/ejercicios/crear/', views.EjercioCreateView.as_view(), name='ejercio-crear'),

    # Evoluciones
    path('<int:historia_pk>/evoluciones/', views.EvolucionListView.as_view(), name='evoluciones'),
    path('<int:historia_pk>/evoluciones/crear/', views.EvolucionCreateView.as_view(), name='evolucion-crear'),

    # Estudios clínicos
    path('<int:historia_pk>/estudios/', views.EstudioListView.as_view(), name='estudios'),
    path('<int:historia_pk>/estudios/crear/', views.EstudioCreateView.as_view(), name='estudio-crear'),
    path('estudios/', views.EstudioGlobalListView.as_view(), name='estudios-global'),
]
