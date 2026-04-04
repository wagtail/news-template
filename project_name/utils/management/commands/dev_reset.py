from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Reset local SQLite database and reload initial data"

    def handle(self, *args, **kwargs):
        db = Path("db.sqlite3")

        if db.exists():
            self.stdout.write("Deleting db.sqlite3...")
            db.unlink()
        else:
            self.stdout.write("No existing db.sqlite3 found.")

        self.stdout.write("Running migrations...")
        call_command("migrate")

        self.stdout.write("Creating cache table...")
        call_command("createcachetable")

        self.stdout.write("Loading initial data...")
        call_command("load_initial_data")

        self.stdout.write(self.style.SUCCESS("Database reset complete."))