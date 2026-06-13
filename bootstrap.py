import argparse
import os
import subprocess
import sys


def is_venv_active():
    return (
        hasattr(sys, "real_prefix")
        or sys.prefix != sys.base_prefix
        or "VIRTUAL_ENV" in os.environ
    )


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap a Wagtail News Template development environment."
    )
    parser.add_argument(
        "--no-sample-data",
        action="store_true",
        help="Skip loading sample/demo content.",
    )
    args = parser.parse_args()

    if not is_venv_active():
        print(
            "\nNo virtual environment detected.\n"
            "\nPlease create and activate a virtual environment first.\n"
            "\nWindows:\n"
            "python -m venv .venv\n"
            ".venv\\Scripts\\activate\n"
            "\nLinux/macOS:\n"
            "python -m venv .venv\n"
            "source .venv/bin/activate\n"
        )
        sys.exit(1)

    print("Installing dependencies...")

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        check=True,
    )

    print("\nRunning development setup...")

    command = [sys.executable, "manage.py", "dev_setup"]

    if args.no_sample_data:
        command.append("--no-sample-data")

    subprocess.run(command, check=True)

    print(
        "\nBootstrap complete!\n"
        "\nStart the development server with:\n"
        "python manage.py runserver\n"
    )


if __name__ == "__main__":
    main()
