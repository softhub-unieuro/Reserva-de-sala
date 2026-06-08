from django.contrib import admin
from .models import Sala, Bloco, Curso, Turma

@admin.register(Bloco)
class BlocoAdmin(admin.ModelAdmin):
    list_display = ('bloco', 'ativo', 'criador_por', 'created_at')
    list_filter = ('ativo',)
    search_fields = ('bloco',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('bloco',)

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('bloco', 'criador_por')
        }),
        ('Status', {
            'fields': ('ativo', 'motivo_inativo')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Esconde essa seção por padrão
        }),
    )

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = (
        'get_sala_completa', 
        'capacidade', 
        'tv_tamanho', 
        'data_show', 
        'ativo', 
        'is_deleted'
    )
    list_filter = ('ativo', 'is_deleted', 'data_show', 'id_bloco', 'andar')
    # O uso de __ permite pesquisar em campos de tabelas relacionadas
    search_fields = ('numero_sala', 'id_bloco__bloco') 
    # Otimiza consultas SQL para chaves estrangeiras
    list_select_related = ('id_bloco', 'criador_por')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
    ordering = ('id_bloco', 'numero_sala')

    fieldsets = (
        ('Localização', {
            'fields': ('id_bloco', 'andar', 'numero_sala')
        }),
        ('Recursos', {
            'fields': ('capacidade', 'tv_tamanho', 'data_show')
        }),
        ('Controle de Status', {
            'fields': ('ativo', 'motivo_inativo', 'is_deleted', 'deleted_at')
        }),
        ('Auditoria', {
            'fields': ('criador_por', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Método personalizado para exibir no list_display
    @admin.display(description='Sala', ordering='numero_sala')
    def get_sala_completa(self, obj):
        return f"{obj.id_bloco.bloco} - {obj.numero_sala}"

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome_curso', 'criador_por', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('nome_curso',)
    readonly_fields = ('created_at', 'deleted_at')
    ordering = ('nome_curso',)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_turma', 
        'id_curso', 
        'periodo_letivo', 
        'quantidade_aluno', 
        'is_deleted'
    )
    list_filter = ('periodo_letivo', 'is_deleted', 'id_curso')
    # Permite pesquisar pelo código da turma E pelo nome do curso relacionado
    search_fields = ('codigo_turma', 'id_curso__nome_curso')
    list_select_related = ('id_curso', 'criador_por')
    readonly_fields = ('created_at', 'deleted_at')
    ordering = ('-periodo_letivo', 'codigo_turma') # Ordena por período mais recente primeiro