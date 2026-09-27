from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='visitor')  # admin, security, faculty, staff, student, visitor
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile fields
    department = db.Column(db.String(100))
    rfid_tag = db.Column(db.String(50), unique=True)
    
    # Relationships
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    violations = db.relationship('Violation', foreign_keys='Violation.user_id', backref='user', lazy=True)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_role(self, role):
        return self.role == role
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_security(self):
        return self.role == 'security'

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(20), default='car')  # car, bike, ev
    model = db.Column(db.String(50))
    color = db.Column(db.String(30))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='vehicle', lazy=True)

class ParkingSlot(db.Model):
    __tablename__ = 'parking_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    slot_number = db.Column(db.String(10), unique=True, nullable=False)
    slot_type = db.Column(db.String(20), default='visitor')  # faculty, staff, student, visitor
    is_occupied = db.Column(db.Boolean, default=False)
    is_reserved = db.Column(db.Boolean, default=False)
    floor = db.Column(db.Integer, default=1)
    section = db.Column(db.String(10), default='A')
    coordinates = db.Column(db.String(50))  # GPS coordinates for navigation
    
    # Relationships
    current_booking = db.relationship('Booking', backref='parking_slot', 
                                      foreign_keys='Booking.slot_id', uselist=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('parking_slots.id'), nullable=True)
    
    # Timing
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    actual_entry = db.Column(db.DateTime)
    actual_exit = db.Column(db.DateTime)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled, expired
    
    # Payment
    amount = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    payment_method = db.Column(db.String(20))
    
    # QR Code
    qr_code_path = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_duration_hours(self):
        if self.actual_entry and self.actual_exit:
            duration = self.actual_exit - self.actual_entry
            return duration.total_seconds() / 3600
        return 0
    
    def is_overstayed(self):
        if self.status == 'active' and self.end_time:
            return datetime.utcnow() > self.end_time
        return False

class Violation(db.Model):
    __tablename__ = 'violations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True)
    license_plate = db.Column(db.String(20))
    
    violation_type = db.Column(db.String(50))  # overstay, wrong_zone, no_booking
    description = db.Column(db.Text)
    fine_amount = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, paid, dismissed
    
    # Evidence
    photo_path = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class ParkingLog(db.Model):
    __tablename__ = 'parking_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
    license_plate = db.Column(db.String(20))
    action = db.Column(db.String(20))  # entry, exit
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    verified_by = db.Column(db.String(50))  # QR, RFID, Manual
    security_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(20))  # booking, fine, pass
    status = db.Column(db.String(20), default='pending')
    transaction_id = db.Column(db.String(100))
    payment_method = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MonthlyPass(db.Model):
    __tablename__ = 'monthly_passes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    pass_type = db.Column(db.String(20))  # faculty, staff, student
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
