# core/__init__.py
from __future__ import absolute_import, unicode_literals

# Importa la aplicación Celery
from .celery import app as celery_app

# Hace que Celery esté disponible en el contexto de Django
__all__ = ('celery_app',)
