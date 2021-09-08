from certificados.models import Certificado
from django.contrib import admin
from .models import Categoria, Certificado, Curso, Perfil

admin.site.register(Certificado)
admin.site.register(Categoria)
admin.site.register(Curso)
admin.site.register(Perfil)