import string
from django import forms
from django.forms import ModelForm
from usuarios.models import Usuario
import re

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