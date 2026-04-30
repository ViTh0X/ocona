from django.urls import path
from . import views



urlpatterns = [
    path('',views.menu_transferencias,name='menu_transferencias'),
    path('agregar-transferencias',views.agregar_transferencias,name='agregar_transferencias'),
    path('agregar-transferencias-huertos',views.agregar_transferencias_con_inmueble,name='agregar_transferencias_con_inmueble'),
    path('agregar-transferencias-parcelas',views.agregar_transferencias_sin_inmueble,name='agregar_transferencias_sin_inmueble'),
    path('buscar-huertos',views.buscar_huertos,name='buscar_huertos'),
    path('buscar-parcelas',views.buscar_parcelas,name='buscar_parcelas'),
    path('mas-transferentes',views.mas_transferentes,name='mas_transferentes'),
    path('mas-transferidos',views.mas_transferidos,name='mas_transferidos'),
    path('editar-transferencia/<int:pk>/<str:socio_id>/',views.editar_transferencia,name='editar_transferencia')      
]
