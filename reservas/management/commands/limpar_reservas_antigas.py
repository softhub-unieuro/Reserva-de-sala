from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservas.models import Reserva

class Command(BaseCommand):
    help = 'Remove definitivamente reservas com mais de 1 ano (baseado na data final)'

    def handle(self, *args, **kwargs):
        # Define a data de corte (hoje - 365 dias)
        data_corte = timezone.now().date() - timedelta(days=365)
        
        self.stdout.write(f"Buscando reservas anteriores a {data_corte}...")

        # Filtra reservas antigas (independente se estão deletadas ou não)
        reservas_velhas = Reserva.objects.filter(data_final__lt=data_corte)
        total = reservas_velhas.count()

        if total > 0:
            # O Django já lida com o CASCADE (apagará ReservasSala e HorarioOcupado vinculados)
            reservas_velhas.delete()
            msg = f"Sucesso! {total} reservas antigas foram removidas permanentemente do banco de dados."
            self.stdout.write(self.style.SUCCESS(msg))
        else:
            msg = "Nenhuma reserva antiga encontrada para exclusão."
            self.stdout.write(self.style.WARNING(msg))
        
        return msg