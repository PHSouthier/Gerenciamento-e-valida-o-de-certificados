import datetime
from django.contrib.auth.backends import UserModel
from django.db.models import fields
from django.forms.widgets import HiddenInput, Widget
from .models import Categoria, Certificado
from django import forms

class FormFiltro(forms.Form):
    operacao = forms.CharField()

class FormValidarCertificado(forms.Form):
    operacao = forms.CharField()

class FormCertificado(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['titulo', 'horas', 'data_emissao', 'categoria', 'imagem']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(FormCertificado, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(curso=user.perfil.curso)

class FormLogin(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=20)
    senha = forms.CharField(widget=forms.PasswordInput, min_length=5, max_length=20)
        

