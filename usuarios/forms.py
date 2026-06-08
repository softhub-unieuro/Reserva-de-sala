import string
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario
import re

class PasswordInputWithToggle(forms.PasswordInput):
    """Widget customizado para campo de senha com toggle de visibilidade"""
    template_name = 'widgets/password_input_toggle.html'
    
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if self.attrs is None:
            self.attrs = {}
        self.attrs['class'] = self.attrs.get('class', '') + ' pr-10'

class ValidacaoUsuario(forms.ModelForm):

    senha = forms.CharField(widget=forms.PasswordInput(), label='Senha', required=True)
    senha2 = forms.CharField(widget=forms.PasswordInput(), label='Confirmação da senha', required=True)
    email_institucional = forms.EmailField(required=True, help_text='O email e obrigatorio!')
    
    #cria um formulario com os campos abaixo para validacao dos dados
    class Meta:
        model = Usuario
        fields = ('matricula', 'nome', 'email_institucional', 'telefone', 'data_nascimento', 'sexo', 'cargo',)

    #Faz a validacao da matricula 
    def clean_matricula(self):
        matricula = str(self.cleaned_data.get("matricula"))
        if not matricula.isdigit():
            raise forms.ValidationError('Matricula incorreta')
        if len(matricula) < 6:
            raise forms.ValidationError('Matricula incorreta')
        return matricula
    
    #Faz a validacao do email institucional
    def clean_email_institucional(self):
        email = self.cleaned_data.get("email_institucional")
        usuario_id = getattr(self.instance, "id", None)
        if Usuario.objects.filter(email_institucional=email).exclude(id=usuario_id).exists():
            raise forms.ValidationError("Email ja cadastrado!")
        return email
    
    #Faz a validacao do telefone
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '')
        telefone_validado = re.sub(r'\D', '', telefone)
        if len(telefone_validado) < 10:
            raise forms.ValidationError("Telefone incorreto. Deve ter DDD e número.")
        return telefone_validado

    def clean_senha(self):
        maisculas = string.ascii_uppercase
        minusculas = string.ascii_lowercase
        caracteres = string.punctuation
        
        senha = self.cleaned_data.get('senha')
        senhaconfirmada = self.cleaned_data.get('confirmacaosenha')

        if len(senha) < 8:
            raise forms.ValidationError('A senha precisa ter no minimo 8 digitos')
        
        if not any(char in maisculas for char in senha):
            raise forms.ValidationError('A senha precisa ter uma letra maiscula')
        
        if not any(char in minusculas for char in senha):
            raise forms.ValidationError('A senha precisa ter uma letra minuscula')
        
        if not any(char in caracteres for char in senha):
            raise forms.ValidationError('A senha precisa ter um caractere')
        
        if senha and senhaconfirmada and senha != senhaconfirmada:
            raise forms.ValidationError('Coloque a senha')
        return senha
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        senha = self.cleaned_data.get('senha')
        if senha:
            usuario.set_password(senha)
        if commit:
            usuario.save()
        return usuario


class UsuarioAdminCreationForm(UserCreationForm):
    """Formulário customizado para admin adicionar usuários com toggle de senha"""
    
    class Meta:
        model = Usuario
        fields = ('matricula', 'nome', 'email_institucional', 'telefone', 'data_nascimento', 'sexo', 'cargo')
    
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
            )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js',
            'js/admin_password_toggle.js',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classe CSS ao password1 e password2 para styling
        self.fields['password1'].widget = PasswordInputWithToggle(attrs={
            'class': 'form-control pr-10',
            'data-toggle-password': 'true',
            'id': 'id_password1'
        })
        self.fields['password2'].widget = PasswordInputWithToggle(attrs={
            'class': 'form-control pr-10',
            'data-toggle-password': 'true',
            'id': 'id_password2'
        })