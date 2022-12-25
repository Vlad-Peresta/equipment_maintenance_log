from django import template

from task.models import Task, TaskType

register = template.Library()


@register.simple_tag
def performed_tasks_number():
    return Task.objects.filter(is_completed=True).count()


@register.simple_tag
def active_tasks_number():
    return Task.objects.filter(is_completed=False).count()


@register.simple_tag
def created_task_names_number():
    return TaskType.objects.count()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()

    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, 0)

    return updated.urlencode()
