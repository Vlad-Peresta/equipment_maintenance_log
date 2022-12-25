from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from worker.models import Position, Worker

admin.site.register(Position)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info", {"fields": ("position",)}
        ),

    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": ("position",)
            }
        ),
    )
