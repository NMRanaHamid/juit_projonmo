from django.shortcuts import render, get_object_or_404
from .models import Alumni

def alumni_directory(request):
    alumni_list = Alumni.objects.all()
    return render(request, 'alumni/directory.html', {'alumni_list': alumni_list})

def alumni_detail(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    return render(request, 'alumni/detail.html', {'alumni': alumni})
