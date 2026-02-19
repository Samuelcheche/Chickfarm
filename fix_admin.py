#!/usr/bin/env python
"""
Fix Admin Access Script
This script will make the specified user an admin/staff member
Run this from the project root: python fix_admin.py koech@gmail.com
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChickenFarm.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User

def make_user_admin(email):
    """Make a user an admin/staff member"""
    email = email.lower().strip()
    
    try:
        user = User.objects.get(username=email)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"✓ Success! User {email} is now an admin.")
        print(f"  - Staff: {user.is_staff}")
        print(f"  - Superuser: {user.is_superuser}")
        return True
    except User.DoesNotExist:
        print(f"✗ Error: User with email '{email}' not found.")
        print(f"\nAvailable users:")
        for user in User.objects.all():
            print(f"  - {user.username} ({user.email})")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_admin.py <email>")
        print("Example: python fix_admin.py koech@gmail.com")
        sys.exit(1)
    
    email = sys.argv[1]
    success = make_user_admin(email)
    sys.exit(0 if success else 1)
