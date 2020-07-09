#!/bin/sh
python app.py db migrate
python app.py db upgrade
uwsgi --ini wsgi.ini
