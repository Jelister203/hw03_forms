from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    post_list = User.objects.get(username=username).posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': User.objects.get(username=username),
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    context = {
        'post': Post.objects.get(pk=post_id),
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            return render(request, 'posts/create_post.html', {'form': form})
        request.POST.get("group", None)
        post = form.save(commit=False)
        post.text = request.POST.get("text")
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    form = PostForm()
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            return render(request, 'posts/create_post.html',
                                   {'is_edit': is_edit, 'form': form})
        post.text = request.POST.get("text")
        group = request.POST.get("group")
        if group == '':
            post.group = None
            post.save()
            return redirect('posts:profile', username=post.author)
        post.group = Group.objects.get(pk=group)
        post.save()
        return redirect('posts:post_detail', post_id=post.pk)
    form = PostForm()
    form.text = post.text
    form.group = post.group
    context = {'is_edit': is_edit, 'form': form}
    return render(request, 'posts/create_post.html', context)
