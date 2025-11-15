from django.forms import ModelForm, Textarea
from .models import Resenia

class ReviewForm(ModelForm):
    class Meta:
        model = Resenia
        fields = ['estrellas','comentario']

        widgets = {
            'comentario' : Textarea(attrs={"rows":4, "style": "resize:none"})

        }

        labels = {
            'estrellas':'Puntuación',
            'comentario':'Comentario'
        }