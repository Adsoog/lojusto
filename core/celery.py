# core/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer el entorno de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Crear una instancia de Celery
app = Celery('core')

# Usar la configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas de todos los módulos Django registrados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
