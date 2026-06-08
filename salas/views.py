from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from salas.models import Sala, Bloco, Curso, Turma 

class ListarSalas(LoginRequiredMixin, ListView):
    model = Sala
    template_name = "salas/listarsalas.html"
    context_object_name = 'salas'
    paginate_by = 20

    def get_queryset(self):
        qs = Sala.objects.filter(is_deleted=False).select_related('id_bloco').order_by('id_bloco__bloco', 'andar', 'numero_sala')

        bloco = self.request.GET.get('bloco')
        andar = self.request.GET.get('andar')
        numero = self.request.GET.get('numero')
        capacidade = self.request.GET.get('capacidade')
        tv = self.request.GET.get('tv')

        if bloco:
            qs = qs.filter(id_bloco__bloco=bloco)

        if andar:
            qs = qs.filter(andar=andar)

        if numero:
            qs = qs.filter(numero_sala=numero)

        if capacidade:
            qs = qs.filter(capacidade=capacidade)

        if tv == 'sim':
            qs = qs.exclude(tv_tamanho__isnull=True).exclude(tv_tamanho='')
        elif tv == '-':
            qs = qs.filter(Q(tv_tamanho__isnull=True) | Q(tv_tamanho=''))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['blocos'] = Bloco.objects.filter(ativo=True).order_by('bloco')
        context['andares'] = Sala.objects.values_list("andar", flat=True).distinct().order_by('andar')
        context['numeros_salas'] = Sala.objects.values_list("numero_sala", flat=True).distinct().order_by('numero_sala')
        context['capacidades'] = Sala.objects.values_list("capacidade", flat=True).distinct().order_by('capacidade')
        context['tvs'] = [
            {"value": "sim", "label": "Com TV"},
            {"value": "-", "label": "Sem TV"},
        ]

        return context