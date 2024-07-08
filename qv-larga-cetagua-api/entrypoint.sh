#!/bin/bash
python3 manage.py makegrations
python3 manage.py migrate
# python manage.py loaddata initial_data.json
python manage.py runserver 0.0.0.0:8001