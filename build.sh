#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Populate/Update Content (Safe to run multiple times for this app)
python manage.py populate_alphabet
python manage.py populate_vocab
