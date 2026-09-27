# Changelog

All notable changes to **Smart Parking Pro** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-09-27

### Added
- Core Flask + SQLAlchemy parking management system (SIH25414).
- Role-based access: admin, security, faculty, staff, student, visitor.
- Slot pre-booking with vehicle selection, duration, and price preview.
- QR-code entry passes generated per booking.
- Security guard dashboard with QR/RFID/manual verification and violation logging.
- Admin dashboard with occupancy, utilisation, and revenue analytics.
- Payments and monthly-pass management.
- Real-time availability API (`/api/slots/available`, `/api/slots/status`, `/api/booking/<code>`).
- 100 pre-configured slots across faculty / staff / student / visitor categories.
- Premium UI redesign: glassmorphic navbar, gradient brand palette, animated
  background graphics, live-availability landing dashboard, and responsive cards.
- Project documentation: README with badges & screenshots, MIT LICENSE,
  CONTRIBUTING guide, issue/PR templates, and `.env.example`.

[Unreleased]: https://github.com/Akshaysb730/smart-parking-pro/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Akshaysb730/smart-parking-pro/releases/tag/v1.0.0
