#!/bin/bash

gunicorn --threads 4 --workers 4 --bind 0.0.0.0:5000 wsgi:app
