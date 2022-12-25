from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="workers"
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
