from django.urls import path
from tratamientos import views

app_name = 'tratamientos'

urlpatterns = [
    # Tratamientos estéticos
    path('', views.TratamientoEstaticoListView.as_view(), name='lista'),
    path('crear/', views.TratamientoEstaticoCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.TratamientoEstaticoDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.TratamientoEstaticoUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.TratamientoEstaticoDeleteView.as_view(), name='eliminar'),

    # Medidas
    path('<int:tratamiento_pk>/medidas/crear/', views.MedidasZonaCreateView.as_view(), name='medida-crear'),

    # Evoluciones
    path('<int:tratamiento_pk>/evoluciones/crear/', views.EvolucionEstaticoCreateView.as_view(), name='evolucion-crear'),
    
    # Estado de Cuentas
    path('<int:tratamiento_pk>/estado-cuenta/', views.EstadoCuentaDetailView.as_view(), name='estado_cuenta'),
    path('<int:tratamiento_pk>/estado-cuenta/editar/', views.EstadoCuentaUpdateView.as_view(), name='estado_cuenta_editar'),
    
    # Anticipos
    path('<int:tratamiento_pk>/anticipos/crear/', views.AnticipoCreateView.as_view(), name='anticipo_crear'),
    path('anticipos/<int:pk>/editar/', views.AnticipoUpdateView.as_view(), name='anticipo_editar'),
    path('anticipos/<int:pk>/eliminar/', views.AnticipoDeleteView.as_view(), name='anticipo_eliminar'),
        path('<int:pk>/historial/', views.TratamientoHistorialView.as_view(), name='historial'),
]
