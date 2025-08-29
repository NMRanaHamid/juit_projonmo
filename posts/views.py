from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, PostImage, Like, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    
    liked_ids = []
    if request.user.is_authenticated:
        liked_ids = request.user.like_set.values_list('post_id', flat=True)  # posts user liked

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'liked_ids': liked_ids
    })



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by('-created_at')
    form = CommentForm()

    user_liked = False
    if request.user.is_authenticated:
        user_liked = post.likes.filter(user=request.user).exists()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('posts:post_detail', pk=pk)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'user_liked': user_liked
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        images = request.FILES.getlist('images')  # multiple images

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for img in images:
                PostImage.objects.create(post=post, image=img)

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
        images = request.FILES.getlist('images')

        if form.is_valid():
            form.save()
            for img in images:
                PostImage.objects.create(post=post, image=img)

            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def delete_images(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        ids = request.POST.getlist("delete_images")
        PostImage.objects.filter(id__in=ids, post=post).delete()
    return redirect("posts:post_detail", pk=post.pk)


@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        return redirect('posts:post_detail', pk=comment.post.pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'posts/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if comment.user == request.user:
        comment.delete()
    return redirect('posts:post_detail', pk=post_pk)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Only the author can delete
    if post.author != request.user:
        return redirect('posts:post_detail', pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect('posts:post_list')  # Redirect to posts list after deletion

    # Optional: confirmation page
    return render(request, 'posts/post_confirm_delete.html', {'post': post})
