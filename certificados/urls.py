from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.mostrar_todos_certificados, name='mostrar_todos_certificados'),
    path('<int:id>/', views.ver_certificado, name='ver_certificado'),
    path('novo_certificado/', views.novo_certificado, name='novo_certificado'),
    path('validar/', views.validar, name='validar'),
    path('validar/<int:id>/', views.validar_certificado, name='validar_certificado'),
    path('login/', views.fazer_login, name='fazer_login'),
    path('logout/', views.fazer_logout, name='fazer_logout'),
]
