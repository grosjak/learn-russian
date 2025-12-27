import os
import sys

# Add project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from cyrillic_tutor.wsgi import application
