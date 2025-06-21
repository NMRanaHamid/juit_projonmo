from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_by', 'posted_at', 'deadline')
    search_fields = ('title', 'company', 'location')
    list_filter = ('posted_at', 'deadline')
