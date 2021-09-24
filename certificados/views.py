from django.contrib import messages
from django.contrib.auth.backends import UserModel
from certificados.forms import FormCertificado, FormFiltro, FormLogin, FormValidarCertificado
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Certificado, Perfil
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            lista_certificados = Certificado.objects.order_by("-data_envio").filter(curso=request.user.perfil.curso)[0:10]
        else:
            lista_certificados = Certificado.objects.filter(usuario=request.user).order_by("-data_envio")[0:10]
        
        situacao = ["Aprovado", "Pendente", "Recusado", "Erro"]
        contexto = {'lista_certificados': lista_certificados, 'situacao':situacao}
        return render(request, 'certificados/index.html', contexto)
    else:
        return HttpResponseRedirect("/certificados/login/")

def mostrar_todos_certificados(request):
    if request.user.is_authenticated:
        operacao = ''
        if request.method == "POST":
            form = FormFiltro(request.POST)
            if form.is_valid():
                operacao = form.cleaned_data['operacao']

                if operacao == "data_emissao":
                    if request.user.is_superuser:
                        lista_certificados = Certificado.objects.order_by("-data_emissao").filter(curso=request.user.perfil.curso)
                    else:
                        lista_certificados = Certificado.objects.filter(usuario=request.user).order_by("-data_emissao")
                elif operacao == "autor":
                    if request.user.is_superuser:
                        lista_certificados = Certificado.objects.order_by("usuario").filter(curso=request.user.perfil.curso)
                    else:
                        lista_certificados = Certificado.objects.filter(usuario=request.user).order_by("usuario")
                elif operacao == "data_envio":
                    if request.user.is_superuser:
                        lista_certificados = Certificado.objects.order_by("-data_envio").filter(curso=request.user.perfil.curso)
                    else:
                        lista_certificados = Certificado.objects.filter(usuario=request.user).order_by("-data_envio")
                elif operacao == "titulo":
                    if request.user.is_superuser:
                        lista_certificados = Certificado.objects.order_by("titulo").filter(curso=request.user.perfil.curso)
                    else:
                        lista_certificados = Certificado.objects.filter(usuario=request.user).order_by("titulo")
                elif operacao == "horas":
                    if request.user.is_superuser:
                        lista_certificados = Certificado.objects.order_by("-horas").filter(curso=request.user.perfil.curso)
                    else:
                        lista_certificados = Certificado.objects.filter(usuario=request.user).order_by("-horas")
                elif operacao == "situacao":
                    if request.user.is_superuser:
                        lista_certificados = Certificado.objects.order_by("situacao").filter(curso=request.user.perfil.curso)
                    else:
                        lista_certificados = Certificado.objects.filter(usuario=request.user).order_by("situacao")
                else:
                    if request.user.is_superuser:
                        lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso)
                    else:
                        lista_certificados = Certificado.objects.filter(usuario=request.user)
        else:
            form = FormFiltro()
            if request.user.is_superuser:
                lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso)
            else:
                lista_certificados = Certificado.objects.filter(usuario=request.user)

        formulario = "certificados"
        horas_aprovado = 0
        horas_pendente = 0
        horas_recusado = 0
        for p in lista_certificados:
            if p.situacao == 1:
                horas_aprovado = horas_aprovado + p.horas
            elif p.situacao == 2:
                horas_pendente = horas_pendente + p.horas
            elif p.situacao == 3:
                horas_recusado = horas_recusado + p.horas

        situacao = ["Aprovado", "Pendente", "Recusado", "Erro"]
        contexto = {'lista_certificados': lista_certificados, 'situacao': situacao, 'form': form, 'horas_aprovado': horas_aprovado, 'horas_pendente': horas_pendente, 'horas_recusado': horas_recusado, 'formulario': formulario}
        return render(request, 'certificados/certificados.html', contexto)
    else:
        return HttpResponseRedirect("/certificados/login/")

