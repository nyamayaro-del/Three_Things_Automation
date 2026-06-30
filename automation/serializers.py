from rest_framework import serializers
from .models import (
    Employee,
    DailySubmission,
    ProgressUpdate
)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class DailySubmissionSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    class Meta:
        model = DailySubmission
        fields = "__all__"


class ProgressUpdateSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source="submission.employee.name",
        read_only=True
    )

    class Meta:
        model = ProgressUpdate
        fields = "__all__"