import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', password='admin@123', email='admin@admin.com')
            print("Superuser created")
        else:
            print("Superuser Already Created")