import io
import os
import django
from django.core.management import call_command
from django.core.management.base import CommandError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_store.settings')

django.setup()


try:
    with io.open('data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', '--indent', '4', stdout=f)
except CommandError as e:
    print(f"CommandError: {e}")