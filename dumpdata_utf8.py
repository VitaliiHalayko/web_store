import io
import os
import django
from django.core.management import call_command
from django.core.management.base import CommandError
from django.conf import settings

# Встановлюємо змінну оточення для налаштувань Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_store.settings')

# Ініціалізуємо Django
django.setup()

try:
    # Відкриваємо файл для запису з кодуванням UTF-8
    with io.open('data.json', 'w', encoding='utf-8') as f:
        # Викликаємо команду dumpdata та направляємо вихідний потік у файл
        call_command('dumpdata', '--indent', '4', stdout=f)
except CommandError as e:
    print(f"CommandError: {e}")
