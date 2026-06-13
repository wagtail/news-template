from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set up local development environment"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-sample-data",
            action="store_true",
            help="Skip loading sample/demo content",
        )

    def handle(self, *args, **options):
        self.stdout.write("Running migrations...")
        call_command("migrate")

        self.stdout.write("Creating cache table...")
        call_command("createcachetable")

        if options["no_sample_data"]:
            self.stdout.write(self.style.WARNING("Skipping sample data."))
            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING("No administrator account has been created.")
            )
            self.stdout.write("Create one with:\npython manage.py createsuperuser")
            self.stdout.write("")
        else:
            self.stdout.write("Loading initial data...")
            call_command("load_initial_data")

        self.stdout.write("Collecting static files...")
        call_command("collectstatic", interactive=False)

        self.stdout.write(self.style.SUCCESS("Local setup complete."))
