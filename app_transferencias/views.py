from gettext import find
from django.contrib import messages

from django.shortcuts import redirect, render
from .models import *
from .forms import *
from datetime import datetime
# Create your views here.


def menu_transferencias(request):
    transferencias = Transferencias.objects.all()
    return render(request,'app_transferencias/menu_transferencias.html',{'transferencias':transferencias})

def agregar_transferencias(request):
    return render(request,'app_transferencias/form_agregar_transferencia_opciones.html')


def agregar_transferencias_con_inmueble(request):    
    if request.method == 'POST':
        huerto_error = request.POST.get('h_error')
        parcela_error = request.POST.get('p_error')
        huerto_validado = request.POST.get('h_validado')
        parcela_validada = request.POST.get('p_validado')
        codigo_asociado_transferencia = request.POST.get('codigo_transferencia','')
        numero_folio = request.POST.get('numero_folio') 
        fecha_trans = request.POST.get('fecha_transferencia')
        manzana_huerto = request.POST.get('manzana_h')
        lote_huerto = request.POST.get('lote_h')
        manzana_parcela = request.POST.get('manzana_p')
        lote_parcela = request.POST.get('lote_p')
        dnis_transferentes = request.POST.getlist('dni_transferente','SinDNI')
        apellidos_transferentes = request.POST.getlist('apellidos_transferente','')
        nombres_transferentes = request.POST.getlist('nombres_transferente','')
        dnis_transferidos = request.POST.getlist('dni_transferido','SinDNI')
        apellidos_transferidos = request.POST.getlist('apellidos_transferido','')
        nombres_transferidos = request.POST.getlist('nombres_transferido','')
        observaciones = request.POST.get('observaciones','')
        if huerto_error or parcela_error:
            messages.error(request, "Error no valido Huerto ni Parcela")
        if not huerto_validado or not parcela_validada:
            messages.error(request, "Debe encontrar el Huerto o Parcela")
        for d_tes,a_tes,n_tes in zip(dnis_transferentes,apellidos_transferentes,nombres_transferentes):
             # Solo intentamos crear si el DNI no viene vacío            
            if d_tes:
                d_tes = d_tes.strip()
                a_tes = a_tes.strip().upper()
                n_tes = n_tes.strip().upper()
                socio, creado = Socios.objects.get_or_create(
                    dni=d_tes, # Criterio de búsqueda (exacto)
                    defaults={
                        'apellidos': a_tes,
                        'nombres': n_tes
                    }
                )
                if creado:
                    print(f"Socio {d_tes} creado con éxito.")
                else:
                    print(f"Socio {d_tes} ya existía, no se hizo nada.")
        for d_ido,a_ido,n_ido in zip(dnis_transferidos,apellidos_transferidos,nombres_transferidos):
             # Solo intentamos crear si el DNI no viene vacío
            if d_ido:
                print("ingreso al if")
                d_ido = d_ido.strip()
                a_ido = a_ido.strip()
                n_ido = n_ido.strip()
                socio, creado = Socios.objects.get_or_create(
                    dni=d_ido, # Criterio de búsqueda (exacto)
                    defaults={
                        'apellidos': a_ido,
                        'nombres': n_ido
                    }
                )
                if creado:
                    print(f"Socio {d_tes} creado con éxito.")
                else:
                    print(f"Socio {d_tes} ya existía, no se hizo nada.")
        dni_transferente = dnis_transferentes[0]
        dni_transferido = dnis_transferidos[0]            
        transferente =  Socios.objects.get(dni=dni_transferente.strip())
        transferido = Socios.objects.get(dni=dni_transferido.strip())
        huerto = Inmuebles.objects.filter(manzana=manzana_huerto,lote=lote_huerto).first()
        parcela = Inmuebles.objects.filter(manzana=manzana_parcela,lote=lote_parcela).first()
        transferencia_identificada = TipoTransferencias.objects.get(pk=1)
        if fecha_trans:
            fecha_transferencia = datetime.strptime(fecha_trans, '%Y-%m-%d')
        else:
            messages.error(request, "La fecha de transferencia es obligatoria.")
        if huerto and parcela:                   
            nueva_transferencia = Transferencias.objects.create(
                codigo_documento = numero_folio,
                tipo_transferencia = transferencia_identificada,
                codigo_relacionado_transferencia = codigo_asociado_transferencia,
                inmueble_huerto = huerto,
                inmueble_parcela = parcela,
                socio_transferente = transferente,
                socio_transferido = transferido,
                fecha_transferencia = fecha_transferencia,
                observaciones = observaciones                                                                                
            )
            for dnis in dnis_transferentes:
                socio=Socios.objects.get(dni=dnis.strip())
                RelacionPersonasTransferencias.objects.create(
                    transferencia = nueva_transferencia,
                    socio=socio,
                    tipo='Transferente'                
                )
            for dnis in dnis_transferidos:
                socio=Socios.objects.get(dni=dnis.strip())
                RelacionPersonasTransferencias.objects.create(
                    transferencia = nueva_transferencia,
                    socio=socio,
                    tipo='Transferido'                
                ) 
        if huerto and not parcela:                   
            nueva_transferencia = Transferencias.objects.create(
                codigo_documento = numero_folio,
                tipo_transferencia = transferencia_identificada,
                codigo_relacionado_transferencia = codigo_asociado_transferencia,
                inmueble_huerto = huerto,
                socio_transferente = transferente,
                socio_transferido = transferido,
                fecha_transferencia = fecha_transferencia,
                observaciones = observaciones                                                                                
            )
            for dnis in dnis_transferentes:
                socio=Socios.objects.get(dni=dnis.strip())
                RelacionPersonasTransferencias.objects.create(
                    transferencia = nueva_transferencia,
                    socio=socio,
                    tipo='Transferente'                
                )
            for dnis in dnis_transferidos:
                socio=Socios.objects.get(dni=dnis.strip())
                RelacionPersonasTransferencias.objects.create(
                    transferencia = nueva_transferencia,
                    socio=socio,
                    tipo='Transferido'                
                ) 
        if not huerto and parcela:
            nueva_transferencia = Transferencias.objects.create(
                codigo_documento = numero_folio,
                tipo_transferencia = transferencia_identificada,
                codigo_relacionado_transferencia = codigo_asociado_transferencia,
                inmueble_parcela = parcela,
                socio_transferente = transferente,
                socio_transferido = transferido,
                fecha_transferencia = fecha_transferencia,
                observaciones = observaciones                                                                                
            )
            for dnis in dnis_transferentes:
                socio=Socios.objects.get(dni=dnis.strip())
                RelacionPersonasTransferencias.objects.create(
                    transferencia = nueva_transferencia,
                    socio=socio,
                    tipo='Transferente'                
                )
            for dnis in dnis_transferidos:
                socio=Socios.objects.get(dni=dnis.strip())
                RelacionPersonasTransferencias.objects.create(
                    transferencia = nueva_transferencia,
                    socio=socio,
                    tipo='Transferido'                
                )
        #Creando el registro del movimiento
        tipo_conyugue = TipoFamiliar.objects.get(pk=1)
        ################################
        if len(dnis_transferentes) > 1:
            dni_conyugue_transferente = dnis_transferentes[1]
            conyugue_transferente =  Socios.objects.get(dni=dni_conyugue_transferente.strip())
            PersonasRelacionadasSocio.objects.create(
                socio_asociado = transferente,
                apellidos = conyugue_transferente.apellidos,
                nombres = conyugue_transferente.nombres,
                tipo_familiar = tipo_conyugue,
                dni = conyugue_transferente.dni
            )
        if len(dnis_transferidos) > 1:
            dni_conyugue_transferido = dnis_transferidos[1]
            conyugue_transferido = Socios.objects.get(dni=dni_conyugue_transferido.strip())
            PersonasRelacionadasSocio.objects.create(
                socio_asociado = transferido,
                apellidos = conyugue_transferido.apellidos,
                nombres = conyugue_transferido.nombres,
                tipo_familiar = tipo_conyugue,
                dni = conyugue_transferido.dni
            )
        return redirect('menu_transferencias')
    return render(request,'app_transferencias/form_agregar_transferencia_con_inmueble.html')


