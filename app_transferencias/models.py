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

class Transferencias(models.Model):
    id = models.AutoField(primary_key=True)
    inmueble = models.ForeignKey(Inmuebles,on_delete=models.CASCADE,blank=True,null=True)
    socio_transferente = models.ForeignKey(Socios,on_delete=models.CASCADE)
    socio_transferido = models.ForeignKey(Socios,on_delete=models.CASCADE)
    fecha_transferencia = models.DateField()
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transferencias'
        
    def __str__(self):
        return self.inmueble
    