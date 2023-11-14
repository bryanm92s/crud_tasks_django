from django.contrib import admin
from .models import Task


# Show fields hidden (created)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields=("created",)

# Register your models here.
admin.site.register(Task, TaskAdmin)