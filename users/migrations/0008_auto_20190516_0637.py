# Generated by Django 2.1.7 on 2019-05-16 05:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190516_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersbloqueados',
            name='ocultados',
            field=models.ManyToManyField(default='', related_name='bloqueados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usersocultados',
            name='ocultados',
            field=models.ManyToManyField(default='', related_name='ocultados', to=settings.AUTH_USER_MODEL),
        ),
    ]
