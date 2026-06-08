from django import forms
from django.forms import ModelForm, ValidationError
from .models import Sala

class ValidacaoSala(forms.ModelForm):

    class Meta:
        model = Sala
        fields = ['id_bloco', 'criador_por', 'andar', 'numero_sala', 'capacidade', 'tv_tamanho', 'data_show']

    def clean(self):
        cleaned_data = super().clean()
        _id_bloco = cleaned_data.get('id_bloco')
        _andar = cleaned_data.get('andar')
        _numero_sala = cleaned_data.get('numero_sala')

        if _id_bloco and _andar and _numero_sala:
            consulta = Sala.objects.filter(
                id_bloco=_id_bloco,
                andar=_andar,
                numero_sala=_numero_sala
            )

            if consulta.exists():
                raise ValidationError('Já existe uma sala com este número neste bloco e andar.')
        
        return cleaned_data