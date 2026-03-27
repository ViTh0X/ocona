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
    nombre = models.CharField(max_length=50)    
    socio_relacionado = models.ForeignKey(Socios,on_delete=models.CASCADE)
    codigo_socio_asociado = models.ForeignKey(CodigosAsociadosSocio,on_delete=models.CASCADE)
    tipo_enlace_socio = models.ForeignKey(TipoEnlaceSocio,on_delete=models.CASCADE,blank=True,null=True)   
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inmuebles'
        ordering = ['id']
        
    def __str__(self):
        return self.nombre