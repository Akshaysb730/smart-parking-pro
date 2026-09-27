from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
import string

from config import Config
from models import db, User, Vehicle, ParkingSlot, Booking, Violation, ParkingLog, Payment, MonthlyPass

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Ensure upload directories exist
os.makedirs(os.path.join(app.root_path, Config.QR_CODE_DIR), exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'uploads/violations'), exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_booking_code():
    """Generate unique booking code"""
    return 'SP' + ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def init_parking_slots():
    """Initialize parking slots"""
    if ParkingSlot.query.first() is None:
        type_prefixes = {'faculty': 'F', 'staff': 'T', 'student': 'S', 'visitor': 'V'}
        slot_counters = {'faculty': 0, 'staff': 0, 'student': 0, 'visitor': 0}
        for slot_type, config in Config.SLOT_TYPES.items():
            for i in range(config['count']):
                slot_counters[slot_type] += 1
                counter = slot_counters[slot_type]
                floor = (counter - 1) // 25 + 1
                section = chr(65 + ((counter - 1) % 25) // 5)
                prefix = type_prefixes.get(slot_type, slot_type[0].upper())
                slot = ParkingSlot(
                    slot_number=f'{prefix}{section}{counter:02d}',
                    slot_type=slot_type,
                    floor=floor,
                    section=section,
                    coordinates=f'{floor}-{section}-{counter}'
                )
                db.session.add(slot)
        db.session.commit()

def create_admin_user():
    """Create default admin user"""
    if not User.query.filter_by(role='admin').first():
        admin = User(
            email='admin@smartparking.com',
            password_hash=generate_password_hash('admin123'),
            first_name='System',
            last_name='Administrator',
            phone='0000000000',
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash('Your account has been deactivated.', 'error')
                return redirect(url_for('login'))
            
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        role = request.form.get('role', 'visitor')
        
        # Validation
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('register'))
        
        # Create user
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ==================== DASHBOARD ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Role-based dashboard redirect"""
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    elif current_user.is_security():
        return redirect(url_for('security_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    """User dashboard"""
    if current_user.is_admin() or current_user.is_security():
        return redirect(url_for('dashboard'))
    
    # Get user's active bookings
    active_bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).filter(Booking.status.in_(['pending', 'active'])).all()
    
    # Get user's vehicles
    vehicles = Vehicle.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    # Get parking statistics
    total_bookings = Booking.query.filter_by(user_id=current_user.id).count()
    completed_bookings = Booking.query.filter_by(
        user_id=current_user.id, status='completed'
    ).count()
    
    # Get available slots count
    available_slots = ParkingSlot.query.filter_by(is_occupied=False, is_reserved=False).count()
    
    return render_template('user/dashboard.html',
                         active_bookings=active_bookings,
                         vehicles=vehicles,
                         total_bookings=total_bookings,
                         completed_bookings=completed_bookings,
                         available_slots=available_slots)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    if not current_user.is_admin():
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    # Statistics
    total_users = User.query.count()
    total_bookings_today = Booking.query.filter(
        db.func.date(Booking.created_at) == datetime.utcnow().date()
    ).count()
    active_parkings = Booking.query.filter_by(status='active').count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter(
        Payment.status == 'completed'
    ).scalar() or 0
    
    # Recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    
    # Slot utilization
    total_slots = ParkingSlot.query.count()
    occupied_slots = ParkingSlot.query.filter_by(is_occupied=True).count()
    utilization_rate = (occupied_slots / total_slots * 100) if total_slots > 0 else 0
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_bookings_today=total_bookings_today,
                         active_parkings=active_parkings,
                         total_revenue=total_revenue,
                         recent_bookings=recent_bookings,
                         utilization_rate=utilization_rate,
                         total_slots=total_slots,
                         occupied_slots=occupied_slots)

@app.route('/security/dashboard')
@login_required
def security_dashboard():
    """Security dashboard"""
    if not current_user.is_security() and not current_user.is_admin():
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    # Active parkings
    active_bookings = Booking.query.filter_by(status='active').all()
    
    # Recent entries/exits
    recent_logs = ParkingLog.query.order_by(ParkingLog.timestamp.desc()).limit(20).all()
    
    # Pending violations
    pending_violations = Violation.query.filter_by(status='pending').all()
    
    # Today's stats
    today = datetime.utcnow().date()
    entries_today = ParkingLog.query.filter(
        db.func.date(ParkingLog.timestamp) == today,
        ParkingLog.action == 'entry'
    ).count()
    exits_today = ParkingLog.query.filter(
        db.func.date(ParkingLog.timestamp) == today,
        ParkingLog.action == 'exit'
    ).count()
    
    return render_template('security/dashboard.html',
                         active_bookings=active_bookings,
                         recent_logs=recent_logs,
                         pending_violations=pending_violations,
                         entries_today=entries_today,
                         exits_today=exits_today)

# ==================== USER BOOKING ROUTES ====================

@app.route('/user/book', methods=['GET', 'POST'])
@login_required
def book_parking():
    """Book parking slot"""
    if current_user.is_admin() or current_user.is_security():
        return redirect(url_for('dashboard'))
    
    vehicles = Vehicle.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    if not vehicles:
        flash('Please add a vehicle first.', 'warning')
        return redirect(url_for('add_vehicle'))
    
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        slot_type = request.form.get('slot_type')
        start_time_str = request.form.get('start_time')
        duration_hours = int(request.form.get('duration_hours', 1))
        
        # Parse start time
        start_time = datetime.fromisoformat(start_time_str)
        end_time = start_time + timedelta(hours=duration_hours)
        
        # Find available slot
        slot = ParkingSlot.query.filter_by(
            slot_type=slot_type,
            is_occupied=False,
            is_reserved=False
        ).first()
        
        if not slot:
            flash('No slots available for the selected type.', 'error')
            return redirect(url_for('book_parking'))
        
        # Calculate amount
        price_per_hour = Config.SLOT_TYPES.get(slot_type, {}).get('price_per_hour', 10)
        amount = price_per_hour * duration_hours
        
        # Create booking
        booking = Booking(
            booking_code=generate_booking_code(),
            user_id=current_user.id,
            vehicle_id=vehicle_id,
            slot_id=slot.id,
            start_time=start_time,
            end_time=end_time,
            amount=amount,
            status='pending'
        )
        db.session.add(booking)
        db.session.commit()
        
        flash(f'Booking created! Code: {booking.booking_code}. Please proceed to payment.', 'success')
        return redirect(url_for('payment', booking_id=booking.id))
    
    # Get available slot counts
    available_counts = {}
    for slot_type in Config.SLOT_TYPES.keys():
        count = ParkingSlot.query.filter_by(
            slot_type=slot_type,
            is_occupied=False,
            is_reserved=False
        ).count()
        available_counts[slot_type] = count
    
    return render_template('user/book.html',
                         vehicles=vehicles,
                         available_counts=available_counts,
                         slot_types=Config.SLOT_TYPES)

@app.route('/user/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id):
    """Process payment"""
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('user_dashboard'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        
        # Simulate payment processing
        payment = Payment(
            booking_id=booking.id,
            user_id=current_user.id,
            amount=booking.amount,
            payment_type='booking',
            status='completed',
            transaction_id='TXN' + generate_booking_code(),
            payment_method=payment_method
        )
        db.session.add(payment)
        
        # Update booking
        booking.payment_status = 'paid'
        booking.status = 'pending'
        
        # Reserve slot
        slot = ParkingSlot.query.get(booking.slot_id)
        slot.is_reserved = True
        
        db.session.commit()
        
        # Generate QR code
        generate_qr_code(booking)
        
        flash('Payment successful! Your QR code has been generated.', 'success')
        return redirect(url_for('booking_details', booking_id=booking.id))
    
    return render_template('user/payment.html', booking=booking)

def generate_qr_code(booking):
    """Generate QR code for booking"""
    try:
        import qrcode
        from PIL import Image
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(booking.booking_code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        filename = f'qr_{booking.booking_code}.png'
        filepath = os.path.join(app.root_path, Config.QR_CODE_DIR, filename)
        img.save(filepath)
        
        booking.qr_code_path = filename
        db.session.commit()
    except ImportError:
        # If qrcode not installed, just save the code
        booking.qr_code_path = booking.booking_code + '.txt'
        db.session.commit()

@app.route('/user/bookings')
@login_required
def my_bookings():
    """User's booking history"""
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('user/bookings.html', bookings=bookings)

@app.route('/user/booking/<int:booking_id>')
@login_required
def booking_details(booking_id):
    """Booking details"""
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and not current_user.is_admin():
        flash('Access denied.', 'error')
        return redirect(url_for('user_dashboard'))
    return render_template('user/booking_details.html', booking=booking)

# ==================== VEHICLE MANAGEMENT ====================

@app.route('/user/vehicles')
@login_required
def my_vehicles():
    """User's vehicles"""
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template('user/vehicles.html', vehicles=vehicles)

@app.route('/user/vehicle/add', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    """Add new vehicle"""
    if request.method == 'POST':
        license_plate = request.form.get('license_plate').upper().replace(' ', '')
        vehicle_type = request.form.get('vehicle_type')
        model = request.form.get('model')
        color = request.form.get('color')
        
        # Check if vehicle already exists
        if Vehicle.query.filter_by(license_plate=license_plate).first():
            flash('Vehicle already registered.', 'error')
            return redirect(url_for('add_vehicle'))
        
        vehicle = Vehicle(
            user_id=current_user.id,
            license_plate=license_plate,
            vehicle_type=vehicle_type,
            model=model,
            color=color
        )
        db.session.add(vehicle)
        db.session.commit()
        
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('my_vehicles'))
    
    return render_template('user/add_vehicle.html')

# ==================== SECURITY OPERATIONS ====================

@app.route('/security/verify', methods=['POST'])
@login_required
def verify_entry():
    """Verify vehicle entry/exit"""
    if not current_user.is_security() and not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    booking_code = data.get('booking_code')
    action = data.get('action')  # entry or exit
    
    booking = Booking.query.filter_by(booking_code=booking_code).first()
    
    if not booking:
        return jsonify({'error': 'Invalid booking code'}), 404
    
    slot = ParkingSlot.query.get(booking.slot_id)
    
    if action == 'entry':
        if booking.status != 'pending':
            return jsonify({'error': 'Booking is not pending'}), 400
        
        booking.status = 'active'
        booking.actual_entry = datetime.utcnow()
        slot.is_occupied = True
        slot.is_reserved = False
        
        log = ParkingLog(
            booking_id=booking.id,
            license_plate=booking.vehicle.license_plate,
            action='entry',
            verified_by='QR',
            security_id=current_user.id
        )
        db.session.add(log)
        
    elif action == 'exit':
        if booking.status != 'active':
            return jsonify({'error': 'Booking is not active'}), 400
        
        booking.status = 'completed'
        booking.actual_exit = datetime.utcnow()
        slot.is_occupied = False
        slot.is_reserved = False
        
        log = ParkingLog(
            booking_id=booking.id,
            license_plate=booking.vehicle.license_plate,
            action='exit',
            verified_by='QR',
            security_id=current_user.id
        )
        db.session.add(log)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{action.capitalize()} recorded successfully',
        'booking': {
            'code': booking.booking_code,
            'user': booking.user.get_full_name(),
            'vehicle': booking.vehicle.license_plate,
            'slot': slot.slot_number
        }
    })

