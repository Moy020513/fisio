from django.urls import path
from citas import views

app_name = 'citas'

urlpatterns = [
    # Citas
    path('', views.CitaListView.as_view(), name='lista'),
    path('proximas/', views.CitasProximasView.as_view(), name='proximas'),
    path('crear/', views.CitaCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.CitaDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.CitaUpdateView.as_view(), name='editar'),
    path('<int:pk>/cancelar/', views.CitaDeleteView.as_view(), name='cancelar'),

    # Terapeutas
    path('terapeutas/', views.TerapeutaListView.as_view(), name='terapeutas'),
    path('terapeutas/crear/', views.TerapeutaCreateView.as_view(), name='terapeuta-crear'),
    path('terapeutas/<int:pk>/', views.TerapeutaDetailView.as_view(), name='terapeuta-detalle'),
    path('terapeutas/<int:pk>/editar/', views.TerapeutaUpdateView.as_view(), name='terapeuta-editar'),
]
