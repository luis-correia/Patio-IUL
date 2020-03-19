from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class UserProfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    curso = models.CharField(max_length=20, default = '')
    n_matriculas = models.IntegerField(default=0)
    facebook = models.CharField(max_length=50, default= '')
    instagram = models.CharField(max_length=50, default = '')
    twitter = models.CharField(max_length=50, default = '')
    profil_image = models.ImageField(default='default_user_profile_pic.png', upload_to='profile_pic')
    description = models.CharField(max_length=100, default='')

    def __str__(self):
        return f'Profile: {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profil_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profil_image.path)


class UsersOcultados(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lista_ocultados' )
    ocultados = models.ManyToManyField(User, related_name='ocultado_por', default = '')


class UsersBloqueados(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lista_bloqueados' )
    bloqueados = models.ManyToManyField(User, related_name='bloqueado_por', default = '')