'''
signal -> evento de criar conta passando o cargo
sender -> objeto q envia o sinal "usuario"
receive -> ouve o sinal e faz a funcao

usados
post_save()
user.save()
'''

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Usuario

@receiver(post_save, sender=Usuario)
def atualizar_grupo_do_usuario(sender, instance, created, **kwargs):
    cargo = instance.cargo
    
    try:
        novo_grupo = Group.objects.get(name=cargo)
    except Group.DoesNotExist:
        return
    
    if created:
        instance.groups.clear()
        instance.groups.add(novo_grupo)
        return

    grupos_atuais = instance.groups.all()

    if novo_grupo not in grupos_atuais:
        instance.groups.set([novo_grupo])