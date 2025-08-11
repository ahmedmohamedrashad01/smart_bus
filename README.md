# 🚍 School Transport Management System

**Project Nexus – Backend Implementation with Django REST Framework**

A smart, secure, and real-time platform for managing school transportation operations — from tracking buses to notifying parents — built as part of the **Project Nexus** professional development challenge.

---

## 📖 Overview

In an era where safety, efficiency, and communication are paramount, traditional school transport systems often fall short.  
This project addresses these shortcomings by providing a **centralized digital solution** to manage buses, students, routes, drivers, and notifications in real time.

The platform enables:
- **Real-time GPS tracking** of school buses
- **Efficient route management**
- **Parent notifications** for delays or emergencies
- **Attendance and student management**
- **Maintenance scheduling**
- **Data-driven decision-making** through reports and analytics

---

## 🎯 Objectives

- Provide **centralized data management** for students, drivers, supervisors, and buses.
- Enable **real-time bus tracking** with GPS integration.
- Offer **direct communication channels** with guardians via notifications.
- Improve **safety and reliability** in student transportation.
- Generate **comprehensive reports** for performance, attendance, and maintenance.
- Automate repetitive tasks to **save time and reduce costs**.

---

## 🛠 Tech Stack

| Layer           | Technology |
|-----------------|------------|
| Backend         | Django 5.x, Django REST Framework |
| Database        | PostgreSQL / MySQL (configurable) |
| Authentication  | Django Auth (Custom User Roles) |
| Media Handling  | Django File & Image Fields |
| Geolocation     | Decimal GPS fields, integration-ready with Google Maps / Mapbox |
| Deployment      | Docker / Heroku / AWS EC2 (configurable) |

---

## 📂 Features & Modules

### 1. **Core Management**
- **Bus Management** – Register, assign, and monitor buses with capacity and status tracking.
- **User Roles** – Admin, Supervisor, Driver, Guardian, Student.
- **Class Management** – Organize students by grade and section.

### 2. **Student & Guardian**
- Student profile with **parent/guardian linking**.
- Multiple guardians per student.
- QR code & registration code support.

### 3. **Transportation & Tracking**
- **Bus Routes** – Define and manage route points (lat/long + order).
- **Trips** – Schedule, assign routes, and link students.
- **GPS Tracking** – Store location logs for real-time mapping.

### 4. **Attendance & Communication**
- Attendance tracking per trip.
- Announcements & notifications.
- Reminders for events or maintenance.

### 5. **Maintenance & Safety**
- Maintenance logs per bus.
- Alerts for upcoming service schedules.

---

## 🗄 Database Models

Key entities:

- **Bus**  
- **Admin, Supervisor, Driver, Guardian, Student**  
- **Class, BusRoute, BusRoutePoint**  
- **Trip, TripStudent**  
- **Attendance, Announcement, Notification, Reminder**  
- **MaintenanceLog, GPSTracking**

> See [`models.py`](./school_transport/models.py) for full implementation.

---

## 🔄 API Endpoints

The API is RESTful and can be extended with GraphQL.

Example endpoints (REST):

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/buses/` | List all buses |
| POST   | `/api/students/` | Create a new student |
| GET    | `/api/trips/{id}/` | Get trip details |
| POST   | `/api/attendance/` | Record attendance |
| GET    | `/api/notifications/` | List notifications |

Full API documentation is available via **Swagger** or **DRF's API Docs**.

---

## 🚀 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Smart_bus_back-end.git
cd school-transport-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

