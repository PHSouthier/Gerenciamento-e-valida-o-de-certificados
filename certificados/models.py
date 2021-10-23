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

    def horas_concluidas(self):
        horas_aprovado = 0
        categoria_atual = ''
        horas_categoria_atual = 0
        todas_categorias = []
        horas_categorias = []
        certificados = Certificado.objects.filter(usuario=self.user)
        categorias = Categoria.objects.filter(curso=self.curso)
        for c in categorias:
            horas_categorias.append(c.limite_horas)
            todas_categorias.append(c.nome)
        for c in certificados:
            if c.situacao == 1:
                for i in range(len(categorias)):
                    categoria_atual = todas_categorias[i]
                    horas_categoria_atual = horas_categorias[i]
                    if(categoria_atual == c.categoria.nome):
                        if(horas_categoria_atual <= c.horas and c.horas >= 0):
                            horas_aprovado = horas_aprovado + horas_categoria_atual
                            horas_categorias[i] = 0
                        else:
                            if(horas_categoria_atual > 0 and c.horas >= 0):       
                                horas_aprovado = horas_aprovado + c.horas
                                horas_categorias[i] = horas_categorias[i] - c.horas
                            else:
                                pass
                    else:
                        pass
        
        return horas_aprovado
    
    def horas_concluidas_categorias(self):
        categoria_atual = ''
        todas_categorias = []
        horas_categorias = []
        categoria_limites_horas = []
        horas_and_categorias = []
        certificados = Certificado.objects.filter(usuario=self.user)
        categorias = Categoria.objects.filter(curso=self.curso)
        for c in categorias:
            horas_categorias.append(0)
            todas_categorias.append(c.nome)
            categoria_limites_horas.append(c.limite_horas)
        for c in certificados:
            if c.situacao == 1:
                for i in range(len(categorias)):
                    categoria_atual = todas_categorias[i]
                    if(categoria_atual == c.categoria.nome):
                        horas_categorias[i] = horas_categorias[i] + c.horas 
                    else:
                        pass
            else:
                pass

        for i in range(len(categorias)):
            horas_and_categorias.append({'categoria': todas_categorias[i], 'horas': horas_categorias[i], 'limite_horas': categoria_limites_horas[i]})


        return horas_and_categorias 

    def percentual_integralizado(self):
        return int((self.horas_concluidas()/self.curso.quantidade_horas)*100)