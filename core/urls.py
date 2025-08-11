from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BusViewSet, AdminViewSet, SupervisorViewSet, DriverViewSet, StudentViewSet, GuardianViewSet,
    AttendanceViewSet, AnnouncementViewSet, BusAssignmentViewSet, BusRouteViewSet, BusRoutePointViewSet,
    TripViewSet, TripStudentViewSet, FeedbackViewSet, MaintenanceLogViewSet, NotificationViewSet,
    ReminderViewSet, GPSTrackingViewSet, ClassViewSet, health
)

router = DefaultRouter()
router.register(r'buses', BusViewSet)
router.register(r'admins', AdminViewSet)
router.register(r'supervisors', SupervisorViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'students', StudentViewSet)
router.register(r'guardians', GuardianViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'bus-assignments', BusAssignmentViewSet)
router.register(r'bus-routes', BusRouteViewSet)
router.register(r'bus-route-points', BusRoutePointViewSet)
router.register(r'trips', TripViewSet)
router.register(r'trip-students', TripStudentViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'maintenance-logs', MaintenanceLogViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'reminders', ReminderViewSet)
router.register(r'gps-tracking', GPSTrackingViewSet)
router.register(r'classes', ClassViewSet)

urlpatterns = [
    path('health/', health, name='health'),
    path('', include(router.urls)),
]
