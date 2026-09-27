# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 1.0.x   | ✅        |

## Reporting a vulnerability

Please do **not** open a public issue for security problems.

Email the maintainer at **acharakshay344@gmail.com** with a description of the
issue and steps to reproduce. You'll receive a response as soon as possible.

## Deployment hardening notes

Before running Smart Parking Pro outside of local development:

- Set a strong, random `SECRET_KEY` (see `.env.example`).
- Change the default admin credentials (`admin@smartparking.com` / `admin123`).
- Use a production WSGI server (e.g. Gunicorn) instead of the Flask dev server.
- Serve over HTTPS.
- Keep `instance/` (database) and `uploads/` out of version control.
