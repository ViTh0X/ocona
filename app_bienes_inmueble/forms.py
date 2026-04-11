from django import forms
from .models import *


class HuertoFormulario(forms.ModelForm):
    class Meta:
        model = Inmuebles
        fields = ['manzana','lote','socio_poseedor_actual']