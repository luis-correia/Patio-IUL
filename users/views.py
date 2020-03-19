from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import UserProfil, UsersOcultados, UsersBloqueados
from posts.models import PostImage
from django.forms import modelformset_factory
from posts.forms import MakePost, AddImage
from .forms import RegisterForm, EditProfilForm, SendUserReport
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

MAX_IMAGES_PER_POST = 5


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect(reverse('posts:timeline'))
    login_view_response = LoginView.as_view(template_name='users/login.html')
    return login_view_response(request)


def register(request):
    user = request.user
    if user.is_authenticated:
        return redirect(reverse('posts:timeline'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            UserProfil.objects.create(user=user)
            UsersOcultados.objects.create(user=user)
            UsersBloqueados.objects.create(user=user)
            #adicionar mensagem
            return redirect(reverse('users:current_user_profile'))
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})


@login_required
def privacidade(request):

    posts_hided = request.user.hidepost_set.all()
    users_hided = request.user.lista_ocultados.ocultados.all()
    users_blocked = request.user.lista_bloqueados.bloqueados.all()

    return render(request, 'users/privacidade.html', context={'posts_hided': posts_hided,
                                                              'users_hided': users_hided,
                                                              'users_blocked': users_blocked
                                                                })


@login_required
def tirar_post_ocultado(request, post_id):
    if request.method == 'POST':
        if request.POST['opcao'] == 'Sim':
            post = request.user.hidepost_set.get(post_id=post_id)
            post.delete()
            # mensagem
            return redirect(reverse('users:privacidade'))

        else:
            return redirect(reverse('users:privacidade'))

    return render(request, 'users/tirar_post_ocultado.html')


@login_required
def tirar_user_ocultado(request, user_id):
    if request.method == 'POST':
        if request.POST['opcao'] == 'Sim':
            user = User.objects.get(id=user_id)
            request.user.lista_ocultados.ocultados.remove(user)
            # mensagem
            return redirect(reverse('users:privacidade'))

        else:
            return redirect(reverse('users:privacidade'))

    return render(request, 'users/tirar_user_ocultado.html')


@login_required
def tirar_user_bloqueado(request, user_id):
    if request.method == 'POST':
        if request.POST['opcao'] == 'Sim':
            user = User.objects.get(id=user_id)
            request.user.lista_bloqueados.bloqueados.remove(user)
            # mensagem
            return redirect(reverse('users:privacidade'))

        else:
            return redirect(reverse('users:privacidade'))

    return render(request, 'users/tirar_user_bloqueado.html')


@login_required
def show_all_users(request):
    users = User.objects.exclude(id=request.user.id).order_by('username')

    #Users ocultados
    users_to_hide = request.user.lista_ocultados.ocultados.all().values('id')
    if users_to_hide:
        users = users.exclude(id__in=users_to_hide)

    #Users that blocked me
    users_that_blocked_me = request.user.bloqueado_por.all().values('user_id')
    if users_that_blocked_me:
        users = users.exclude(id__in=users_that_blocked_me)

    return render(request, 'users/all_users.html', context={'users': users})


@login_required
def current_user_profile(request):

    AddImageSet = modelformset_factory(
        PostImage,
        form=AddImage,
        extra=MAX_IMAGES_PER_POST,
    )
    if request.method == 'POST':
        form_content = MakePost(request.POST)
        form_image = AddImageSet(request.POST,
                                 request.FILES,
                                 queryset=PostImage.objects.none(),
                                 )
        if form_content.is_valid() and form_image.is_valid():
            post = form_content.save(commit=False)
            post.author = request.user
            post.save()

            for form in form_image.cleaned_data:
                if form:
                    image = form['image']
                    photo = PostImage(post=post, image=image)
                    photo.save()
            # mandar mensagem
            return redirect(reverse('users:current_user_profile'))
        else:
            #mandar mensagem
            return redirect(reverse('users:current_user_profile'))
        pass

    form_content = MakePost()
    form_image = AddImageSet(queryset=PostImage.objects.none())
    posts = request.user.post_set.order_by('-date')
    liked_posts = request.user.postlikes_set.order_by('-id')
    comments = request.user.postcomment_set.order_by('-date')

    #Post ocultados
    posts_to_hide = request.user.hidepost_set.all().values('post_id')
    if posts_to_hide:
        liked_posts = liked_posts.exclude(post_id__in=posts_to_hide)

    #Users ocultados
    users_to_hide = request.user.lista_ocultados.ocultados.all().values('id')
    if users_to_hide:
        liked_posts = liked_posts.exclude(post__author_id__in=users_to_hide)

    return render(request, 'users/current_user_profile.html', context={'form_content': form_content,
                                                                       'form_image': form_image,
                                                                       'posts': posts,
                                                                       'comments': comments,
                                                                       'likes': liked_posts,
                                                                       })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfilForm(
                              request.POST,
                              request.FILES,
                              instance=request.user.userprofil,
                              )
        if form.is_valid():
            form.save()
            #adicionar mensagem
            return redirect(reverse('users:current_user_profile'))
    else:
        form = EditProfilForm(instance=request.user.userprofil)
    return render(request, 'users/edit_profile.html', context={'form': form})


@login_required
def user_profile(request, user_id):

    user = get_object_or_404(User, id=user_id)

    #Users ocultados
    users_to_hide = request.user.lista_ocultados.ocultados.all().values('id')
    if users_to_hide.filter(id=user_id).exists():
        #mensagem
        return redirect(reverse('posts:timeline'))

    #Users bloqueados
    users_blocked = user.lista_bloqueados.bloqueados.all().values('id')
    if users_blocked.filter(id=request.user.id).exists():
        #mensagem
        return redirect(reverse('posts:timeline'))

    if user.id == request.user.id:
        return redirect(reverse('users:current_user_profile'))

    posts = user.post_set.order_by('-date')
    comments = user.postcomment_set.order_by('-date')
    return render(request, 'users/other_user_profile.html', context={'user': user,
                                                                     'posts': posts,
                                                                     'comments': comments,
                                                                     })


@login_required
def send_report(request, user_id):

    if request.method == 'POST':
        form = SendUserReport(request.POST)

        if form.is_valid():
            assunto = f'User_id = {user_id} report'
            msg = form.cleaned_data['report']
            send_mail(assunto,
                      msg,
                      settings.EMAIL_HOST_USER,
                      ['luis-a-d-correia@live.com.pt'],
                      fail_silently=False)
            return redirect(reverse('users:user_profile', kwargs={'user_id':user_id}))

    form = SendUserReport()
    return render(request, 'users/send_user_report.html', context={'form': form,})



@login_required
def ocultar_user(request, user_id):

    if request.method == 'POST':
        if request.POST['opcao'] == 'Sim':
            user_a_ocultar = User.objects.get(id=user_id)
            request.user.lista_ocultados.ocultados.add(user_a_ocultar)
            #mensagem
            return redirect(reverse('posts:timeline'))

        else:
            return redirect(reverse('users:user_profile', kwargs={'user_id': user_id}))
    return render(request, 'users/ocultar_user.html')


@login_required
def bloquear_user(request, user_id):
    if request.method == 'POST':
        if request.POST['opcao'] == 'Sim':
            user_a_bloquear = User.objects.get(id=user_id)
            request.user.lista_bloqueados.bloqueados.add(user_a_bloquear)
            #mensagem
            return redirect(reverse('posts:timeline'))
        
        else:
            return redirect(reverse('users:user_profile', kwargs={'user_id': user_id}))
    return render(request, 'users/bloquear_user.html')
