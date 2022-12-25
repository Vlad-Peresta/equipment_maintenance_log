from django.contrib import admin

from log.models import (
    Breakdown,
    BreakdownType,
    Equipment,
    EquipmentType,
)


admin.site.register(EquipmentType)
admin.site.register(BreakdownType)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "inventory_number", "type")
    search_fields = ("name",)
    list_filter = ("type",)


@admin.register(Breakdown)
class BreakdownAdmin(admin.ModelAdmin):
    list_display = (
        "equipment", "breakdown_type", "time", "repair_duration", "status",
    )
    search_fields = ("equipment", "breakdown_type",)
    list_filter = ("equipment", "repair_staff", "breakdown_type", "time",)
