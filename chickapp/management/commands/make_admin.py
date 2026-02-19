from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Make a user a superuser and staff member'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address of the user')

    def handle(self, *args, **options):
        email = options['email'].lower()
        
        try:
            user = User.objects.get(username=email)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Success! User {email} is now a superuser and staff member.'
                )
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'User with email {email} not found.'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error: {str(e)}'
                )
            )
