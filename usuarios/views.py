from datetime import datetime
import secrets
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import View
from django.views.generic import UpdateView
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ._forms import EditarUsuario
from .models import Usuario
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.forms import SetPasswordForm
from django.conf import settings

# Create your views here.

# As views serao criadas seguindo o modelo CBVs

# CBV para login de usuario passando matricula e senha
class LoginUsuario(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "usuarios/login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        matricula = request.POST.get("matricula")
        senha = request.POST.get("senha")
        usuario = authenticate(request, username=matricula, password=senha)
        if usuario is not None:
            login(request, usuario)
            messages.success(request, f"Bem-vindo(a) de volta, {usuario.nome}!")
            return redirect("home")
        
        messages.error(request, "Matrícula ou senha inválidos.")
        return render(request, "usuarios/login.html")


# CBV para logout de usuario
class LogoutUsuario(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        messages.success(request, "Você saiu do sistema.")
        return redirect("login")


# CBV para edicao de usuario
class Perfil(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = EditarUsuario
    template_name = "usuarios/edicao.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Dados atualizados com sucesso!")
        return super().form_valid(form)

#-------------------------------------------------------------------------------

class EnviarEmail(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "usuarios/enviar_email.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get("email")
        request.session["email_recuperacao"] = email
        if not email:
            messages.error(request, "Por favor, informe seu email")
            return render(request, "usuarios/enviar_email.html")

        try:
            usuario = Usuario.objects.get(email_institucional=email)
        except Usuario.DoesNotExist:
            usuario = None

        if usuario:
            codigo = secrets.randbelow(10**6)
            request.session["codigo"] = codigo
            request.session["codigo_generated_at"] = timezone.now().isoformat()
            send_mail(
                "Troca de senha",
                f"Este e o codigo para trocar de senha {codigo}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, "Código de recuperação enviado para o seu e-mail.")
        else:
            messages.error(request, "E-mail não encontrado em nossa base de dados.")
            return render(request, "usuarios/enviar_email.html")
            
        return redirect("confirmacaocodigo")


class ConfirmacaoCodigo(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "usuarios/codigo.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        usuario_codigo = request.POST.get("usuario_codigo")
        codigo = request.session.get("codigo")
        tentativas = request.session.get("tentativas_codigo", 0) + 1
        request.session["tentativas_codigo"] = tentativas

        generated_at_iso = request.session.get("codigo_generated_at")
        if generated_at_iso:
            try:
                generated_at = datetime.fromisoformat(generated_at_iso)
                
                if timezone.is_aware(generated_at):
                    agora = timezone.now()
                else:
                    agora = datetime.now()

                if agora - generated_at > timezone.timedelta(minutes=10):
                    self.limpar_sessao_codigo(request)
                    messages.error(request, "Código expirado, solicite novamente")
                    return redirect("enviaremail")
            except Exception as e:
                self.limpar_sessao_codigo(request)
                messages.error(request, "Erro na validação, solicite novamente")
                return redirect("enviaremail")

        # 2. Verifica Limite de Tentativas
        if tentativas >= 5:
            self.limpar_sessao_codigo(request)
            messages.error(request, "Número de tentativas excedido")
            return redirect("enviaremail")

        # 3. Verifica se o Código bate
        if str(codigo) == str(usuario_codigo):
            self.limpar_sessao_codigo(request)
            request.session["codigo_verificado"] = True
            messages.success(request, "Código validado! Agora você pode criar sua nova senha.")
            return redirect("novasenha")

        messages.error(request, f"Código incorreto. Você tem mais {5 - tentativas} tentativas.")
        return render(request, "usuarios/codigo.html")
    
    def limpar_sessao_codigo(self, request):
        """Helper para limpar dados sensíveis da sessão"""
        request.session.pop("codigo", None)
        request.session.pop("codigo_generated_at", None)
        request.session.pop("tentativas_codigo", None)

class NovaSenha(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.session.get("codigo_verificado"):
            messages.error(request, "Acesso nao autorizado")
            return redirect("enviaremail")
        form = SetPasswordForm(user=None)
        return render(request, "usuarios/nova_senha.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        if not request.session.get("codigo_verificado"):
            messages.error(request, "Acesso nao autorizado")
            return redirect("enviaremail")
        email = request.session.get("email_recuperacao")
        try:
            usuario = Usuario.objects.get(email_institucional=email)
        except Usuario.DoesNotExist:
            messages.error(request, "Erro inesperado, tente novamente")
            return redirect("enviaremail")

        form = SetPasswordForm(user=usuario, data=request.POST)
        if form.is_valid():
            form.save()
            request.session.pop("email_recuperacao", None)
            request.session.pop("codigo_verificado", None)
            return redirect("login")
        return render(request, "usuarios/nova_senha.html", {"form": form})