from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Alumni

def alumni_directory(request):
    query = request.GET.get('q', '')  # Get search query from GET params

    # Fetch all alumni and order by batch ascending, then by full name
    alumni_list = Alumni.objects.select_related('user', 'user__profile').order_by(
        'user__profile__batch', 'user__first_name', 'user__last_name'
    )

    # Filter if search query exists
    if query:
        alumni_list = alumni_list.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__profile__batch__icontains=query)
        )

    return render(request, 'alumni/directory.html', {
        'alumni_list': alumni_list,
        'query': query
    })


def alumni_detail(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    return render(request, 'alumni/detail.html', {'alumni': alumni})
