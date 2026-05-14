from django.db import models
from app_socios.models import *
from app_bienes_inmueble.models import *

# Create your models here.
class TipoTransferencias(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=30)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta: 
        
        db_table ='tipo_transferencias'        
    
    def __str__(self):
        return self.denominacion
    
class CategoriaTransferencia(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=30)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta: 
        
        db_table ='categoria_transferencia'        
    
    def __str__(self):
        return self.denominacion

class Transferencias(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_documento = models.IntegerField()
    tipo_transferencia = models.ForeignKey(TipoTransferencias,on_delete=models.CASCADE,blank=True,null=True)
    categoria_transferencia = models.ForeignKey(CategoriaTransferencia,on_delete=models.CASCADE,blank=True,null=True)
    codigo_relacionado_transferencia =  models.CharField(max_length=10,blank=True,null=True)
    inmueble_huerto = models.ForeignKey(Inmuebles,on_delete=models.CASCADE,blank=True,null=True,related_name='transferencia_huerto')
    inmueble_parcela = models.ForeignKey(Inmuebles,on_delete=models.CASCADE,blank=True,null=True,related_name='transferencia_parcela')
    socio_transferente = models.ForeignKey(Socios,on_delete=models.CASCADE,related_name='transferente')
    socio_transferido = models.ForeignKey(Socios,on_delete=models.CASCADE,related_name='transferido')
    fecha_transferencia = models.DateField()
    observaciones = models.CharField(max_length=300,blank=True,null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)    
    
    class Meta:
        db_table = 'transferencias'
        ordering = ['codigo_documento']
        
    def __str__(self):
        return self.inmueble


class RelacionPersonasTransferencias(models.Model):
    id = models.AutoField(primary_key=True)
    transferencia=models.ForeignKey(Transferencias,on_delete=models.CASCADE)
    socio=models.ForeignKey(Socios,on_delete=models.CASCADE)
    tipo=models.CharField(max_length=15)
    
    class Meta:
        db_table = 'relacion_personas_transferencias'
    
    
    def __str__(self):
        return f"{self.transferencia}{self.socio}"
    
    