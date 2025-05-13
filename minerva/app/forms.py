from django import forms
from dal import autocomplete
from .models import Link, Articulo, EstadoClasificacion, ItemInteres

# === Formulario para carga de links por Prensa ===
class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['estado_clasificacion', 'fecha_aprobacion', 'clasificado_por']
        widgets = {
            'individuos_mencionados': autocomplete.ModelSelect2Multiple(url='individuo-autocomplete'),
            'bandas_mencionadas': autocomplete.ModelSelect2Multiple(url='banda-autocomplete'),
            'barrios_mencionados': autocomplete.ModelSelect2Multiple(url='barrio-autocomplete'),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.estado_clasificacion = EstadoClasificacion.PENDIENTE
        if commit:
            instance.save()
            self.save_m2m()
        return instance

# === Formulario para clasificación de links ===
class ClasificacionForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['estado_clasificacion']
        widgets = {
            'estado_clasificacion': forms.Select(choices=[
                (EstadoClasificacion.APROBADO, 'Aprobar'),
                (EstadoClasificacion.DESCARTADO, 'Descartar')
            ])
        }

# === Formulario para creación de artículos por Redacción ===
class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'links_usados', 'items_interes']
        widgets = {
            'links_usados': forms.CheckboxSelectMultiple,
            'items_interes': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['links_usados'].queryset = Link.objects.filter(estado_clasificacion=EstadoClasificacion.APROBADO)
        self.fields['items_interes'].queryset = ItemInteres.objects.none()  # Se puede actualizar vía JS
