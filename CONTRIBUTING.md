# Contributing to Smart Parking Pro

Thanks for your interest in improving Smart Parking Pro! 🎉

## How to contribute

1. **Fork** the repository and clone your fork:
   ```bash
   git clone https://github.com/Akshaysb730/smart-parking-pro.git
   cd SmartParkingPro
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes and test them locally (`python app.py`).
5. Commit using a clear, conventional message:
   ```bash
   git commit -m "feat: add short description of change"
   ```
6. Push and open a **Pull Request** against `main`.

## Guidelines

- Follow the existing code style (Flask + SQLAlchemy patterns).
- Keep UI changes consistent with the design system in `static/css/style.css`.
- Do **not** commit the SQLite database, `uploads/`, or any secrets — these are
  covered by `.gitignore`.
- Update the README if you add or change user-facing features.

## Reporting issues

Please open an issue with a clear title, steps to reproduce, and the expected
vs. actual behaviour.

## License

By contributing, you agree that your contributions will be licensed under the
project's [MIT License](LICENSE).