def novo_certificado(request):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            if request.method == 'POST':
                form = FormCertificado(request.POST, request.FILES, user=request.user)
                if form.is_valid():
                    c = form.save(commit=False)
                    c.usuario = request.user
                    c.curso = request.user.perfil.curso
                    c.save()

                    messages.success(request, "O certificado foi salvo com sucesso!")
                    return HttpResponseRedirect('/certificados/novo_certificado/')
                else:
                    messages.error(request, "Preencha corretamente o formulário.")
            else:
                form = FormCertificado(user=request.user)

            contexto = {'form': form}
            return render(request, 'certificados/novo_certificado.html', contexto)
        else:
            return HttpResponseRedirect('/certificados/')
    else:
        return HttpResponseRedirect("/certificados/login/")

def fazer_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/certificados/")

    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=usuario, password=senha) # retorna None se o usuário não é válido
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/certificados/")
            else:
                messages.error(request, "Usuário e/ou senha incorretos. Tente de novo.")
        else:
            messages.error(request, "Preencha corretamento o formulário")

    else:
        form = FormLogin()

    contexto = {"form": form}
    return render(request, 'certificados/login.html', contexto)

def fazer_logout(request):
    logout(request)
    return HttpResponseRedirect("/certificados/login/")

def ver_certificado(request, id):
    if request.user.is_authenticated:
        c = Certificado.objects.get(id=id)
        if c.usuario == request.user or request.user.is_superuser:
            form = FormValidarCertificado()
            situacao = ["Aprovado", "Pendente", "Recusado", "Erro"]
            link = 'ver-certificado'
            userDeletar = False
            if c.usuario == request.user:
                if c.situacao == 2:
                    userDeletar = True
                else:
                    pass
            else:
                pass
            contexto = {'c': c, 'situacao': situacao, 'form': form, 'link': link, 'userDeletar': userDeletar}
            return render(request, 'certificados/certificado.html', contexto)
        else:
            return HttpResponseRedirect("/certificados/")
    else:
        return HttpResponseRedirect("/certificados/login/")

def validar(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            operacao = ''
            if request.method == "POST":
                form = FormFiltro(request.POST)
                if form.is_valid():
                    operacao = form.cleaned_data['operacao']

                    if operacao == "data_emissao":
                        lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso).order_by("-data_emissao").filter(situacao=2)
                    elif operacao == "autor":
                        lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso).order_by("usuario").filter(situacao=2)
                    elif operacao == "data_envio":
                        lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso).order_by("-data_envio").filter(situacao=2)
                    elif operacao == "titulo":
                        lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso).order_by("titulo").filter(situacao=2)
                    elif operacao == "horas":
                        lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso).order_by("-horas").filter(situacao=2)
                    else:
                        lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso).filter(situacao=2)
            else:
                form = FormFiltro()
                lista_certificados = Certificado.objects.filter(curso=request.user.perfil.curso).filter(situacao=2)

            formulario = "validar"
            situacao = ["Aprovado", "Pendente", "Recusado", "Erro"]
            contexto = {'lista_certificados': lista_certificados, 'situacao': situacao, 'form': form, 'formulario': formulario}
            return render(request, 'certificados/certificados.html', contexto)
        else:
            return HttpResponseRedirect("/certificados/")
    else:
        return HttpResponseRedirect("/certificados/login/")

