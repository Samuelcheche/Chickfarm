import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChickenFarm.settings')
django.setup()

from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import Client

print("Testing different URL paths for contact page:\n")

client = Client()

urls_to_test = [
    '/contact/',
    '/contact',
    'contact/',
    'contact',
]

for url in urls_to_test:
    try:
        response = client.get(f'/{url}' if not url.startswith('/') else url)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} {url:20} → Status: {response.status_code}")
    except Exception as e:
        print(f"❌ {url:20} → Error: {str(e)[:50]}")

# Check if the view exists
print("\nChecking if contact view exists:")
from chickapp.views import contact
print(f"✅ contact view exists: {contact}")

# Check if the template file exists
import os
template_path = os.path.join(os.path.dirname(__file__), 'chickapp', 'templates', 'contact.html')
template_exists = os.path.exists(template_path)
print(f"{'✅' if template_exists else '❌'} Template file exists: {template_path}")
print(f"{'✅' if template_exists else '❌'} File size: {os.path.getsize(template_path) if template_exists else 'N/A'} bytes")
