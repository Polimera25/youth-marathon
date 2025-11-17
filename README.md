# Marathon Registration (Django)

A clean, ready-to-run Django site for marathon/10K registrations.

## Quick Start

```bash
cd marathon_site
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Create database and admin user
python manage.py migrate
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

## Usage

1. Visit http://127.0.0.1:8000/ — add races via **/admin** (Race model).
2. Share the **/register** page with runners.
3. See participant list per race, CSV export, and a simple dashboard.

## Models

- **Race**: name, date, distance, capacity, location
- **Runner**: person info with unique email
- **Registration**: runner x race, t‑shirt size, paid flag

## Notes

- Time zone defaults to **Asia/Kolkata**.
- Uses SQLite by default.
- Tailwind via CDN in templates (no build step).
