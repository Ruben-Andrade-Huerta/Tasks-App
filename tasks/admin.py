from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'user', 'created_at', 'terminated_at')
    list_filter = ('priority', 'user')
    search_fields = ('title', 'description')


# Register your models here.
admin.site.register(Task, TaskAdmin)