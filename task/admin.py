from django.contrib import admin

from task.models import Task, TaskType

admin.site.register(TaskType)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_completed",
        "task_type",
    )
    search_fields = ("name",)
