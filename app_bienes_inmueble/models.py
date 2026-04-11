from django.db import models
from app_socios.models import *

# Create your models here.

class TipoInmueble(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=30)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta: 
        
        db_table ='tipo_inmueble'        
    
    def __str__(self):
        return self.denominacion
    

class TipoEnlaceSocio(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=30)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta: 
        
        db_table ='tipo_enlace_socio'        
    
    def __str__(self):
        return self.denominacion
    
    
class Inmuebles(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(TipoInmueble,on_delete=models.CASCADE)
    manzana = models.CharField(max_length=10)    
    lote = models.CharField(max_length=10)    
    socio_poseedor_actual = models.ForeignKey(Socios,on_delete=models.CASCADE,blank=True,null=True)    
    tipo_enlace_socio = models.ForeignKey(TipoEnlaceSocio,on_delete=models.CASCADE,blank=True,null=True)   
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inmuebles'
        ordering = ['manzana']
        
    def __str__(self):
        return f"{self.manzana}-{self.lote}"
            