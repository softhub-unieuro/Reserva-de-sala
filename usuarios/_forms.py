from django import forms
from usuarios.models import Usuario

class EditarUsuario(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'placeholder': 'Seu nome completo'})
        self.fields['telefone'].widget.attrs.update({'placeholder': 'Digite seu Telefone'})
        self.fields['data_nascimento'].widget.attrs.update({'placeholder': 'Digite sua data de nascimento'})
        
    class Meta:
        model = Usuario 
        fields =  ['nome', 'telefone', 'data_nascimento']
        
