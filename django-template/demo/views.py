import json
import os
from django.http import JsonResponse
from django.db import connection
from .models import Note


def index(request):
    """Root endpoint - app info and status."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")

    return JsonResponse({
        'app': 'Django Demo',
        'status': 'running',
        'version': os.getenv('APP_VERSION', 'dev'),
        'database': 'connected',
        'storage': 's3' if os.getenv('AWS_STORAGE_BUCKET_NAME') else 'local',
    })


def notes_api(request):
    """Simple CRUD endpoint for notes."""
    if request.method == 'GET':
        notes = list(Note.objects.values('id', 'title', 'content', 'created_at'))
        return JsonResponse({'notes': notes}, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        note = Note.objects.create(
            title=data.get('title', ''),
            content=data.get('content', ''),
        )
        return JsonResponse({
            'id': note.id,
            'title': note.title,
            'created_at': note.created_at.isoformat(),
        }, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
