from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, Value, IntegerField
from .models import Alumni

def alumni_directory(request):
    query = request.GET.get('q', '')  

    alumni_list = Alumni.objects.select_related('user', 'user__profile')

    # Filter if search query exists
    if query:
        alumni_list = alumni_list.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__profile__batch__icontains=query)
        )

    # Custom ordering: teacher → staff → lab assistant → unknown → numeric batches ascending
    alumni_list = alumni_list.annotate(
        batch_order=Case(
            When(user__profile__batch__iexact="teacher", then=Value(0)),
            When(user__profile__batch__iexact="staff", then=Value(1)),
            When(user__profile__batch__iexact="lab assistant", then=Value(2)),
            When(Q(user__profile__batch__isnull=True) | Q(user__profile__batch=""), then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    ).order_by("batch_order", "user__profile__batch", "user__first_name", "user__last_name")

    return render(request, 'alumni/directory.html', {
        'alumni_list': alumni_list,
        'query': query
    })


def alumni_detail(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    return render(request, 'alumni/detail.html', {'alumni': alumni})
