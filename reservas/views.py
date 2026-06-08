from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from salas.models import Bloco, Sala, Curso, Turma
from .models import Reserva, ReservaSala, HorarioOcupado
from .forms import VerificacaoReserva
from django.db import transaction
from .services import validar_conflito
from .relatorios import PDFMapaSalas
from django.utils import timezone
from django.core.management import call_command
from io import StringIO

class ReservarSala(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'reservas.add_reserva'

    def get(self, request: HttpRequest, bloco_nome: str, numero_sala: int) -> HttpResponse:
        sala = get_object_or_404(
            Sala,
            numero_sala=numero_sala,
            id_bloco__bloco=bloco_nome,
            is_deleted=False
        )
        
        bloco = sala.id_bloco

        cursos = Curso.objects.all().order_by('nome_curso')
        turmas = Turma.objects.all().order_by('codigo_turma')

        form = VerificacaoReserva(initial={
            'id_sala': sala.id, 
            'id_bloco': bloco.id
        })

        context = {
            'form': form,
            'bloco': bloco,
            'sala': sala,
            'cursos': cursos,
            'turmas': turmas,
        }
        return render(request, "reservas/reservarsala.html", context)


    def post(self, request: HttpRequest, bloco_nome: str, numero_sala: int) -> HttpResponse:
        sala = get_object_or_404(
            Sala,
            numero_sala=numero_sala,
            id_bloco__bloco=bloco_nome,
            is_deleted=False
            )


        bloco = sala.id_bloco
        cursos = Curso.objects.all().order_by('nome_curso')
        turmas = Turma.objects.all().order_by('codigo_turma')

        form = VerificacaoReserva(request.POST)
        
        if form.is_valid():
            dados = form.cleaned_data

            dias_form =  dados['dias_semana']
            periodos_form = dados['periodos']

            periodos_ids = []
            if 'integral' in periodos_form:
                periodos_ids = [1, 2, 3, 4]
            else:
                mapa_periodos = {'primeiro': 1, 'segundo': 2, 'terceiro': 3, 'quarto': 4}
                for p in periodos_form:
                    if p in mapa_periodos:
                        periodos_ids.append(mapa_periodos[p])
                
            mapa_dias = {'segunda': 0, 'terca': 1, 'quarta': 2, 'quinta': 3, 'sexta': 4, 'sabado': 5, 'domingo': 6}
            dias_ids = [mapa_dias[d] for d in dias_form if d in mapa_dias]

            erro_conflito = validar_conflito(
                sala_id=sala.id,
                turma_id=dados['id_turma'],
                data_ini=dados['data_inicial'],
                data_fim=dados['data_final'],
                turno=dados['turno'],
                listar_dias=dias_ids,
                listar_periodos=periodos_ids
            )

            if erro_conflito:
                messages.error(request, erro_conflito)
                
            else:
                try:
                    with transaction.atomic():
                        nova_reserva = Reserva.objects.create(
                            criador_por=request.user,
                            id_curso=dados['id_curso'],
                            id_turma=dados['id_turma'],
                            codigo_turma=dados['id_turma'].codigo_turma,
                            data_inicial=dados['data_inicial'],
                            data_final=dados['data_final']
                        )

                        nova_reserva_sala = ReservaSala.objects.create(
                            id_reserva=nova_reserva,
                            id_sala=sala,
                            turno=dados['turno'],
                            responsavel=dados['professor'],
                            descricao_reserva=dados['descricao']
                        )

                        lista_objetos_horario = []
                        for d in dias_ids:
                            for p in periodos_ids:
                                lista_objetos_horario.append(
                                    HorarioOcupado(
                                        reserva_sala=nova_reserva_sala,
                                        dia_semana=d,
                                        periodo=p
                                    )
                                )
                        HorarioOcupado.objects.bulk_create(lista_objetos_horario)
                        
                    messages.success(request, 'Reserva realizada com sucesso!')
                    return redirect('home')
                
                except Exception as e:
                    messages.error(request, f'Erro interno ao salvar: {str(e)}')

        context = {
            'form': form,
            'sala': sala,
            'bloco': bloco,
            'cursos': cursos,
            'turmas': turmas
        }
        return render(request, 'reservas/reservarsala.html', context)
    
class EditarReserva(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'reservas.add_reserva'

    def get(self, reserva_id, request:HttpRequest)->HttpResponse:
        reserva = get_object_or_404(Reserva, pk=reserva_id, is_deleted=False)
        reserva_sala = get_object_or_404(ReservaSala, id_reserva=reserva)

        horarios = reserva_sala.horario.all()
        dias_salvos = set(h.dia_semana for h in horarios)
        periodos_salvos = set(h.periodos for h in horarios)

        mapa_dias_rev = {0: 'segunda', 1: 'terca', 2: 'quarta', 3: 'quinta', 4: 'sexta', 5: 'sabado', 6: 'domingo'}
        mapa_periodos_rev = {1: 'primeiro', 2: 'segundo', 3: 'terceiro', 4: 'quarto'}

        initial_dias = [mapa_dias_rev[d] for d in dias_salvos if d in mapa_dias_rev]

        if {1, 2, 3, 4}.issubset(periodos_salvos):
            initial_periodos = ['integral']
        else:
            initial_periodos = [mapa_periodos_rev[p] for p in periodos_salvos if p in mapa_periodos_rev]

        form = VerificacaoReserva(initial={
            'id_curso': reserva.id_curso,
            'id_turma': reserva.id_turma,
            'professor': reserva_sala.responsavel,
            'id_bloco': reserva_sala.id_sala.id_bloco,
            'id_sala': reserva_sala.id_sala,
            'data_inicial': reserva.data_inicial,
            'data_final': reserva.data_final,
            'turno': reserva_sala.turno,
            'dias_semana': initial_dias,
            'periodos': initial_periodos,
            'descricao': reserva_sala.descricao_reserva
        })

        context = {
            'form': form,
            'sala': reserva_sala.id_sala,
            'bloco': reserva_sala.id_sala.id_bloco,
            'cursos': Curso.objects.all(),
            'turmas': Turma.objects.all(),
            'edicao': True 
        }
        return render(request, "reservas/reservarsala.html", context)
    
    def post(self, reserva_id, request:HttpRequest)->HttpResponse:
        reserva = get_object_or_404(Reserva, pk=reserva_id)
        reserva_sala = get_object_or_404(ReservaSala, id_reserva=reserva)
        sala = reserva_sala.id_sala

        cursos = Curso.objects.all()
        turmas = Turma.objects.all()

        form = VerificacaoReserva(request.POST)

        if form.is_valid():
            dados = form.cleaned_data

            dias_form =  dados['dias_semana']
            periodos_form = dados['periodos']

            periodos_ids = []
            if 'integral' in periodos_form:
                periodos_ids = [1, 2, 3, 4]
            else:
                mapa_periodos = {'primeiro': 1, 'segundo': 2, 'terceiro': 3, 'quarto': 4}
                for p in periodos_form:
                    if p in mapa_periodos:
                        periodos_ids.append(mapa_periodos[p])
                
            mapa_dias = {'segunda': 0, 'terca': 1, 'quarta': 2, 'quinta': 3, 'sexta': 4, 'sabado': 5, 'domingo': 6}
            dias_ids = [mapa_dias[d] for d in dias_form if d in mapa_dias]

            erro_conflito = validar_conflito(
                sala_id=sala.id,
                turma_id=dados['id_turma'],
                data_ini=dados['data_inicial'],
                data_fim=dados['data_final'],
                listar_dias=dias_ids,
                listar_periodos=periodos_ids,
                turno=dados['turno'],
                ignorar_reserva_id=reserva.id
            )

            if erro_conflito:
                messages.error(request, erro_conflito)
            else:
                try:
                    with transaction.atomic():
                        reserva.id_curso = dados['id_curso']
                        reserva.id_turma = dados['id_turma']
                        reserva.codigo_turma = dados['id_turma'].codigo_turma
                        reserva.data_inicial = dados['data_inicial']
                        reserva.data_final = dados['data_final']
                        reserva.save()

                        reserva_sala.turno = dados['turno']
                        reserva_sala.responsavel = dados['professor']
                        reserva_sala.descricao_reserva = dados['descricao']
                        reserva_sala.save()

                        reserva_sala.horarios.all().delete()

                        lista_objetos_horario = []
                        for d in dias_ids:
                            for p in periodos_ids:
                                lista_objetos_horario.append(
                                    HorarioOcupado(
                                        reserva_sala=reserva_sala,
                                        dia_semana=d,
                                        periodo=p
                                    )
                                )
                        HorarioOcupado.objects.bulk_create(lista_objetos_horario)

                    messages.success(request, 'Reserva atualizada com sucesso!')
                    return redirect('home')

                except Exception as e:
                    messages.error(request, f"Erro ao atualizar: {e}")

        context = {
            'form': form,
            'sala': sala,
            'bloco': sala.id_bloco,
            'cursos': cursos,
            'turmas': turmas,
            'edicao': True
        }
        return render(request, 'reservas/reservarsala.html', context)
    
class FechamentoSemestre(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'reservas.delete_reserva' 

    def get_semestre_info(self):
        hoje = timezone.now().date()
        mes = hoje.month
        ano = hoje.year

        if 1 <= mes <= 7:
            semestre_label = f"1º Semestre de {ano}"
            data_inicio = f"{ano}-01-01"
            data_fim = f"{ano}-07-30"
        else:
            semestre_label = f"2º Semestre de {ano}"
            data_inicio = f"{ano}-08-01"
            data_fim = f"{ano}-12-31"

        reservas_count = Reserva.objects.filter(
            is_deleted=False,
            data_inicial__gte=data_inicio,
            data_inicial__lte=data_fim
        ).count()

        return {
            'label': semestre_label,
            'count': reservas_count,
            'ano': ano,
            'semestre_num': 1 if mes <= 7 else 2
        }

    def get(self, request: HttpRequest) -> HttpResponse:
        context = self.get_semestre_info()
        return render(request, 'reservas/fechamento_semestre.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        acao = request.POST.get('acao')

        if acao == 'baixar_pdf':
            # Gera o PDF
            relatorio = PDFMapaSalas()
            pdf_content = relatorio.gerar_pdf()
            
            response = HttpResponse(content_type='application/pdf')
            filename = f"Mapa_Salas_{timezone.now().strftime('%Y_%m')}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response.write(pdf_content)
            return response

        elif acao == 'limpar_banco':
            confirmacao = request.POST.get('confirmacao_seguranca')
            
            if confirmacao != 'SIM':
                messages.error(request, "Você deve confirmar a caixa de seleção para prosseguir.")
                return redirect('fechamento_semestre')

            try:
                # 1. ARQUIVAR O SEMESTRE ATUAL (Soft Delete)
                reservas_afetadas = Reserva.objects.filter(is_deleted=False)
                count_arquivadas = reservas_afetadas.count()
                
                reservas_afetadas.update(is_deleted=True, deleted_at=timezone.now())
                ReservaSala.objects.filter(is_deleted=False).update(is_deleted=True, deleted_at=timezone.now())

                # 2. LIMPEZA PROFUNDA (> 1 ANO) - Chama o comando
                out = StringIO()
                call_command('limpar_reservas_antigas', stdout=out)
                msg_limpeza = out.getvalue().strip()

                messages.success(request, f"Semestre encerrado! {count_arquivadas} reservas foram arquivadas.")
                messages.info(request, f"Manutenção automática: {msg_limpeza}")
                
                return redirect('home')

            except Exception as e:
                messages.error(request, f"Erro crítico ao processar: {e}")
                return redirect('fechamento_semestre')
        
        elif acao == 'limpar_historico_antigo':
            out = StringIO()
            try:
                call_command('limpar_historico', stdout=out)
                resultado = out.getvalue()
                
                if "Nenhuma reserva" in resultado:
                    messages.info(request, "O sistema verificou e não há dados antigos (mais de 1 ano) para excluir.")
                else:
                    messages.success(request, f"Manutenção concluída: {resultado}")
                    
            except Exception as e:
                messages.error(request, f"Erro ao executar limpeza: {e}")
            
            return redirect('fechamento_semestre')
        
        return redirect('fechamento_semestre')

    
class Relatorio(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'reservas.add_reserva' 

    def get(self, request: HttpRequest) -> HttpResponse:
        relatorio = PDFMapaSalas()
        pdf_content = relatorio.gerar_pdf()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mapa_de_salas.pdf"'
        
        response.write(pdf_content)
        return response