#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r ./enyata_api/requirements.txt


python manage.py collectstatic --no-input

python manage.py makemigrations
python manage.py migrate
python manage.py populate_db --no-input