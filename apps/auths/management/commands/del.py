from auths.models import CastomUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.delete_users()

    def delete_users(self):
        users_to_delete = CastomUser.objects.all()[:900000]
        for user in users_to_delete:
            user.delete()