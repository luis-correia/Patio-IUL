# Generated by Django 2.1.7 on 2019-05-16 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_usersboqueados'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersOcultados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocultados', models.ManyToManyField(related_name='ocultados', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='usersboqueados',
            name='users',
        ),
        migrations.DeleteModel(
            name='UsersBoqueados',
        ),
    ]
