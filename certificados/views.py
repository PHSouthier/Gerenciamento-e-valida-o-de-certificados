from django.contrib import messages
from certificados.forms import FormCertificado, FormFiltro, FormLogin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Certificado
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

def index(request):
    lista_certificados = Certificado.objects.order_by("-data_envio")[0:10]
    situacao = ["Aprovado", "Pendente", "Recusado", "Erro"]
    contexto = {'lista_certificados': lista_certificados, 'situacao':situacao}
    return render(request, 'certificados/index.html', contexto)

def mostrar_todos_certificados(request):
    resultado = ''
    operacao = ''
    if request.method == "POST":
        form = FormFiltro(request.POST)
        if form.is_valid():
            operacao = form.cleaned_data['operacao']

            if operacao == "data_emissao":
                lista_certificados = Certificado.objects.order_by("-data_emissao")
            elif operacao == "autor":
                lista_certificados = Certificado.objects.order_by("usuario")
            elif operacao == "data_envio":
                lista_certificados = Certificado.objects.order_by("-data_envio")
            elif operacao == "titulo":
                lista_certificados = Certificado.objects.order_by("titulo")
            elif operacao == "horas":
                lista_certificados = Certificado.objects.order_by("-horas")
            elif operacao == "situacao":
                lista_certificados = Certificado.objects.order_by("situacao")
            else:
                lista_certificados = Certificado.objects.all()
    else:
        form = FormFiltro()
        lista_certificados = Certificado.objects.all()

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
    contexto = {'lista_certificados': lista_certificados, 'situacao': situacao, 'form': form, 'horas_aprovado': horas_aprovado, 'horas_pendente': horas_pendente, 'horas_recusado': horas_recusado, 'resultado': resultado, 'operacao': operacao}
    return render(request, 'certificados/certificados.html', contexto)

def novo_certificado(request):
    if request.method == 'POST':
        form = FormCertificado(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.usuario = request.user
            c.save()

            messages.success(request, "O certificado foi salvo com sucesso!")
            return HttpResponseRedirect('/certificados/novo_certificado/')
        else:
            messages.error(request, "Preencha corretamente o formulário.")
    else:
        form = FormCertificado()
    
    contexto = {'form': form}
    return render(request, 'certificados/novo_certificado.html', contexto)

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
    return HttpResponseRedirect("/certificados/")

def ver_certificado(request, id):
    c = Certificado.objects.get(id=id)
    situacao = ["Aprovado", "Pendente", "Recusado", "Erro"]
    contexto = {'c': c, 'situacao': situacao}
    return render(request, 'certificados/certificado.html', contexto)