from django.contrib import admin
from .models import UserProfil, UsersOcultados, UsersBloqueados

admin.site.register(UserProfil)
admin.site.register(UsersOcultados)
admin.site.register(UsersBloqueados)