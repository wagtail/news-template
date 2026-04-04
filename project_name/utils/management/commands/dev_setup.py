from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Set up local development environment"

    def handle(self, *args, **kwargs):
        self.stdout.write("Running migrations...")
        call_command("migrate")

        self.stdout.write("Creating cache table...")
        call_command("createcachetable")

        self.stdout.write("Loading initial data...")
        call_command("load_initial_data")

        self.stdout.write("Collecting static files...")
        call_command("collectstatic", interactive=False)

        self.stdout.write(self.style.SUCCESS("Local setup complete."))