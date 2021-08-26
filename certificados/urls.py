from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.mostrar_todos_certificados, name='mostrar_todos_certificados'),
    path('<int:id>/', views.ver_certificado, name='ver_certificado'),
    path('novo_certificado/', views.novo_certificado, name='novo_certificado'),
    path('validar/', views.validar, name='validar'),
    path('validar/<int:id>/', views.validar_certificado, name='validar_certificado'),
    path('usuario/', views.perfil, name='perfil'),
    path('usuario/<int:id>/', views.usuario, name='usuario'),
    path('usuario/<int:id>/certificado/<int:id2>/', views.ver_certificado_usuario, name='ver_certificado_usuario'),
    path('usuario/<int:id>/certificado/validar/<int:id2>/', views.validar_certificado_usuario, name='validar_certificado_usuario'),
    path('usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('login/', views.fazer_login, name='fazer_login'),
    path('logout/', views.fazer_logout, name='fazer_logout'),
]