def validar_certificado(request, id):
    if request.user.is_authenticated:
        c = Certificado.objects.get(id=id)
        if request.user.is_superuser:
            if request.user.perfil.curso == c.curso:
                operacao = ''
                certificados = Certificado.objects.filter(curso=request.user.perfil.curso).filter(situacao=2).order_by("id")[0:1]
                if request.method == "POST":
                    form = FormValidarCertificado(request.POST)
                    if form.is_valid():
                        operacao = form.cleaned_data['operacao']

                        if operacao == "recusar":
                            c.situacao = 3
                            c.save()
                        elif operacao == "aprovar":
                            c.situacao = 1
                            c.save()
                        elif operacao == "deletar":
                            c.delete()
                            messages.success(request, "Certificado deletado com sucesso!")
                            return HttpResponseRedirect("/certificados/todos/")
                        elif operacao == "aprovar-proximo":
                            c.situacao = 1
                            c.save()
                            if certificados:
                                proximo = Certificado.objects.get(id=certificados)
                                return HttpResponseRedirect(f"/certificados/{proximo.id}")
                            else:
                                messages.success(request, "Todos certificados já foram validados!")
                                return HttpResponseRedirect("/certificados/todos/")
                        else:
                            return HttpResponseRedirect(f"/certificados/{id}")
                    else:
                        return HttpResponseRedirect(f"/certificados/{id}")
                else:
                    return HttpResponseRedirect(f"/certificados/{id}")

                if certificados:
                    messages.success(request, "Certificado validado com sucesso!")
                    return HttpResponseRedirect("/certificados/validar/")
                else:
                    messages.success(request, "Todos certificados já foram validados!")
                    return HttpResponseRedirect("/certificados/todos/")
            else:
                return HttpResponseRedirect(f"/certificados/{id}")
        else:
            if c.usuario == request.user:
                if c.situacao == 2:
                    operacao = ''
                    if request.method == "POST":
                        form = FormValidarCertificado(request.POST)
                        if form.is_valid():
                            operacao = form.cleaned_data['operacao']

                            if operacao == "deletar":
                                c.delete()
                                messages.success(request, "Certificado deletado com sucesso!")
                                return HttpResponseRedirect("/certificados/todos/")
                            else:
                                return HttpResponseRedirect(f"/certificados/{id}")
                        else:
                            return HttpResponseRedirect(f"/certificados/{id}")
                    else:
                        return HttpResponseRedirect(f"/certificados/{id}")
                else:
                    return HttpResponseRedirect(f"/certificados/{id}")
            else:
                return HttpResponseRedirect("/certificados/")
    else:
        return HttpResponseRedirect("/certificados/login/")

def perfil(request):
    if request.user.is_authenticated:
        u = request.user
        return HttpResponseRedirect(f"/certificados/usuario/{u.id}")
    else:
        return HttpResponseRedirect("/certificados/login/")

def usuario(request, id):
    if request.user.is_authenticated:
        if request.user.id == id or request.user.is_superuser:
            u = UserModel.objects.get(id=id)
            operacao = ''
            if request.method == "POST":
                form = FormFiltro(request.POST)
                if form.is_valid():
                    operacao = form.cleaned_data['operacao']

                    if operacao == "data_emissao":
                        lista_certificados = Certificado.objects.filter(usuario=u).order_by("-data_emissao")
                    elif operacao == "data_envio":
                        lista_certificados = Certificado.objects.filter(usuario=u).order_by("-data_envio")
                    elif operacao == "titulo":
                        lista_certificados = Certificado.objects.filter(usuario=u).order_by("titulo")
                    elif operacao == "horas":
                        lista_certificados = Certificado.objects.filter(usuario=u).order_by("-horas")
                    elif operacao == "situacao":
                        lista_certificados = Certificado.objects.filter(usuario=u).order_by("situacao")
                    else:
                        lista_certificados = Certificado.objects.filter(usuario=u)
            else:
                form = FormFiltro()
                lista_certificados = Certificado.objects.filter(usuario=u)

            formulario = "certificados"
            horas_aprovado = 0
            horas_pendente = 0
            horas_recusado = 0
            for p in lista_certificados:
                if p.situacao == 1:
                    horas_aprovado = horas_aprovado + p.horas
                elif p.situacao == 2:
                    horas_pendente = horas_pendente + p.horas
                elif p.situacao == 3:
                    horas_recusado = horas_recusado + p.horas

            situacao = ["Aprovado", "Pendente", "Recusado", "Erro"]
            nome = u.first_name + u.last_name
            email = u.email
            contexto = {'u': u, 'nome': nome, 'email': email, 'lista_certificados': lista_certificados, 'situacao': situacao, 'form': form, 'horas_aprovado': horas_aprovado, 'horas_pendente': horas_pendente, 'horas_recusado': horas_recusado, 'formulario': formulario}
            return render(request, 'certificados/perfil.html', contexto)
        else:
            return HttpResponseRedirect("/certificados/")
    else:
        return HttpResponseRedirect("/certificados/login/")

