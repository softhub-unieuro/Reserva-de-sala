from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from salas.models import Bloco, Sala, Curso, Turma
from reservas.models import Reserva, ReservaSala
from salas.forms import ValidacaoSala
from usuarios.forms import ValidacaoUsuario
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

# DashBoard Principal deve ser responsavel pela passagens da salas reservadas!
class Home(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request: HttpRequest) -> HttpResponse:
        reservas = self.get_filtered_queryset(request)

        paginator = Paginator(reservas, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = self.get_context_data()
        context['page_obj'] = page_obj
        context['filtros_at'] = request.GET 

        return render(request, 'home/home.html', context)

    def get_filtered_queryset(self, request):
        hoje = timezone.now().date()

        qs = ReservaSala.objects.filter(
            is_deleted=False,
            status_reserva=True,
            id_reserva__data_final__gte=hoje
        ).select_related(
            'id_sala', 
            'id_sala__id_bloco', 
            'id_reserva', 
            'id_reserva__id_curso'
        ).order_by('id_reserva__data_inicial', 'id_sala__id_bloco__bloco', 'id_sala__numero_sala')

        # --- APLICAÇÃO DOS FILTROS ---
        bloco = request.GET.get('bloco')
        andar = request.GET.get('andar')
        curso = request.GET.get('curso')
        data_inicial = request.GET.get('data_inicial')
        capacidade = request.GET.get('capacidade')

        if bloco and bloco != 'Todos':
            qs = qs.filter(id_sala__id_bloco__bloco=bloco)

        if andar and andar != 'Todos':
            qs = qs.filter(id_sala__andar=andar)

        if curso and curso != 'Todas':
            qs = qs.filter(id_reserva__id_curso__nome_curso=curso) 

        if data_inicial and data_inicial != 'Todas':
            qs = qs.filter(id_reserva__data_inicial=data_inicial)

        if capacidade and capacidade != 'Todas':
            qs = qs.filter(id_sala__capacidade=capacidade)

        return qs

    def get_context_data(self):
        return {
            "blocos": Bloco.objects.filter(ativo=True).order_by("bloco"),
            "andares": Sala.objects.values_list("andar", flat=True).distinct().order_by('andar'),
            "cursos": Curso.objects.all().order_by('nome_curso'),
            "datas_iniciais": Reserva.objects.values_list("data_inicial", flat=True).distinct().order_by('data_inicial'),
            "capacidades": Sala.objects.values_list("capacidade", flat=True).distinct().order_by('capacidade'),
        }
        

class Cadastro(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'usuarios.add_usuario'

    def get(self, request:HttpRequest)->HttpResponse:
        blocos = Bloco.objects.filter().order_by('bloco')
        salaForm = ValidacaoSala()
        usuarioForm = ValidacaoUsuario()
        context = {
            'sala_form': salaForm,
            'usuario_form': usuarioForm,
            'blocos': blocos
        }
        return render(request, 'home/cadastrar.html', context)
    
    def post(self, request:HttpRequest)->HttpResponse:
        salaForm = ValidacaoSala()
        usuarioForm = ValidacaoUsuario()

        if 'cadastro_sala' in request.POST: 
            print('entrou no post de sala')
            salaForm = ValidacaoSala(request.POST)
            if salaForm.is_valid():
                print('formulario validado')
                salaForm.save()
                return redirect('home')
            else:
                print('--- ERRO DE VALIDAÇÃO ---')
                print(salaForm.errors)
            return render(request, 'home/cadastrar.html', {'form': salaForm})
                
        elif 'cadastro_usuario' in request.POST:
            usuarioForm = ValidacaoUsuario(request.POST)
            if usuarioForm.is_valid():
                usuarioForm.save()
                return redirect('home')
            return render(request, 'home/cadastrar.html', {'form': usuarioForm})
        
        context = {
            'sala_form': salaForm,
            'usuario_form': usuarioForm
        }
        
        return render(request, 'home/cadastrar.html', context)
    