def agregar_transferencias_sin_inmueble(request):    
    if request.method == 'POST':
        codigo_asociado_transferencia = request.POST.get('codigo_transferencia','')
        numero_folio = request.POST.get('numero_folio') 
        fecha_trans = request.POST.get('fecha_transferencia')
        dnis_transferentes = request.POST.getlist('dni_transferente','SinDNI')
        apellidos_transferentes = request.POST.getlist('apellidos_transferente','')
        nombres_transferentes = request.POST.getlist('nombres_transferente','')
        dnis_transferidos = request.POST.getlist('dni_transferido','SinDNI')
        apellidos_transferidos = request.POST.getlist('apellidos_transferido','')
        nombres_transferidos = request.POST.getlist('nombres_transferido','')
        observaciones = request.POST.get('observaciones','')
        for d_tes,a_tes,n_tes in zip(dnis_transferentes,apellidos_transferentes,nombres_transferentes):
             # Solo intentamos crear si el DNI no viene vacío            
            if d_tes:
                d_tes = d_tes.strip()
                a_tes = a_tes.strip().upper()
                n_tes = n_tes.strip().upper()
                socio, creado = Socios.objects.get_or_create(
                    dni=d_tes, # Criterio de búsqueda (exacto)
                    defaults={
                        'apellidos': a_tes,
                        'nombres': n_tes
                    }
                )
                if creado:
                    print(f"Socio {d_tes} creado con éxito.")
                else:
                    print(f"Socio {d_tes} ya existía, no se hizo nada.")
        for d_ido,a_ido,n_ido in zip(dnis_transferidos,apellidos_transferidos,nombres_transferidos):
             # Solo intentamos crear si el DNI no viene vacío
            if d_ido:
                d_ido = d_ido.strip()
                a_ido = a_ido.strip()
                n_ido = n_ido.strip()
                socio, creado = Socios.objects.get_or_create(
                    dni=d_ido, # Criterio de búsqueda (exacto)
                    defaults={
                        'apellidos': a_ido,
                        'nombres': n_ido
                    }
                )
                if creado:
                    print(f"Socio {d_tes} creado con éxito.")
                else:
                    print(f"Socio {d_tes} ya existía, no se hizo nada.")
        dni_transferente = dnis_transferentes[0]
        dni_transferido = dnis_transferidos[0]            
        transferente =  Socios.objects.get(dni=dni_transferente.strip())
        transferido = Socios.objects.get(dni=dni_transferido.strip())
        transferencia_no_identificada = TipoTransferencias.objects.get(pk=2)
        if fecha_trans:
            fecha_transferencia = datetime.strptime(fecha_trans, '%Y-%m-%d')
        else:
            messages.error(request, "La fecha de transferencia es obligatoria.")     
        nueva_transferencia = Transferencias.objects.create(
            codigo_documento = numero_folio,
            tipo_transferencia = transferencia_no_identificada,
            codigo_relacionado_transferencia = codigo_asociado_transferencia,
            socio_transferente = transferente,
            socio_transferido = transferido,
            fecha_transferencia = fecha_transferencia,
            observaciones = observaciones                                                                                
        )
        #Relacion de personas a transferencia
        for dnis in dnis_transferentes:
            socio=Socios.objects.get(dni=dnis.strip())
            RelacionPersonasTransferencias.objects.create(
                transferencia = nueva_transferencia,
                socio=socio,
                tipo='Transferente'                
            )
        for dnis in dnis_transferidos:
            socio=Socios.objects.get(dni=dnis.strip())
            RelacionPersonasTransferencias.objects.create(
                transferencia = nueva_transferencia,
                socio=socio,
                tipo='Transferido'                
            ) 
        #Creando los fammiliares
        tipo_conyugue = TipoFamiliar.objects.get(pk=1)
        if len(dnis_transferentes) > 1:
            dni_conyugue_transferente = dnis_transferentes[1]
            conyugue_transferente =  Socios.objects.get(dni=dni_conyugue_transferente.strip())            
        ################################
            PersonasRelacionadasSocio.objects.create(
                socio_asociado = transferente,
                apellidos = conyugue_transferente.apellidos,
                nombres = conyugue_transferente.nombres,
                tipo_familiar = tipo_conyugue,
                dni = conyugue_transferente.dni
            )
        if len(dnis_transferidos) > 1:
            dni_conyugue_transferido = dnis_transferidos[1]
            conyugue_transferido = Socios.objects.get(dni=dni_conyugue_transferido.strip())
            PersonasRelacionadasSocio.objects.create(
                socio_asociado = transferido,
                apellidos = conyugue_transferido.apellidos,
                nombres = conyugue_transferido.nombres,
                tipo_familiar = tipo_conyugue,
                dni = conyugue_transferido.dni
            )
        return redirect('menu_transferencias')
    return render(request,'app_transferencias/form_agregar_transferencia_sin_inmueble.html')

def buscar_huertos(request):      
    data_manzana = request.GET.get('manzana_h').upper()
    data_lote = request.GET.get('lote_h')
    print(data_manzana)
    print(data_lote)
    if data_manzana and data_lote:
        inmueble = Inmuebles.objects.filter(manzana=data_manzana,lote=data_lote).first()
    else:
        messages.error(request, "Debe llenar ambos campos de manera obligatoria")
    if inmueble:
        print("lo valido")
        return render(request,'app_transferencias/fragmento_validar_huerto.html',{'inmueble':inmueble})
    else:
        print("no lo valido")
        return render(request,'app_transferencias/fragmento_validar_huerto_error.html',{'data_manzana':data_manzana,'data_lote':data_lote})

def buscar_parcelas(request):      
    data_manzana = request.GET.get('manzana_p').upper()
    data_lote = request.GET.get('lote_p')
    print(data_manzana)
    print(data_lote)
    if data_manzana and data_lote:
        inmueble = Inmuebles.objects.filter(manzana=data_manzana,lote=data_lote).first()
    else:
        messages.error(request, "Debe llenar ambos campos de manera obligatoria")
    if inmueble:
        print("lo valido")
        return render(request,'app_transferencias/fragmento_validar_parcela.html',{'inmueble':inmueble})
    else:
        print("no lo valido")
        return render(request,'app_transferencias/fragmento_validar_parcela_error.html',{'data_manzana':data_manzana,'data_lote':data_lote})

