from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# UserManager para criacao de usuarios e super usuarios
class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, nome, email_institucional, telefone, data_nascimento, sexo, cargo, password=None, **extra_fields):
        if not matricula or not nome or not email_institucional or not telefone or not data_nascimento or not cargo:
            raise ValueError("Informe todos os campos")
        email_institucional = self.normalize_email(email_institucional)
        usuario = self.model(
            matricula= matricula,
            nome= nome,
            email_institucional= email_institucional,
            telefone=telefone,
            data_nascimento=data_nascimento,
            sexo=sexo,
            cargo=cargo,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, matricula, nome, email_institucional, telefone, data_nascimento, sexo, cargo, password=None, **extra_fields):
        if not matricula or not nome or not email_institucional or not telefone or not data_nascimento or not sexo or not cargo:
            raise ValueError("Informe todos os campos")
        email_institucional = self.normalize_email(email_institucional)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  
        usuario = self.model(
            matricula= matricula,
            nome= nome,
            email_institucional= email_institucional,
            telefone=telefone,
            data_nascimento=data_nascimento,
            sexo=sexo,
            cargo=cargo,
            **extra_fields
            )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

# Criacao do modelo 'Usuario'
class Usuario(AbstractBaseUser, PermissionsMixin):

    CARGOS = [
        ("Diretor", "Diretor"),
        ("Assessora Administrativa","Assessora Administrativa"),
        ("Núcleo de Tecnologia e Informação", "Núcleo de Tecnologia e Informação"),
        ("Coordenador", "Coordenador"),
        ("Secretário", "Secretário"),
        ("Núcleo de Apoio Psicopedagógico", "Núcleo de Apoio Psicopedagógico"),
        ("Manutenção", "Manutenção"),
    ]

    matricula = models.CharField(max_length=6, unique=True, verbose_name='Matrícula')
    criado_por = models.ForeignKey(
        "self",
        models.SET_NULL,
        db_column="criador_por_matricula",
        to_field="matricula",
        related_name="usuarios_criados",
        blank=True,
        null=True,
    )
    nome = models.CharField(max_length=255)
    email_institucional = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    data_nascimento = models.DateField(verbose_name='Data de nascimento')
    sexo = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        choices=[("Masculino", "Masculino"), ("Feminino", "Feminino"), ("Outro", "Outro"), ("Prefiro não informar", "Prefiro não informar")],
    )
    cargo = models.CharField(max_length=40, choices=CARGOS)

    status_login = models.BooleanField(default=False)
    dth_insert = models.DateTimeField(default=timezone.now)
    dth_delete = models.DateTimeField(blank=True, null=True)
    status_delete = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True, verbose_name='Ativo', help_text='Indica se este usuário deve ser tratado como ativo.')
    is_staff = models.BooleanField(default=True, verbose_name='Membro da Equipe', help_text='Indica se o usuário pode acessar este site de administração.')

    objects = UsuarioManager()

    REQUIRED_FIELDS = ['nome', 'email_institucional', 'telefone', 'data_nascimento', 'sexo', 'cargo']
    USERNAME_FIELD = "matricula"

    def __str__(self):
        return f"{self.nome} - ({self.get_cargo_display()})"

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