def ver_usuarios(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            curso = request.user.perfil.curso
            lista_usuarios = []
            lista_perfil = Perfil.objects.filter(curso=curso)
            for p in lista_perfil:
                lista_usuarios.append(p.user)
            
            if request.method == "POST":
                operacao = ''
                form = FormFiltro(request.POST)
                if form.is_valid():
                    operacao = form.cleaned_data['operacao']

                    if operacao == "nome":
                        lista_usuarios = sorted(lista_usuarios, key=lambda k: k.first_name)
                    elif operacao == "email":
                        lista_usuarios = sorted(lista_usuarios, key=lambda k: k.email)
                    else:
                        pass
            else:
                form = FormFiltro()
        
            contexto = {'lista_usuarios': lista_usuarios, 'form': form}
            return render(request, 'certificados/usuarios.html', contexto)
        else:
            return HttpResponseRedirect("/certificados/")
    else:
        return HttpResponseRedirect("/certificados/login/")

def ver_certificado_usuario(request, id, id2):
    if request.user.is_authenticated:
        c = Certificado.objects.get(id=id2)
        u = UserModel.objects.get(id=id)
        userDeletar = False
        if request.user.is_superuser:
            if c.usuario == u:
                form = FormValidarCertificado()
                situacao = ["Aprovado", "Pendente", "Recusado", "Erro"]
                link = 'ver-certificado-usuario'
                contexto = {'c': c, 'u':u, 'situacao': situacao, 'form': form, 'link': link, 'userDeletar': userDeletar}
                return render(request, 'certificados/certificado.html', contexto)
            else:
                return HttpResponseRedirect(f"/certificados/usuario/{id}")
        else:
            if c.usuario == request.user:
                return HttpResponseRedirect(f"/certificados/{id2}")
            else:
                return HttpResponseRedirect("/certificados/")
    else:
        return HttpResponseRedirect("/certificados/login/")

def validar_certificado_usuario(request, id, id2):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            operacao = ''
            u = UserModel.objects.get(id=id)
            certificados = Certificado.objects.filter(usuario=u, situacao=2).order_by("id")[0:1]
            if request.method == "POST":
                form = FormValidarCertificado(request.POST)
                if form.is_valid():
                    c = Certificado.objects.get(id=id2)
                    operacao = form.cleaned_data['operacao']

                    if operacao == "recusar":
                        c.situacao = 3
                        c.save()
                    elif operacao == "aprovar":
                        c.situacao = 1
                        c.save()
                    elif operacao == "deletar":
                        c.delete()
                        messages.success(request, "Certificado deletado com sucesso!")
                        return HttpResponseRedirect(f"/certificados/usuario/{u.id}/")
                    elif operacao == "aprovar-proximo":
                        c.situacao = 1
                        c.save()
                        if certificados:
                            proximo = Certificado.objects.get(id=certificados)
                            return HttpResponseRedirect(f"/certificados/usuario/{u.id}/certificado/{proximo.id}")
                        else:
                            messages.success(request, "Todos certificados deste usuário já foram validados!")
                            return HttpResponseRedirect(f"/certificados/usuario/{u.id}")
                    else:
                        return HttpResponseRedirect(f"/certificados/usuario/{u.id}/certificado/{id2}")
            else:
                return HttpResponseRedirect(f"/certificados/usuario/{u.id}/certificado/{id2}")

            if certificados:
                messages.success(request, "certificado validado com sucesso!")
                return HttpResponseRedirect(f"/certificados/usuario/{u.id}/")
            else:
                messages.success(request, "Todos certificados deste usuário já foram validados!")
                return HttpResponseRedirect(f"/certificados/usuario/{u.id}/")
        else:
            return HttpResponseRedirect("/certificados/")
    else:
        return HttpResponseRedirect("/certificados/login/")