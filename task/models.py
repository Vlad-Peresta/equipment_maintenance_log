from django.db import models

from worker.models import Worker


class TaskType(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    PRIORITY_CHOICES = (("urgent", "Urgent"), ("high", "High"), ("low", "Low"))

    name = models.CharField(max_length=127)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["is_completed", "deadline"]

    def __str__(self):
        return f"{self.name}, is_completed - {self.is_completed}"
