from django.contrib import admin
from .models import Reserva, ReservaSala, HorarioOcupado

# --- INLINES ---

class HorarioOcupadoInline(admin.TabularInline):
    """
    Permite visualizar e editar os slots de tempo (Dia/Período)
    diretamente dentro da Reserva de Sala.
    """
    model = HorarioOcupado
    extra = 0
    can_delete = True
    classes = ('collapse',)  # Inicia recolhido para não poluir visualmente

class ReservaSalaInline(admin.StackedInline):
    """
    Permite ver qual sala foi alocada dentro da tela da Reserva principal.
    """
    model = ReservaSala
    extra = 0
    can_delete = True
    show_change_link = True  # Botão para ir para a edição detalhada da ReservaSala
    readonly_fields = ('created_at', 'deleted_at')
    
    fieldsets = (
        (None, {
            'fields': (('id_sala', 'turno'), 'responsavel', 'status_reserva', 'is_deleted')
        }),
        ('Detalhes', {
            'fields': ('descricao_reserva',),
            'classes': ('collapse',)
        }),
    )

# --- ADMINS ---

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_turma',
        'get_curso_nome',
        'data_inicial',
        'data_final',
        'criador_por',
        'is_deleted'
    )
    list_filter = ('data_inicial', 'data_final', 'is_deleted', 'id_curso')
    search_fields = ('codigo_turma', 'id_curso__nome_curso', 'criador_por__username')
    readonly_fields = ('created_at', 'deleted_at')
    list_select_related = ('id_curso', 'id_turma', 'criador_por')
    
    # Aqui conectamos a ReservaSala como filha da Reserva
    inlines = [ReservaSalaInline]

    fieldsets = (
        ('Informações da Turma', {
            'fields': ('id_curso', 'id_turma', 'codigo_turma')
        }),
        ('Vigência', {
            'fields': (('data_inicial', 'data_final'),)
        }),
        ('Auditoria', {
            'fields': ('criador_por', 'created_at', 'deleted_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Curso', ordering='id_curso__nome_curso')
    def get_curso_nome(self, obj):
        return obj.id_curso.nome_curso if obj.id_curso else '-'

@admin.register(ReservaSala)
class ReservaSalaAdmin(admin.ModelAdmin):
    list_display = (
        'get_reserva_turma',
        'id_sala',
        'turno',
        'responsavel',
        'get_qtd_horarios', # Novo: mostra quantos slots ocupou
        'status_reserva',
        'is_deleted'
    )
    list_filter = ('status_reserva', 'turno', 'is_deleted', 'id_sala__id_bloco')
    search_fields = ('responsavel', 'id_reserva__codigo_turma', 'id_sala__numero_sala')
    list_select_related = ('id_reserva', 'id_sala')
    readonly_fields = ('created_at', 'deleted_at')
    
    # Aqui conectamos os horários verticais como filhos da ReservaSala
    inlines = [HorarioOcupadoInline]

    fieldsets = (
        ('Dados Principais', {
            'fields': ('id_reserva', 'id_sala', 'turno', 'responsavel')
        }),
        ('Status', {
            'fields': ('status_reserva', 'is_deleted', 'descricao_reserva')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Turma', ordering='id_reserva__codigo_turma')
    def get_reserva_turma(self, obj):
        if obj.id_reserva:
             return f"{obj.id_reserva.codigo_turma}"
        return "-"

    @admin.display(description='Slots')
    def get_qtd_horarios(self, obj):
        return obj.horarios.count()

# Opcional: Se quiser ver a tabela crua de horários para debug
@admin.register(HorarioOcupado)
class HorarioOcupadoAdmin(admin.ModelAdmin):
    list_display = ('reserva_sala', 'get_dia_display', 'get_periodo_display')
    list_filter = ('dia_semana', 'periodo')
    
    def get_dia_display(self, obj):
        return obj.get_dia_semana_display()
    get_dia_display.short_description = 'Dia'

    def get_periodo_display(self, obj):
        return obj.get_periodo_display()
    get_periodo_display.short_description = 'Período'