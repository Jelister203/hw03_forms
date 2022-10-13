from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from django.http import HttpResponseRedirect
from .forms import PostForm
from django.core.paginator import Paginator


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
    'user': User.objects.get(username=username),
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
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    form = PostForm()
    context = {'form': form,}
    return render(request, 'posts/create_post.html', context)
