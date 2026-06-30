from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    DailySubmissionViewSet,
    ProgressUpdateViewSet
)

router = DefaultRouter()

router.register(
    r'employees',
    EmployeeViewSet,
    basename='employees'
)

router.register(
    r'submissions',
    DailySubmissionViewSet,
    basename='submissions'
)

router.register(
    r'progress',
    ProgressUpdateViewSet,
    basename='progress'
)

urlpatterns = router.urls