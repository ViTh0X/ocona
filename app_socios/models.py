from django.db import models

# Create your models here.
class TipoSocio(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=15)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tipo_socios'

    def __str__(self):
        return self.denominacion

class TipoSexos(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=15)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tipo_sexos'

    def __str__(self):
        return self.denominacion
    
    
class TipoEstadosCivil(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=15)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tipo_estados_civil'

    def __str__(self):
        return self.denominacion
        
class EstadosSocio(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=15)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'estados_socio'

    def __str__(self):
        return self.denominacion


class Socios(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_folio = models.IntegerField(blank=True,null=True)        
    tipo_socio = models.ForeignKey(TipoSocio,on_delete=models.CASCADE,blank=True,null=True)    
    apellidos = models.CharField(max_length=120)
    nombres = models.CharField(max_length=120)    
    dni = models.CharField(max_length=12,blank=True,null=True)
    sexo =  models.ForeignKey(TipoSexos,on_delete=models.CASCADE,blank=True,null=True)
    domicilio = models.CharField(max_length=180,blank=True,null=True)
    estado_civil = models.ForeignKey(TipoEstadosCivil,on_delete=models.CASCADE,blank=True,null=True)
    numero_contacto = models.CharField(max_length=15,default=0,blank=True,null=True)
    fecha_ingreso = models.DateField(null=True,blank=True)
    ##Nuevos
    fecha_nacimiento = models.DateField(null=True,blank=True)
    lugar_nacimiento = models.CharField(max_length=50,null=True,blank=True)
    provincia = models.CharField(max_length=50,null=True,blank=True)
    distrito = models.CharField(max_length=50,null=True,blank=True)
    departamento = models.CharField(max_length=50,null=True,blank=True)
    nacionalidad = models.CharField(max_length=50,null=True,blank=True)
    profesion = models.CharField(max_length=50,null=True,blank=True)
    ocupacion = models.CharField(max_length=50,null=True,blank=True)
    centro_trabajo = models.CharField(max_length=100,null=True,blank=True)
    grado_instruccion = models.CharField(max_length=50,null=True,blank=True)
    correo = models.CharField(max_length=100,null=True,blank=True)
    numero_contacto_adicional = models.CharField(max_length=50,null=True,blank=True)
    activo_hasta = models.DateField(null=True,blank=True) 
    estado_actual_socio = models.ForeignKey(EstadosSocio,on_delete=models.CASCADE,blank=True,null=True)
    #fin de nuevos    
    
    fecha_modificacion = models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        db_table = 'socios'
        
    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


class TipoFamiliar(models.Model):
    id = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=15)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tipo_familiar'

    def __str__(self):
        return self.denominacion
    

class CodigosAsociadosSocio(models.Model):
    id = models.AutoField(primary_key=True)
    socio_asociado = models.ForeignKey(Socios,on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'codigos_asociados_socio'
        
    def __str__(self):
        if self.codigo == '':
            return "SinCodigo"    
        else:
            return self.codigo
    
    
class PersonasRelacionadasSocio(models.Model):
    id = models.AutoField(primary_key=True)
    socio_asociado = models.ForeignKey(Socios,on_delete=models.CASCADE)
    apellidos = models.CharField(max_length=40)
    nombres = models.CharField(max_length=40)
    tipo_familiar = models.ForeignKey(TipoFamiliar,on_delete=models.CASCADE,blank=True,null=True)
    es_socio = models.CharField(max_length=10,null=True,blank=True)
    dni = models.CharField(max_length=12,null=True,blank=True)    
    fecha_nacimiento = models.DateField(null=True,blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'personas_relacionadas_socio'
        
    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"

