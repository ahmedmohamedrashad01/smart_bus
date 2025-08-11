from django.contrib import admin
from .models import (
    Bus, Admin, Supervisor, Driver, Student, Guardian, Attendance, Announcement,
    BusAssignment, BusRoute, BusRoutePoint, Trip, TripStudent, Feedback,
    MaintenanceLog, Notification, Reminder, GPSTracking, Class
)

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_id', 'title', 'number', 'capacity', 'status')
    search_fields = ('bus_id', 'title', 'number')
    list_filter = ('status',)

admin.site.register(Admin)
admin.site.register(Supervisor)
admin.site.register(Driver)
admin.site.register(Student)
admin.site.register(Guardian)
admin.site.register(Attendance)
admin.site.register(Announcement)
admin.site.register(BusAssignment)
admin.site.register(BusRoute)
admin.site.register(BusRoutePoint)
admin.site.register(Trip)
admin.site.register(TripStudent)
admin.site.register(Feedback)
admin.site.register(MaintenanceLog)
admin.site.register(Notification)
admin.site.register(Reminder)
admin.site.register(GPSTracking)
admin.site.register(Class)
