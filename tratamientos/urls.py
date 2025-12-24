from django.urls import path
from tratamientos import views

app_name = 'tratamientos'

urlpatterns = [
    # Tratamientos estéticos
    path('', views.TratamientoEstaticoListView.as_view(), name='lista'),
    path('crear/', views.TratamientoEstaticoCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.TratamientoEstaticoDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.TratamientoEstaticoUpdateView.as_view(), name='editar'),

    # Medidas
    path('<int:tratamiento_pk>/medidas/crear/', views.MedidasZonaCreateView.as_view(), name='medida-crear'),

    # Evoluciones
    path('<int:tratamiento_pk>/evoluciones/crear/', views.EvolucionEstaticoCreateView.as_view(), name='evolucion-crear'),
]
