from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('posts:post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})
