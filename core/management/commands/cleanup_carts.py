from django.core.management.base import BaseCommand

from core.helpers.clean_up import delete_old_carts

class Command(BaseCommand):
    help = "Deletes guest carts that have not been updated for 7 days."

    def handle(self, *args, **options):
        old_carts = delete_old_carts(7)

        self.stdout.write(self.style.SUCCESS(f"Deleted {old_carts} guest carts older than 7 days."))