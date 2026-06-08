from django import forms
from django.utils import timezone
from salas.models import Bloco, Sala, Turma, Curso

DIAS_CHOICES = (
    ('segunda', 'Segunda-feira'),
    ('terca', 'Terça-feira'),
    ('quarta', 'Quarta-feira'),
    ('quinta', 'Quinta-feira'),
    ('sexta', 'Sexta-feira'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
)

PERIODOS_CHOICES = (
    ('primeiro', '1º Período'),
    ('segundo', '2º Período'),
    ('terceiro', '3º Período'),
    ('quarto', '4º Período'),
    ('integral', 'Integral'),
)

class VerificacaoReserva(forms.Form):
    
    id_curso = forms.ModelChoiceField(queryset=Curso.objects.all(), required=False, label='Curso')
    id_turma = forms.ModelChoiceField(queryset=Turma.objects.all(), required=True, label="Turma")
    professor = forms.CharField(max_length=255, required=True, label="Professor responsável")

    id_bloco = forms.ModelChoiceField(Bloco.objects.all(), required=True)
    id_sala = forms.ModelChoiceField(Sala.objects.all(), required=True)
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_final = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    turno = forms.ChoiceField(choices=[
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno'),
    ])
    dias_semana = forms.MultipleChoiceField(choices=DIAS_CHOICES, widget=forms.CheckboxSelectMultiple, required=True)
    periodos = forms.MultipleChoiceField(choices=PERIODOS_CHOICES, widget=forms.CheckboxSelectMultiple, required=True)
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)

    def clean(self):
        cleaned_data = super().clean()

        sala = cleaned_data.get('id_sala')
        turma = cleaned_data.get('id_turma')
        bloco = cleaned_data.get('id_bloco')
        data_inicial = cleaned_data.get('data_inicial')
        data_final = cleaned_data.get('data_final')
        turno_reserva = cleaned_data.get('turno')

        # 1. Validação de Data Retroativa (Passado)
        if data_inicial:
            if data_inicial < timezone.now().date():
                 self.add_error('data_inicial', "Não é possível criar reservas em datas passadas.")

        # 2. Validação de Hierarquia (Ativos/Inativos)
        if sala and hasattr(sala, 'ativo') and not sala.ativo:
            self.add_error('id_sala', "Esta sala está desativada no sistema.")
        
        if bloco and hasattr(bloco, 'ativo') and not bloco.ativo: # <--- REINSERIDO
            self.add_error('id_bloco', f"O Bloco {bloco.bloco} está fechado/inativo.")

        # 3. Validação de Capacidade e Turno
        if sala and turma:
            cap_sala = sala.capacidade
            qtd_alunos = turma.quantidade_aluno

            # Capacidade
            if qtd_alunos > cap_sala:
                self.add_error('id_turma', 
                    f"Superlotação: A turma tem {qtd_alunos} alunos, mas a sala suporta apenas {cap_sala}.")
            
            # Compatibilidade de Turno
            turno_turma = getattr(turma, 'turno', None)
            if turno_turma and turno_reserva:
                if turno_turma != turno_reserva:
                    self.add_error('turno', 
                        f"Atenção: A turma é do turno {turno_turma}, mas você está agendando para o {turno_reserva}."
                    )

        # 4. Validação de Ordem das Datas (Protegido contra None)
        if data_inicial and data_final:
            if data_final < data_inicial:
                self.add_error('data_final', "A data final não pode ser anterior a data inicial")

        # 5. Validação do Integral (Sem duplicidade)
        periodos = cleaned_data.get("periodos", [])
        if "integral" in periodos and len(periodos) > 1:
            raise forms.ValidationError("Se 'Integral' for selecionado, nenhum outro período pode ser marcado.")
        
        return cleaned_data