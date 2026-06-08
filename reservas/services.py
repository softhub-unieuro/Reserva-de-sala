from django.db.models import Q
from reservas.models import HorarioOcupado

def validar_conflito(sala_id, turma_id, data_ini, data_fim, listar_dias, listar_periodos, turno, ignorar_reserva_id=None):

    query = HorarioOcupado.objects.filter(
        # Procura reservas ativas
        reserva_sala__status_reserva=True,
        reserva_sala__is_deleted=False,
        reserva_sala__id_reserva__is_deleted=False,

        # Procura por reservas no msm intervalo de tempo
        reserva_sala__id_reserva__data_inicial__lte=data_fim,
        reserva_sala__id_reserva__data_final__gte=data_ini,

        # Procura reservas no msm dia / periodo
        dia_semana__in=listar_dias,
        periodo__in=listar_periodos,
        reserva_sala__turno =turno,
    ).filter(
        Q(reserva_sala__id_sala_id=sala_id) |
        Q(reserva_sala__id_reserva__id_turma_id=turma_id)
    )

    if ignorar_reserva_id:
        query = query.exclude(reserva_sala__id_reserva__id=ignorar_reserva_id)

    conflito = query.select_related('reserva_sala__id_reserva', 'reserva_sala__id_sala').first()

    if conflito:
        reserva_encontrada = conflito.reserva_sala

        data_fmt = reserva_encontrada.id_reserva.data_inicial.strftime('%d/%m')

        if reserva_encontrada.id_sala.id == sala_id:
            return (f"CONFLITO DE SALA: A {reserva_encontrada.id_sala.numero_sala} já está ocupada "
                    f"neste horário (Dia: {conflito.get_dia_semana_display()}, "
                    f"Período: {conflito.get_periodo_display()}) pela turma "
                    f"{reserva_encontrada.id_reserva.codigo_turma}.")
        else:
            return (f"CONFLITO DE TURMA: A turma {turma_id.codigo_turma} já possui aula "
                    f"na sala {reserva_encontrada.id_sala.numero_sala} neste horário.")

    return None