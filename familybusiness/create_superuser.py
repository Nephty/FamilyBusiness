from django.contrib.auth import get_user_model

User = get_user_model()

email = "admin@admin.be"
password = "admin"
first_name = "Admin"
last_name = "Admin"

# Check if user already exists
if not User.objects.filter(email=email).exists():
    user = User.objects.create_superuser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    user.is_active = True
    user.save()
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
