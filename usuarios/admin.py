from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('matricula', 'nome', 'email_institucional', 'cargo', 'is_superuser')
    list_filter = ('matricula', 'cargo', 'is_superuser')
    search_fields = ('matricula', 'nome', 'email_institucional')
    ordering = ('matricula',)

    fieldsets = (
        (None, {'fields': ('matricula', 'password')}),
        ('Informações pessoais', {'fields': ('nome', 'email_institucional', 'telefone', 'data_nascimento', 'sexo', 'cargo')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricula', 'nome', 'email_institucional', 'telefone', 'data_nascimento', 'sexo', 'cargo', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )

    # Mapeia senha para AbstractBaseUser corretamente
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

admin.site.register(Usuario, UsuarioAdmin)
