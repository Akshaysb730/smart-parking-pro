import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'smart-parking-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///smart_parking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Parking Configuration
    TOTAL_SLOTS = 100
    SLOT_TYPES = {
        'faculty': {'count': 30, 'price_per_hour': 10},
        'staff': {'count': 30, 'price_per_hour': 8},
        'student': {'count': 25, 'price_per_hour': 5},
        'visitor': {'count': 15, 'price_per_hour': 20}
    }
    
    # QR Code Configuration
    QR_CODE_DIR = 'uploads/qr_codes'
    
    # Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
