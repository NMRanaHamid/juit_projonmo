from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import News
from .forms import NewsForm

def news_list(request):
    news_items = News.objects.order_by('-published_date')
    return render(request, 'news/news_list.html', {'news_items': news_items})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})

# Admin check
def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news:news_list')
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form, 'update': False})

@user_passes_test(is_admin)
def news_update(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news:news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/news_form.html', {'form': form, 'update': True})

@user_passes_test(is_admin)
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('news:news_list')
    return render(request, 'news/news_confirm_delete.html', {'news': news})
