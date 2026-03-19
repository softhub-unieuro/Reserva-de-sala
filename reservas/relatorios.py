from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from io import BytesIO
from django.db.models import Prefetch  # Importação necessária
from salas.models import Bloco, Sala
from reservas.models import ReservaSala

class PDFMapaSalas:
    def __init__(self):
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer, 
            pagesize=landscape(A4),
            rightMargin=1*cm, leftMargin=1*cm, 
            topMargin=1*cm, bottomMargin=1*cm
        )
        self.elements = []
        self.styles = getSampleStyleSheet()

    def _criar_intervalo_dias(self, lista_dias_idxs):
        """
        Transforma [1, 2, 3, 4] em 'TER A SEX'
        Ou [0, 2, 4] em 'SEG, QUA, SEX'
        """
        mapa_dias = {0: 'SEG', 1: 'TER', 2: 'QUA', 3: 'QUI', 4: 'SEX', 5: 'SAB', 6: 'DOM'}
        
        if not lista_dias_idxs:
            return ""
            
        lista_dias_idxs.sort()
        
        if len(lista_dias_idxs) >= 3:
            consecutivos = True
            for i in range(len(lista_dias_idxs) - 1):
                if lista_dias_idxs[i+1] != lista_dias_idxs[i] + 1:
                    consecutivos = False
                    break
            
            if consecutivos:
                return f"{mapa_dias[lista_dias_idxs[0]]} A {mapa_dias[lista_dias_idxs[-1]]}"

        return ", ".join([mapa_dias[d] for d in lista_dias_idxs])

    def _formatar_frequencia(self, reserva_sala):
        horarios = reserva_sala.horarios.all().order_by('dia_semana', 'periodo')
        
        if not horarios.exists():
            return ""

        dias_periodos = {}
        for h in horarios:
            dias_periodos.setdefault(h.dia_semana, set()).add(h.periodo)

        periodos_para_dias = {}
        for dia, periodos_set in dias_periodos.items():
            chave_periodos = frozenset(periodos_set)
            periodos_para_dias.setdefault(chave_periodos, []).append(dia)

        linhas = []
        for periodos_set, lista_dias in periodos_para_dias.items():
            texto_dias = self._criar_intervalo_dias(lista_dias)
            
            if {1, 2, 3, 4}.issubset(periodos_set):
                linhas.append(texto_dias)
            else:
                lista_p = sorted(list(periodos_set))
                texto_p = ",".join([f"{p}ºH" for p in lista_p])
                linhas.append(f"{texto_dias} {texto_p}")

        return "\n".join(linhas)

    def _montar_texto_celula(self, reservas_lista):
        if not reservas_lista:
            return "LIVRE"
        
        textos = []
        for r in reservas_lista:
            turma = r.id_reserva.codigo_turma if r.id_reserva else "Sem Turma"
            responsavel = r.responsavel
            
            dias_horarios = self._formatar_frequencia(r)
            
            item = f"{turma}\n{dias_horarios}\n({responsavel})"
            textos.append(item)
        
        return "\n\n".join(textos)

    def gerar_pdf(self):
        title_style = self.styles['Heading1']
        title_style.alignment = 1
        self.elements.append(Paragraph("Mapa de Distribuição de Salas - Unieuro", title_style))
        self.elements.append(Spacer(1, 0.5*cm))

        blocos = Bloco.objects.filter(ativo=True).order_by('bloco')

        for bloco in blocos:
            self.elements.append(Paragraph(f"BLOCO {bloco.bloco}", self.styles['Heading2']))
            
            data = [['Sala / Andar', 'Matutino', 'Vespertino', 'Noturno', 'Capacidade', 'Recursos']]
            
            salas = Sala.objects.filter(id_bloco=bloco, is_deleted=False).order_by('andar', 'numero_sala').prefetch_related(
                Prefetch(
                    'reservasala_set',
                    queryset=ReservaSala.objects.filter(status_reserva=True, is_deleted=False).select_related('id_reserva'),
                    to_attr='reservas_ativas'
                ),
                'reservas_ativas__horarios'
            )

            if not salas.exists():
                self.elements.append(Paragraph("Nenhuma sala cadastrada.", self.styles['Normal']))
                self.elements.append(Spacer(1, 0.5*cm))
                continue

            for sala in salas:

                matutino_res = [r for r in sala.reservas_ativas if r.turno == 'Matutino']
                vespertino_res = [r for r in sala.reservas_ativas if r.turno == 'Vespertino']
                noturno_res = [r for r in sala.reservas_ativas if r.turno == 'Noturno']
                
                matutino_txt = self._montar_texto_celula(matutino_res)
                vespertino_txt = self._montar_texto_celula(vespertino_res)
                noturno_txt = self._montar_texto_celula(noturno_res)
                
                recursos = []
                if sala.tv_tamanho: recursos.append(f"TV {sala.tv_tamanho}")
                if sala.data_show: recursos.append("DataShow")
                str_recursos = "\n".join(recursos) if recursos else "-"

                data.append([
                    f"{sala.numero_sala}\n({sala.andar})",
                    matutino_txt,
                    vespertino_txt,
                    noturno_txt,
                    str(sala.capacidade),
                    str_recursos
                ])

            tabela = Table(data, colWidths=[2.5*cm, 7*cm, 7*cm, 7*cm, 2.5*cm, 3*cm])
            
            estilo_tabela = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ])
            
            tabela.setStyle(estilo_tabela)
            self.elements.append(tabela)
            self.elements.append(Spacer(1, 1*cm))

        self.doc.build(self.elements)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf