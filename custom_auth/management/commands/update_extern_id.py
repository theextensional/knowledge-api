from django.core.management.base import BaseCommand

from custom_auth.models import get_hash, ExternGoogleUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        for ext in ExternGoogleUser.objects.all():
            ext.extern_id = get_hash(ext.extern_id)
            ext.save()
