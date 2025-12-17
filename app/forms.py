from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Resenia, Usuario

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

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            'username': 'Nombre de usuario',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email