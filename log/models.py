from django.contrib.auth import get_user_model
from django.db import models


class EquipmentType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Equipment(models.Model):
    name = models.CharField(max_length=127, unique=True)
    inventory_number = models.CharField(max_length=63, unique=True)
    type = models.ForeignKey(
        EquipmentType, on_delete=models.CASCADE, related_name="equipment"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "equipment"
        verbose_name_plural = "equipment"

    def __str__(self):
        return f"{self.name} - {self.type}"


class BreakdownType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Breakdown(models.Model):
    STATUS_CHOICES = (("completed", "Completed"), ("process", "In process"))

    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="breakdowns"
    )
    repair_staff = models.ManyToManyField(
        get_user_model(), related_name="breakdowns"
    )
    breakdown_type = models.ForeignKey(
        BreakdownType, on_delete=models.CASCADE, related_name="breakdowns"
    )
    circumstance = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="process"
    )
    repair_duration = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return f"{self.equipment} - {self.time}"
