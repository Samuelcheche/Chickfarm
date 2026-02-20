import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChickenFarm.settings')
django.setup()

from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import Client

print("=" * 70)
print("TESTING CONTACT PAGE ACCESSIBILITY")
print("=" * 70)

client = Client()

# Test GET contact page
print("\n[TEST 1] Testing GET /contact/...")
response = client.get('/contact/')
print(f"  Status Code: {response.status_code}")

if response.status_code == 200:
    print(f"  ✅ Page loaded successfully")
    
    # Check if template was rendered
    if 'contact' in response.content.decode('utf-8').lower():
        print(f"  ✅ Template content found in response")
    else:
        print(f"  ⚠️ Template might not be rendering correctly")
        
    # Check for key elements
    content = response.content.decode('utf-8')
    checks = [
        ('Contact form', '<form' in content or 'contactForm' in content),
        ('Form inputs', 'name="name"' in content),
        ('Submit button', 'submit' in content.lower()),
    ]
    
    for check_name, check_result in checks:
        status = "✅" if check_result else "❌"
        print(f"  {status} {check_name}")
else:
    print(f"  ❌ Page failed to load")
    print(f"  Response: {response.status_code}")
    print(f"  Content: {response.content[:200]}")

# List all URL patterns
print(f"\n[TEST 2] Checking URL configuration...")
from django.urls import get_resolver
from django.urls.exceptions import Resolver404

resolver = get_resolver()
print(f"  Available URL patterns:")
for pattern in resolver.url_patterns:
    print(f"    • {pattern.pattern}")

print("\n" + "=" * 70)
