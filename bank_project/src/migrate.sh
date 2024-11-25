#!/bin/bash

# Activate virtual environment
source ../venv/bin/activate

# Fake remove accounts app migrations
echo "Faking removal of accounts app migrations..."
python3 manage.py migrate accounts zero --fake

# Fake initial migrations for new apps
echo "Faking initial migrations for users app..."
python3 manage.py migrate users 0001 --fake-initial

echo "Faking initial migrations for transactions app..."
python3 manage.py migrate transactions 0001 --fake-initial

# Run remaining migrations normally
echo "Running remaining migrations..."
python3 manage.py migrate
