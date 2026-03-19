from django.urls import path
from .views import FechamentoSemestre, ReservarSala, EditarReserva, Relatorio

urlpatterns = [
    path("reservar/<str:bloco_nome>/<int:numero_sala>/", ReservarSala.as_view(), name="reservarsala"),
    path('reservas/editar/<int:reserva_id>/', EditarReserva.as_view(), name='editar_reserva'),
    path("reservas/relatorio/", Relatorio.as_view(), name="relatorio"),
    path("reservas/fechamento/", FechamentoSemestre.as_view(), name="fechamento_semestre")
]