@app.route('/security/violation/add', methods=['POST'])
@login_required
def add_violation():
    """Add parking violation"""
    if not current_user.is_security() and not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    violation = Violation(
        user_id=data.get('user_id'),
        license_plate=data.get('license_plate'),
        violation_type=data.get('violation_type'),
        description=data.get('description'),
        fine_amount=data.get('fine_amount', 0),
        status='pending'
    )
    db.session.add(violation)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Violation recorded'})

# ==================== API ROUTES ====================

@app.route('/api/slots/available')
def api_available_slots():
    """Get available slots"""
    slots = ParkingSlot.query.filter_by(is_occupied=False, is_reserved=False).all()
    return jsonify([{
        'id': s.id,
        'number': s.slot_number,
        'type': s.slot_type,
        'floor': s.floor,
        'section': s.section
    } for s in slots])

@app.route('/api/slots/status')
def api_slots_status():
    """Get all slots with status"""
    slots = ParkingSlot.query.all()
    return jsonify([{
        'id': s.id,
        'number': s.slot_number,
        'type': s.slot_type,
        'floor': s.floor,
        'section': s.section,
        'is_occupied': s.is_occupied,
        'is_reserved': s.is_reserved
    } for s in slots])

@app.route('/api/booking/<booking_code>')
def api_booking_details(booking_code):
    """Get booking details by code"""
    booking = Booking.query.filter_by(booking_code=booking_code).first()
    if not booking:
        return jsonify({'error': 'Not found'}), 404
    
    return jsonify({
        'code': booking.booking_code,
        'status': booking.status,
        'user': booking.user.get_full_name(),
        'vehicle': booking.vehicle.license_plate,
        'slot': booking.parking_slot.slot_number if booking.parking_slot else None,
        'start_time': booking.start_time.isoformat(),
        'end_time': booking.end_time.isoformat()
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# ==================== CONTEXT PROCESSORS ====================

@app.context_processor
def inject_globals():
    return {
        'app_name': 'Smart Parking Pro',
        'current_year': datetime.utcnow().year
    }

# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_parking_slots()
        create_admin_user()
    app.run(debug=True, host='0.0.0.0', port=5000)
