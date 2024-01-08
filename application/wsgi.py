"""Application entry point."""
import sys

# Set path for wsgi
sys.path.insert(0, '/var/www/application')

# Load app
from tutorlink import app as application
