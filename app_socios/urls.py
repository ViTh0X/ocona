from django.urls import path
from . import views

urlpatterns = [
    path('',views.socios,name='socios'),
    path('filtrar-socios',views.filtrar_socios_nombre,name='filtrar_socios_nombre'),
    path('filtrar-socios-dni',views.filtrar_socios_dni,name='filtrar_socios_dni'),
    path('detalles-socios/<int:pk>',views.ver_detalles_socio,name='ver_detalles_socio'),
    path('editar-socio/<int:pk>',views.editar_socio,name='editar_socio'),
    path('agregar-socio',views.agregar_socio,name='agregar_socio'),
    path('buscar-socio/<int:pk>',views.buscar_socio,name='buscar_socio'),
    path('encontrar-socios-familiares',views.encontrar_socios_familiares,name='encontrar_socios_familiares'),
    path('seleccionar-socio-familiar/<int:pk>',views.seleccionar_socio_familiar,name='seleccionar_socio_familiar'),
    path('seleccionar-no-socio-familiar',views.seleccionar_no_socio_familiar,name='seleccionar_no_socio_familiar'),
    path('transferencias-socio/<int:pk>',views.transferencias_socio,name='transferencias_socio'),
]
