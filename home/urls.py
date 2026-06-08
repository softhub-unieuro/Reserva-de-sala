from django.urls import path
from .views import Home, Cadastro

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('cadastro/', Cadastro.as_view(), name='cadastro')
]
