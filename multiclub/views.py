from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from .forms import CreationPost
from django.views.decorators.cache import cache_page


@login_required
def new_post(request):
    group = Group.objects.all()
    if request.method == 'POST':
        form = CreationPost(request.POST, files=request.FILES)
        get = request.POST.get('group')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if get == 0:
                post.group = None
            else:
                post.group = Group.objects.filter(id=get).first()
            post.save()
            return redirect(f'social:profile', request.user)
    else:
        form = CreationPost()
    context = {
        'form': form,
        'group': group,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def index(request):
    title = 'Главная страница'
    user = User.objects.get(username=str(request.user))
    following = user.follower.all().values_list('author', flat=True)
    # posts = Post.objects.filter(author_id__in=following).order_by('-pub_date')
    posts = Post.objects.select_related('group').all().order_by('-pub_date')
    pag = Paginator(posts, 10)
    pag_number = request.GET.get('page')
    page_obj = pag.get_page(pag_number)
    context = {
        'title': title,
        'posts': page_obj,
    }

    return render(request, 'posts/index.html', context)

@login_required
def sub(request):
    title = 'Главная страница'
    user = User.objects.get(username=str(request.user))
    following = user.follower.all().values_list('author', flat=True)
    posts = Post.objects.filter(author_id__in=following).order_by('-pub_date')
    # posts = Post.objects.select_related('group').all().order_by('-pub_date')
    pag = Paginator(posts, 10)
    pag_number = request.GET.get('page')
    page_obj = pag.get_page(pag_number)
    context = {
        'title': title,
        'posts': page_obj,
    }

    return render(request, 'posts/index.html', context)

@login_required
def group_posts(request, slug):
    if not Group.objects.filter(slug=slug).exists():
        raise Http404("Page not found")
    else:
        group_post = Post.objects.select_related('group').all().filter(group__slug=slug).order_by('-pub_date')
        pag = Paginator(group_post, 10)
        pag_number = request.GET.get('page')
        page_obj = pag.get_page(pag_number)
        group_name = Group.objects.filter(slug=slug).first().title
    context = {
        'name': group_name,
        'posts': page_obj,
        'slug_name': slug,
        'title': f'Группа {group_name}',
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def profile(request, username):
    user_post = Post.objects.select_related('author').filter(author__username=username).order_by('-pub_date')
    follow_check = False
    follower = User.objects.filter(username=str(request.user)).first().id
    author = User.objects.filter(username=username).first().id
    if not Follow.objects.filter(user_id=follower).filter(author_id=author).exists():
        follow_check = True
    pag = Paginator(user_post, 10)
    pag_number = request.GET.get('page')
    page_obj = pag.get_page(pag_number)
    count_post = user_post.count()

    context = {
        'username': username,
        'posts': page_obj,
        'count': count_post,
        'follow': follow_check,
        'curruser': str(request.user),
    }
    if User.objects.filter(username=username).exists():
        return render(request, 'posts/profile.html', context)
    else:
        raise Http404("Page not found")


@login_required
def post_detail(request, post_id):
    if not Post.objects.filter(id=post_id).exists():
        raise Http404("Page not found")
    comments = Comment.objects.filter(post=post_id).all()
    info_post = Post.objects.select_related('author').filter(id=post_id).first()
    post_count = Post.objects.select_related('author').filter(author__username=info_post.author.username).count()
    group_post = Post.objects.select_related('group').filter(id=post_id).first()
    user = str(request.user)
    pag = Paginator(comments, 10)
    pag_number = request.GET.get('page')
    page_obj = pag.get_page(pag_number)
    context = {
        'posts': info_post,
        'count': post_count,
        'group_posts': group_post,
        'user_post': user,
        'comment': comments,
        'comments': page_obj,
    }
    return render(request, 'posts/post_detail.html', context)


class about(TemplateView):
    template_name = 'posts/aboutus.html'


class tech(TemplateView):
    template_name = 'posts/tech.html'


@login_required
def update_post(request, post_id):
    user = Post.objects.select_related('author').filter(id=post_id).first()
    if user.author.username != str(request.user):
        raise Http404("Страница не найдена")
    post = Post.objects.select_related('group').filter(id=post_id).first()
    if post.group and post.group.title:
        group = Group.objects.exclude(title=post.group.title)
    else:
        group = Group.objects.all()
    if request.method == 'POST':
        form = CreationPost(request.POST, files=request.FILES, instance=post)
        get = request.POST.get('group')
        print('-----------------\n', get, '\n---------------')
        if form.is_valid():
            if get == '':
                pass
            else:
                if get == 0:
                    post.group = None
                else:
                    post.group = Group.objects.filter(id=get).first()
            post.save()
            return redirect(f'social:profile', request.user)
    else:
        form = CreationPost(instance=post)
    context = {
        'form': form,
        'group': group,
        'edit': 1,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)


def follow(request, username):
    follower = User.objects.filter(username=str(request.user)).first().id
    following = User.objects.filter(username=username).first().id
    if Follow.objects.filter(author_id=following).filter(user_id=follower).exists():
        follows = Follow.objects.filter(author_id=following).filter(user_id=follower)
        follows.delete()
    else:
        follows = Follow.objects.create(author_id=following,user_id=follower)
        follows.save()
    return redirect('social:profile', username)

@login_required
def comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        text = request.POST['text']
        comment = Comment.objects.create(com_text=text, post=post, com_author=request.user)
        comment.save()
        messages.success(request, 'Комментарий успешно добавлен!')
        return redirect('social:post_detail', post.pk)
    else:
        return redirect('social:post_detail', post.pk)


def page_not_found(request, exception):
    return render(request, 'includes/404.html', {'path': request.path}, status=404)
