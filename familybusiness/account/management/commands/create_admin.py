from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates the default admin user"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = "admin@admin.be"

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                first_name="Admin",
                last_name="Admin",
                password="admin"
            )
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write("Superuser already exists")
