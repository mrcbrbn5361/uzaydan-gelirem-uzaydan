#!/bin/bash
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:3000 --timeout 120 --workers 3 --threads 3 