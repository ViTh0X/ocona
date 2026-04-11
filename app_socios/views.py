from django.shortcuts import redirect, render 
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from app_bienes_inmueble.models import Inmuebles
from app_transferencias.models import Transferencias
from .models import *
from django.urls import reverse
from .forms import *

from django.db.models import Q
from django.db.models import IntegerField
from django.db.models.functions import Cast
# Create your views here.

from datetime import datetime

def socios(request):
    socios = Socios.objects.all()[:15]    
    cantidad_socios = Socios.objects.all().count()
    return render(request,'app_socios/menu_socios.html',{'socios':socios,'cantidad_socios':cantidad_socios})

def filtrar_socios_nombre(request):
    pista_nombre = request.GET.get('nombre','').strip()    
    palabras = pista_nombre.split() # Esto crea ['Samir', 'Quispe']
    query = Q()
    for palabra in palabras:
        # Por cada palabra, buscamos en nombres O apellidos
        query &= (Q(nombres__icontains=palabra) | Q(apellidos__icontains=palabra))

    socios = Socios.objects.filter(query)    
    return render(request,'app_socios/socios_filtrados.html',{'socios':socios})
    

def filtrar_socios_dni(request):
    pista_dni = request.GET.get('dni','').strip()
    socios = Socios.objects.filter(dni__icontains=pista_dni)
    return render(request,'app_socios/socios_filtrados.html',{'socios':socios})

    

def ver_detalles_socio(request,pk):
    socio = Socios.objects.get(pk=pk)
    huertos_socio = Inmuebles.objects.filter(tipo=1,socio_poseedor_actual=socio)
    parcelas_socio = Inmuebles.objects.filter(tipo=2,socio_poseedor_actual=socio)
    codigos_asociados = CodigosAsociadosSocio.objects.filter(
        socio_asociado=pk
    ).annotate(
        codigo_int=Cast('codigo', output_field=IntegerField())
    ).order_by('codigo_int')
    personas_asociadas = PersonasRelacionadasSocio.objects.filter(socio_asociado=pk)
    return render (request,'app_socios/ver_detalles_socio.html',{'socio':socio,'huertos_socio':huertos_socio,'parcelas_socio':parcelas_socio,'codigos_asociados':codigos_asociados,'personas_asociadas':personas_asociadas})
    

def editar_socio(request,pk):
    socio = Socios.objects.get(pk=pk)
    huertos_socio = Inmuebles.objects.filter(tipo=1,socio_poseedor_actual=socio)
    parcelas_socio = Inmuebles.objects.filter(tipo=2,socio_poseedor_actual=socio)
    codigos_asociados = CodigosAsociadosSocio.objects.filter(
        socio_asociado=pk
    ).annotate(
        codigo_int=Cast('codigo', output_field=IntegerField())
    ).order_by('codigo_int')
    personas_asociadas = PersonasRelacionadasSocio.objects.filter(socio_asociado=pk)
    if request.method == 'POST':
        form = SocioFormulario(request.POST,instance=socio)
        if form.is_valid():
            form.save()
            return redirect('ver_detalles_socio',pk=socio.id)
    else:
        form = SocioFormulario(instance=socio)
    return render(request,'app_socios/editar_socio.html',{'form':form,'huertos_socio':huertos_socio,'parcelas_socio':parcelas_socio,'codigos_asociados':codigos_asociados,'personas_asociadas':personas_asociadas})

def buscar_socio(request,pk):
    socio = Socios.objects.get(pk=pk)
    return render(request,'app_socios/buscar_socio.html',{'socio':socio})

def encontrar_socios_familiares(request):
    pista_socio = request.GET.get('nombre', '').strip()    
    palabras = pista_socio.split()

    # SI NO HAY PALABRAS, DEVOLVEMOS LISTA VACÍA PARA QUE SALTE EL {% empty %}
    if not palabras:
        return render(request, 'app_socios/socios_encontrados.html', {'socios': []})

    query = Q()
    for palabra in palabras:
        query &= (Q(nombres__icontains=palabra) | Q(apellidos__icontains=palabra))
    
    socios = Socios.objects.filter(query)
    print(socios.__len__())
    # OPCIONAL: Imprime en consola para depurar
    # print(f"Buscando: {palabras} - Encontrados: {socios.count()}")
    return render(request, 'app_socios/socios_encontrados.html', {'socios': socios})

