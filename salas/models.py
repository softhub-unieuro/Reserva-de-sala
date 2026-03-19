from django.db import models

class Bloco(models.Model):
    bloco = models.CharField(max_length=1)
    criador_por = models.ForeignKey(
        'usuarios.Usuario', 
        on_delete=models.SET_NULL,
        to_field='matricula',
        blank=True,
        null=True
    )
    ativo = models.BooleanField(default=True)
    motivo_inativo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bloco {self.bloco}"


class Sala(models.Model):
    id_bloco = models.ForeignKey(Bloco, on_delete=models.PROTECT, verbose_name='Bloco')
    criador_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        to_field='matricula',
        blank=True,
        null=True
    )
    andar = models.CharField(max_length=50)
    numero_sala = models.IntegerField(verbose_name='Número da sala')
    capacidade = models.IntegerField()
    tv_tamanho = models.CharField(max_length=5, null=True, blank=True, verbose_name='Tamanho da TV')
    data_show = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    motivo_inativo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Sala {self.numero_sala} - Bloco {self.id_bloco.bloco}"


class Curso(models.Model):
    criador_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        to_field='matricula',
        blank=True,
        null=True
    )
    nome_curso = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_curso


class Turma(models.Model):
    id_curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Curso')
    criador_por = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        to_field='matricula',
        blank=True,
        null=True
    )
    codigo_turma = models.CharField(max_length=255, verbose_name='Código da turma')
    periodo_letivo = models.CharField(max_length=25, null=True)
    quantidade_aluno = models.IntegerField(null=True, verbose_name='Quantidade de alunos')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.codigo_turma} - {self.id_curso.nome_curso if self.id_curso else 'Sem curso'}"
