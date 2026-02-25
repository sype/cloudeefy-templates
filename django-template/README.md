# Django Demo App

A minimal Django application configured for cloud deployment with PostgreSQL and S3 storage.

## What's Inside

- **Django 4.2** with Gunicorn
- **PostgreSQL** database via `DATABASE_URL` (SQLite fallback for local dev)
- **S3 object storage** for media files via `django-storages` (local filesystem fallback)
- **WhiteNoise** for static file serving
- **Health checks** at `/health/`
- **Admin panel** at `/admin/`
- **Demo API** — notes CRUD at `/api/notes/`
- **Multi-stage Dockerfile** for small production images

## Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://localhost:8000 — returns a JSON status page.

## Deploy on Cloudeefly

1. Push this repo to GitHub
2. In Cloudeefly, select **Git Repository** deployment mode
3. Connect your repo — Cloudeefly provisions PostgreSQL and S3 automatically
4. Push code, app deploys

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | `change-me-in-production` | Django secret key |
| `DATABASE_URL` | Yes | `sqlite:///db.sqlite3` | PostgreSQL connection string |
| `DEBUG` | No | `false` | Enable debug mode |
| `ALLOWED_HOSTS` | No | `*` | Comma-separated allowed hosts |
| `AWS_STORAGE_BUCKET_NAME` | No | — | S3 bucket name (enables S3 storage) |
| `AWS_S3_ENDPOINT_URL` | No | — | S3 endpoint URL |
| `AWS_S3_REGION_NAME` | No | `fr-par` | S3 region |
| `AWS_ACCESS_KEY_ID` | No | — | S3 access key |
| `AWS_SECRET_ACCESS_KEY` | No | — | S3 secret key |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | App status (db, storage info) |
| GET | `/health/` | Health check |
| GET | `/admin/` | Django admin |
| GET | `/api/notes/` | List notes |
| POST | `/api/notes/` | Create note `{"title": "...", "content": "..."}` |

## Build Docker Image

```bash
docker build -t django-demo --target production .
docker run -p 8000:8000 -e SECRET_KEY=test -e DEBUG=true django-demo
```
