from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Group, Post

User = get_user_model()


def my_paginator(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}


def index(request):
    post_list = Post.objects.select_related("group", "author")
    context = my_paginator(request, post_list)
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    context = my_paginator(request, post_list)
    context.update({
        'group': group,
    })
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    context = my_paginator(request, post_list)
    context.update({
        'author': User.objects.get(username=username),
    })
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    context = {
        'post': Post.objects.get(pk=post_id),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.text = request.POST.get('text')  # без этих строк текст поста
        form.save()
        return redirect('posts:profile', request.user)
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    if post.author != request.user:
        return redirect('posts:post_detail', post.pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.text = request.POST.get('text')  # становится True
        post.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {'form': form, 'is_edit': is_edit}
    return render(request, 'posts/create_post.html', context)
