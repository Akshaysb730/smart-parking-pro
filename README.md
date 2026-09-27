# 🅿️ Smart Parking Pro

A premium **smart parking management system** for educational institutions (campuses). It digitises the entire parking workflow — from pre-booking a slot to QR-code gate entry, real-time availability, violation tracking, payments, and analytics — replacing paper logs and manual search with a fast, automated web app.

> Built for **SIH25414 — Smart Parking Slot Management**.

---

## ✨ Features

### 🚗 For Users (faculty / staff / students / visitors)
- **Pre-book parking slots** by user category, vehicle, and duration
- **Multiple vehicle management** (car, bike, EV) with licence-plate records
- **QR code entry passes** generated per booking for seamless gate access
- **Live availability** via a real-time slot map and status API
- **Online payments** with booking summary and price preview
- **Monthly passes** for regular parkers

### 🛡️ For Security Guards
- **QR / RFID / manual verification** of vehicles at entry & exit
- **Real-time occupancy** of parked vehicles
- **Violation logging** (overstay, wrong zone, no booking) with photo evidence and fines
- **Gate activity logs** for full audit trail

### 📊 For Administrators
- **Dashboard analytics** — occupancy, utilisation, revenue, and usage trends
- **Slot & pricing management** across categories
- **User and booking oversight** with digital records (zero paper)
- **Violation and payment monitoring**

---

## 🧱 Tech Stack

| Layer            | Technology                                   |
|------------------|----------------------------------------------|
| Backend          | Python, Flask                                 |
| ORM / Database   | Flask-SQLAlchemy, SQLite                      |
| Authentication   | Flask-Login, Werkzeug password hashing        |
| Frontend         | Bootstrap 5, Font Awesome, custom premium CSS |
| QR Codes         | `qrcode` + `Pillow`                           |
| Fonts            | Sora (display) + Inter (body)                 |

---

## 🗂️ Project Structure

```
SmartParkingPro/
├── app.py                 # Flask app, routes, and controllers
├── config.py              # Configuration & parking slot setup
├── models.py              # Database models (ORM)
├── requirements.txt       # Python dependencies
├── instance/
│   └── smart_parking.db   # SQLite database (gitignored)
├── static/
│   ├── css/style.css      # Premium styling
│   ├── js/app.js          # Frontend scripts
│   └── images/            # Static images
├── templates/
│   ├── base.html          # Shared layout (navbar, footer)
│   ├── index.html         # Landing page
│   ├── login.html
│   ├── register.html
│   ├── admin/             # Admin dashboard
│   ├── security/          # Security guard dashboard
│   ├── user/              # User booking, vehicles, payment
│   └── errors/            # 404 / 500 pages
└── uploads/               # QR codes & violation photos (gitignored)
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.13** (or 3.10+) installed on your machine

### 2. Clone the repository
```bash
git clone https://github.com/Akshaysb730/smart-parking-pro.git
cd SmartParkingPro
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

On first launch the app automatically:
- creates the SQLite database and tables,
- initialises the parking slots, and
- seeds a default **admin** account.

The server starts at **http://127.0.0.1:5000**

---

## 🔑 Default Admin Login

| Field    | Value                     |
|----------|---------------------------|
| Email    | `admin@smartparking.com`  |
| Password | `admin123`                |

> ⚠️ Change the default admin password and `SECRET_KEY` before any real deployment.

---

## 🅿️ Parking Slot Configuration

The campus lot is pre-configured with **100 slots** across four categories:

| Category | Slots | Price / hour |
|----------|:-----:|:------------:|
| Faculty  |  30   |     ₹10      |
| Staff    |  30   |      ₹8      |
| Student  |  25   |      ₹5      |
| Visitor  |  15   |     ₹20      |

Slots are auto-labelled by type, floor, and section (e.g. `FA01`, `SE25`, `VC13`). Edit counts or pricing in [`config.py`](config.py) → `SLOT_TYPES`.

---

## 🗃️ Data Model

| Model         | Purpose                                                  |
|---------------|----------------------------------------------------------|
| `User`        | Accounts + roles (admin, security, faculty, staff, student, visitor) |
| `Vehicle`     | Registered vehicles (car / bike / EV) per user            |
| `ParkingSlot` | Physical slots with type, floor, section, status          |
| `Booking`     | Slot reservations, timing, status, payment & QR code      |
| `Violation`   | Overstay / wrong-zone / no-booking records with fines     |
| `ParkingLog`  | Entry / exit gate events and verification method          |
| `Payment`     | Transactions for bookings, fines, and passes              |
| `MonthlyPass` | Subscription passes for regular parkers                   |

---

## 🔌 API Endpoints

| Method | Endpoint                | Description                     |
|--------|-------------------------|---------------------------------|
| GET    | `/api/slots/available`  | List currently available slots  |
| GET    | `/api/slots/status`     | Live status of all slots        |
| GET    | `/api/booking/<code>`   | Booking details by booking code |

---

## 🎨 UI / Design

The interface uses a premium design system: glassmorphic navigation, gradient brand palette (indigo → violet → cyan), animated background graphics, a live-availability dashboard mock on the landing page, and responsive cards throughout. Styles live in [`static/css/style.css`](static/css/style.css).

---

## 🔒 Configuration & Security

Environment variables (optional, sensible defaults are provided):

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///smart_parking.db
```

The `.gitignore` keeps the database, `__pycache__`, and `uploads/` (QR codes & violation photos) out of version control.

---

## 📈 Impact

- **60–80%** reduction in parking search time
- **100%** digital records
- **24/7** automated access
- **Zero** paper waste

---

## 🤝 Contributing

Contributions are welcome! Fork the repo, create a feature branch, and open a pull request.

---

## 📄 License

This project is built for the **SIH25414** Smart Parking Slot Management challenge. All rights reserved by the author.

---

<p align="center">Made with ❤️ by <a href="https://github.com/Akshaysb730">Akshaysb730</a></p>
