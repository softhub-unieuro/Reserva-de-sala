from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Retorna os parâmetros GET atuais (filtros) com a página atualizada.
    Exemplo de uso: ?{% param_replace page=page_obj.next_page_number %}
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()