from django.urls import path
from .views import LoginUsuario, LogoutUsuario, Perfil, EnviarEmail, ConfirmacaoCodigo, NovaSenha

urlpatterns = [
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', LogoutUsuario.as_view(), name='logout'),
    path('perfil/', Perfil.as_view(), name="perfil" ),
    path('recuperar/', EnviarEmail.as_view(), name='enviaremail'),
    path('codigo/', ConfirmacaoCodigo.as_view(), name='confirmacaocodigo'),
    path('nova-senha/', NovaSenha.as_view(), name='novasenha')
]
