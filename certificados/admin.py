from certificados.models import Certificado
from django.contrib import admin
from .models import Categoria, Certificado

admin.site.register(Certificado)
admin.site.register(Categoria)