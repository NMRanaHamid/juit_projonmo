from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm
from django.contrib import messages

def job_list(request):
    jobs = Job.objects.order_by('-posted_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.user != job.posted_by:
        messages.error(request, 'You are not authorized to edit this job.')
        return redirect('jobs:job_detail', pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('jobs:job_detail', pk=pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'update': True})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.user != job.posted_by:
        messages.error(request, 'You are not authorized to delete this job.')
        return redirect('jobs:job_detail', pk=pk)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('jobs:job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})
