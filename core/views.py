from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import (
    Bus, Admin, Supervisor, Driver, Student, Guardian, Attendance, Announcement,
    BusAssignment, BusRoute, BusRoutePoint, Trip, TripStudent, Feedback,
    MaintenanceLog, Notification, Reminder, GPSTracking, Class
)
from .serializers import (
    BusSerializer, AdminSerializer, SupervisorSerializer, DriverSerializer, StudentSerializer, GuardianSerializer,
    AttendanceSerializer, AnnouncementSerializer, BusAssignmentSerializer, BusRouteSerializer, BusRoutePointSerializer,
    TripSerializer, TripStudentSerializer, FeedbackSerializer, MaintenanceLogSerializer, NotificationSerializer,
    ReminderSerializer, GPSTrackingSerializer, ClassSerializer
)

# Create your views here.
def index(request):
    return HttpResponse("Welcome to School Transport API")

# Health check endpoint
def health(request):
    return JsonResponse({"status": "ok"})

class BusViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing buses.
    - Filtering, searching, ordering enabled.
    - Pagination enabled.
    - Example request/response in Swagger.
    """
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['title', 'number', 'bus_id', 'status']
    ordering_fields = '__all__'
    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['get'], url_path='live')
    def live(self, request, pk=None):
        bus = self.get_object()
        now = timezone.localtime()
        today = now.date()
        # Latest GPS for this bus
        latest = GPSTracking.objects.filter(bus=bus).order_by('-timestamp').first()
        # Current or last trip
        trip = Trip.objects.select_related('route').filter(
            bus=bus, date=today, start_time__lte=now.time(), end_time__gte=now.time()
        ).first()
        if not trip:
            trip = Trip.objects.select_related('route').filter(bus=bus).order_by('-date', '-start_time').first()
        route = trip.route if trip else BusRoute.objects.filter(bus=bus).order_by('-id').first()
        route_points = list(BusRoutePoint.objects.filter(route=route).order_by('order')) if route else []
        # Students on the trip or assigned to the bus
        if trip:
            trip_students = TripStudent.objects.select_related('student').filter(trip=trip)
            students = [ts.student for ts in trip_students]
        else:
            students = list(Student.objects.filter(busassignment__bus=bus).distinct())

        features = []
        # Bus current position
        if latest:
            try:
                bus_lon = float(latest.longitude)
                bus_lat = float(latest.latitude)
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [bus_lon, bus_lat]},
                    "properties": {
                        "kind": "bus",
                        "bus_id": bus.id,
                        "title": bus.title,
                        "number": bus.number,
                        "timestamp": latest.timestamp.isoformat(),
                    },
                })
            except (TypeError, ValueError):
                pass

        # Route as LineString + stops
        if route_points:
            coords = []
            for p in route_points:
                try:
                    coords.append([float(p.longitude), float(p.latitude)])
                except (TypeError, ValueError):
                    continue
            if coords:
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": coords},
                    "properties": {"kind": "route", "route_name": route.route_name if route else None},
                })
            for p in route_points:
                try:
                    lon = float(p.longitude)
                    lat = float(p.latitude)
                except (TypeError, ValueError):
                    continue
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "properties": {"kind": "stop", "order": p.order, "location_name": p.location_name},
                })

        # Students points
        for s in students:
            if s.latitude is not None and s.longitude is not None:
                try:
                    lon = float(s.longitude)
                    lat = float(s.latitude)
                except (TypeError, ValueError):
                    continue
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "properties": {
                        "kind": "student",
                        "id": s.id,
                        "name": f"{s.fname} {s.lname}".strip(),
                        "registration_code": s.registration_code,
                    },
                })

        data = {
            "type": "FeatureCollection",
            "features": features,
            "meta": {
                "bus": {"id": bus.id, "title": bus.title, "number": bus.number, "status": bus.status, "bus_id": bus.bus_id},
                "trip": ({
                    "id": trip.id,
                    "date": trip.date.isoformat(),
                    "start_time": trip.start_time.isoformat(),
                    "end_time": trip.end_time.isoformat(),
                    "route_name": trip.route.route_name if trip and trip.route else None,
                } if trip else None),
                "counts": {"route_points": len(route_points) if route_points else 0, "students": len(students)},
            },
        }
        return Response(data)

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = '__all__'
    search_fields = ['user__username', 'user__email', 'phone']
    ordering_fields = '__all__'

class SupervisorViewSet(viewsets.ModelViewSet):
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['user__username', 'assigned_bus__title', 'assigned_bus__number']
    ordering_fields = '__all__'

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['user__username', 'license_number', 'assigned_bus__title', 'assigned_bus__number']
    ordering_fields = '__all__'

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing students.
    - Filtering, searching, ordering enabled.
    - Pagination enabled.
    - Example request/response in Swagger.
    """
    queryset = Student.objects.select_related('student_class').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    # Avoid ImageField in auto filter generation (breaks django-filter schema for Swagger)
    filterset_fields = [
        'fname', 'lname', 'father', 'gender', 'student_class', 'section',
        'dob', 'phone', 'email', 'address', 'city', 'registration_code', 'reg_code_status',
        'request_date', 'request_time', 'request', 'qrcode', 'latitude', 'longitude'
    ]
    search_fields = ['fname', 'lname', 'registration_code']
    ordering_fields = '__all__'
    def get_serializer_context(self):
        return {'request': self.request}

class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['user__username', 'user__email', 'phone']
    ordering_fields = '__all__'

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['student__fname', 'student__lname', 'date']
    ordering_fields = '__all__'

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['title', 'message']
    ordering_fields = '__all__'

class BusAssignmentViewSet(viewsets.ModelViewSet):
    queryset = BusAssignment.objects.select_related('bus', 'student').all()
    serializer_class = BusAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['student__fname', 'student__lname', 'bus__title', 'bus__number']
    ordering_fields = '__all__'

class BusRouteViewSet(viewsets.ModelViewSet):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['route_name', 'bus__title', 'bus__number']
    ordering_fields = '__all__'

class BusRoutePointViewSet(viewsets.ModelViewSet):
    queryset = BusRoutePoint.objects.select_related('route', 'route__bus').all()
    serializer_class = BusRoutePointSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['location_name', 'route__route_name', 'route__bus__title']
    ordering_fields = '__all__'

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related('bus', 'route').all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['bus__title', 'bus__number', 'route__route_name', 'date']
    ordering_fields = '__all__'

class TripStudentViewSet(viewsets.ModelViewSet):
    queryset = TripStudent.objects.select_related('trip', 'student').all()
    serializer_class = TripStudentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['trip__date', 'trip__bus__title', 'student__fname', 'student__lname']
    ordering_fields = '__all__'

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['user__username', 'message']
    ordering_fields = '__all__'

class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['bus__title', 'bus__number', 'maintenance_type', 'description']
    ordering_fields = '__all__'

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['title', 'message', 'bus__title']
    ordering_fields = '__all__'

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['user__username', 'message', 'remind_at']
    ordering_fields = '__all__'

class GPSTrackingViewSet(viewsets.ModelViewSet):
    queryset = GPSTracking.objects.select_related('bus').all()
    serializer_class = GPSTrackingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['bus__title', 'bus__number', 'latitude', 'longitude']
    ordering_fields = '__all__'

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = '__all__'
    search_fields = ['name']
    ordering_fields = '__all__'
