from django import forms
from .models import *

class SocioFormulario(forms.ModelForm):
    class Meta:
        model = Socios
        fields= ['codigo_folio','fecha_nacimiento','lugar_nacimiento','provincia','distrito','departamento','nacionalidad','profesion','ocupacion','centro_trabajo','grado_instruccion','correo','numero_contacto_adicional','tipo_socio','dni','apellidos','nombres','sexo','domicilio','estado_civil','numero_contacto','fecha_ingreso']
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type':'date'
                }
            ),
            'fecha_ingreso': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type':'date'
                }
            )
        }