# create_superuser.py

import os
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

# Set the Django settings module if it's not already set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminapp.settings')

# Execute Django's start-up procedure
execute_from_command_line(['manage.py', 'makemigrations'])
execute_from_command_line(['manage.py', 'migrate'])

# Create the superuser
User = get_user_model()

# Check if the superuser already exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
