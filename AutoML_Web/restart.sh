#!/bin/bash

# remove old database
rm db.sqlite3
rm ./_app/migrations/0001_initial.py
# recreate database and reset user
python manage.py makemigrations
python manage.py migrate