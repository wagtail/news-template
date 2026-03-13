import gunicorn

# Replace gunicorn's 'Server' HTTP header to avoid leaking info to attackers
gunicorn.SERVER = ""

# Restart gunicorn worker processes every 1200-1250 requests
max_requests = 1200
max_requests_jitter = 50

# Log to stdout
accesslog = "-"

# Time out after 25 seconds
timeout = 25

# Workers can be overridden by `$WEB_CONCURRENCY`
workers = 2

# Load app pre-fork to save memory and worker startup time
preload_app = True
