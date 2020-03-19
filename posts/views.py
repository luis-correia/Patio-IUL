from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.forms import modelformset_factory
from django.conf import settings
from django.core.mail import send_mail
from .models import Post, PostImage, PostLikes, PostComment, HidePost
from .forms import MakePost, AddImage, AddComment, SendPostReport
from django.contrib.auth.decorators import login_required

MAX_IMAGES_PER_POST = 5

@login_required
def timeline(request):
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
            #mandar mensagem
            return redirect(reverse('posts:timeline'))

        else:
            #mandar mensagem
            return redirect(reverse('posts:timeline'))

    form_content = MakePost()
    form_image = AddImageSet(queryset=PostImage.objects.none())
    posts = Post.objects.order_by('-date')

    #Posts ocultados
    posts_to_hide = request.user.hidepost_set.all().values('post_id')
    if posts_to_hide:
        posts = posts.exclude(id__in=posts_to_hide)

    #Users Ocultados
    users_to_hide = request.user.lista_ocultados.ocultados.all().values('id')
    if users_to_hide:
        posts = posts.exclude(author_id__in=users_to_hide)

    # Users that blocked me
    users_that_blocked_me = request.user.bloqueado_por.all().values('user_id')
    if users_that_blocked_me:
        posts = posts.exclude(author_id__in=users_that_blocked_me)

    return render(request, 'posts/timeline.html', context={'form_content': form_content,
                                                           'form_image': form_image,
                                                           'posts': posts
                                                           })


@login_required
def view_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    comments = post.postcomment_set.order_by('-date')

    #Post ocultados
    posts_to_hide = request.user.hidepost_set.all().values('post_id')

    #Users ocultados
    users_to_hide = request.user.lista_ocultados.ocultados.all().values('id')

    # Users bloqueados
    users_blocked = post.author.lista_bloqueados.bloqueados.all().values('id')

    # Users that blocked me
    users_that_blocked_me = request.user.bloqueado_por.all().values('user_id')

    #Voltar a timeline caso este post tenha sido ocultado ou o autor do post tenha sido ocultado ou o autor do post tenha bloqueado o user atual
    if posts_to_hide.filter(post_id=post_id).exists() or users_to_hide.filter(id=post.author.id).exists() or users_blocked.filter(id=request.user.id).exists():
        return redirect(reverse('posts:timeline'))

    #Ocultar comentarios de users ocultados e/ou users que tenham bloqueado o user atual
    if users_to_hide:
        comments = comments.exclude(author_id__in=users_to_hide)

    if users_that_blocked_me:
        comments = comments.exclude(author_id__in=users_that_blocked_me)

    user_has_like= False
    n_likes = post.postlikes_set.count()
    n_comments =  post.postcomment_set.count()
    like = None

    #Ver se o user tem like no post (por causa da cor do botão)
    for postlike in post.postlikes_set.all():
        if postlike.author.id == request.user.id:
            user_has_like=True
            like = postlike
            break

    if request.method == 'POST':
        if request.POST.get('like') == 'Like':
            if user_has_like:
                like.delete()
            else:
                like = PostLikes(post=post, author=request.user)
                like.save()
            return redirect(reverse('posts:view_post', kwargs={'post_id': post.id}))
        else:
            form = AddComment(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                # mensagem
                return redirect(reverse('posts:view_post', kwargs={'post_id': post.id}))

    form = AddComment()
    return render(request, 'posts/view_post.html', context={'post': post,
                                                            'form':form,
                                                            'comments': comments,
                                                            'user_has_like': user_has_like,
                                                            'n_likes': n_likes,
                                                            'n_comments': n_comments,
                                                             })


@login_required
def send_post_report(request, post_id):

    if request.method == 'POST':
        form = SendPostReport(request.POST)

        if form.is_valid():
            assunto = f'Post_id = {post_id} report'
            msg = form.cleaned_data['report']
            send_mail(assunto,
                      msg,
                      settings.EMAIL_HOST_USER,
                      ['luis-a-d-correia@live.com.pt'],
                      fail_silently=False)
            return redirect(reverse('posts:view_post', kwargs={'post_id':post_id}))

    form = SendPostReport()
    return render(request, 'users/send_user_report.html', context={'form': form,})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user.id != post.author.id:
        return redirect(reverse('posts:view_post', kwargs={'post_id': post_id}))
    if request.method == 'POST':
        if request.POST['opcao'] == 'Sim':
            post.delete()
            #mensagem
            return redirect(reverse('posts:timeline'))
        else:
            return redirect(reverse('posts:view_post', kwargs={'post_id': post_id}))
    return render(request, 'posts/delete_post.html')


@login_required
def ocultar_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        if request.POST['opcao'] == 'Sim':
            ocultar = HidePost(post=post, user=request.user)
            ocultar.save()
            # mensagem
            return redirect(reverse('posts:timeline'))
        else:
            return redirect(reverse('posts:view_post', kwargs={'post_id': post_id}))
    return render(request, 'posts/ocultar_post.html')


@login_required
def delete_comment(request, post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = PostComment.objects.get(id=comment_id)

    if request.user.id != comment.author.id and request.user.id != post.author.id:
        return redirect(reverse('posts:view_post', kwargs={'post_id': post_id}))

    if request.method == 'POST':
        if request.POST['opcao'] == 'Sim':
            comment.delete()
            #mensagem
            return redirect(reverse('posts:view_post', kwargs={'post_id': post_id}))
        else:
            return redirect(reverse('posts:view_post', kwargs={'post_id': post_id}))
    return render(request, 'posts/delete_comment.html')
