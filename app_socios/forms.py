from django import forms
from .models import *

class SocioFormulario(forms.ModelForm):
    class Meta:
        model = Socios
        fields= ['activo_hasta','estado_actual_socio','codigo_folio','fecha_nacimiento','lugar_nacimiento','provincia','distrito','departamento','nacionalidad','profesion','ocupacion','observaciones','grado_instruccion','codigos_asociados','numero_contacto_adicional','tipo_socio','dni','apellidos','nombres','sexo','domicilio','estado_civil','numero_contacto','fecha_ingreso']
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
            ),
            'activo_hasta': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type':'date'
                }
            )
        }