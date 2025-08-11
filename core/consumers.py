import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import Bus, GPSTracking, Trip, BusRoute, BusRoutePoint, TripStudent, Student

class BusLiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.bus_id = self.scope['url_route']['kwargs'].get('bus_id')
        self.group_name = f"bus_{self.bus_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self._send_snapshot()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Optional: allow client to request a refresh
        await self._send_snapshot()

    async def bus_update(self, event):
        # Triggered by signals when new GPS point comes in
        await self._send_snapshot()

    async def _send_snapshot(self):
        data = await self._build_geojson()
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def _build_geojson(self):
        try:
            bus = Bus.objects.get(id=self.bus_id)
        except Bus.DoesNotExist:
            return {"type": "FeatureCollection", "features": [], "error": "bus_not_found"}

        now = timezone.localtime()
        today = now.date()
        latest = GPSTracking.objects.filter(bus=bus).order_by('-timestamp').first()
        trip = Trip.objects.select_related('route').filter(
            bus=bus, date=today, start_time__lte=now.time(), end_time__gte=now.time()
        ).first()
        if not trip:
            trip = Trip.objects.select_related('route').filter(bus=bus).order_by('-date', '-start_time').first()
        route = trip.route if trip else BusRoute.objects.filter(bus=bus).order_by('-id').first()
        route_points = list(BusRoutePoint.objects.filter(route=route).order_by('order')) if route else []

        if trip:
            trip_students = TripStudent.objects.select_related('student').filter(trip=trip)
            students = [ts.student for ts in trip_students]
        else:
            students = list(Student.objects.filter(busassignment__bus=bus).distinct())

        features = []
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
        return data