def seleccionar_no_socio_familiar(request):
    id_socio = request.POST.get('id_socio') or request.GET.get('id_socio')
    if not id_socio:
        return HttpResponse("Error: No se encontró el ID del socio principal.")
    socio_principal = Socios.objects.get(pk=int(id_socio))
    tipos_familiar = TipoFamiliar.objects.all()
    if request.method == 'POST':
        tipo_id = request.POST.get('tipo_familiar')
        apellido_familiar = request.POST.get('apellido_familiar')
        nombre_familiar = request.POST.get('nombre_familiar')
        es_socio_txt = request.POST.get('es_socio_texto')
        dni = request.POST.get('dni_familiar')
        fecha_nacimiento = request.POST.get('fecha_nacimiento_familiar')
        if fecha_nacimiento:        
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            except (ValueError, TypeError):
                fecha_nacimiento = fecha_nacimiento
        else:
            fecha_nacimiento=None
        #socio_repetido = PersonasRelacionadasSocio.objects.filter(dni=dni).first()
        #if socio_repetido:
        #    return HttpResponse("Error: Esta persona ya esta agregada como familiar")
        try:
            tipo_f = TipoFamiliar.objects.get(pk=int(tipo_id))
            
            # Guardamos la relación
            PersonasRelacionadasSocio.objects.create(
                socio_asociado=socio_principal,
                denominacion=f"{apellido_familiar}, {nombre_familiar}",
                tipo_familiar=tipo_f,
                es_socio=es_socio_txt,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento
            )
            
            # MAGIA PARA HTMX: 
            # Esto le dice al navegador que haga un refresh total a la página de detalles
            response = HttpResponse()
            response['HX-Redirect'] = reverse('ver_detalles_socio', kwargs={'pk': socio_principal.id})
            return response
            
        except Exception as e:
            import traceback
            print(traceback.format_exc()) # Esto imprimirá el error exacto en la consola
            return HttpResponse(f"Error interno: {e}", status=500)            

    # Si es GET, mostramos el formulario
    return render(request, 'app_socios/form_agregar_no_familiar.html', {
        'tipos_familiar': tipos_familiar,        
        'socio_principal': socio_principal
    })
    
def seleccionar_socio_familiar(request,pk):
    familiar_socio = Socios.objects.get(pk=pk)
    
    # Buscamos el ID en POST (que ahora enviamos como id_socio) o en GET
    id_socio = request.POST.get('id_socio') or request.GET.get('id_socio')
    
    if not id_socio:
        return HttpResponse("Error: No se encontró el ID del socio principal.")

    socio_principal = Socios.objects.get(pk=int(id_socio))
    tipos_familiar = TipoFamiliar.objects.all()
    
    if request.method == 'POST':
        tipo_id = request.POST.get('tipo_familiar')
        es_socio_txt = request.POST.get('es_socio_texto')
        #socio_repetido = PersonasRelacionadasSocio.objects.get(dni=familiar_socio.dni)
        #if socio_repetido:
        #    return HttpResponse("Error: Esta persona ya esta agregada como familiar")
        try:
            tipo_f = TipoFamiliar.objects.get(pk=int(tipo_id))
            
            # Guardamos la relación
            PersonasRelacionadasSocio.objects.create(
                socio_asociado=socio_principal,
                denominacion=f"{familiar_socio.apellidos}, {familiar_socio.nombres}",
                tipo_familiar=tipo_f,
                es_socio=es_socio_txt,
                dni=familiar_socio.dni,
                fecha_nacimiento=familiar_socio.fecha_nacimiento
            )
            
            # MAGIA PARA HTMX: 
            # Esto le dice al navegador que haga un refresh total a la página de detalles
            response = HttpResponse()
            response['HX-Redirect'] = reverse('ver_detalles_socio', kwargs={'pk': socio_principal.id})
            return response
            
        except Exception as e:
            import traceback
            print(traceback.format_exc()) # Esto imprimirá el error exacto en la consola
            return HttpResponse(f"Error interno: {e}", status=500)            

    # Si es GET, mostramos el formulario
    return render(request, 'app_socios/form_agregar_familiar.html', {
        'tipos_familiar': tipos_familiar,
        'familiar_socio': familiar_socio,
        'socio_principal': socio_principal
    })

def agregar_socio(request):
    if request.method == 'POST':
        form = SocioFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('socios')
    else:
        form = SocioFormulario()        
    return render(request,'app_socios/form_agregar_socio.html',{'form':form})


def transferencias_socio(request,pk):
    socio = Socios.objects.get(pk=pk)
    transferencias_como_transferentes = Transferencias.objects.filter(socio_transferente=socio)
    transferencias_como_transferido = Transferencias.objects.filter(socio_transferido=socio)
    transferencias = transferencias_como_transferentes|transferencias_como_transferido
    transferencias =transferencias.order_by('-fecha_transferencia')
    return render(request,'app_socios/transferencias_socio.html',{'socio':socio,'transferencias':transferencias})