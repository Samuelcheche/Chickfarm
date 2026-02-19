import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChickenFarm.settings')
django.setup()

from django.contrib.auth.models import User

print('All Users in Database:')
print('-' * 80)
for u in User.objects.all():
    print(f'Username: {u.username}')
    print(f'Email: {u.email}')
    print(f'First Name: {u.first_name}')
    print(f'Last Name: {u.last_name}')
    print(f'Is Staff: {u.is_staff}')
    print(f'Is Superuser: {u.is_superuser}')
    print('-' * 80)
