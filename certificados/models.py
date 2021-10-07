from django.contrib.auth.backends import UserModel
from django.db import models
from django.utils import timezone
from .validators import validate_file_extension

class Certificado(models.Model):
    horas = models.IntegerField()
    titulo = models.CharField(max_length=150)
    data_emissao = models.DateTimeField()
    data_envio = models.DateTimeField(default=timezone.now)
    situacao = models.SmallIntegerField(default = 2)
    imagem = models.FileField(
        upload_to = 'certificados/',
        validators=[validate_file_extension]
    )
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + " (" + str(self.id) + ")"

    def tamanho_titulo(self):
        t = len(self.titulo)

        if t <= 120:
            return self.titulo[0:120]
        else:
            return self.titulo[0:117] + "..."
    
    def tamanho_autor(self):
        a = len(self.usuario.first_name + " " + self.usuario.last_name)

        if a <= 100:
            return (self.usuario.first_name + " " + self.usuario.last_name)[0:100]
        else:
            return (self.usuario.first_name + " " + self.usuario.last_name)[0:97] + "..."
        
    def pdf(self):
        return self.imagem.name.endswith('.pdf')
    
class Categoria(models.Model):
    nome = models.CharField(max_length=170)
    limite_horas = models.IntegerField()
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome + " (" + str(self.limite_horas) + ")"

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    quantidade_horas = models.IntegerField()

    def __str__(self):
        return self.nome + " (" + str(self.quantidade_horas) + ")"

class Perfil(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    matricula = models.IntegerField()
    turma = models.IntegerField()
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name