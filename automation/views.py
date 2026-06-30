from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Employee,
    DailySubmission,
    ProgressUpdate
)

from .serializers import (
    EmployeeSerializer,
    DailySubmissionSerializer,
    ProgressUpdateSerializer
)


def missing_fields_response(request, fields):
    missing_fields = [
        field for field in fields
        if request.data.get(field) in (None, "")
    ]

    if missing_fields:
        return Response(
            {
                "error": "Missing required fields",
                "fields": missing_fields,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return None


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DailySubmissionViewSet(viewsets.ModelViewSet):
    queryset = DailySubmission.objects.all()
    serializer_class = DailySubmissionSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="submit"
    )
    def submit(self, request):

        validation_error = missing_fields_response(
            request,
            ["phone_number", "task_1", "task_2", "task_3"]
        )
        if validation_error:
            return validation_error

        phone_number = request.data.get("phone_number")
        today = timezone.localdate()

        try:
            employee = Employee.objects.get(
                phone_number=phone_number, active=True
            )
        except Employee.DoesNotExist:
            return Response(
                {
                    "error": "Employee not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if DailySubmission.objects.filter(
            employee=employee,
            submission_date=today
        ).exists():

            return Response(
                {
                    "message": "Submission already exists for today"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        submission = DailySubmission.objects.create(
            employee=employee,
            task_1=request.data.get("task_1"),
            task_2=request.data.get("task_2"),
            task_3=request.data.get("task_3"),
        )

        serializer = self.get_serializer(submission)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    

    @action(
        detail=False,
        methods=["get"],
        url_path="missing"
    )
    def missing_submissions(self, request):

        submitted_ids = DailySubmission.objects.filter(
            submission_date=timezone.localdate()
        ).values_list(
            "employee_id",
            flat=True
        )

        missing = Employee.objects.filter(active=True).exclude(
            id__in=submitted_ids
        )

        serializer = EmployeeSerializer(
            missing,
            many=True
        )

        return Response(serializer.data)


class ProgressUpdateViewSet(viewsets.ModelViewSet):
    queryset = ProgressUpdate.objects.all().order_by("-updated_at")
    serializer_class = ProgressUpdateSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="submit"
    )
    def submit_update(self, request):

        validation_error = missing_fields_response(
            request,
            ["phone_number", "completed_tasks", "pending_tasks", "challenges"]
        )
        if validation_error:
            return validation_error

        phone_number = request.data.get(
            "phone_number"
        )
        today = timezone.localdate()

        try:
            employee = Employee.objects.get(
                phone_number=phone_number
            )
        
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found"},
                status = status.HTTP_404_NOT_FOUND
            )
        
        
        try:
            submission = DailySubmission.objects.get(
                employee=employee,
                submission_date=today
            )

        except DailySubmission.DoesNotExist:
            
            return Response(
                {
                    "error": "No submission found for today"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        progress, created = ProgressUpdate.objects.update_or_create(
            submission=submission,
            defaults={
                "completed_tasks": request.data.get(
                    "completed_tasks"
                ),
                "pending_tasks": request.data.get(
                    "pending_tasks"
                ),
                "challenges": request.data.get(
                    "challenges"
                ),
            }
        )

        serializer = self.get_serializer(progress)

        return Response(serializer.data)


    @action(
        detail=False,
        methods=["get"],
        url_path="weekly-report"
    )
    def weekly_report(self, request):

        total_employees = Employee.objects.filter(active=True).count()
        
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())
        total_submissions = DailySubmission.objects.filter(submission_date__gte=week_start).count()

        return Response({
            "week_start": week_start,
            "active_employees": total_employees,
            "weekly_submissions": total_submissions,
        })
