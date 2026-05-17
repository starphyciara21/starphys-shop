#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install all the python libraries from your requirements text file
pip install -r requirements.txt

# 2. Run your catalog script to wipe and reload your database with the clean images
python populate_shop.py
