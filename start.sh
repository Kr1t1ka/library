#!/bin/sh
python app.py db migrate
python app.py db upgrade
python app.py runserver -h 0.0.0.0