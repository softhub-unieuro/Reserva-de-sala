import os
from django.core.management.base import BaseCommand
from usuarios.models import Usuario
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Configura o sistema com grupos de permissão e superusuário inicial'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('--- Iniciando configuração de Usuários e Grupos ---'))
        
        grupos = {
            'Diretor': {
                'permissions': Permission.objects.all(),
            },
            'Assessora Administrativa': {
                'permissions': Permission.objects.all(),
            },
            'Núcleo de Tecnologia e Informação': {
                'permissions': Permission.objects.all(),
            },
            'Coordenador': {
                'permissions': Permission.objects.filter(codename__in=[
                    'view_bloco',
                    'view_sala',
                    'view_curso',
                    'view_turma',
                    'view_reserva',
                    'view_reservasala',
                    'view_horarioocupado',
                    'view_usuario',
                ]),
            },
            'Secretário': {
                'permissions': Permission.objects.filter(codename__in=[
                    'view_bloco',
                    'view_sala',
                    'view_curso',
                    'view_turma',
                    'view_reserva',
                    'view_reservasala',
                    'view_horarioocupado',
                    'view_usuario',
                ]),
            },
            'Núcleo de Apoio Psicopedagógico': {
                'permissions': Permission.objects.filter(codename__in=[
                    'view_bloco',
                    'view_sala',
                    'view_curso',
                    'view_turma',
                    'view_reserva',
                    'view_reservasala',
                    'view_horarioocupado',
                    'view_usuario',
                ]),
            },
            'Manutenção': {
                'permissions': Permission.objects.filter(codename__in=[
                    'view_bloco',
                    'view_sala',
                    'view_curso',
                    'view_turma',
                    'view_reserva',
                    'view_reservasala',
                    'view_horarioocupado',
                    'view_usuario',
                ]),
            },
        }

        for grupo_nome, grupo_info in grupos.items():
            grupo, criado = Group.objects.get_or_create(name=grupo_nome)
            grupo.permissions.set(grupo_info['permissions'])
            grupo.save()
            if criado:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{grupo_nome}" criado com sucesso.'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{grupo_nome}" já existe.'))

            
        # Super Usuario Inicial

        admin_matricula = os.getenv('ADMIN_MATRICULA')
        admin_nome = os.getenv('ADMIN_NOME')
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_telefone = os.getenv('ADMIN_TELEFONE')
        admin_data_nascimento = os.getenv('ADMIN_DATA_NASCIMENTO')
        admin_sexo = os.getenv('ADMIN_SEXO')
        admin_cargo = os.getenv('ADMIN_CARGO')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if not admin_matricula or not admin_password:
            self.stdout.write(self.style.ERROR('ERRO: ADMIN_MATRICULA ou ADMIN_PASSWORD não definidos no .env'))
            return

        if not Usuario.objects.filter(matricula=admin_matricula).exists():
            try:
                Usuario.objects.create_superuser(
                    matricula=admin_matricula,
                    nome=admin_nome,
                    email_institucional=admin_email,
                    telefone=admin_telefone,
                    data_nascimento=admin_data_nascimento,
                    sexo=admin_sexo,
                    cargo=admin_cargo,
                    password=admin_password
                )
                self.stdout.write(self.style.SUCCESS(f'Usuário administrador "{admin_nome}" criado com sucesso.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao criar superusuário: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'Usuário administrador com matrícula "{admin_matricula}" já existe.'))

        self.stdout.write(self.style.SUCCESS('--- Configuração concluída ---'))
        