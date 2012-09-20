#!/bin/bash

source /var/www/vhosts/lobby_web/lobby_adamsschool_com/venv/bin/activate
export DJANGO_SETTINGS_MODULE=settings

/var/www/vhosts/lobby_web/lobby_adamsschool_com/manage.py update_superslides
