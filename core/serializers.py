from rest_framework import serializers
from .models import (
    Bus, Admin, Supervisor, Driver, Student, Guardian, Attendance, Announcement,
    BusAssignment, BusRoute, BusRoutePoint, Trip, TripStudent, Feedback,
    MaintenanceLog, Notification, Reminder, GPSTracking, Class
)

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate_fname(self, value):
        if not value:
            raise serializers.ValidationError("First name is required.")
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters.")
        return value

    def validate_lname(self, value):
        if not value:
            raise serializers.ValidationError("Last name is required.")
        if len(value) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters.")
        return value

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class BusAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusAssignment
        fields = '__all__'

class BusRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRoute
        fields = '__all__'

class BusRoutePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRoutePoint
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class TripStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripStudent
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class MaintenanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'

class GPSTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSTracking
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
