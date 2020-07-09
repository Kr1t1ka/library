#!/bin/sh
python app.py db migrate
python app.py db upgrade
uwsgi --config wsgi.ini
