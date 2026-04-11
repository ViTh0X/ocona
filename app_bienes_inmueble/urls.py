from django.urls import path
from . import views

urlpatterns = [
    path('huertos',views.menu_bienes_inmueble_huertos,name='menu_bienes_inmueble_huertos'),
    path('filtrar-huertos',views.filtrar_huertos_nombres,name='filtrar_huertos_nombres'),
    path('editar-huerto/<int:pk>',views.editar_huerto,name='editar_huerto'),
    path('parcelas',views.menu_bienes_inmueble_parcelas,name='menu_bienes_inmueble_parcelas'),
    path('filtrar-parcelas',views.filtrar_parcelas_nombres,name='filtrar_parcelas_nombres'),
    path('editar-parcela/<int:pk>',views.editar_parcela,name='editar_parcela'),
    path('detalles-huertos/<int:pk>',views.detalles_huertos,name='detalles_huertos'),
    path('agregar-huerto',views.agregar_huerto,name='agregar_huerto'),    
    path('detalles-parcelas/<int:pk>',views.detalles_parcelas,name='detalles_parcelas'),
    path('agregar-parcela',views.agregar_parcela,name='agregar_parcela'),    
]
