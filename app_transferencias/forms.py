from django import forms
from .models import *


class TransferenciaFormulario(forms.ModelForm):
    class Meta:
        model=Transferencias
        fields=['codigo_documento','categoria_transferencia','tipo_transferencia','codigo_relacionado_transferencia','inmueble_huerto','inmueble_parcela','socio_transferente','socio_transferido','fecha_transferencia','observaciones']
        widgets={
            'fecha_transferencia':forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type':'date'
                }
            ),
            'observaciones':forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Añada alguna observacion...'
                }
            )
        }
    def __init__(self, *args, **kwargs):
        super(TransferenciaFormulario, self).__init__(*args, **kwargs)
        
        # Supongamos que en tu modelo Inmuebles tienes un campo llamado 'tipo'
        # Ajusta el filtro según tu lógica real (ej. tipo='HUERTO' o tipo_id=1)
        
        self.fields['inmueble_huerto'].queryset = Inmuebles.objects.filter(tipo=1)
        self.fields['inmueble_parcela'].queryset = Inmuebles.objects.filter(tipo=2)