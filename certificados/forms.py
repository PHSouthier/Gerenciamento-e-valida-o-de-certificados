import datetime
from django.db.models import fields
from django.forms.widgets import HiddenInput, Widget
from .models import Certificado
from django import forms

class FormFiltro(forms.Form):
    operacao = forms.CharField()

class FormCertificado(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['titulo', 'horas', 'data_emissao', 'categoria', 'situacao', 'imagem']

class FormLogin(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=20)
    senha = forms.CharField(widget=forms.PasswordInput, min_length=5, max_length=20)
        

