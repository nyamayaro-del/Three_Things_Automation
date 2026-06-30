from django.contrib import admin
from .models import (
    Employee,
    DailySubmission,
    ProgressUpdate
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "department",
        "active",
        "created_at",
    )

    list_filter = (
        "department",
        "active",
    )

    search_fields = (
        "name",
        "phone_number",
    )


@admin.register(DailySubmission)
class DailySubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "submission_date",
        "submitted_at",
    )

    list_filter = (
        "submission_date",
        "employee__department",
    )

    search_fields = (
        "employee__name",
    )


@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = (
        "submission",
        "updated_at",
    )

    search_fields = (
        "submission__employee__name",
    )

    list_filter = (
        "updated_at",
    )