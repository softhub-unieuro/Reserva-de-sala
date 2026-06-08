from django.urls import path
from salas.views import ListarSalas

urlpatterns = [
    path('', ListarSalas.as_view(), name='listarsalas'),
]
