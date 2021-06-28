#!/bin/bash
git stash
git pull origin main --rebase
git stash apply
source venv/bin/activate
gunicorn wsgi:app --bind 127.0.0.1:5000 --daemon --log-syslog
deactivate