def mas_transferentes(request):
    return render(request,'app_transferencias/fragmento_transferente.html')

def mas_transferidos(request):
    return render(request,'app_transferencias/fragmento_transferido.html')

def editar_transferencia(request,pk,socio_id=None):
    if socio_id != None:
        socio = Socios.objects.get(pk=socio_id)
        transferencia = Transferencias.objects.get(pk=pk)
        if request.method == 'POST':
            print("Entro al POST")
            form = TransferenciaFormulario(request.POST,instance=transferencia)
            if form.is_valid():
                print("Es valido")
                form.save()
                print("Formulario se guardo")
                return redirect('transferencias_socio',pk=socio.id)
            else:
                print(f"No es valido{form.errors}")
        else:
            form = TransferenciaFormulario(instance=transferencia)
        return render(request,'app_transferencias/form_editar_transferencia.html',{'transferencia':transferencia,'form':form})
    else:
        transferencia = Transferencias.objects.get(pk=pk)
        if request.method == 'POST':
            print("Entro al POST")
            form = TransferenciaFormulario(request.POST,instance=transferencia)
            if form.is_valid():
                print("Es valido")
                form.save()
                print("Formulario se guardo")
                return redirect('menu_transferencias')
            else:
                print(f"No es valido{form.errors}")
        else:
            form = TransferenciaFormulario(instance=transferencia)
        return render(request,'app_transferencias/form_editar_transferencia.html',{'transferencia':transferencia,'form':form})
        
 