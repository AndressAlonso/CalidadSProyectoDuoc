from django import forms

class ProductoFilterForm(forms.Form):
    FECHA_CHOICES = [
        ('mes', 'Este Mes'),
        ('dia', 'Este Dia'),
        ('ano', 'Este Año'),
    ]
    TIPO_CHOICES = [
        ('semilla', 'Semilla'),
        ('insumo', 'Insumo'),
    ]
    ORDEN_CHOICES = [
        ('precio_desc', 'Precio Mayor a Menor'),
        ('precio_asc', 'Precio Menor a Mayor'),
        ('vendidos_desc', 'Más Vendidos'),
        ('vendidos_asc', 'Menos Vendidos'),
    ]

    fecha_subida = forms.ChoiceField(choices=FECHA_CHOICES, required=False)
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=False)
    ordenar = forms.ChoiceField(choices=ORDEN_CHOICES, required=False)
