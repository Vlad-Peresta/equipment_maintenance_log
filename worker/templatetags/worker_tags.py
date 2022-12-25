from django import template

from log.models import Breakdown
from task.models import Task

register = template.Library()


@register.simple_tag()
def performed_tasks_by_worker(worker_id):
    return Task.objects.filter(assignees=worker_id, is_completed=True).count()


@register.simple_tag()
def repaired_equipment_by_worker(worker_id):
    return Breakdown.objects.filter(
        status="completed", repair_staff=worker_id
    ).count()
